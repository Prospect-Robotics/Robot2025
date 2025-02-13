// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import com.ctre.phoenix6.SignalLogger;
import com.pathplanner.lib.auto.AutoBuilder;
import com.team2813.commands.DefaultDriveCommand;
import com.team2813.subsystems.Drive;
import com.team2813.sysid.*;
import edu.wpi.first.units.Units;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.DeferredCommand;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;
import org.json.simple.parser.ParseException;


import static com.team2813.Constants.DriverConstants.DRIVER_CONTROLLER;
import static com.team2813.Constants.DriverConstants.SYSID_RUN;

public class RobotContainer {
  private final Drive drive = new Drive();
  private final SendableChooser<Command> autoChooser;

  public RobotContainer() {
    // Build an auto chooser. This will use Commands.none() as the default option.
    autoChooser = AutoBuilder.buildAutoChooser();

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
  
  private static SwerveSysidRequest DRIVE_SYSID = new SwerveSysidRequest(MotorType.Drive, RequestType.VoltageOut);
  private static SwerveSysidRequest STEER_SYSID = new SwerveSysidRequest(MotorType.Swerve, RequestType.VoltageOut);
  
  private static List<DropdownEntry> getSysIdRoutines(SubsystemRegistry registry) {
    List<DropdownEntry> routines = new ArrayList<>();
    routines.add(new DropdownEntry("Drive-Drive Motor", new SysIdRoutine(
            new SysIdRoutine.Config(null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
            new SysIdRoutine.Mechanism(
                    (v) -> registry.getSubsystem(Drive.class).runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)
            )
    )));
    routines.add(new DropdownEntry("Drive-Steer Motor", new SysIdRoutine(
            new SysIdRoutine.Config(null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
            new SysIdRoutine.Mechanism(
                    (v) -> registry.getSubsystem(Drive.class).runSysIdRequest(STEER_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)
            )
    )));
    routines.add(new DropdownEntry("Drive-Slip Test (Forward Quasistatic only)", new SysIdRoutine(
            new SysIdRoutine.Config(Units.Volts.of(0.25).per(Units.Second), null, null, (s) -> SignalLogger.writeString("state", s.toString())),
            new SysIdRoutine.Mechanism(
                    (v) -> registry.getSubsystem(Drive.class).runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)
            )
    )));
    return routines;
  }

    public Command getAutonomousCommand() {
      return autoChooser.getSelected();
    }
  }
