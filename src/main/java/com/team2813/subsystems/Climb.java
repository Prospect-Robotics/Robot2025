package com.team2813.subsystems;

import com.ctre.phoenix6.configs.SoftwareLimitSwitchConfigs;
import com.ctre.phoenix6.configs.TalonFXConfigurator;
import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.util.ConfigUtils;
import edu.wpi.first.wpilibj.DigitalInput;


import edu.wpi.first.wpilibj2.command.SubsystemBase;

import static com.team2813.Constants.*;
/**
* This is the Climb. Her name is Lisa.
* Please be kind to her and say hi.
* Have a nice day!
*/
public class Climb extends SubsystemBase implements AutoCloseable {

    private final PIDMotor climbMotor1;
	private DigitalInput limitSwitch;

    public Climb() {
		limitSwitch = new DigitalInput(0);
        TalonFXWrapper climbMotor1 = new TalonFXWrapper(CLIMB_1, InvertType.CLOCKWISE);
				climbMotor1.motor().setNeutralMode(NeutralModeValue.Brake);
				TalonFXConfigurator cnf = climbMotor1.motor().getConfigurator();
				ConfigUtils.phoenix6Config(
						() -> cnf.apply(
							new SoftwareLimitSwitchConfigs()
							.withForwardSoftLimitEnable(false)
							.withForwardSoftLimitThreshold(0)
							.withReverseSoftLimitEnable(false)
							.withReverseSoftLimitThreshold(0)
						)
				);
				this.climbMotor1 = climbMotor1;
				climbMotor1.addFollower(CLIMB_2, InvertType.FOLLOW_MASTER);
    }
    public void raise () {
		if (!limitSwitch.get()) {
            climbMotor1.set(ControlMode.VOLTAGE, -8);
        } else {
			climbMotor1.set(ControlMode.VOLTAGE, 0);
		}
	}
	public void lower() {
		climbMotor1.set(ControlMode.VOLTAGE, 8);
	}

	public void stop() {
		climbMotor1.set(ControlMode.VOLTAGE, 0);
	}
	@Override
	public void periodic() {
		if (limitSwitch.get()){
			climbMotor1.set(ControlMode.VOLTAGE, 0);
		}
	}

    @Override
    public void close() {
        limitSwitch.close();
    }
}
