package com.team2813;

import com.pathplanner.lib.auto.NamedCommands;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Rule;
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
  private final FakeShuffleboardTabs shuffleboard = new FakeShuffleboardTabs();
  private RobotContainer robotContainer;
  
  @Before
  public void startRobotContainer() {
    try {
      robotContainer = new RobotContainer(shuffleboard);
    } catch (Exception e) {
      // Don't need to do anything
    }
  }
  
  @Parameter(0)
  public String commandName;
  
  @Test
  public void commandExists() {
    assumeNotNull(commandName, robotContainer);
    assertThat(NamedCommands.hasCommand(commandName)).isTrue();
  }
}
