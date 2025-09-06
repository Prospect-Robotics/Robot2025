package com.team2813;

import edu.wpi.first.wpilibj.Preferences;
import java.util.List;
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

  public static final List<String> DRIVE_BOOLEAN_PREFERENCE_KEYS =
      List.of(
          "addLimelightMeasurement", "usePhotonVisionLocation", "usePnpDistanceTrigSolveStrategy");
  public static final List<String> DRIVE_DOUBLE_PREFERENCE_KEYS =
      List.of(
          "maxLimelightDifferenceMeters", "maxRotationsPerSecond", "maxVelocityInMetersPerSecond");

  /** Migrate Preferences stored on the robot from older keys to current keys. */
  static synchronized void migrateLegacyPreferences() {
    for (var entry : LEGACY_BOOLEAN_PREFERENCES.entrySet()) {
      String oldKey = entry.getKey().name();
      String newKey = entry.getValue();
      migratePreference(oldKey, newKey, AllPreferences::booleanPreferenceMigrator);
    }

    for (var key : REMOVED_PREFERENCES) {
      if (Preferences.containsKey(key)) {
        Preferences.remove(key);
      }
    }

    migrateDrivePreferences(
        DRIVE_BOOLEAN_PREFERENCE_KEYS, AllPreferences::booleanPreferenceMigrator);
    migrateDrivePreferences(DRIVE_DOUBLE_PREFERENCE_KEYS, AllPreferences::doublePreferenceMigrator);
  }

  @FunctionalInterface
  private interface PreferenceMigrator {
    void migrate(String oldKey, String newKey);
  }

  private static void migrateDrivePreferences(List<String> keys, PreferenceMigrator migrator) {
    for (String key : keys) {
      String oldKey = "subsystems.Drive.DriveConfiguration." + key;
      String newKey = "Drive/" + key;
      migratePreference(oldKey, newKey, migrator);
    }
  }

  private static void booleanPreferenceMigrator(String oldKey, String newKey) {
    boolean value = Preferences.getBoolean(oldKey, false);
    Preferences.initBoolean(newKey, value);
  }

  private static void doublePreferenceMigrator(String oldKey, String newKey) {
    double value = Preferences.getDouble(oldKey, -1);
    if (value > 0) {
      Preferences.initDouble(newKey, value);
    }
  }

  private static void migratePreference(String oldKey, String newKey, PreferenceMigrator migrator) {
    if (Preferences.containsKey(oldKey)) {
      if (!Preferences.containsKey(newKey)) {
        migrator.migrate(oldKey, newKey);
      }
      Preferences.remove(oldKey);
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
