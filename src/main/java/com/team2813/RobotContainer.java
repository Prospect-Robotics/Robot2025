// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.team2813.Commands.DefaultDriveCommand;
import com.team2813.Commands.RobotCommands;
import com.team2813.subsystems.Drive;
import com.team2813.subsystems.Elevator;
import com.team2813.subsystems.Intake;
import com.team2813.subsystems.AlgeaIntake;
import com.team2813.subsystems.IntakePivot;
import com.team2813.subsystems.Climb;
import com.pathplanner.lib.auto.NamedCommands;

import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import edu.wpi.first.wpilibj2.command.button.CommandPS4Controller;
import edu.wpi.first.wpilibj2.command.button.Trigger;

public class RobotContainer {
  private final CommandPS4Controller driverController = new CommandPS4Controller(0);
  private final Drive drive = new Drive();
  private final Intake intake = new Intake();
  private final Elevator elevate = new Elevator();
  //private final AlgeaIntake algeaIntake = new AlgeaIntake();
  private static IntakePivot intakePivot = new IntakePivot();
  private final Climb climb = new Climb();
  
  // Controller bindings
  private final Trigger slowmodeButton = driverController.L1();
  private final Trigger placeCoral = driverController.R1();
  private final Trigger autoPlaceLeft = driverController.square();
  private final Trigger autoPlaceRight = driverController.circle();
  private final Trigger scoreAlgea = driverController.L2();
  private final SendableChooser<Command> autoChooser;


  public RobotContainer() {
      drive.setDefaultCommand(new DefaultDriveCommand(
          () -> -modifyAxis(driverController.getLeftY()) * Drive.MAX_VELOCITY,
          () -> -modifyAxis(driverController.getLeftX()) * Drive.MAX_VELOCITY,
          () -> -modifyAxis(driverController.getRightX()) * Drive.MAX_ANGULAR_VELOCITY,
          drive));

      RobotCommands autoCommands = new RobotCommands(intake, intakePivot, elevate, climb);
      configureBindings(autoCommands);
      //addDriveCommand(autoCommands);
  }

  private void configureBindings(com.Commands.RobotCommands autoCommands) {
    placeCoral.onTrue(autoCommands.placeCoral());
    scoreAlgea.onTrue(autoCommands.scoreAlgea());
    //autoPlaceLeft.onTrue(autoCommands.autoPlaceLeft());
    //autoPlaceRight.onTrue(autoCommands.autoPlaceRight());
    slowmodeButton.whileTrue(new InstantCommand(() -> drive.enableSlowMode(), drive));
    slowmodeButton.onFalse(new InstantCommand(() -> drive.enableSlowMode(), drive));

  }

  /*public void addDriveCommand(RobotCommands autoCommands) {
    NamedCommands.registerCommand("place-coral", autoCommands.placeCoral());
    NamedCommands.registerCommand("score-algea", autoCommands.scoreAlgea());
    //NamedCommands.registerCommand("autoplace-left", autoCommands.autoPlaceLeft());
    //NamedCommands.registerCommand("autoplace-right", autoCommands.autoPlaceRight());
  }
    */

  public Command getAutonomousCommand() {
    return autoChooser.getSelected();
  }
  private static double deadband(double value, double deadband) {
    if (Math.abs(value) > deadband) {
      if (value > 0) {
        return (value - deadband) / (1 - deadband);
      } else {
        return (value + deadband) / (1 - deadband);
      }
    } else {
      return 0;
    }
  }

  private static double modifyAxis(double value) {
    value = deadband(value, 0.1);
    value = Math.copySign(value * value, value);
    return value;
  }
}
