package com.team2813;

import edu.wpi.first.hal.HAL;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import org.junit.jupiter.api.extension.AfterAllCallback;
import org.junit.jupiter.api.extension.AfterEachCallback;
import org.junit.jupiter.api.extension.BeforeAllCallback;
import org.junit.jupiter.api.extension.Extension;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.ParameterContext;
import org.junit.jupiter.api.extension.ParameterResolutionException;
import org.junit.jupiter.api.extension.ParameterResolver;

/**
 * JUnit Jupiter extension for allowing a test to schedule commands.
 *
 * <p>Example use:
 *
 * <pre>{@code
 * @ExtendWith(CommandTesterExtension.class)
 * public final class FlightSubsystemTest {
 *
 *   @Test
 *   public void takesFlight(CommandTester commandTester) {}
 *     var flight = new FlightSubsystem();
 *     Command takeOff = flight.createTakeOffCommandCommand();
 *     assertThat(flight.inAir()).isFalse();
 *
 *     commandTester.runUntilComplete(takeOff);
 *
 *     assertThat(flight.inAir()).isTrue();
 *   }
 * }
 * }</pre>
 */
public final class CommandTesterExtension
    implements Extension,
        AfterAllCallback,
        AfterEachCallback,
        BeforeAllCallback,
        ParameterResolver {

  @Override
  public void beforeAll(ExtensionContext context) {
    // See https://www.chiefdelphi.com/t/driverstation-getalliance-in-gradle-test/
    HAL.initialize(500, 0);
    DriverStationSim.setEnabled(true);
    DriverStationSim.notifyNewData();
    CommandScheduler.getInstance().enable();
    CommandScheduler.getInstance().unregisterAllSubsystems();
  }

  @Override
  public void afterEach(ExtensionContext context) {
    CommandScheduler.getInstance().unregisterAllSubsystems();
  }

  @Override
  public void afterAll(ExtensionContext context) {
    CommandScheduler.getInstance().unregisterAllSubsystems();
    CommandScheduler.getInstance().disable();
    DriverStationSim.setEnabled(false);
    DriverStationSim.notifyNewData();
  }

  @Override
  public boolean supportsParameter(
      ParameterContext parameterContext, ExtensionContext extensionContext)
      throws ParameterResolutionException {
    return CommandTester.class.equals(parameterContext.getParameter().getType());
  }

  @Override
  public CommandTester resolveParameter(
      ParameterContext parameterContext, ExtensionContext extensionContext) {
    return command -> {
      CommandScheduler scheduler = CommandScheduler.getInstance();
      command.schedule();
      do {
        scheduler.run();
      } while (scheduler.isScheduled(command));
    };
  }
}
