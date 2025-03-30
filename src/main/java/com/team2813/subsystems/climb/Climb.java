package com.team2813.subsystems.climb;

import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj2.command.Command;

public interface Climb extends AutoCloseable {

  static Climb create(NetworkTableInstance networkTableInstance) {
    return new ClimbSubsystem(networkTableInstance);
  }

  Command stopCommand();

  Command raiseCommand();

  Command lowerCommand();

  @Override
  void close();
}
