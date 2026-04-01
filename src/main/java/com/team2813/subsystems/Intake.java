package com.team2813.subsystems;

import static com.team2813.Constants.INTAKE_WHEEL;

import com.ctre.phoenix6.configs.CurrentLimitsConfigs;
import com.ctre.phoenix6.configs.TalonFXConfigurator;
import com.ctre.phoenix6.configs.VoltageConfigs;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.Motor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.subsystems.ParameterizedIntakeSubsystem;
import com.team2813.lib2813.util.ConfigUtils;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj2.command.Command;

/** This is the Intake. His name is Joe. Please be kind to him and say hi. Have a nice day! */
public final class Intake extends ParameterizedIntakeSubsystem {
  static final Params PARAMS = Params.builder().setIntakeDemand(4).setOuttakeDemand(-3).build();

  static final double BUMP_VOLTAGE = -4;

  private final DigitalInput beamBreak;

  public Intake(NetworkTableInstance networkTableInstance) {
    this(
        new TalonFXWrapper(INTAKE_WHEEL, InvertType.CLOCKWISE),
        new DigitalInput(1),
        networkTableInstance);
  }

  Intake(Motor motor, DigitalInput beamBreak, NetworkTableInstance networkTableInstance) {
    super(motor, PARAMS);
    this.beamBreak = beamBreak;
    if (motor instanceof TalonFXWrapper wrapper) {
      TalonFXConfigurator config = wrapper.motor().getConfigurator();
      ConfigUtils.phoenix6Config(
          () -> config.apply(new CurrentLimitsConfigs().withStatorCurrentLimitEnable(false)));
      ConfigUtils.phoenix6Config(
          () ->
              config.apply(
                  new VoltageConfigs().withPeakForwardVoltage(12).withPeakReverseVoltage(12)));
    }
    NetworkTable networkTable = networkTableInstance.getTable("Intake");
    hasCoralPublisher = networkTable.getBooleanTopic("Has Coral").publish();
  }

  public Command bumpAlgaeCommand() {
    return setMotorDemandCommand(BUMP_VOLTAGE);
  }

  public Command slowOuttakeItemCommand() {
    return setMotorDemandCommand(0.75 * PARAMS.outtakeDemand());
  }

  public boolean hasCoral() {
    return !beamBreak.get();
  }

  private final BooleanPublisher hasCoralPublisher;

  @Override
  public void periodic() {
    hasCoralPublisher.accept(hasCoral());
  }

  @Override
  public void close() {
    beamBreak.close();
  }
}
