package com.team2813.subsystems;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;

import edu.wpi.first.wpilibj2.command.SubsystemBase;


import static com.team2813.Constants.INTAKE_WHEEL;

public class Intake extends SubsystemBase{

    // This is Griffith. He is the Intake Subsystem. Treat him with respect.
    
    private boolean isIntaking = false;
    private final PIDMotor intakeMotor = new TalonFXWrapper(INTAKE_WHEEL, InvertType.COUNTER_CLOCKWISE);
    private static final double intakeSpeed = 0.6;
    private static final double outakeSpeed = -0.6;

    public void intakeCoral(){
        intakeMotor.set(ControlMode.DUTY_CYCLE, intakeSpeed);
        isIntaking = true;
    }
    public void outakeCoral(){
        intakeMotor.set(ControlMode.DUTY_CYCLE, outakeSpeed); 
        isIntaking = false;
    }
    public void stopIntakeMotor(){
        intakeMotor.set(ControlMode.DUTY_CYCLE,0);
        isIntaking = false;
    }
}
