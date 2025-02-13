package com.team2813.subsystems;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;

import edu.wpi.first.wpilibj2.command.SubsystemBase;


import static com.team2813.Constants.INTAKE_WHEEL;
/**
* This is the Intake. His name is Joe.
* Please be kind to him and say hi.
* Have a nice day!
*/
public class Intake extends SubsystemBase{
    
    private boolean isIntaking = false;
    private final PIDMotor intakeMotor;
    static final double INTAKE_SPEED = 0.6;
    static final double OUTTAKE_SPEED = -0.6;

    public Intake() {
        this(new TalonFXWrapper(INTAKE_WHEEL, InvertType.COUNTER_CLOCKWISE));
    }

    Intake(PIDMotor motor) {
        this.intakeMotor = motor;
    }

    public void intakeCoral(){
        intakeMotor.set(ControlMode.DUTY_CYCLE, INTAKE_SPEED);
        isIntaking = true;
    }
    public void outakeCoral(){
        intakeMotor.set(ControlMode.DUTY_CYCLE, OUTTAKE_SPEED);
        isIntaking = false;
    }
    public void stopIntakeMotor(){
        intakeMotor.set(ControlMode.DUTY_CYCLE,0);
        isIntaking = false;
    }

    boolean intaking() {
        return isIntaking;
    }
}
