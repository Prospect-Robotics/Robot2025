package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.subsystems.Intake.BUMP_VOLTAGE;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import com.team2813.IsolatedNetworkTablesExtension;
import com.team2813.lib2813.testing.junit.jupiter.CommandTester;
import com.team2813.lib2813.testing.junit.jupiter.WPILibExtension;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj2.command.Command;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Answers;

@ExtendWith({IsolatedNetworkTablesExtension.class, WPILibExtension.class})
public final class IntakeTest {
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);
  final DigitalInput mockBeamBreak = mock(DigitalInput.class);

  @Test
  public void constructRealInstance(NetworkTableInstance ntInstance) {
    try (Intake ignored = new Intake(ntInstance)) {
      assertThat(fakeMotor.demand).isWithin(0.01).of(0.0);
    }
  }

  @Test
  public void initialState(NetworkTableInstance ntInstance) {
    try (Intake ignored = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      assertThat(fakeMotor.demand).isWithin(0.01).of(0.0);
      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeCoral(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.intakeItemCommand();
      assertThat(fakeMotor.demand).isWithin(0.01).of(0.0);

      commandTester.runUntilComplete(command);

      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(Intake.PARAMS.intakeDemand());
    }
  }

  @Test
  public void stopAfterIntakingCoral(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.intakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertMotorIsStopped();
    }
  }

  @Test
  public void outtakeCoral(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(Intake.PARAMS.outtakeDemand());
    }
  }

  @Test
  public void stopAfterOutakingCoral(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
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
  public void bumpAlgae(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      intake.intakeGamePiece();
      Command command = intake.bumpAlgaeCommand();
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(BUMP_VOLTAGE);
    }
  }

  @Test
  public void stopAfterBumpingAlgae(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.bumpAlgaeCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertMotorIsRunning();

      commandTester.runUntilComplete(command);

      assertMotorIsStopped();
    }
  }

  @Test
  public void hasCoral_withCoral(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      when(mockBeamBreak.get()).thenReturn(false);
      assertThat(intake.hasCoral()).isTrue();
    }
  }

  @Test
  public void hasCoral_withoutCoral(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
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
