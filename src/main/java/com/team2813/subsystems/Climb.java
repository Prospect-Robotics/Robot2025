package com.team2813.subsystems;
// import static com.team2813.Constants.CLIMBER; 

import com.ctre.phoenix6.configs.SoftwareLimitSwitchConfigs;
import com.ctre.phoenix6.configs.TalonFXConfigurator;
import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.util.ConfigUtils;

import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
public class Climb extends SubsystemBase{ 

    private final PIDMotor ClimbMotor1; 
    private final PIDMotor ClimbMotor2;

    public Climber() {
        TalonFXWrapper ClimbMotor1 = new TalonFXWrapper(null, InvertType.CLOCKWISE);
		ClimbMotor1.motor().setNeutralMode(NeutralModeValue.Brake);
		TalonFXConfigurator cnf1 = ClimbMotor1.motor().getConfigurator();
		ConfigUtils.phoenix6Config(
				() -> cnf.apply(
					new SoftwareLimitSwitchConfigs()
					.withForwardSoftLimitEnable(true)
					.withForwardSoftLimitThreshold(null)
					.withReverseSoftLimitEnable(true)
					.withReverseSoftLimitThreshold(null)
				)
		); 
        this.ClimbMotor1 = ClimbMotor1; 
        TalonFXWrapper ClimbMotor2 = new TalonFXWrapper(null, InvertType.CLOCKWISE);
		ClimbMotor2.motor().setNeutralMode(NeutralModeValue.Brake);
		TalonFXConfigurator cnf2 = ClimbMotor2.motor().getConfigurator();
		ConfigUtils.phoenix6Config(
				() -> cnf.apply(
					new SoftwareLimitSwitchConfigs()
					.withForwardSoftLimitEnable(true)
					.withForwardSoftLimitThreshold(null)
					.withReverseSoftLimitEnable(true)
					.withReverseSoftLimitThreshold(null)
				)
		); 
        this.ClimbMotor2 = ClimbMotor2; 
    }
    public void extend() {
		ClimbMotor1.set(ControlMode.DUTY_CYCLE, null);
        ClimbMotor2.set(ControlMode.DUTY_CYCLE, null);
	}

	public void retract() {
		ClimbMotor1.set(ControlMode.DUTY_CYCLE, null);
        ClimbMotor2.set(ControlMode.DUTY_CYCLE, null);
	}

	public void stop() {
		ClimbMotor1.set(ControlMode.DUTY_CYCLE, null);
        ClimbMotor2.set(ControlMode.DUTY_CYCLE, null);
	}
   
}
