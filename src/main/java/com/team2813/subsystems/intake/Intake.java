package com.team2813.subsystems.intake;

import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Subsystem;

public interface Intake extends AutoCloseable {

  static Intake create() {
    return create(NetworkTableInstance.getDefault());
  }

  static Intake create(NetworkTableInstance ntInstance) {
    return new IntakeSubsystem(ntInstance);
  }

  boolean hasCoral();

  Command bumpAlgaeCommand();

  Command intakeItemCommand();

  Command outtakeItemCommand();

  Command slowOuttakeItemCommand();

  Command stopMotorCommand();

  Subsystem asSubsystem();

  void stopMotor();

  @Override
  void close();
}
