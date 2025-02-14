package com.team2813;

import com.pathplanner.lib.auto.NamedCommands;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameter;
import org.junit.runners.Parameterized.Parameters;

import java.util.Arrays;
import java.util.Collection;

import static com.google.common.truth.Truth.assertThat;
import static org.junit.Assume.assumeNotNull;

@RunWith(Parameterized.class)
public class NamedCommandTest {
  @Parameters
  public static Collection<Object[]> data() {
    return Arrays.asList(new Object[][] {
            {"ScoreL1"}, {"ScoreL2"}, {"ScoreL3"}, {"BumpAlgaeLow"}, {"BumpAlgaeHigh"}, {"IntakeCoral"}
    });
  }
  private static final RobotContainer robotContainer = new RobotContainer();
  @Parameter(0)
  public String commandName;
  @Test
  public void commandExists() {
    assumeNotNull(commandName);
    assertThat(NamedCommands.hasCommand(commandName)).isTrue();
  }
}
