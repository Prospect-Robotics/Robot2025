package com.team2813.vision;

import static com.team2813.vision.CameraConstants.LIMELIGHT_CAMERA_NAME;
import static com.team2813.vision.VisionNetworkTables.CAMERA_POSE_TOPIC;
import static com.team2813.vision.VisionNetworkTables.getTableForCamera;

import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.math.geometry.*;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructPublisher;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Consumer;
import java.util.function.Function;
import org.photonvision.EstimatedRobotPose;
import org.photonvision.PhotonCamera;
import org.photonvision.PhotonPoseEstimator;
import org.photonvision.simulation.PhotonCameraSim;
import org.photonvision.simulation.SimCameraProperties;
import org.photonvision.simulation.VisionSystemSim;

public class MultiPhotonPoseEstimator implements AutoCloseable {
  private final List<CameraData> cameraDatas = new ArrayList<>();

  public static class Builder {
    private final Map<String, CameraConfig> cameraConfigs = new HashMap<>();
    private final AprilTagFieldLayout fieldTags;
    private final NetworkTableInstance ntInstance;
    private final PhotonPoseEstimator.PoseStrategy poseStrategy;

    public Builder(
        NetworkTableInstance ntInstance,
        AprilTagFieldLayout fieldTags,
        PhotonPoseEstimator.PoseStrategy poseStrategy) {
      this.fieldTags = fieldTags;
      this.ntInstance = ntInstance;
      this.poseStrategy = poseStrategy;
    }

    public Builder addCamera(String name, Transform3d transform) {
      return addCamera(name, transform, Optional.empty());
    }

    public Builder addCamera(String name, Transform3d transform, String description) {
      return addCamera(name, transform, Optional.of(description));
    }

    private Builder addCamera(String name, Transform3d transform, Optional<String> description) {
      if (name.equals(LIMELIGHT_CAMERA_NAME)) {
        throw new IllegalArgumentException(String.format("Invalid camera name: '%s'", name));
      }
      if (cameraConfigs.put(name, new CameraConfig(transform, description)) != null) {
        throw new IllegalArgumentException(String.format("Already a camera with name '%s'", name));
      }

      return this;
    }

    public MultiPhotonPoseEstimator build() {
      return new MultiPhotonPoseEstimator(this);
    }
  }

  /**
   * Adds the cameras to the provided simulated vision system.
   *
   * @param propertyFactory Called to get the simulated camera properties for each camera.
   */
  public void addToSim(
      VisionSystemSim simVisionSystem, Function<String, SimCameraProperties> propertyFactory) {
    cameraDatas.forEach(
        estimatorData -> {
          SimCameraProperties cameraProp = propertyFactory.apply(estimatorData.camera.getName());
          PhotonCameraSim simCamera = new PhotonCameraSim(estimatorData.camera(), cameraProp);
          simVisionSystem.addCamera(simCamera, estimatorData.estimator.getRobotToCameraTransform());
        });
  }

  private record CameraConfig(Transform3d robotToCamera, Optional<String> description) {}

  private record CameraData(
      PhotonCamera camera,
      PhotonPoseEstimator estimator,
      Transform3d robotToCamera,
      PhotonVisionPosePublisher publisher,
      StructPublisher<Pose3d> cameraPosePublisher) {}

  private MultiPhotonPoseEstimator(Builder builder) {
    for (Map.Entry<String, CameraConfig> entry : builder.cameraConfigs.entrySet()) {
      String cameraName = entry.getKey();
      PhotonCamera camera = new PhotonCamera(builder.ntInstance, cameraName);
      CameraConfig cameraConfig = entry.getValue();
      PhotonPoseEstimator estimator =
          new PhotonPoseEstimator(
              builder.fieldTags, builder.poseStrategy, cameraConfig.robotToCamera);
      var estimatedPosePublisher = new PhotonVisionPosePublisher(camera, builder.fieldTags);
      NetworkTable table = getTableForCamera(camera);
      var cameraPosePublisher = table.getStructTopic(CAMERA_POSE_TOPIC, Pose3d.struct).publish();

      cameraDatas.add(
          new CameraData(
              camera,
              estimator,
              cameraConfig.robotToCamera,
              estimatedPosePublisher,
              cameraPosePublisher));

      cameraConfig.description.ifPresent(
          description -> table.getEntry("description").setString(description));
    }
  }

  public void setDrivePose(Pose2d pose) {
    Pose3d pose3d = new Pose3d(pose);
    for (CameraData cameraData : cameraDatas) {
      cameraData.cameraPosePublisher.set(pose3d.plus(cameraData.robotToCamera));
    }
  }

  /**
   * Add robot heading data to buffer. Must be called periodically for the
   * <b>PNP_DISTANCE_TRIG_SOLVE</b> strategy.
   *
   * @param timestampSeconds timestamp of the robot heading data.
   * @param heading Field-relative robot heading at given timestamp. Standard WPILIB field
   *     coordinates.
   */
  public void addHeadingData(double timestampSeconds, Rotation2d heading) {
    for (CameraData cameraData : cameraDatas) {
      cameraData.estimator.addHeadingData(timestampSeconds, heading);
    }
  }

  /**
   * Add robot heading data to buffer. Must be called periodically for the
   * <b>PNP_DISTANCE_TRIG_SOLVE</b> strategy.
   *
   * @param timestampSeconds timestamp of the robot heading data.
   * @param heading Field-relative robot heading at given timestamp. Standard WPILIB field
   *     coordinates.
   */
  public void addHeadingData(double timestampSeconds, Rotation3d heading) {
    for (CameraData cameraData : cameraDatas) {
      cameraData.estimator.addHeadingData(timestampSeconds, heading);
    }
  }

  /**
   * Clears all heading data in the buffer, and adds a new seed. Useful for preventing estimates
   * from utilizing heading data provided prior to a pose or rotation reset.
   *
   * @param timestampSeconds timestamp of the robot heading data.
   * @param heading Field-relative robot heading at given timestamp. Standard WPILIB field
   *     coordinates.
   */
  public void resetHeadingData(double timestampSeconds, Rotation2d heading) {
    for (CameraData cameraData : cameraDatas) {
      cameraData.estimator.resetHeadingData(timestampSeconds, heading);
    }
  }

  public void resetHeadingData(double timestampSeconds, Rotation3d heading) {
    // FIXME(photonvision): Use resetHeadingData with Rotation3d (when added to PhotonVision)
    for (CameraData cameraData : cameraDatas) {
      cameraData.estimator.resetHeadingData(timestampSeconds, heading.toRotation2d());
      cameraData.estimator.addHeadingData(timestampSeconds, heading);
    }
  }

  public void update(Consumer<? super EstimatedRobotPose> apply) {
    for (CameraData cameraData : cameraDatas) {
      List<EstimatedRobotPose> poses =
          cameraData.camera.getAllUnreadResults().stream()
              .map(cameraData.estimator::update)
              .flatMap(Optional::stream)
              .toList();

      poses.forEach(apply);
      cameraData.publisher.publish(poses);
    }
  }

  @Override
  public void close() {
    for (CameraData cameraData : cameraDatas) {
      cameraData.camera.close();
    }
    cameraDatas.clear();
  }
}
