package com.team2813.subsystems;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import org.mockito.Answers;

import static com.google.common.truth.Truth.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verifyNoInteractions;

@RunWith(JUnit4.class)
public final class IntakeTest {
  final FakePIDMotor fakeMotor = mock(FakePIDMotor.class, Answers.CALLS_REAL_METHODS);

  static abstract class FakePIDMotor implements PIDMotor {
    double dutyCycle = 0.0f;

    @Override
    public void set(ControlMode mode, double demand) {
      assertThat(mode).isEqualTo(ControlMode.VOLTAGE);
      this.dutyCycle = demand;
    }
  }

  @Test
  public void constructRealInstance() {
    Intake intake = new Intake();

    assertThat(intake.intaking()).isFalse();
  }

  @Test
  public void initialState() {
    Intake intake = new Intake(fakeMotor);

    assertThat(intake.intaking()).isFalse();
    verifyNoInteractions(fakeMotor);
  }

  @Test
  public void intakeCoral() {
    Intake intake = new Intake(fakeMotor);

    intake.intakeCoral();

    assertThat(intake.intaking()).isTrue();
    assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.INTAKE_SPEED);
  }

  @Test
  public void stopAfterIntakingCoral() {
    Intake intake = new Intake(fakeMotor);
    intake.intakeCoral();

    intake.stopIntakeMotor();

    assertThat(intake.intaking()).isFalse();
    assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
  }

  @Test
  public void outtakeCoral() {
    Intake intake = new Intake(fakeMotor);

    intake.outakeCoral();

    assertThat(intake.intaking()).isFalse();
    assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.OUTTAKE_SPEED);
  }

  @Test
  public void stopAfterOutakingCoral() {
    Intake intake = new Intake(fakeMotor);
    intake.outakeCoral();

    intake.stopIntakeMotor();

    assertThat(intake.intaking()).isFalse();
    assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
  }
  
  @Test
  public void bumpAlgae() {
    Intake intake = new Intake(fakeMotor);
    
    intake.bumpAlgae();
    
    assertThat(intake.intaking()).isFalse();
    assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(Intake.BUMP_SPEED);
  }
  
  @Test
  public void stopAfterBumpingAlgae() {
    Intake intake = new Intake(fakeMotor);
    intake.bumpAlgae();
    
    intake.stopIntakeMotor();
    
    assertThat(intake.intaking()).isFalse();
    assertThat(fakeMotor.dutyCycle).isWithin(0.01).of(0);
  }
}
