package com.team2813.sysid;

import com.ctre.phoenix6.controls.NeutralOut;
import com.ctre.phoenix6.controls.TorqueCurrentFOC;
import com.ctre.phoenix6.controls.VoltageOut;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Voltage;

import java.util.function.Function;

class Requests {
  public static NeutralOut NEUTRAL_OUT = new NeutralOut();
  public static VoltageOut VOLTAGE_OUT = new VoltageOut(0);
  public static TorqueCurrentFOC TORQUE_CURRENT_FOC = new TorqueCurrentFOC(0);
  public static Function<Voltage, Double> CONVERT_VOLTAGE = (v) -> v.in(Units.Volts);
  public static SwerveSysidRequest DRIVE_SYSID = new SwerveSysidRequest(MotorType.Drive, RequestType.VoltageOut);
  public static SwerveSysidRequest STEER_SYSID = new SwerveSysidRequest(MotorType.Swerve, RequestType.VoltageOut);
  private Requests() {
    throw new AssertionError("Not instantiable!");
  }
}
