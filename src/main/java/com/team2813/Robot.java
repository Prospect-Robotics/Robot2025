// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.team2813.BuildConstants;

import com.ctre.phoenix6.SignalLogger;
import edu.wpi.first.wpilibj.DataLogManager;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.cameraserver.CameraServer;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StringPublisher;
import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import edu.wpi.first.cameraserver.CameraServer;

public class Robot extends TimedRobot {
  private final static StringPublisher m_buildConstantsGitShaPublisher = NetworkTableInstance.getDefault()
          .getStringTopic("/BuildConstants/GitSha").publish();
  private Command m_autonomousCommand;

  private final RobotContainer m_robotContainer;

  public Robot() {
    m_robotContainer = new RobotContainer(new RealShuffleboardTabs());
  }
  
  @Override
  public void robotInit() {
    m_buildConstantsGitShaPublisher.set(BuildConstants.GIT_SHA);

    SignalLogger.setPath("/U/logs");
    DataLogManager.start("/U/logs");
    DataLogManager.logNetworkTables(true);
    DriverStation.startDataLog(DataLogManager.getLog());
    SignalLogger.enableAutoLogging(true);
    String eventName = DriverStation.getEventName();
    if (eventName == null || eventName.isBlank()) {
      SignalLogger.start();
    }

  CameraServer.startAutomaticCapture();
  }

  @Override
  public void robotPeriodic() {
    CommandScheduler.getInstance().run();
  }

  @Override
  public void disabledInit() {
  }

  @Override
  public void disabledPeriodic() {
  }

  @Override
  public void disabledExit() {
  }

  @Override
  public void autonomousInit() {
    m_autonomousCommand = m_robotContainer.getAutonomousCommand();

    if (m_autonomousCommand != null) {
      m_autonomousCommand.schedule();
    }
  }

  @Override
  public void autonomousPeriodic() {
  }

  @Override
  public void autonomousExit() {
  }

  @Override
  public void teleopInit() {
    if (m_autonomousCommand != null) {
      m_autonomousCommand.cancel();
    }
  }

  @Override
  public void teleopPeriodic() {
  }

  @Override
  public void teleopExit() {
  }

  @Override
  public void testInit() {
    CommandScheduler.getInstance().cancelAll();
  }

  @Override
  public void testPeriodic() {
  }

  @Override
  public void testExit() {
  }

  private static class RealShuffleboardTabs implements ShuffleboardTabs {
    @Override
    public ShuffleboardTab getTab(String title) {
      return Shuffleboard.getTab(title);
    }

    @Override
    public void selectTab(String title) {
      Shuffleboard.selectTab(title);
    }
  };
}
