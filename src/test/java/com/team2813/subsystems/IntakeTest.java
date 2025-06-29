package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.subsystems.Intake.BUMP_VOLTAGE;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

import com.team2813.CommandTester;
import com.team2813.CommandTesterExtension;
import com.team2813.IsolatedNetworkTablesExtension;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj2.command.Command;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Answers;

@ExtendWith({IsolatedNetworkTablesExtension.class, CommandTesterExtension.class})
public final class IntakeTest {
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);
  final DigitalInput mockBeamBreak = mock(DigitalInput.class);

  @Test
  public void constructRealInstance(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(ntInstance)) {
      assertThat(intake.intaking()).isFalse();
    }
  }

  @Test
  public void initialState(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      assertThat(intake.intaking()).isFalse();
      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeCoral(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.intakeItemCommand();
      assertThat(intake.intaking()).isFalse();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isTrue();
      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(Intake.PARAMS.intakeDemand());
    }
  }

  @Test
  public void stopAfterIntakingCoral(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.intakeItemCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(0);
    }
  }

  @Test
  public void outtakeCoral(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      intake.intakeGamePiece();
      Command command = intake.outtakeItemCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
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

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(0);
    }
  }

  @Test
  public void bumpAlgae(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      intake.intakeGamePiece();
      Command command = intake.bumpAlgaeCommand();
      assertThat(intake.intaking()).isTrue();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(BUMP_VOLTAGE);
    }
  }

  @Test
  public void stopAfterBumpingAlgae(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (Intake intake = new Intake(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.bumpAlgaeCommand();
      commandTester.runUntilComplete(command);
      command = intake.stopMotorCommand();

      commandTester.runUntilComplete(command);

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.getVoltage()).isWithin(0.01).of(0);
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
}
