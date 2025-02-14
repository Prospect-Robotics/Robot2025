// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

//import com.team2813.Commands.DefaultDriveCommand;
import com.team2813.Commands.RobotCommands;
import com.team2813.subsystems.Drive;
import com.team2813.subsystems.Elevator;
import com.team2813.subsystems.Intake;
import com.team2813.subsystems.IntakePivot;
import com.pathplanner.lib.auto.AutoBuilder;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.button.CommandPS4Controller;
import edu.wpi.first.wpilibj2.command.button.Trigger;

public class RobotContainer {
  private final CommandPS4Controller driverController = new CommandPS4Controller(0);
  private final Drive drive;
  private final Intake intake;
  private final Elevator elevator;
  private final IntakePivot intakePivot;
  
  // Controller bindings
  private final Trigger slowmodeButton = driverController.L1();
  private final Trigger placeCoral = driverController.R1();
  private final SendableChooser<Command> autoChooser;


  public RobotContainer() {
    drive = new Drive();
    intake = new Intake();
    elevator = new Elevator();
    intakePivot = new IntakePivot();
    autoChooser = AutoBuilder.buildAutoChooser();
    /*drive.setDefaultCommand(new DefaultDriveCommand(
        () -> -modifyAxis(driverController.getLeftY()) * Drive.MAX_VELOCITY,
        () -> -modifyAxis(driverController.getLeftX()) * Drive.MAX_VELOCITY,
        () -> -modifyAxis(driverController.getRightX()) * Drive.MAX_ANGULAR_VELOCITY,
        drive));
    */

    RobotCommands autoCommands = new RobotCommands(intake, intakePivot, elevator);
    configureBindings(autoCommands);
      
  }

  private void configureBindings(RobotCommands autoCommands) {
    //Driver
    placeCoral.onTrue(autoCommands.placeCoral());
    //scoreAlgea.onTrue(autoCommands.scoreAlgea());
    slowmodeButton.onTrue(new InstantCommand(() -> drive.enableSlowMode(), drive));
    slowmodeButton.onFalse(new InstantCommand(() -> drive.enableSlowMode(), drive));

  }

  
  public Command getAutonomousCommand() {
    return autoChooser.getSelected();
  }
}
