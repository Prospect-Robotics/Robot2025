package com.team2813.sysid;

import static com.team2813.sysid.Requests.NEUTRAL_OUT;

import com.ctre.phoenix6.controls.ControlRequest;
import com.ctre.phoenix6.controls.NeutralOut;
import com.ctre.phoenix6.swerve.SwerveModule;
import java.util.function.BiConsumer;

public enum MotorType {
  Swerve(
      (m, r) -> {
        m.getDriveMotor().setControl(NEUTRAL_OUT);
        m.getSteerMotor().setControl(r);
      }),
  Drive(
      (m, r) -> {
        m.getDriveMotor().setControl(r);
        m.getSteerMotor().setControl(NEUTRAL_OUT);
      });
  private static final NeutralOut neutral = new NeutralOut();
  private final BiConsumer<SwerveModule<?, ?, ?>, ControlRequest> performOperation;

  MotorType(BiConsumer<SwerveModule<?, ?, ?>, ControlRequest> performOperation) {
    this.performOperation = performOperation;
  }

  public void performControl(SwerveModule<?, ?, ?> module, ControlRequest request) {
    performOperation.accept(module, request);
  }
}
