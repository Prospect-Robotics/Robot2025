package com.team2813.subsystems.intake;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.subsystems.intake.IntakeSubsystem.BUMP_SPEED;
import static com.team2813.subsystems.intake.IntakeSubsystem.INTAKE_SPEED;
import static com.team2813.subsystems.intake.IntakeSubsystem.OUTTAKE_SPEED;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;

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
public final class IntakeSubsystemTest {
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
    try (var intake = new IntakeSubsystem(ntResource.getNetworkTableInstance())) {
      assertThat(intake.intaking()).isFalse();
    }
  }

  @Test
  public void initialState() {
    try (var intake =
        new IntakeSubsystem(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      assertThat(intake.intaking()).isFalse();
      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeCoral() {
    try (var intake =
        new IntakeSubsystem(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.intakeCoralCommand();
      assertThat(intake.intaking()).isFalse();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isTrue();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(INTAKE_SPEED);
    }
  }

  @Test
  public void stopAfterIntakingCoral() {
    try (var intake =
        new IntakeSubsystem(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.intakeCoralCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopIntakeMotorCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void outtakeCoral() {
    try (var intake =
        new IntakeSubsystem(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      intake.intakeCoral();
      Command command = intake.outakeCoralCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(OUTTAKE_SPEED);
    }
  }

  @Test
  public void stopAfterOutakingCoral() {
    try (var intake =
        new IntakeSubsystem(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      intake.intakeCoral();
      Command command = intake.outakeCoralCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopIntakeMotorCommand();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void bumpAlgae() {
    try (var intake =
        new IntakeSubsystem(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      intake.intakeCoral();
      Command command = intake.bumpAlgaeCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(BUMP_SPEED);
    }
  }

  @Test
  public void stopAfterBumpingAlgae() {
    try (var intake =
        new IntakeSubsystem(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.bumpAlgaeCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopIntakeMotorCommand();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }
}
