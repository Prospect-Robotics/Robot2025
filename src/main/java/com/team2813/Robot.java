// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import com.team2813.BuildConstants;

public class Robot extends TimedRobot {
  private Command m_autonomousCommand;

  private final RobotContainer m_robotContainer;

  public Robot() {
    m_robotContainer = new RobotContainer();
  }

  @Override
  public void robotInit() {
    System.out.println("Build Information:");
    System.out.println("  MAVEN_NAME     : " + BuildConstants.MAVEN_NAME);
    System.out.println("  VERSION        : " + BuildConstants.VERSION);
    System.out.println("  GIT_REVISION   : " + BuildConstants.GIT_REVISION);
    System.out.println("  GIT_SHA        : " + BuildConstants.GIT_SHA);
    System.out.println("  GIT_DATE       : " + BuildConstants.GIT_DATE);
    System.out.println("  GIT_BRANCH     : " + BuildConstants.GIT_BRANCH);
    System.out.println("  BUILD_DATE     : " + BuildConstants.BUILD_DATE);
  }

  @Override
  public void robotPeriodic() {
    CommandScheduler.getInstance().run();
  }

  @Override
  public void disabledInit() {}

  @Override
  public void disabledPeriodic() {}

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
    System.out.println("Hhhhhhhhh: " + BuildConstants.GIT_SHA);
    // DriverStation.reportWarning("Hhhhhhhhh: " + BuildConstants.GIT_SHA, false);
    CommandScheduler.getInstance().cancelAll();
  }

  @Override
  public void testPeriodic() {}

  @Override
  public void testExit() {}
}
