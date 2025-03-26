package com.team2813.subsystems.intake;

import static com.google.common.truth.Truth.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;

import com.team2813.IsolatedNetworkTablesExtension;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.testing.junit.jupiter.CommandTester;
import com.team2813.lib2813.testing.junit.jupiter.WPILibExtension;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj2.command.Command;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Answers;

@ExtendWith({IsolatedNetworkTablesExtension.class, WPILibExtension.class})
public final class IntakeSubsystemTest {
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);
  final DigitalInput mockBeamBreak = mock(DigitalInput.class);

  abstract static class FakePIDMotor implements PIDMotor {
    double dutyCycle = 0.0f;

    @Override
    public void set(ControlMode mode, double demand) {
      assertThat(mode).isEqualTo(ControlMode.VOLTAGE);
      this.dutyCycle = demand;
    }
  }

  @Test
  public void constructRealInstance(NetworkTableInstance ntInstance) {
    try (IntakeSubsystem intake = new IntakeSubsystem(ntInstance)) {
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0.0);
    }
  }

  @Test
  public void initialState(NetworkTableInstance ntInstance) {
    try (IntakeSubsystem intake = new IntakeSubsystem(fakeMotor, mockBeamBreak, ntInstance)) {
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0.0);
      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeCoral(NetworkTableInstance ntInstance, CommandTester CommandTesterInterface) {
    try (var intake = new IntakeSubsystem(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.intakeItemCommand();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0.0);

      CommandTesterInterface.runUntilComplete(command);

      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(IntakeSubsystem.PARAMS.intakeDemand());
    }
  }

  @Test
  public void stopAfterIntakingCoral(
      NetworkTableInstance ntInstance, CommandTester CommandTesterInterface) {
    try (var intake = new IntakeSubsystem(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.intakeItemCommand();
      CommandTesterInterface.runUntilComplete(command);
      command = intake.stopMotorCommand();
      assertThat(fakeMotor.dutyCycle).isGreaterThan(0.01);

      CommandTesterInterface.runUntilComplete(command);

      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0.0);
    }
  }

  @Test
  public void outtakeCoral(NetworkTableInstance ntInstance, CommandTester CommandTesterInterface) {
    try (var intake = new IntakeSubsystem(fakeMotor, mockBeamBreak, ntInstance)) {
      intake.intakeCoral();
      Command command = intake.outtakeItemCommand();
      assertThat(fakeMotor.dutyCycle).isGreaterThan(0.01);

      CommandTesterInterface.runUntilComplete(command);

      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(IntakeSubsystem.PARAMS.outtakeDemand());
    }
  }

  @Test
  public void stopAfterOuttakingCoral(
      NetworkTableInstance ntInstance, CommandTester CommandTesterInterface) {
    try (var intake = new IntakeSubsystem(fakeMotor, mockBeamBreak, ntInstance)) {
      intake.intakeCoral();
      Command command = intake.outtakeItemCommand();
      CommandTesterInterface.runUntilComplete(command);
      command = intake.stopMotorCommand();

      CommandTesterInterface.runUntilComplete(command);

      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0.0);
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void bumpAlgae(NetworkTableInstance ntInstance, CommandTester CommandTesterInterface) {
    try (var intake = new IntakeSubsystem(fakeMotor, mockBeamBreak, ntInstance)) {
      intake.intakeCoral();
      Command command = intake.bumpAlgaeCommand();
      assertThat(fakeMotor.dutyCycle).isGreaterThan(0.01);

      CommandTesterInterface.runUntilComplete(command);

      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(IntakeSubsystem.BUMP_VOLTAGE);
    }
  }

  @Test
  public void stopAfterBumpingAlgae(
      NetworkTableInstance ntInstance, CommandTester CommandTesterInterface) {
    try (var intake = new IntakeSubsystem(fakeMotor, mockBeamBreak, ntInstance)) {
      Command command = intake.bumpAlgaeCommand();
      CommandTesterInterface.runUntilComplete(command);
      command = intake.stopMotorCommand();

      CommandTesterInterface.runUntilComplete(command);

      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0.0);
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }
}
