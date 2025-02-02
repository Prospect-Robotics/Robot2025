package com.team2813.sysid;

import com.ctre.phoenix6.controls.ControlRequest;
import edu.wpi.first.units.measure.Voltage;

import java.util.function.Function;

import static com.team2813.sysid.Requests.*;

enum RequestType {
  VoltageOut(VOLTAGE_OUT::withOutput),
  TorqueCurrentFOC(CONVERT_VOLTAGE.andThen(TORQUE_CURRENT_FOC::withOutput));
  private final Function<Voltage, ControlRequest> convertVoltage;
  
  RequestType(Function<Voltage, ControlRequest> convertVoltage) {
    this.convertVoltage = convertVoltage;
  }
  
  public ControlRequest fromVoltage(Voltage voltage) {
    return convertVoltage.apply(voltage);
  }
}
