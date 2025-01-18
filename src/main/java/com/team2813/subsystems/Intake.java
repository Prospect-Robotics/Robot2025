package com.team2813.subsystems;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;

import edu.wpi.first.wpilibj2.command.SubsystemBase;


//import static com.team2813.Constants.INTAKE;

public class Intake extends SubsystemBase{
    private boolean isIntaking = false;
    private final PIDMotor intakeMotor = new TalonFXWrapper(20, InvertType.COUNTER_CLOCKWISE);// canID = 20, arbitrary canID;
    private static final double intakeSpeed = 0.1;
    private static final double outakeSpeed = 0.6;

    public void intakeCoral(){
        intakeMotor.set(null, intakeSpeed);
        isIntaking = true;
    }
    public void outakeCoral(){
        intakeMotor.set(null, outakeSpeed);
        isIntaking = false;
    }
    public void stopIntakeMotor(){
        intakeMotor.set(null,0);
        isIntaking = false;
    }
}
