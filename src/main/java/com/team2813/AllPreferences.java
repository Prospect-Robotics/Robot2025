package com.team2813;

import edu.wpi.first.wpilibj.Preferences;
import java.util.Map;
import java.util.function.BooleanSupplier;

/**
 * Holder for all values stored in {@link Preferences} for the robot.
 *
 * <p>The values can be viewed and edited on SmartDashboard or Shuffleboard. If the values are
 * edited, the updated values are persisted across reboots.
 */
public class AllPreferences {
  private static final Map<Key, String> LEGACY_BOOLEAN_PREFERENCES =
      Map.of(
          Key.USE_PHOTON_VISION_LOCATION,
          "subsystems.Drive.DriveConfiguration.usePhotonVisionLocation");

  static synchronized void migrateLegacyPreferences() {
    for (var entry : LEGACY_BOOLEAN_PREFERENCES.entrySet()) {
      String oldKey = entry.getKey().name();
      String newKey = entry.getValue();
      if (Preferences.containsKey(oldKey)) {
        if (!Preferences.containsKey(newKey)) {
          boolean value = Preferences.getBoolean(oldKey, false);
          Preferences.initBoolean(newKey, value);
        }
        Preferences.remove(oldKey);
      }
    }
  }

  public static BooleanSupplier useAutoAlignWaypoints() {
    return booleanPref(Key.USE_AUTO_ALIGN_WAYPOINTS, true);
  }

  private static BooleanSupplier booleanPref(Key key, boolean defaultValue) {
    String name = key.name();
    if (!Preferences.containsKey(name)) {
      Preferences.initBoolean(name, defaultValue);
    }
    return () -> Preferences.getBoolean(name, defaultValue);
  }

  private enum Key {
    USE_AUTO_ALIGN_WAYPOINTS,
    USE_PHOTON_VISION_LOCATION,
  }

  private AllPreferences() {
    throw new AssertionError("Not instantiable");
  }
}
