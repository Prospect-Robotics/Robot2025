package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;

import com.team2813.IsolatedNetworkTablesExtension;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import edu.wpi.first.networktables.NetworkTableInstance;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Answers;

@ExtendWith(IsolatedNetworkTablesExtension.class)
public final class IntakeTest {
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);

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
    try (Intake intake = new Intake(ntInstance)) {
      assertThat(intake.intaking()).isFalse();
    }
  }

  @Test
  public void initialState(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, ntInstance)) {
      assertThat(intake.intaking()).isFalse();
      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeCoral(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, ntInstance)) {
      intake.intakeCoral();

      assertThat(intake.intaking()).isTrue();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.INTAKE_SPEED);
    }
  }

  @Test
  public void stopAfterIntakingCoral(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, ntInstance)) {
      intake.intakeCoral();

      intake.stopIntakeMotor();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void outtakeCoral(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, ntInstance)) {
      intake.outakeCoral();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.OUTTAKE_SPEED);
    }
  }

  @Test
  public void stopAfterOutakingCoral(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, ntInstance)) {
      intake.outakeCoral();

      intake.stopIntakeMotor();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void bumpAlgae(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, ntInstance)) {
      intake.bumpAlgae();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.BUMP_SPEED);
    }
  }

  @Test
  public void stopAfterBumpingAlgae(NetworkTableInstance ntInstance) {
    try (Intake intake = new Intake(fakeMotor, ntInstance)) {
      intake.bumpAlgae();

      intake.stopIntakeMotor();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }
}
