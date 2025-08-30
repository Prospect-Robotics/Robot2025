package com.team2813.vision;

import static com.team2813.vision.CameraConstants.LIMELIGHT_CAMERA_NAME;
import static com.team2813.vision.VisionNetworkTables.CAMERA_POSE_TOPIC;
import static com.team2813.vision.VisionNetworkTables.getTableForCamera;

import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Rotation3d;
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

/**
 * Provides estimated robot positions, in field pose, from multiple PhotonVision cameras.
 *
 * <p>This class manages one or more PhotonVision cameras, and provides an API {@link
 * #update(Consumer)} to provide an updated estimated robot pose by combining readings from
 * AprilTags visible from the cameras. It also supports adding camera configurations to
 * PhotonVision's simulated vision system.
 *
 * <p>Note that, when we are dealing with 2D and 3D poses, the we follow the transformation
 * conventions established by WPILib and PhotonVision:
 * https://docs.photonvision.org/en/latest/docs/apriltag-pipelines/coordinate-systems.html
 *
 * <p>Furthermore note that the global robot pose or any of the camera global poses are also
 * referred to as "field-centric pose". In our librarires, field-centric poses are always specified
 * relative to the blue origin per
 * https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html#always-blue-origin
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
     * @param fieldTags WPILib field description (dimensions) including AprilTag 3D locations.
     * @param poseStrategy Posing strategy (for instance, multi tag PnP, closest to camera tag,
     *     etc.)
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

  /** A camera that is connected to PhotonVision. */
  private record CameraConfig(Transform3d robotToCamera, Optional<String> description) {}

  /**
   * Holds configuration for a camera for the Builder.
   *
   * @param camera A camera connected to PhotonVision.
   * @param estimator A pose estimator configured for this camera.
   * @param robotToCamera The 3D fixed pose of the camera relative to the robot. Intuitively, this
   *     field describes where on the robot the camera is mounted.
   * @param publisher A publisher reporting PhotonVision pose detections to NetworkTables during the
   *     robot runtime.
   * @param cameraPosePublisher A publisher reporting the position of the camera in field-centric
   *     coordinates. In other words, this is the pose most recently set by {@link @setDrivePose}
   *     with the camera's own robotToCamera pose appended to it.
   */
  private record CameraData(
      PhotonCamera camera,
      PhotonPoseEstimator estimator,
      Transform3d robotToCamera,
      PhotonVisionPosePublisher publisher,
      StructPublisher<Pose3d> cameraPosePublisher) {}

  /** Creates an instance using values from a {@code Builder}. */
  private MultiPhotonPoseEstimator(Builder builder) {
    for (var entry : builder.cameraConfigs.entrySet()) {
      String cameraName = entry.getKey();
      CameraConfig cameraConfig = entry.getValue();

      PhotonCamera camera = new PhotonCamera(builder.ntInstance, cameraName);
      PhotonPoseEstimator estimator =
          new PhotonPoseEstimator(
              builder.fieldTags, builder.poseStrategy, cameraConfig.robotToCamera);
      // A NetworkTables publisher, preconfigured to post timestamped pose estimates from `camera`.
      var estimatedPosePublisher = new PhotonVisionPosePublisher(camera, builder.fieldTags);
      // Gets a NetworkTables subtable, dedicated to `camera`.
      // It will typically be nested under `photonvision/Vision/<camera_name>`
      // (TODO(vdikov): consider restructuring how the topics under which we publish in network
      // tables are more explicitly listed somewhere, e.g., in a constants file of sorts. Right now,
      // the actual path under which we publish is constructed across multiple levels of function
      // calls, so if a software developer needs to track where a specific value they observe in,
      // say, Advantage Scope is reported from, they have to trace through all these function
      // calls. In contrast, the easiest paths to track from one system back to the code are the
      // hard-coded paths - but that's not really an option here either, since we need dynamic
      // information, like the camera name, to be part of the final topic path. Using template paths
      // might be a good middle ground.)
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
   * Sets a 2D pose estimate in a field-centric frame (relative to the blue origin).
   *
   * <p>This method takes a field-centric drive train pose (drive train and robot are the same
   * here), update the camera field-centric poses and publish them on network tables.
   *
   * <p>TODO(vdikov): This method sits very counter-intiutively in this class. The class is all
   * about estimating pose and feeding it to the drive train pose estimation. Yet, this method is
   * feeding a drive-train `pose` back to it. One could reasonably assume that the drive train pose
   * is somehow used for the multi-photon pose estimation and plays some role there. But the method
   * code tells a much more prosaic story - the `pose` is only used for reporting camera poses,
   * relative to "some" drive-train (at that point we don't even know if that pose is derived from
   * the multi-photon pose estimation whatsoever). The MultiPhotonPoseEstimator API would become
   * cleaner if we remove this method and find other ways to report Camera poses. kcooney@ has
   * drafted several cool ideas how we can address that with a better class/interfaces architecture
   * here: https://github.com/Prospect-Robotics/Robot2025/pull/157#discussion_r2282753534
   *
   * @param pose 2D field-centric (relative to blue origin) pose of the drive train (i.e., the
   *     robot).
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
   * Takes a consumer for estimated poses and applies all unread robot-pose estimatations from all
   * cameras against `apply`.
   *
   * <p>This method is supposed to be called from a routine updating drive-train pose with pose
   * estimates from the photon vision cameras.
   *
   * <p>TODO(vdikov): Further ideas how to refactor this interface are suggested by kcooney@ in this
   * comment https://github.com/Prospect-Robotics/Robot2025/pull/157#discussion_r2282806711
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
