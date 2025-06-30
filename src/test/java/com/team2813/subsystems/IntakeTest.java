package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.subsystems.Intake.BUMP_SPEED;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import com.team2813.CommandTester;
import com.team2813.NetworkTableResource;
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

  @Test
  public void constructRealInstance() {
    try (Intake ignored = new Intake(ntResource.getNetworkTableInstance())) {
      assertThat(fakeMotor.demand).isWithin(0.01).of(0.0);
    }
  }

  @Test
  public void initialState() {
    try (Intake ignored =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      assertThat(fakeMotor.demand).isWithin(0.01).of(0.0);
      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.intakeItemCommand();
      assertThat(fakeMotor.demand).isWithin(0.01).of(0.0);

      commandTester.runUntilComplete(command);

      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(Intake.PARAMS.intakeDemand());
    }
  }

  @Test
  public void stopAfterIntakingCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.intakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertMotorIsStopped();
    }
  }

  @Test
  public void outtakeCoral() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(Intake.PARAMS.outtakeDemand());
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
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertMotorIsStopped();
    }
  }

  @Test
  public void bumpAlgae() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      intake.intakeGamePiece();
      Command command = intake.bumpAlgaeCommand();
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(BUMP_SPEED);
    }
  }

  @Test
  public void stopAfterBumpingAlgae() {
    try (Intake intake =
        new Intake(fakeMotor, mockBeamBreak, ntResource.getNetworkTableInstance())) {
      Command command = intake.bumpAlgaeCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertMotorIsStopped();
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

  private void assertMotorIsStopped() {
    assertThat(fakeMotor.demand).isWithin(0.01).of(0.0);
  }

  private void assertMotorIsRunning() {
    assertThat(fakeMotor.demand).isNotWithin(0.01).of(0.0);
  }
}
