package com.team2813;

import edu.wpi.first.hal.HAL;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import org.junit.rules.ExternalResource;
import org.junit.rules.TestRule;
import org.junit.runner.Description;
import org.junit.runners.model.Statement;

/**
 * JUnit Rule for allowing a test to schedule commands.
 *
 * <p>Typically used with {@code ClassRule} and {@code Rule}. Example use:
 *
 * {@snippet :
 * public final class FlightSubsystemTest {
 *
 *   @Rule @ClassRule
 *   public static final CommandTester commandTester = new CommandTester();
 *
 *   @Test
 *   public void takesFlight() {}
 *     var flight = new FlightSubsystem();
 *     Command takeOff = flight.createTakeOffCommandCommand();
 *     assertThat(flight.inAir()).isFalse();
 *
 *     commandTester.runUntilComplete(takeOff);
 *
 *     assertThat(flight.inAir()).isTrue();
 *   }
 * }
 *
 * }
 */
public final class CommandTester implements TestRule {

  /** Schedules the provided command and runs it until it completes.= */
  public void runUntilComplete(Command command) {
    CommandScheduler scheduler = CommandScheduler.getInstance();
    command.schedule();
    do {
      scheduler.run();
    } while (scheduler.isScheduled(command));
  }

  private static class AroundClass extends ExternalResource {

    @Override
    protected void before() throws Throwable {
      // See https://www.chiefdelphi.com/t/driverstation-getalliance-in-gradle-test/
      HAL.initialize(500, 0);
      DriverStationSim.setEnabled(true);
      DriverStationSim.notifyNewData();
      CommandScheduler.getInstance().enable();
      CommandScheduler.getInstance().unregisterAllSubsystems();
    }

    @Override
    protected void after() {
      CommandScheduler.getInstance().unregisterAllSubsystems();
      CommandScheduler.getInstance().disable();
      DriverStationSim.setEnabled(false);
      DriverStationSim.notifyNewData();
    }
  }

  private static class AroundTest extends ExternalResource {

    @Override
    protected void before() throws Throwable {
      if (!DriverStationSim.getEnabled()) {
        throw new IllegalStateException(
            "DriverStationSim not enabled (did you forget to annotate your CommandTester field with"
                + " @ClassRule?)");
      }
    }

    @Override
    protected void after() {
      CommandScheduler.getInstance().unregisterAllSubsystems();
    }
  }

  @Override
  public Statement apply(Statement base, Description description) {
    if (description.isSuite()) {
      return new AroundClass().apply(base, description);
    }
    return new AroundTest().apply(base, description);
  }
}
