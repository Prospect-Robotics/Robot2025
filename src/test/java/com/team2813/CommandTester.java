package com.team2813;

import edu.wpi.first.wpilibj2.command.Command;

/**
 * Allows tests to run commands.
 *
 * <p>Tests can get an instance by using {@link CommandTesterExtension}.
 */
public interface CommandTester {

  /** Schedules the provided command and runs it until it completes. */
  void runUntilComplete(Command command);
}
