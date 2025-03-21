package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;

import com.team2813.NetworkTableResource;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import org.mockito.Answers;

@RunWith(JUnit4.class)
public final class IntakeTest {
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);
  @Rule public final NetworkTableResource ntResource = new NetworkTableResource();

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
    try (Intake intake = new Intake(fakeMotor, ntResource.getNetworkTableInstance())) {
      assertThat(intake.intaking()).isFalse();
      verifyNoInteractions(fakeMotor);
    }
  }

  @Test
  public void intakeCoral() {
    try (Intake intake = new Intake(fakeMotor, ntResource.getNetworkTableInstance())) {
      intake.intakeCoral();

      assertThat(intake.intaking()).isTrue();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.INTAKE_SPEED);
    }
  }

  @Test
  public void stopAfterIntakingCoral() {
    try (Intake intake = new Intake(fakeMotor, ntResource.getNetworkTableInstance())) {
      intake.intakeCoral();

      intake.stopIntakeMotor();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void outtakeCoral() {
    try (Intake intake = new Intake(fakeMotor, ntResource.getNetworkTableInstance())) {
      intake.outakeCoral();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.OUTTAKE_SPEED);
    }
  }

  @Test
  public void stopAfterOutakingCoral() {
    try (Intake intake = new Intake(fakeMotor, ntResource.getNetworkTableInstance())) {
      intake.outakeCoral();

      intake.stopIntakeMotor();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }

  @Test
  public void bumpAlgae() {
    try (Intake intake = new Intake(fakeMotor, ntResource.getNetworkTableInstance())) {
      intake.bumpAlgae();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.BUMP_SPEED);
    }
  }

  @Test
  public void stopAfterBumpingAlgae() {
    try (Intake intake = new Intake(fakeMotor, ntResource.getNetworkTableInstance())) {
      intake.bumpAlgae();

      intake.stopIntakeMotor();

      assertThat(intake.intaking()).isFalse();
      assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
    }
  }
}
