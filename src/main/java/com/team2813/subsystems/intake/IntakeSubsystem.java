package com.team2813.subsystems.intake;

import static com.team2813.Constants.INTAKE_WHEEL;

import com.ctre.phoenix6.configs.CurrentLimitsConfigs;
import com.ctre.phoenix6.configs.TalonFXConfigurator;
import com.ctre.phoenix6.configs.VoltageConfigs;
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
import edu.wpi.first.wpilibj2.command.SubsystemBase;

/** This is the Intake. His name is Joe. Please be kind to him and say hi. Have a nice day! */
class IntakeSubsystem extends SubsystemBase implements Intake {

  private boolean isIntaking = false;
  private final PIDMotor intakeMotor;
  static final double INTAKE_SPEED = 4;
  static final double OUTTAKE_SPEED = -3;
  static final double BUMP_SPEED = -4;

  private final DigitalInput beamBreak;

  public IntakeSubsystem(NetworkTableInstance networkTableInstance) {
    this(
        new TalonFXWrapper(INTAKE_WHEEL, InvertType.CLOCKWISE),
        new DigitalInput(1),
        networkTableInstance);
  }

  IntakeSubsystem(
      PIDMotor motor, DigitalInput beamBreak, NetworkTableInstance networkTableInstance) {
    this.intakeMotor = motor;
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

  @Override
  public Command bumpAlgaeCommand() {
    return new InstantCommand(this::bumpAlgae, this).handleInterrupt(this::stopIntakeMotor);
  }

  @Override
  public Command intakeCoralCommand() {
    return new InstantCommand(this::intakeCoral, this).handleInterrupt(this::stopIntakeMotor);
  }

  @Override
  public Command outakeCoralCommand() {
    return new InstantCommand(this::outakeCoral, this).handleInterrupt(this::stopIntakeMotor);
  }

  @Override
  public Command slowOutakeCoralCommand() {
    return new InstantCommand(this::slowOuttakeCoral, this).handleInterrupt(this::stopIntakeMotor);
  }

  @Override
  public Command stopIntakeMotorCommand() {
    return new InstantCommand(this::stopIntakeMotor, this);
  }

  // Visible for testing
  void intakeCoral() {
    intakeMotor.set(ControlMode.VOLTAGE, INTAKE_SPEED);
    isIntaking = true;
  }

  private void outakeCoral() {
    intakeMotor.set(ControlMode.VOLTAGE, OUTTAKE_SPEED);
    isIntaking = false;
  }

  private void slowOuttakeCoral() {
    intakeMotor.set(ControlMode.VOLTAGE, 0.75 * OUTTAKE_SPEED);
    isIntaking = false;
  }

  private void bumpAlgae() {
    intakeMotor.set(ControlMode.VOLTAGE, BUMP_SPEED);
    isIntaking = false;
  }

  private void stopIntakeMotor() {
    intakeMotor.set(ControlMode.VOLTAGE, 0);
    isIntaking = false;
  }

  @Override
  public boolean intaking() {
    return isIntaking;
  }

  @Override
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
