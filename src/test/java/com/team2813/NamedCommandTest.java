package com.team2813;

import com.pathplanner.lib.auto.NamedCommands;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameter;
import org.junit.runners.Parameterized.Parameters;

import java.util.Arrays;
import java.util.Collection;

import static com.google.common.truth.Truth.assertThat;

@RunWith(Parameterized.class)
public class NamedCommandTest {
  @Rule
  public final RobotContainerProvider robotContainerProvider = new RobotContainerProvider();

  @Parameters(name = "{0}")
  public static Collection<?> data() {
    return Arrays.asList("ScoreL1", "ScoreL2", "ScoreL3", "BumpAlgaeLow", "BumpAlgaeHigh", "IntakeCoral");
  }
  
  @Parameter
  public String commandName;
  
  @Test
  public void commandExists() {
    assertThat(NamedCommands.hasCommand(commandName)).isTrue();
  }
}
