package com.team2813.commands;

import com.team2813.subsystems.IntakePivot;
import com.team2813.subsystems.elevator.Elevator;
import com.team2813.subsystems.intake.Intake;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import edu.wpi.first.wpilibj2.command.WaitCommand;

public class RobotCommands {
  private final Intake intake;
  private final IntakePivot intakePivot;
  private final Elevator elevator;

  // private  AlgeaIntake algeaIntake;
  public RobotCommands(Intake intake, IntakePivot intakePivot, Elevator elevator) {
    this.intake = intake;
    this.intakePivot = intakePivot;
    this.elevator = elevator;
  }

  private volatile Command placeCoral = null;

  private Command createPlaceCoral() {
    return new SequentialCommandGroup(
        intake.outakeCoralCommand(), // run intake wheels backward
        new WaitCommand(1.0),
        intake.stopIntakeMotorCommand());
  }

  public Command placeCoral() {
    if (placeCoral == null) {
      synchronized (RobotCommands.class) {
        if (placeCoral == null) {
          placeCoral = createPlaceCoral();
        }
      }
    }
    return placeCoral;
  }
}
