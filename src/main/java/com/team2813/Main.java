// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.team2813.lib2813.util.RobotFactory;

public final class Main {
  private Main() {}

  public static void main(String[] args) throws Exception {
    RobotFactory.startRobot(Robot::new);
  }
}
