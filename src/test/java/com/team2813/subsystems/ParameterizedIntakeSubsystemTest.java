package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;

import com.team2813.CommandTester;
import com.team2813.NetworkTableResource;
import com.team2813.lib2813.control.ControlMode;
import edu.wpi.first.wpilibj2.command.Command;
import java.util.Arrays;
import java.util.Collection;
import org.junit.*;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.Answers;

@RunWith(Parameterized.class)
public final class ParameterizedIntakeSubsystemTest {
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);
  private final ParameterizedIntakeSubsystem.Params params;

  @Rule public final NetworkTableResource ntResource = new NetworkTableResource();

  @Rule @ClassRule public static final CommandTester commandTester = new CommandTester();

  @Parameterized.Parameters(name = "ControlMode.{0}")
  public static Collection<?> controlModes() {
    return Arrays.asList(ControlMode.values());
  }

  public ParameterizedIntakeSubsystemTest(ControlMode controlMode) {
    params =
        ParameterizedIntakeSubsystem.Params.builder()
            .setControlMode(controlMode)
            .setIntakeDemand(42)
            .setOuttakeDemand(-3.1415)
            .build();
  }

  @Test
  public void initialState() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, params)) {
      assertThat(intake.intaking()).isFalse();

      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeItem() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, params)) {
      Command command = intake.intakeItemCommand();
      assertThat(intake.intaking()).isFalse();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isTrue();
      assertThat(fakeMotor.getDemand()).isWithin(0.01).of(params.intakeDemand());
    }
  }

  @Test
  public void stopAfterIntakingItem() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, params)) {
      Command command = intake.intakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.getDemand()).isWithin(0.01).of(0);
    }
  }

  @Test
  public void outtakeItem() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, params)) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.getDemand()).isWithin(0.01).of(params.outtakeDemand());
    }
  }

  @Test
  public void stopAfterOuttakingItem() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, params)) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.getDemand()).isWithin(0.01).of(0);
    }
  }
}
