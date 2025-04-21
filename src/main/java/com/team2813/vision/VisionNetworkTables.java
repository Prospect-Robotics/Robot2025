package com.team2813.vision;

import static com.team2813.vision.CameraConstants.LIMELIGHT_CAMERA_NAME;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import org.photonvision.PhotonCamera;

public final class VisionNetworkTables {
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
