package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;

import com.team2813.CommandTester;
import com.team2813.NetworkTableResource;
import edu.wpi.first.wpilibj2.command.Command;
import org.junit.*;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import org.mockito.Answers;

@RunWith(JUnit4.class)
public final class ParameterizedIntakeSubsystemTest {
  static final ParameterizedIntakeSubsystem.Params PARAMS =
      ParameterizedIntakeSubsystem.Params.builder()
          .setIntakeSpeed(42)
          .setOuttakeSpeed(-3.1415)
          .build();
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);

  @Rule public final NetworkTableResource ntResource = new NetworkTableResource();

  @Rule @ClassRule public static final CommandTester commandTester = new CommandTester();

  @Test
  public void initialState() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, PARAMS)) {
      assertThat(intake.intaking()).isFalse();

      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeItem() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, PARAMS)) {
      Command command = intake.intakeItemCommand();
      assertThat(intake.intaking()).isFalse();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isTrue();
      assertThat(fakeMotor.voltage).isWithin(0.01).of(PARAMS.intakeSpeed());
    }
  }

  @Test
  public void stopAfterIntakingItem() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, PARAMS)) {
      Command command = intake.intakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.voltage).isWithin(0.01).of(0);
    }
  }

  @Test
  public void outtakeItem() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, PARAMS)) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.voltage).isWithin(0.01).of(PARAMS.outtakeSpeed());
    }
  }

  @Test
  public void stopAfterOuttakingItem() {
    try (var intake = new ParameterizedIntakeSubsystem(fakeMotor, PARAMS)) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.voltage).isWithin(0.01).of(0);
    }
  }
}
