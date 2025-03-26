package com.team2813.subsystems.intake;

import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Subsystem;

public interface Intake extends AutoCloseable {

  static Intake create() {
    return new IntakeSubsystem(NetworkTableInstance.getDefault());
  }

  boolean hasCoral();

  boolean intaking();

  Command bumpAlgaeCommand();

  Command intakeCoralCommand();

  Command outakeCoralCommand();

  Command slowOutakeCoralCommand();

  Command stopIntakeMotorCommand();

  Subsystem asSubsystem();

  void stopIntakeMotorNow();

  @Override
  void close();
}
