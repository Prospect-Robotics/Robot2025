package com.team2813.vision;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;

final class VisionUtil {
  private static final String TABLE_NAME = "Vision";

  static NetworkTable getTableForCamera(NetworkTableInstance ntInstance, String cameraName) {
    return ntInstance.getTable(TABLE_NAME).getSubTable(cameraName);
  }

  private VisionUtil() {
    throw new AssertionError("Not instantiable");
  }
}
