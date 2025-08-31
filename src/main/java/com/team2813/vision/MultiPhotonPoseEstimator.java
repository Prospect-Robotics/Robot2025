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
import java.util.stream.Collectors;
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
 * <p>Note that, when we are dealing with 2D and 3D poses, we follow the transformation conventions
 * established by WPILib and PhotonVision:
 * https://docs.photonvision.org/en/latest/docs/apriltag-pipelines/coordinate-systems.html
 *
 * <p>Furthermore note that the global robot pose or any of the camera global poses are also
 * referred to as "field-centric pose". In our libraries, field-centric poses are always specified
 * relative to the blue origin per
 * https://docs.wpilib.org/en/stable/docs/software/basic-programming/coordinate-system.html#always-blue-origin
 */
public class MultiPhotonPoseEstimator implements AutoCloseable {
  private final List<PhotonCameraWrapper> cameraWrappers;

  public static class Builder {
    private final Map<String, CameraConfig> cameraConfigs = new HashMap<>();
    private final AprilTagFieldLayout aprilTagFieldLayout;
    private final NetworkTableInstance ntInstance;
    private final PhotonPoseEstimator.PoseStrategy poseEstimatorStrategy;

    /**
     * MultiPhotonPoseEstimator builder constructor.
     *
     * @param ntInstance Network table instance used to log the pose of AprilTag detections as well
     *     as pose estimates.
     * @param aprilTagFieldLayout WPILib field description (dimensions) including AprilTag 3D
     *     locations.
     * @param poseEstimatorStrategy Posing strategy (for instance, multi tag PnP, closest to camera
     *     tag, etc.)
     */
    public Builder(
        NetworkTableInstance ntInstance,
        AprilTagFieldLayout aprilTagFieldLayout,
        PhotonPoseEstimator.PoseStrategy poseEstimatorStrategy) {
      this.ntInstance = ntInstance;
      this.aprilTagFieldLayout = aprilTagFieldLayout;
      this.poseEstimatorStrategy = poseEstimatorStrategy;
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
    cameraWrappers.forEach(
        cameraWrapper -> {
          SimCameraProperties cameraProp = propertyFactory.apply(cameraWrapper.camera.getName());
          PhotonCameraSim simCamera = new PhotonCameraSim(cameraWrapper.camera(), cameraProp);
          simVisionSystem.addCamera(simCamera, cameraWrapper.estimator.getRobotToCameraTransform());
        });
  }

  /** Configuration for a camera that is connected to PhotonVision. */
  private record CameraConfig(Transform3d robotToCamera, Optional<String> description) {}

  /**
   * Wrapper containing a PhotonVision camera, pose estimator and publishers.
   *
   * @param camera A camera connected to PhotonVision.
   * @param estimator A pose estimator configured for this camera.
   * @param robotToCamera The 3D fixed pose of the camera relative to the robot. Intuitively, this
   *     field describes where on the robot the camera is mounted.
   * @param robotPosePublisher A publisher reporting PhotonVision pose detections to NetworkTables
   *     during the robot runtime.
   * @param cameraPosePublisher A publisher reporting the position of the camera in field-centric
   *     coordinates. In other words, this is the pose most recently set by {@link @setDrivePose}
   *     with the camera's own robotToCamera pose appended to it.
   */
  private record PhotonCameraWrapper(
      PhotonCamera camera,
      PhotonPoseEstimator estimator,
      Transform3d robotToCamera,
      PhotonVisionPosePublisher robotPosePublisher,
      StructPublisher<Pose3d> cameraPosePublisher)
      implements AutoCloseable {

    /**
     * Publishes the estimated drive pose calculated from this camera.
     *
     * @param pose 3D field-centric (relative to blue origin) pose of the drive train.
     */
    void publishEstimatedDrivePose(Pose3d pose) {
      cameraPosePublisher.set(pose.plus(robotToCamera));
    }

    @Override
    public void close() {
      // TODO: Close publishers
      camera.close();
    }
  }

  /** Creates an instance using values from a {@code Builder}. */
  private MultiPhotonPoseEstimator(Builder builder) {
    cameraWrappers =
        builder.cameraConfigs.entrySet().stream()
            .map(entry -> createCameraWrapperFromConfig(builder, entry.getKey(), entry.getValue()))
            .collect(Collectors.toCollection(ArrayList::new));
  }

  /**
   * Creates a {@link PhotonCameraWrapper} instance for a camera with the given name and
   * configuration.
   *
   * <p>The returned value is used to get pose estimates from the camera.
   */
  private static PhotonCameraWrapper createCameraWrapperFromConfig(
      Builder builder, String cameraName, CameraConfig cameraConfig) {
    PhotonCamera camera = new PhotonCamera(builder.ntInstance, cameraName);
    PhotonPoseEstimator estimator =
        new PhotonPoseEstimator(
            builder.aprilTagFieldLayout, builder.poseEstimatorStrategy, cameraConfig.robotToCamera);

    // (TODO(vdikov): consider restructuring how the topics under which we publish in network
    // tables are more explicitly listed somewhere, e.g., in a constants file of sorts. Right now,
    // the actual path under which we publish is constructed across multiple levels of function
    // calls, so if a software developer needs to track where a specific value they observe in,
    // say, Advantage Scope is reported from, they have to trace through all these function
    // calls. In contrast, the easiest paths to track from one system back to the code are the
    // hard-coded paths - but that's not really an option here either, since we need dynamic
    // information, like the camera name, to be part of the final topic path. Using template paths
    // might be a good middle ground.)
    //
    // Note that some of the current code can be simplified when we remove the Limelight code
    // (since VisionNetworkTable.getTableForLimelight() could be removed, allowing us to remove
    // some of the levels of function calls).

    // Create NetworkTables publishers for 1) the position of the camera relative to the robot and
    // 2) the estimated position provided by the camera.
    NetworkTable table = getTableForCamera(camera);
    StructPublisher<Pose3d> cameraPosePublisher =
        table.getStructTopic(CAMERA_POSE_TOPIC, Pose3d.struct).publish();
    var estimatedPosePublisher = new PhotonVisionPosePublisher(camera, builder.aprilTagFieldLayout);

    // If the caller provided a description for this camera, publish it to the camera network table.
    cameraConfig.description.ifPresent(
        description -> table.getEntry("description").setString(description));

    return new PhotonCameraWrapper(
        camera, estimator, cameraConfig.robotToCamera, estimatedPosePublisher, cameraPosePublisher);
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
    for (PhotonCameraWrapper cameraWrapper : cameraWrappers) {
      cameraWrapper.publishEstimatedDrivePose(pose3d);
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
    for (PhotonCameraWrapper cameraWrapper : cameraWrappers) {
      cameraWrapper.estimator.addHeadingData(timestampSeconds, heading);
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
    for (PhotonCameraWrapper cameraWrapper : cameraWrappers) {
      cameraWrapper.estimator.addHeadingData(timestampSeconds, heading);
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
    for (PhotonCameraWrapper cameraWrapper : cameraWrappers) {
      cameraWrapper.estimator.resetHeadingData(timestampSeconds, heading);
    }
  }

  public void resetHeadingData(double timestampSeconds, Rotation3d heading) {
    // TODO: Use PhotonPoseEstimator.resetHeadingData(double, Rotation2d) once we use a version of
    // PhotonVision that includes it (see  https://github.com/PhotonVision/photonvision/pull/2013).
    for (PhotonCameraWrapper cameraWrapper : cameraWrappers) {
      cameraWrapper.estimator.resetHeadingData(timestampSeconds, heading.toRotation2d());
      cameraWrapper.estimator.addHeadingData(timestampSeconds, heading);
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
    for (PhotonCameraWrapper cameraWrapper : cameraWrappers) {
      List<EstimatedRobotPose> poses =
          cameraWrapper.camera.getAllUnreadResults().stream()
              .map(cameraWrapper.estimator::update)
              .flatMap(Optional::stream)
              .toList();

      poses.forEach(apply);
      cameraWrapper.robotPosePublisher.publish(poses);
    }
  }

  @Override
  public void close() {
    cameraWrappers.forEach(PhotonCameraWrapper::close);
    cameraWrappers.clear();
  }
}
