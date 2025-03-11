package com.team2813.subsystems;

import com.ctre.phoenix6.configs.CurrentLimitsConfigs;
import com.ctre.phoenix6.configs.TalonFXConfigurator;
import com.ctre.phoenix6.configs.VoltageConfigs;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;

import com.team2813.lib2813.util.ConfigUtils;
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
    static final double INTAKE_SPEED = 4;
    static final double OUTTAKE_SPEED = -3;
    static final double BUMP_SPEED = -4;

    public Intake() {
        this(new TalonFXWrapper(INTAKE_WHEEL, InvertType.CLOCKWISE));
    }

    Intake(PIDMotor motor) {
        this.intakeMotor = motor;
        if (motor instanceof TalonFXWrapper wrapper) {
          TalonFXConfigurator config = wrapper.motor().getConfigurator();
          ConfigUtils.phoenix6Config(() -> config.apply(new CurrentLimitsConfigs().withStatorCurrentLimitEnable(false)));
          ConfigUtils.phoenix6Config(() -> config.apply(new VoltageConfigs().withPeakForwardVoltage(12).withPeakReverseVoltage(12)));
        }
    }

    public void intakeCoral(){
        intakeMotor.set(ControlMode.VOLTAGE, INTAKE_SPEED);
        isIntaking = true;
    }
    public void outakeCoral(){
        intakeMotor.set(ControlMode.VOLTAGE, OUTTAKE_SPEED);
        isIntaking = false;
    }
    public void slowOuttakeCoral() {
        intakeMotor.set(ControlMode.VOLTAGE, 0.75 * OUTTAKE_SPEED);
        isIntaking = false;
    }
    public void bumpAlgae() {
        intakeMotor.set(ControlMode.VOLTAGE, BUMP_SPEED);
        isIntaking = false;
    }
    public void stopIntakeMotor(){
        intakeMotor.set(ControlMode.VOLTAGE,0);
        isIntaking = false;
    }

    boolean intaking() {
        return isIntaking;
    }
}
