package com.team2813.subsystems;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;

import edu.wpi.first.wpilibj2.command.SubsystemBase;


import static com.team2813.Constants.INTAKE_WHEEL;

public class Intake extends SubsystemBase{
    private boolean isIntaking = false;
    private final PIDMotor intakeMotor = new TalonFXWrapper(INTAKE_WHEEL, InvertType.CLOCKWISE);
    private static final double intakeSpeed = 4;
    private static final double outakeSpeed = -4;

    public void intakeCoral(){
        intakeMotor.set(ControlMode.VOLTAGE, intakeSpeed);
        isIntaking = true;
    }
    public void outakeCoral(){
        intakeMotor.set(ControlMode.VOLTAGE, outakeSpeed);
        isIntaking = false;
    }
    public void stopIntakeMotor(){
        intakeMotor.set(ControlMode.VOLTAGE,0);
        isIntaking = false;
    }
}
