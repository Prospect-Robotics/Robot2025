package com.team2813;

import com.pathplanner.lib.util.PPLibTesting;
import com.team2813.lib2813.testing.junit.jupiter.CommandTester;
import com.team2813.lib2813.testing.junit.jupiter.WPILibExtension;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj2.command.Commands;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

@ExtendWith({IsolatedNetworkTablesExtension.class, WPILibExtension.class})
public final class RobotContainerTest {
  private final FakeShuffleboardTabs shuffleboard = new FakeShuffleboardTabs();

  @BeforeEach
  public void resetPathPlanner() {
    PPLibTesting.resetForTesting();
  }

  @Test
  public void constructorDoesNotRaise(NetworkTableInstance ntInstance) {
    //noinspection EmptyTryBlock
    try (var container = new RobotContainer(shuffleboard, ntInstance)) {}
  }

  @Test
  public void conBeConstructedMultipleTimes(NetworkTableInstance ntInstance) {
    //noinspection EmptyTryBlock
    try (var container = new RobotContainer(shuffleboard, ntInstance)) {}
  }

  @Test
  public void periodicDoesNotFail(CommandTester commandTester, NetworkTableInstance ntInstance) {
    try (RobotContainer container = new RobotContainer(shuffleboard, ntInstance)) {
      // Runs the periodic method at least once. If the periodic method would fail with an
      // exception, this will fail with an exception and fail the test.
      commandTester.runUntilComplete(Commands.none());
    }
  }
}
