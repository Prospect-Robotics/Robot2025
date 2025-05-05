package com.team2813;

import edu.wpi.first.wpilibj.Preferences;
import java.util.Map;
import java.util.Set;

/**
 * Holder for all values stored in {@link Preferences} for the robot.
 *
 * <p>The values can be viewed and edited on SmartDashboard or Shuffleboard. If the values are
 * edited, the updated values are persisted across reboots.
 *
 * @deprecated use {@link com.team2813.lib2813.preferences.PreferencesInjector}
 */
@Deprecated
class AllPreferences {
  private static final Map<Key, String> LEGACY_BOOLEAN_PREFERENCES =
      Map.of(
          Key.USE_AUTO_ALIGN_WAYPOINTS,
          "RobotLocalization/useAutoAlignWaypoints",
          Key.USE_PHOTON_VISION_LOCATION,
          "subsystems.Drive.DriveConfiguration.usePhotonVisionLocation");

  private static final Set<String> REMOVED_PREFERENCES =
      Set.of("USE_LIMELIGHT_LOCATION", "DRIVE_ADD_LIMELIGHT_MEASUREMENT");

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
    for (var key : REMOVED_PREFERENCES) {
      if (Preferences.containsKey(key)) {
        Preferences.remove(key);
      }
    }
  }

  private enum Key {
    USE_AUTO_ALIGN_WAYPOINTS,
    USE_PHOTON_VISION_LOCATION,
  }

  private AllPreferences() {
    throw new AssertionError("Not instantiable");
  }
}
