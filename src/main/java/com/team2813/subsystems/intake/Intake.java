package com.team2813.subsystems.intake;

import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj2.command.Command;

public interface Intake extends AutoCloseable {

  static Intake create(NetworkTableInstance networkTableInstance) {
    return new IntakeSubsystem(networkTableInstance);
  }

  boolean hasCoral();

  Command bumpAlgaeCommand();

  Command intakeItemCommand();

  Command outtakeItemCommand();

  Command slowOuttakeItemCommand();

  Command stopMotorCommand();

  void stopMotor();

  @Override
  void close();
}
