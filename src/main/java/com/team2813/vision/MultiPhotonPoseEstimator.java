package com.team2813.vision;

import static com.team2813.vision.VisionUtil.getTableForCamera;

import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Transform3d;
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
      if (name.equals(LimelightPosePublisher.CAMERA_NAME)) {
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
      var cameraPosePublisher = table.getStructTopic("cameraPose", Pose3d.struct).publish();

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
