package com.team2813;

import edu.wpi.first.wpilibj.Preferences;
import java.util.function.BooleanSupplier;
import java.util.function.DoubleSupplier;

/**
 * Holder for all values stored in {@link Preferences} for the robot.
 *
 * <p>The values can be viewed and edited on SmartDashboard or Shuffleboard. If the values are
 * edited, the updated values are persisted across reboots.
 */
public class AllPreferences {

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

  private static DoubleSupplier doublePref(Key key, double defaultValue) {
    String name = key.name();
    if (!Preferences.containsKey(name)) {
      Preferences.initDouble(name, defaultValue);
    }
    return () -> Preferences.getDouble(name, defaultValue);
  }

  private enum Key {
    USE_AUTO_ALIGN_WAYPOINTS,
  }

  private AllPreferences() {
    throw new AssertionError("Not instantiable");
  }
}
