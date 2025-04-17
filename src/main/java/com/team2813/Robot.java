// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.ctre.phoenix6.SignalLogger;
import com.google.auto.value.AutoBuilder;
import com.team2813.lib2813.preferences.PreferencesInjector;
import edu.wpi.first.cameraserver.CameraServer;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.DataLogManager;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import java.util.function.BooleanSupplier;

public class Robot extends TimedRobot {
  private final LoggingConfig loggingConfig;

  private static final BuildConstantsPublisher m_buildConstantsPublisher =
      new BuildConstantsPublisher(NetworkTableInstance.getDefault());
  private Command m_autonomousCommand;

  private final RobotContainer m_robotContainer;

  public record LoggingConfig(boolean debugLogging, BooleanSupplier alwaysEnable) {
    /** Creates a builder for {@link LoggingConfig} with the default values */
    public static Builder builder() {
      return new AutoBuilder_Robot_LoggingConfig_Builder().debugLogging(false);
    }

    public static LoggingConfig fromPreferences() {
      LoggingConfig defaultConfig = builder().build();
      return PreferencesInjector.DEFAULT_INSTANCE.injectPreferences(defaultConfig);
    }

    @AutoBuilder
    public interface Builder {
      Builder debugLogging(boolean enabled);

      LoggingConfig build();
    }
  }

  public Robot() {
    this(LoggingConfig.fromPreferences());
  }

  public Robot(LoggingConfig loggingConfig) {
    this.loggingConfig = loggingConfig;
    AllPreferences.migrateLegacyPreferences();
    m_robotContainer =
        new RobotContainer(new RealShuffleboardTabs(), NetworkTableInstance.getDefault());
  }

  @Override
  public void robotInit() {
    SignalLogger.setPath("/U/logs");
    DataLogManager.start("/U/logs");
    DataLogManager.logNetworkTables(true);
    DriverStation.startDataLog(DataLogManager.getLog());
    SignalLogger.enableAutoLogging(true);
    if (loggingConfig.debugLogging || DriverStation.getMatchType() != DriverStation.MatchType.None) {
      startLogs();
      SignalLogger.start();
    }
    CameraServer.startAutomaticCapture();
    // Publish build constants to NetworkTables.
    m_buildConstantsPublisher.publish();
  }
  
  private void startLogs() {
    DataLogManager.start("/U/logs");
    DataLogManager.logNetworkTables(true);
    DriverStation.startDataLog(DataLogManager.getLog());
  }
  
  private void stopLogs() {
    DataLogManager.stop();
  }

  @Override
  public void robotPeriodic() {
    CommandScheduler.getInstance().run();
  }

  @Override
  public void disabledInit() {
    if (loggingConfig.debugLogging || DriverStation.getMatchType() != DriverStation.MatchType.None) {
      stopLogs();
    }
  }

  @Override
  public void disabledPeriodic() {}

  @Override
  public void disabledExit() {}

  @Override
  public void autonomousInit() {
    if (loggingConfig.debugLogging || DriverStation.getMatchType() != DriverStation.MatchType.None) {
      startLogs();
    }
    m_autonomousCommand = m_robotContainer.getAutonomousCommand();

    if (m_autonomousCommand != null) {
      m_autonomousCommand.schedule();
    }
  }

  @Override
  public void autonomousPeriodic() {}

  @Override
  public void autonomousExit() {}

  @Override
  public void teleopInit() {
    if (m_autonomousCommand != null) {
      m_autonomousCommand.cancel();
    }
    if (!loggingConfig.debugLogging && DriverStation.getMatchType() != DriverStation.MatchType.None) {
      startLogs();
    }
  }

  @Override
  public void teleopPeriodic() {}

  @Override
  public void teleopExit() {}

  @Override
  public void testInit() {
    if (!loggingConfig.debugLogging && DriverStation.getMatchType() != DriverStation.MatchType.None) {
      startLogs();
    }
    CommandScheduler.getInstance().cancelAll();
  }

  @Override
  public void testPeriodic() {}

  @Override
  public void testExit() {}

  private static class RealShuffleboardTabs implements ShuffleboardTabs {
    @Override
    public ShuffleboardTab getTab(String title) {
      return Shuffleboard.getTab(title);
    }

    @Override
    public void selectTab(String title) {
      Shuffleboard.selectTab(title);
    }
  }
}
