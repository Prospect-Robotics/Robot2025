package com.team2813.vision;

import static com.team2813.vision.CameraConstants.LIMELIGHT_CAMERA_NAME;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import org.photonvision.PhotonCamera;

public final class VisionNetworkTables {
  public static final String HAS_DATA_TOPIC = "hasData";
  public static final String VISIBLE_APRIL_TAG_POSES_TOPIC = "visibleAprilTagPoses";

  static final String CAMERA_POSE_TOPIC = "cameraPose";
  static final String POSE_ESTIMATE_TOPIC = "poseEstimate";
  static final String APRIL_TAG_POSE_TOPIC = "aprilTagPose";

  private static final String TABLE_NAME = "Vision";

  public static NetworkTable getTableForCamera(NetworkTableInstance ntInstance, String cameraName) {
    return ntInstance.getTable(TABLE_NAME).getSubTable(cameraName);
  }

  public static NetworkTable getTableForCamera(PhotonCamera camera) {
    return getTableForCamera(camera.getCameraTable().getInstance(), camera.getName());
  }

  public static NetworkTable getTableForLimelight(NetworkTableInstance ntInstance) {
    return getTableForCamera(ntInstance, LIMELIGHT_CAMERA_NAME);
  }

  private VisionNetworkTables() {
    throw new AssertionError("Not instantiable");
  }
}
