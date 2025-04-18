package com.team2813;

import edu.wpi.first.networktables.NetworkTableInstance;
import org.checkerframework.checker.units.qual.N;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

import java.io.File;
import java.io.IOException;

import static com.google.common.truth.Truth.assertThat;

public class LoggingTest {
  @Rule public TemporaryFolder fakeRoborioSystem = new TemporaryFolder();
  public final FakeShuffleboardTabs shuffleboardTabs = new FakeShuffleboardTabs();
  @Rule public final NetworkTableResource networkTableResource = new NetworkTableResource();
  
  private File getLogDirectory() throws IOException {
    return fakeRoborioSystem.newFolder("U", "logs");
  }
  
  @Test
  public void defaultEmptyDirectory() throws Exception {
    File logDirectory = getLogDirectory();
    assertThat(logDirectory.listFiles()).isEmpty();
    Robot.LoggingConfig config = Robot.LoggingConfig.builder().logFolder(logDirectory).build();
    try (Robot robot = new Robot(config, shuffleboardTabs, networkTableResource.getNetworkTableInstance())) {
      robot.robotInit();
      robot.disabledInit();
      robot.disabledPeriodic();
      assertThat(logDirectory.listFiles()).isEmpty();
    }
  }
  
  @Test
  public void containsLogsOnDebug() throws Exception {
    File logDirectory = getLogDirectory();
    assertThat(logDirectory.listFiles()).isEmpty();
    Robot.LoggingConfig config = Robot.LoggingConfig.builder().logFolder(logDirectory).debugLogging(true).build();
    try (Robot robot = new Robot(config, shuffleboardTabs, networkTableResource.getNetworkTableInstance())) {
      robot.robotInit();
      robot.disabledInit();
      robot.disabledPeriodic();
      assertThat(logDirectory.listFiles()).isNotEmpty();
    }
  }
}
