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

/**
 * A class that manages of one or more Photonvision cameras, their robotToCamera 3D poses and pose
 * estimators. The class provides an interface to consume the pose estimations from all cameras -
 * the `update(...)` method. The class also supports adding the camera configurations to robot
 * simulation.
 */
public class MultiPhotonPoseEstimator implements AutoCloseable {
  private final List<CameraData> cameraDatas = new ArrayList<>();

  public static class Builder {
    private final Map<String, CameraConfig> cameraConfigs = new HashMap<>();
    private final AprilTagFieldLayout fieldTags;
    private final NetworkTableInstance ntInstance;
    private final PhotonPoseEstimator.PoseStrategy poseStrategy;

    /**
     * MultiPhotonPoseEstimator builder constructor.
     *
     * @param ntInstance Network table instance used to log the pose of AprilTag detections as well
     *     as pose estimates.
     * @param fieldTags WPLib field description (dimensions) incl. AprilTag 3D locations.
     * @param poseStrategy Posing strategy (e.g., multi tag PnP, closest to camera tag, etc.)
     */
    public Builder(
        NetworkTableInstance ntInstance,
        AprilTagFieldLayout fieldTags,
        PhotonPoseEstimator.PoseStrategy poseStrategy) {
      this.fieldTags = fieldTags;
      this.ntInstance = ntInstance;
      this.poseStrategy = poseStrategy;
    }

    /**
     * Adds a camera to the multi pose estimator.
     *
     * @param name Unique name of the camera.
     * @param transform 3D position of the camera relative to the robot frame.
     * @return Builder instance.
     */
    public Builder addCamera(String name, Transform3d transform) {
      return addCamera(name, transform, Optional.empty());
    }

    /**
     * Adds a camera to the multi pose estimator.
     *
     * @param name Unique name of the camera.
     * @param transform 3D position of the camera relative to the robot frame.
     * @param description Camera description.
     * @return Builder instance.
     */
    public Builder addCamera(String name, Transform3d transform, String description) {
      return addCamera(name, transform, Optional.of(description));
    }

    /**
     * Adds a camera to the multi pose estimator.
     *
     * @param name Unique name of the camera.
     * @param transform 3D position of the camera relative to the robot frame.
     * @param description Camera description.
     * @return Builder instance.
     */
    private Builder addCamera(String name, Transform3d transform, Optional<String> description) {
      if (name.equals(LIMELIGHT_CAMERA_NAME)) {
        throw new IllegalArgumentException(String.format("Invalid camera name: '%s'", name));
      }
      if (cameraConfigs.put(name, new CameraConfig(transform, description)) != null) {
        throw new IllegalArgumentException(String.format("Already a camera with name '%s'", name));
      }

      return this;
    }

    /** Builds a configured MultiPhotonPoseEstimator. */
    public MultiPhotonPoseEstimator build() {
      return new MultiPhotonPoseEstimator(this);
    }
  }

  /**
   * Adds the current Multi-Photon camera setup to a simulated vision system.
   *
   * @param simVisionSystem The simulated visual system.
   * @param propertyFactory Functor that creates simulated camera properties.
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

  /** Record of robot to camera 3D pose and the camera description. */
  private record CameraConfig(Transform3d robotToCamera, Optional<String> description) {}

  /**
   * Record of a camera that is connected to PhotonVision.
   *
   * @param camera A camera connected to photon vision.
   * @param estimator A pose estimator configured for this camera.
   * @param robotToCamera The 3D fixed pose of the camera relative to the robot. Intuitively, this
   *     field describes where on the robot the camera is mounted.
   * @param publisher A publisher reporting photon vision pose detections to NetworkTables during
   *     the robot runtime.
   * @param cameraPosePublisher A publisher reporting the position of the camera in field frame
   *     (TODO(vdikov): this is presumably just robot pose estimate + robotToCamera pose but I need
   *     to double-check this).
   */
  private record CameraData(
      PhotonCamera camera,
      PhotonPoseEstimator estimator,
      Transform3d robotToCamera,
      PhotonVisionPosePublisher publisher,
      StructPublisher<Pose3d> cameraPosePublisher) {}

  /**
   * MultiPhotonPoseEstimator constructor from a Builder.
   *
   * <p>This constructor is explicitly called by the Builder.build() method. It builds a
   * MultiPhotonPoseEstimator from the user settings configured in `builder`.
   *
   * @param builder A builder configured by the user.
   */
  private MultiPhotonPoseEstimator(Builder builder) {
    for (var entry : builder.cameraConfigs.entrySet()) {
      String cameraName = entry.getKey();
      CameraConfig cameraConfig = entry.getValue();

      PhotonCamera camera = new PhotonCamera(builder.ntInstance, cameraName);
      // Configure a PhotonVision pose estimator, to run against a set of AprilTags (described by
      // `builder.fieldTags`), applying `poseStrategy`, from the perspective of a camera mounted at
      // a 3D position `cameraConfig.robotToCamera`
      PhotonPoseEstimator estimator =
          new PhotonPoseEstimator(
              builder.fieldTags, builder.poseStrategy, cameraConfig.robotToCamera);
      // A NetworkTables publisher, preconfigured to post timestamped pose estimates from `camera`.
      var estimatedPosePublisher = new PhotonVisionPosePublisher(camera, builder.fieldTags);
      // Gets a NetworkTables subtable, dedicated to `camera`.
      // It will typically be nested under `photonvision/Vision/<camera_name>` (TODO(vdikov):
      // confirm that)
      NetworkTable table = getTableForCamera(camera);
      var cameraPosePublisher = table.getStructTopic(CAMERA_POSE_TOPIC, Pose3d.struct).publish();

      // Add the camera data to camera datas for the lifetime of the multi-photon pose estimator.
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

  /**
   * Sets a 2D pose estimate (field-centric ??).
   *
   * <p>This method takes a field-centric (??) drive train pose (drive train and robot are the same
   * here), update the camera field-centric poses and publish them on network tables.
   *
   * <p>TODO(vdikov): This method sits very counter-intiutively in this class. The class is all
   * about estimating pose and feeding it to the drive train pose estimation. Yet, this method is
   * feeding a drive-train `pose` back to it. One could reasonably assume that the drive train pose
   * is somehow used for the multi-photon pose estimation and plays some role there. But the method
   * code tells a much more prosaic story - the `pose` is only used for reporting camera poses,
   * relative to "some" drive-train (at that point we don't even know if that pose is derived from
   * the multi-photon pose estimation whatsoever). The MultiPhotonPoseEstimator API would become
   * cleaner if we remove this method and find other ways to report Camera poses.
   *
   * @param pose 2D field-centric (??) pose of the drive train (i.e., the robot).
   */
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

  /**
   * Takes a consumer for estimated poses and applies all unread robot-pose estimatations from all
   * cameras against `apply`.
   *
   * <p>This method is supposed to be called from a routine updating drive-train pose with pose
   * estimates from the photon vision cameras.
   *
   * @param apply Callback to consume unread photonevision robot-pose estimations.
   */
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
