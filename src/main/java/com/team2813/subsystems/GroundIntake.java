package com.team2813.subsystems;

import static com.team2813.Constants.GROUND_INTAKE_WHEEL;
import static edu.wpi.first.units.Units.*;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import edu.wpi.first.units.measure.AngularVelocity;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

/**
 * The Ground intake for the 2025 Robot. This is for intaking coral on the ground and depositing it
 * in L1.
 *
 * @author spderman333
 */
public class GroundIntake extends SubsystemBase {
  private final PIDMotor groundIntakeMotor;

  private boolean isActive = false;

  private static final double INTAKE_SPEED = 8; // TODO: Tweak speed
  private static final double OUTTAKE_SPEED = -2.75;

  private static final AngularVelocity STALL_SPEED =
      RotationsPerSecond.of(
          0.1); // TODO: Tweak the stall speed, currently at 1 rotation per 10 sec.

  public GroundIntake() { // TODO: Ensure this constructor is actually functional.
    groundIntakeMotor =
        new TalonFXWrapper(
            GROUND_INTAKE_WHEEL, InvertType.CLOCKWISE); // +rotation = intake, -rotation = outtake.
  }

  /** Makes intake wheels spin in the intake direction. */
  public void intakeCoral() { // FIXME: Maybe add a check that the wheels are not stalled.
    groundIntakeMotor.set(ControlMode.VOLTAGE, INTAKE_SPEED);
    isActive = true;
  }

  /** Makes intake wheels spin in the outtake direction. */
  public void outtakeCoral() {
    groundIntakeMotor.set(ControlMode.VOLTAGE, OUTTAKE_SPEED);
    isActive = true;
  }

  public void fastOuttakeCoral() {
    groundIntakeMotor.set(ControlMode.VOLTAGE, 12);
    isActive = true;
  }

  /** Stops the intake wheels entirely. */
  public void stopGroundIntakeMotor() {
    groundIntakeMotor.set(ControlMode.DUTY_CYCLE, 0);
    isActive = false;
  }

  /**
   * Checks to see if the intake has stalled.
   *
   * @deprecated Broken; this will likely immediately return true, as soon as the intake command is
   *     issued.
   * @return <code>true</code> if the intake wheels have stalled, otherwise, returns <code>false
   *     </code>.
   */
  @Deprecated
  public boolean isStalled() {
    AngularVelocity currentVelocity = groundIntakeMotor.getVelocityMeasure();
    boolean isNotMoving = STALL_SPEED.gt(currentVelocity);
    return isActive && isNotMoving;
  }
}
