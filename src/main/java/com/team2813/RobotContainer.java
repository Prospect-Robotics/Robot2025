// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.team2813.commands.DefaultDriveCommand;
import com.team2813.subsystems.Drive;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;

import static com.team2813.Constants.DriverConstants.DRIVER_CONTROLLER;

public class RobotContainer {
  private final Drive drive = new Drive();
  public RobotContainer() {
    drive.setDefaultCommand(
            new DefaultDriveCommand(
                    drive,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getLeftY()) * Drive.MAX_VELOCITY,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getLeftX()) * Drive.MAX_VELOCITY,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getRightX()) * Drive.MAX_ROTATION));
    configureBindings();
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

  private void configureBindings() {}

  public Command getAutonomousCommand() {
    return Commands.print("No autonomous command configured");
  }
}
