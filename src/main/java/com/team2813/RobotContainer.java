// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.team2813.commands.DefaultDriveCommand;
import com.team2813.subsystems.Drive;
import com.team2813.sysid.DropdownEntry;
import com.team2813.sysid.SubsystemRegistry;
import com.team2813.sysid.SysIdRoutineSelector;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.DeferredCommand;

import java.util.List;
import java.util.Set;

import static com.team2813.Constants.DriverConstants.DRIVER_CONTROLLER;
import static com.team2813.Constants.DriverConstants.SYSID_RUN;

public class RobotContainer {
  private final Drive drive = new Drive();
  public RobotContainer() {
    drive.setDefaultCommand(
            new DefaultDriveCommand(
                    drive,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getLeftY()) * Drive.MAX_VELOCITY,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getLeftX()) * Drive.MAX_VELOCITY,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getRightX()) * Drive.MAX_ROTATION));
    sysIdRoutineSelector = new SysIdRoutineSelector(new SubsystemRegistry(Set.of(drive)), RobotContainer::getSysIdRoutines);
    configureBindings();
  }
  
  private final SysIdRoutineSelector sysIdRoutineSelector;
  
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

  private void configureBindings() {
    // Every subsystem should be in the set; we don't know what subsystem will be controlled, so assume we control all of them
    SYSID_RUN.whileTrue(new DeferredCommand(sysIdRoutineSelector::getSelected, sysIdRoutineSelector.getRequirements()));
  }
  
  private static List<DropdownEntry> getSysIdRoutines(SubsystemRegistry registry) {
    return List.of();
  }

  public Command getAutonomousCommand() {
    return Commands.print("No autonomous command configured");
  }
}
