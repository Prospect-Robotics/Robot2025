package com.team2813;

import com.team2813.lib2813.testing.junit.jupiter.IsolatedNetworkTablesExtension;
import edu.wpi.first.networktables.NetworkTableInstance;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

@ExtendWith(IsolatedNetworkTablesExtension.class)
public final class RobotContainerTest {
  private final FakeShuffleboardTabs shuffleboard = new FakeShuffleboardTabs();

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
}
