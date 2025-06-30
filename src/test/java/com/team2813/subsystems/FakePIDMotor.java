package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.AngularVelocity;

abstract class FakePIDMotor implements PIDMotor {
  double voltage = 0.0f;

  @Override
  public void set(ControlMode mode, double voltage) {
    assertThat(mode).isEqualTo(ControlMode.VOLTAGE);
    this.voltage = voltage;
  }

  @Override
  public void set(ControlMode mode, double demand, double feedForward) {
    set(mode, demand);
  }

  @Override
  public AngularVelocity getVelocityMeasure() {
    return Units.RadiansPerSecond.of(voltage * 20);
  }

  @Override
  public double getVelocity() {
    throw new AssertionError("Called deprecated method");
  }
}
