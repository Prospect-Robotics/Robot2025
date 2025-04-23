package com.team2813;

import static com.google.common.truth.Truth.assertThat;

import com.pathplanner.lib.auto.NamedCommands;
import java.util.Arrays;
import java.util.Collection;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameter;
import org.junit.runners.Parameterized.Parameters;

@RunWith(Parameterized.class)
public class NamedCommandTest {
  @Rule public final NetworkTableResource networkTable = new NetworkTableResource();
  // The RobotContainer constructor has a side effect of registering named commands.
  // Sadly, all the methods of NamedCommands are static, so we cannot make this
  // dependency explicit.
  private static RobotContainer container;

  @Before
  public void setup() {
    if (container == null) {
      // We must create the robot container only once. It initializes static state that must not be
      // initialized repeatedly (e.g., the pathplanner's static AutoBuilder)
      container =
          new RobotContainer(
              new FakeShuffleboardTabs(), () -> networkTable.getNetworkTableInstance());
    }
  }

  @Parameters(name = "{0}")
  public static Collection<?> data() {
    return Arrays.asList(
        "ScoreL1",
        "ScoreL2",
        "ScoreL3",
        "BumpAlgaeLow",
        "BumpAlgaeHigh",
        "IntakeCoral",
        "PrepareL2",
        "PrepareL3",
        "PrepareScore",
        "ScoreL1");
  }

  @Parameter public String commandName;

  @Test
  public void commandExists() {
    assertThat(container).isNotNull();
    assertThat(NamedCommands.hasCommand(commandName)).isTrue();
  }
}
