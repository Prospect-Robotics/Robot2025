package com.team2813;

import com.team2813.lib2813.preferences.BooleanPreference;
import com.team2813.lib2813.preferences.DoublePreference;

/**
 * Accessors for preferences for the robot.
 *
 * <p>Preferences are stored in the robot's flash memory. Values for the
 * preferences can be updated in SmartDashboard/Shuffleboard.
 *
 * @see <a href="https://docs.wpilib.org/en/stable/docs/software/basic-programming/robot-preferences.html"
 * target="_top">Setting Robot Preferences</a>
 */
public final class Preferences {

  public enum BooleanPref implements BooleanPreference {
    DRIVE_ADD_LIMELIGHT_MEASUREMENT;

    BooleanPref(boolean defaultValue) {
      this.defaultValue = defaultValue;
      initialize();
    }

    BooleanPref() {
      this(false);
    }

    private final boolean defaultValue;

    @Override
    public boolean defaultValue() {
      return defaultValue;
    }
  }

  public enum DoublePref implements DoublePreference {
    MAX_LIMELIGHT_DRIVE_DIFFERENCE_METERS(1.0);

    DoublePref(double defaultValue) {
      this.defaultValue = defaultValue;
      initialize();
    }

    private final double defaultValue;

    @Override
    public double defaultValue() {
      return defaultValue;
    }
  }

  private Preferences() {
    throw new AssertionError("Not instantiable");
  }
}
