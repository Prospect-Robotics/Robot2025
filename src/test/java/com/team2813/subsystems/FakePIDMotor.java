package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.AngularVelocity;

public abstract class FakePIDMotor implements PIDMotor {
  double demand = 0.0f;
  private ControlMode controlMode;

  double getVoltage() {
    assertThat(controlMode).isEqualTo(ControlMode.VOLTAGE);
    return demand;
  }

  @Override
  public void set(ControlMode mode, double demand) {
    assertThat(mode).isNotNull();
    controlMode = mode;
    this.demand = demand;
  }

  @Override
  public void set(ControlMode mode, double demand, double feedForward) {
    set(mode, demand);
  }

  @Override
  public AngularVelocity getVelocityMeasure() {
    return Units.RadiansPerSecond.of(demand * 20);
  }

  @Override
  public double getVelocity() {
    throw new AssertionError("Called deprecated method");
  }
}
