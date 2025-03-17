package com.team2813.subsystems;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import edu.wpi.first.units.AngularVelocityUnit;
import edu.wpi.first.units.Measure;
import edu.wpi.first.units.measure.AngularVelocity;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import static edu.wpi.first.units.Units.*;

import static com.team2813.Constants.GROUND_INTAKE_WHEEL;

/**
 * The Ground intake for the 2025 Robot, This is for intaking coral on the ground and depositing it in L1.
 * @author spderman333
 */

public class GroundIntake extends SubsystemBase {
    private final PIDMotor groundIntakeMotor;

    private boolean isActive = false;

    private final double INTAKE_SPEED = 0.6; // TODO: Tweak speed
    private final double OUTTAKE_SPEED = -0.6; // TODO: Tweak speed

    private final AngularVelocity stallSpeed = RotationsPerSecond.of(0.1); //TODO: Tweak the stall speed, currently at 1 rotation per 10 sec.

    public GroundIntake() { // TODO: Ensure this constructor is actually functional.
        groundIntakeMotor = new TalonFXWrapper(GROUND_INTAKE_WHEEL, InvertType.CLOCKWISE); // +rotation = intake, -rotation = outtake.
    }

    /**
     * Makes intake wheels spin in the intake direction.
     * <p>Sets <code>isActive</code> to <code>true</code>.</p>
     */
    public void intakeCoral() { // FIXME: Maybe add a check that the wheels are not stalled.
        groundIntakeMotor.set(ControlMode.DUTY_CYCLE, INTAKE_SPEED);
        isActive = true;
    }

    /**
     * Makes intake wheels spin in the outtake direction.
     * <p>Sets <code>isActive</code> to <code>true</code>.</p>
     */
    public void outtakeCoral() {
        groundIntakeMotor.set(ControlMode.DUTY_CYCLE, OUTTAKE_SPEED);
        isActive = true;
    }

    /**
     * Stops the intake wheels entirely.
     * <p>Sets <code>isActive</code> to <code>false</code>.</p>
     */

    public void stopGroundIntakeMotor() {
        groundIntakeMotor.set(ControlMode.DUTY_CYCLE, 0);
        isActive = false;
    }

    /**
     * Checks to see if the intake has stalled.
     * @return <code>true</code> if the intake wheels have stalled, otherwise, returns <code>false</code>.
     */

    public boolean isStalled() {
        AngularVelocity currentVelocity = groundIntakeMotor.getVelocityMeasure();
        boolean isNotMoving = stallSpeed.gt(currentVelocity);
        return isActive && isNotMoving;
    }


}
