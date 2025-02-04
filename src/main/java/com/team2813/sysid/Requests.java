package com.team2813.sysid;

import com.ctre.phoenix6.controls.MotionMagicVoltage;
import com.ctre.phoenix6.controls.TorqueCurrentFOC;
import com.ctre.phoenix6.controls.VoltageOut;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Voltage;

import java.util.function.Function;

class Requests {
  public static final MotionMagicVoltage NEUTRAL_OUT = new MotionMagicVoltage(0)
          .withEnableFOC(false).withFeedForward(0).withSlot(0)
          .withOverrideBrakeDurNeutral(false).withLimitForwardMotion(false)
          .withLimitReverseMotion(false);
  public static VoltageOut VOLTAGE_OUT = new VoltageOut(0);
  public static TorqueCurrentFOC TORQUE_CURRENT_FOC = new TorqueCurrentFOC(0);
  public static Function<Voltage, Double> CONVERT_VOLTAGE = (v) -> v.in(Units.Volts);
  private Requests() {
    throw new AssertionError("Not instantiable!");
  }
}
