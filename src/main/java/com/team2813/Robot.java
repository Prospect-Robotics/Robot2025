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
import java.io.File;

public class Robot extends TimedRobot {
  private final LoggingConfig loggingConfig;

  private static final BuildConstantsPublisher m_buildConstantsPublisher =
      new BuildConstantsPublisher(NetworkTableInstance.getDefault());
  private Command m_autonomousCommand;
  private boolean logsStarted = false;

  private final RobotContainer m_robotContainer;

  public record LoggingConfig(boolean debugLogging, String logFolder) {
    /** Creates a builder for {@link LoggingConfig} with the default values */
    public static Builder builder() {
      return new AutoBuilder_Robot_LoggingConfig_Builder().debugLogging(false).logFolder("/U/logs");
    }

    public static LoggingConfig fromPreferences() {
      LoggingConfig defaultConfig = builder().build();
      return PreferencesInjector.DEFAULT_INSTANCE.injectPreferences(defaultConfig);
    }

    @AutoBuilder
    public interface Builder {
      Builder debugLogging(boolean enabled);

      Builder logFolder(String logFolder);

      /**
       * Sets the log folder
       *
       * @param logFolder the log folder
       * @throws IllegalArgumentException if {@code logFolder} is not a directory
       * @return {@code this} for chaining
       */
      default Builder logFolder(File logFolder) {
        if (!logFolder.isDirectory()) {
          throw new IllegalArgumentException(
              String.format("File with path: \"%s\" is not a directory!", logFolder.getPath()));
        }
        return logFolder(logFolder.getPath());
      }

      LoggingConfig build();
    }
  }

  public Robot() {
    this(LoggingConfig.fromPreferences());
  }

  public Robot(LoggingConfig loggingConfig) {
    this(loggingConfig, new RealShuffleboardTabs(), NetworkTableInstance.getDefault());
  }

  Robot(
      LoggingConfig loggingConfig,
      ShuffleboardTabs shuffleboardTabs,
      NetworkTableInstance networkTableInstance) {
    this.loggingConfig = loggingConfig;
    AllPreferences.migrateLegacyPreferences();
    m_robotContainer = new RobotContainer(shuffleboardTabs, networkTableInstance);
  }

  @Override
  public void robotInit() {
    SignalLogger.setPath(loggingConfig.logFolder);
    SignalLogger.enableAutoLogging(true);
    // won't have match type by now, so no need to check
    if (loggingConfig.debugLogging) {
      startLogs();
      SignalLogger.start();
    }
    CameraServer.startAutomaticCapture();
    // Publish build constants to NetworkTables.
    m_buildConstantsPublisher.publish();
  }

  private void startLogs() {
    DataLogManager.start(loggingConfig.logFolder);
    DataLogManager.logNetworkTables(true);
    DriverStation.startDataLog(DataLogManager.getLog());
    logsStarted = true;
  }

  @Override
  public void robotPeriodic() {
    CommandScheduler.getInstance().run();
  }

  @Override
  public void disabledInit() {}

  @Override
  public void disabledPeriodic() {
    // logs will have already started
    if (!logsStarted && DriverStation.getMatchType() != DriverStation.MatchType.None) {}
  }

  @Override
  public void disabledExit() {}

  @Override
  public void autonomousInit() {
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
  }

  @Override
  public void teleopPeriodic() {}

  @Override
  public void teleopExit() {}

  @Override
  public void testInit() {
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

  @Override
  public void close() {
    super.close();
    m_robotContainer.close();
  }
}
