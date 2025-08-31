package com.team2813.vision;

import static com.team2813.vision.CameraConstants.LIMELIGHT_CAMERA_NAME;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import org.photonvision.PhotonCamera;

/**
 * Contains methods and constants for publishing data from robot vision systems to network tables.
 */
public final class VisionNetworkTables {
  /** Topic name to use when publishing whether a camera has current data. */
  public static final String HAS_DATA_TOPIC = "hasData";

  /** Topic name to use when publishing positions of detected AprilTags as a Pose3d array. */
  public static final String VISIBLE_APRIL_TAG_POSES_TOPIC = "visibleAprilTagPoses";

  /** Topic name to use when publishing the Pose3d position of a camera. */
  static final String CAMERA_POSE_TOPIC = "cameraPose";

  /** Topic name to use when publishing the estimated robot position as a Pose2d value */
  static final String POSE_ESTIMATE_TOPIC = "poseEstimate";

  /** Topic name to use when publishing the position of the detected AprilTag as a Pose2d value. */
  static final String APRIL_TAG_POSE_TOPIC = "aprilTagPose";

  private static final String TABLE_NAME = "Vision";

  /**
   * Gets the network table for the camera with the given name
   *
   * <p>The key of the network table will be `Vision/<cameraName>`.
   *
   * @param ntInstance network table instance to publish to.
   * @param cameraName name of the camera.
   */
  public static NetworkTable getTableForCamera(NetworkTableInstance ntInstance, String cameraName) {
    return ntInstance.getTable(TABLE_NAME).getSubTable(cameraName);
  }

  /**
   * Gets the network table for the provided photon vision camera.
   *
   * <p>The key of the network table will be `Vision/<camera name>`.
   */
  public static NetworkTable getTableForCamera(PhotonCamera camera) {
    return getTableForCamera(camera.getCameraTable().getInstance(), camera.getName());
  }

  /**
   * Gets the network table for the limelight camera.
   *
   * @param ntInstance network table instance to publish to.
   */
  public static NetworkTable getTableForLimelight(NetworkTableInstance ntInstance) {
    return getTableForCamera(ntInstance, LIMELIGHT_CAMERA_NAME);
  }

  private VisionNetworkTables() {
    throw new AssertionError("Not instantiable");
  }
}
