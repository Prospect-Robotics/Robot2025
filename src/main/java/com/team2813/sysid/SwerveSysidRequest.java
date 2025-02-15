package com.team2813.sysid;

import com.ctre.phoenix6.StatusCode;
import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveModule;
import com.ctre.phoenix6.swerve.SwerveRequest;
import edu.wpi.first.units.measure.Voltage;

public final class SwerveSysidRequest implements SwerveRequest {
  private final RequestType requestType;
  private final MotorType motorType;
  private Voltage curVoltage;

  public SwerveSysidRequest(MotorType motorType, RequestType requestType) {
    this.requestType = requestType;
    this.motorType = motorType;
  }

  @Override
  public StatusCode apply(SwerveDrivetrain.SwerveControlParameters parameters, SwerveModule<?, ?, ?>... modulesToApply) {
    for (var module : modulesToApply) {
      motorType.performControl(module, requestType.fromVoltage(curVoltage));
    }
    return StatusCode.OK;
  }

  /**
   * Voltage for modules to use.
   *
   * @param voltage The Voltage
   * @return {@code this} for chaining
   */
  public SwerveSysidRequest withVoltage(Voltage voltage) {
    curVoltage = voltage;
    return this;
  }
}
