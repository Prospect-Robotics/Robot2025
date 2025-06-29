package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.subsystems.Intake.BUMP_SPEED;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import com.team2813.CommandTester;
import com.team2813.NetworkTableResource;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj2.command.Command;
import org.junit.*;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import org.mockito.Answers;

@RunWith(JUnit4.class)
public final class IntakeTest {
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);
  final DigitalInput mockBeamBreak = mock(DigitalInput.class);

  @Rule public final NetworkTableResource ntResource = new NetworkTableResource();

  @Rule @ClassRule public static final CommandTester commandTester = new CommandTester();

  abstract static class FakePIDMotor implements PIDMotor {
    double dutyCycle = 0.0f;

    @Override
    public void set(ControlMode mode, double demand) {
      assertThat(mode).isEqualTo(ControlMode.VOLTAGE);
      this.dutyCycle = demand;
    }
  }

  @Test
  public void constructRealInstance() {
    try (Intake intake = new Intake(ntResource.getNetworkTableInstance())) {
      assertThat(intake.intaking()).isFalse();
    }
  }

  @Test
  public void initialState() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      assertThat(intake.intaking()).isFalse();
      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.intakeItemCommand();
      assertThat(intake.intaking()).isFalse();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isTrue();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.PARAMS.intakeSpeed());
    }
  }

  @Test
  public void stopAfterIntakingCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.intakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void outtakeCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.PARAMS.outtakeSpeed());
    }
  }

  @Test
  public void stopAfterOutakingCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void bumpAlgae() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      intake.intakeGamePiece();
      Command command = intake.bumpAlgaeCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(BUMP_SPEED);
    }
  }

  @Test
  public void stopAfterBumpingAlgae() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.bumpAlgaeCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void hasCoral_withCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      when(mockBeamBreak.get()).thenReturn(false);
      assertThat(intake.hasCoral()).isTrue();
    }
  }

  @Test
  public void hasCoral_withoutCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      when(mockBeamBreak.get()).thenReturn(true);
      assertThat(intake.hasCoral()).isFalse();
    }
  }
}
