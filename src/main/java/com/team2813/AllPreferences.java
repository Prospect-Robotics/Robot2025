package com.team2813;

import edu.wpi.first.wpilibj.Preferences;

import java.util.function.BooleanSupplier;
import java.util.function.DoubleSupplier;

/**
 * Holder for all values stored in {@link Preferences} for the robot.
 *
 * <p>The values can be viewed and edited on SmartDashboard or Shuffleboard. If the values
 * are edited, the updated values are persisted across reboots.
 */
public class AllPreferences {

  public static BooleanSupplier useLimelightLocation() {
    return booleanPref(Key.USE_LIMELIGHT_LOCATION, false);
  }

  public static DoubleSupplier maxLimelightError() {
    return doublePref(Key.MAX_LIMELIGHT_ERROR, 0.1d); // 10%
  }

  private static BooleanSupplier booleanPref(Key key, boolean defaultValue) {
    String name = key.name();
    if (!Preferences.containsKey(name)) {
      Preferences.initBoolean(name, defaultValue);
    }
    return () -> Preferences.getBoolean(name, defaultValue);
  }

  private static DoubleSupplier doublePref(Key key, double defaultValue) {
    String name = key.name();
    if (!Preferences.containsKey(name)) {
      Preferences.initDouble(name, defaultValue);
    }
    return () -> Preferences.getDouble(name, defaultValue);
  }

  private enum Key {
    USE_LIMELIGHT_LOCATION,
    MAX_LIMELIGHT_ERROR,
  }

  private AllPreferences() {
    throw new AssertionError("Not instantiable");
  }
}
