package com.team2813;

import static com.google.common.truth.Truth.assertThat;

import edu.wpi.first.hal.AllianceStationID;
import edu.wpi.first.wpilibj.DataLogManager;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import java.io.File;
import java.io.IOException;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeFormatterBuilder;
import java.time.temporal.ChronoField;
import java.time.temporal.TemporalAccessor;
import java.util.Arrays;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

public class LoggingTest {
  @Rule public final TemporaryFolder fakeRoborioSystem = new TemporaryFolder();
  public final FakeShuffleboardTabs shuffleboardTabs = new FakeShuffleboardTabs();
  @Rule public final NetworkTableResource networkTableResource = new NetworkTableResource();

  @Rule
  public final DriverStationSimResource driverStationSimResource = new DriverStationSimResource();

  @Rule
  public final StaticClassResource loggingResource = new StaticClassResource(DataLogManager.class);

  private File getLogDirectory() throws IOException {
    return fakeRoborioSystem.newFolder("U", "logs");
  }

  @Test
  public void defaultEmptyDirectory() throws Exception {
    File logDirectory = getLogDirectory();
    assertThat(logDirectory.listFiles()).isEmpty();
    Robot.LoggingConfig config =
        Robot.LoggingConfig.builder().logFolder(logDirectory).debugLogging(false).build();
    try (Robot robot =
        new Robot(config, shuffleboardTabs, networkTableResource.getNetworkTableInstance())) {
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
    Robot.LoggingConfig config =
        Robot.LoggingConfig.builder().logFolder(logDirectory).debugLogging(true).build();
    try (Robot robot =
        new Robot(config, shuffleboardTabs, networkTableResource.getNetworkTableInstance())) {
      robot.robotInit();
      robot.disabledInit();
      robot.disabledPeriodic();

      // TODO: figure out how to verify that signal logger has started; this call increases
      // likelihood, but does not guarantee
      Thread.sleep(1000);
      // Should have TBD WPILog file and hoot file; length 2
      File[] directoryFiles =
          logDirectory.listFiles((file, name) -> name.endsWith(".hoot") | name.endsWith(".wpilog"));
      assertThat(directoryFiles).hasLength(2);
      for (File file : directoryFiles) {
        String filename = file.getName();
        if (filename.endsWith(".wpilog")) {
          assertThat(filename).startsWith("FRC_TBD");
        } else {
          // This is the format for the file name. This is not compared with the current time as it
          // may be in a different timezone than what Java thinks the default is
          DateTimeFormatter formatter =
              new DateTimeFormatterBuilder()
                  .appendLiteral("sim_")
                  .append(DateTimeFormatter.ISO_LOCAL_DATE)
                  .appendLiteral("_")
                  .appendValue(ChronoField.HOUR_OF_DAY, 2)
                  .appendLiteral("-")
                  .appendValue(ChronoField.MINUTE_OF_HOUR, 2)
                  .appendLiteral("-")
                  .appendValue(ChronoField.SECOND_OF_MINUTE, 2)
                  .appendLiteral(".hoot")
                  .toFormatter();
          TemporalAccessor fileTime = formatter.parse(filename);
          assertThat(fileTime).isNotNull();
        }
      }
    }
  }

  /**
   * Run after updating DriverStation to contain the needed match info. After running, both CTRE and
   * WPILib logging will contain log folders, and WPILib will have the correct name for the match.
   */
  private void updateLogFiles() throws InterruptedException {
    // DataLogManager requires updates from driver station, and this supplies it. Runs a bunch of
    // times so that it works properly
    for (int i = 0; i < 1_000; i++) {
      DriverStationSim.notifyNewData();
    }

    // sleep to make the hoot file show up
    Thread.sleep(1_000);
  }

  @Test
  public void noDebugInMatch() throws Exception {
    File logDirectory = getLogDirectory();
    assertThat(logDirectory.listFiles()).isEmpty();
    Robot.LoggingConfig config =
        Robot.LoggingConfig.builder().logFolder(logDirectory).debugLogging(false).build();
    try (Robot robot =
        new Robot(config, shuffleboardTabs, networkTableResource.getNetworkTableInstance())) {
      robot.robotInit();
      robot.disabledInit();
      robot.disabledPeriodic();
      assertThat(logDirectory.listFiles()).isEmpty();

      DriverStationSimResource.modificationBuilder()
          .eventName("GALILEO")
          .allianceStationId(AllianceStationID.Blue1)
          .matchType(DriverStation.MatchType.Qualification)
          .matchNumber(1)
          .fmsAttached(true)
          .dsAttahced(true)
          .perform();

      assertThat(DriverStation.getEventName()).isEqualTo("GALILEO");
      assertThat(DriverStation.isFMSAttached()).isTrue();
      assertThat(DriverStation.isDSAttached()).isTrue();

      robot.disabledPeriodic();

      updateLogFiles();

      System.err.println(Arrays.toString(logDirectory.listFiles()));
      File[] directoryFiles =
          logDirectory.listFiles((file, name) -> name.endsWith(".hoot") | name.endsWith(".wpilog"));
      assertThat(directoryFiles).hasLength(2);
      for (File file : directoryFiles) {
        String filename = file.getName();
        if (filename.endsWith(".wpilog")) {
          // filename looks like FRC_yyyymmdd_??????_EVENTCODE_{P,Q,E}MATCHNUM.wpilog
          assertThat(filename).endsWith("GALILEO_Q1.wpilog");
          assertThat(filename).startsWith("FRC");
        }
        // Can't check if .hoot file has correct filename as CTRE does special stuff with
        // simulation, and does not document the circumstances under which they rename the log.
        // Since the implementation is all under closed-source c++ code, barring a decompilation, we
        // can't know how to make it have the right name, or if it is even possible in the first place.
      }
    }
  }
}
