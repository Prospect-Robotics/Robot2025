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
import com.team2813.subsystems.Drive;

public class RobotContainer {

  
  private final SendableChooser<Command> autoChooser;


  public RobotContainer() {
    // Build an auto chooser. This will use Commands.none() as the default option.
    autoChooser = AutoBuilder.buildAutoChooser();

    Drive drive = new Drive(); // Initialize swerve drive

    SmartDashboard.putData("Auto Chooser", autoChooser);
    configureBindings();
  }

  private void configureBindings() {}

    public Command getAutonomousCommand() {
      return autoChooser.getSelected();
    }
  }
