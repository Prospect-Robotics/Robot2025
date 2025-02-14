// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import java.io.IOException;

import org.json.simple.parser.ParseException;

import com.pathplanner.lib.auto.AutoBuilder;

import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.Command;

import com.team2813.subsystems.Climb;
import com.team2813.subsystems.Drive;
import com.team2813.subsystems.Elevator;
import com.team2813.subsystems.Intake;
import com.team2813.subsystems.IntakePivot;

public class RobotContainer {
  private final Climb climb = new Climb();
  private final Intake intake = new Intake();
  private final IntakePivot intakepivot = new IntakePivot();
  private final Elevator elevator = new Elevator(); 
  private final SendableChooser<Command> autoChooser;
  private final Drive drive = new Drive();

  public RobotContainer() {
    // Build an auto chooser. This will use Commands.none() as the default option.
    autoChooser = AutoBuilder.buildAutoChooser();
     
    SmartDashboard.putData("Auto Chooser", autoChooser);
    configureBindings();
  }

private void configureBindings() { 
    IntakeButton.whileTrue(
    new SequentialCommandGroup(
        new InstantCommand(Elavotor.Position.Bottom, elevator),
        new InstantCommand(IntakePivot.Position.Intake, intakepivot),
        new InstantCommand(Intake.intakeCoral, intake)
        )
    );
  OuttakeButton.whileTrue(
    new InstantCommand(Intake.outakeCoral, intake)
    );
  Triangle.onTrue(
    new InstantCommand(Elevator.Poition.Bottom, elevator)
    );
  Cross.onTrue(
    new InstantCommand(Elevator.Poition.Top, elevator)
    );
  /* Is there code for algea intake?
  R2.whileTrue(
    new InstantCommand()
    );*/
  Climb_Down.whileTrue(
  new InstantCommand(Climb.lower, climb)
    );
  Climb_Up.whileTrue(
    new InstantCommand(Climb.raise, climb)
    );
}

    public Command getAutonomousCommand() {
      return autoChooser.getSelected();
    }
   
}


