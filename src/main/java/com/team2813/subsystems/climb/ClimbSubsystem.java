package com.team2813.subsystems.climb;

import static com.team2813.Constants.CLIMB_1;
import static com.team2813.Constants.CLIMB_2;

import com.ctre.phoenix6.configs.SoftwareLimitSwitchConfigs;
import com.ctre.phoenix6.configs.TalonFXConfigurator;
import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.commands.LockFunctionCommand;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.util.ConfigUtils;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

/** This is the Climb. Her name is Lisa. Please be kind to her and say hi. Have a nice day! */
final class ClimbSubsystem extends SubsystemBase implements AutoCloseable, Climb {

  private final PIDMotor climbMotor1;
  private final DigitalInput limitSwitch;

  public ClimbSubsystem(NetworkTableInstance networkTableInstance) {
    limitSwitch = new DigitalInput(0);
    TalonFXWrapper climbMotor1 = new TalonFXWrapper(CLIMB_1, InvertType.CLOCKWISE);
    climbMotor1.motor().setNeutralMode(NeutralModeValue.Brake);
    TalonFXConfigurator cnf = climbMotor1.motor().getConfigurator();
    ConfigUtils.phoenix6Config(
        () ->
            cnf.apply(
                new SoftwareLimitSwitchConfigs()
                    .withForwardSoftLimitEnable(false)
                    .withForwardSoftLimitThreshold(0)
                    .withReverseSoftLimitEnable(false)
                    .withReverseSoftLimitThreshold(0)));
    this.climbMotor1 = climbMotor1;
    climbMotor1.addFollower(CLIMB_2, InvertType.FOLLOW_MASTER);
    // Logging
    NetworkTable networkTable = networkTableInstance.getTable("Climb");
    limitSwitchPressed = networkTable.getBooleanTopic("limit switch pressed").publish();
  }

  @Override
  public Command stopCommand() {
    return new InstantCommand(this::stop, this);
  }

  @Override
  public Command raiseCommand() {
    return new SequentialCommandGroup(
        new LockFunctionCommand(this::limitSwitchPressed, this::raise, this), stopCommand());
  }

  @Override
  public Command lowerCommand() {
    return new InstantCommand(this::lower, this);
  }

  public void raise() {
    if (!limitSwitchPressed()) {
      climbMotor1.set(ControlMode.VOLTAGE, -8);
    }
  }

  public void lower() {
    climbMotor1.set(ControlMode.VOLTAGE, 8);
  }

  private void stop() {
    climbMotor1.set(ControlMode.VOLTAGE, 0);
  }

  public boolean limitSwitchPressed() {
    return limitSwitch.get();
  }

  private final BooleanPublisher limitSwitchPressed;

  @Override
  public void close() {
    limitSwitch.close();
  }

  @Override
  public void periodic() {
    limitSwitchPressed.set(limitSwitchPressed());
  }
}
