package com.team2813.subsystems.intake;

import static com.team2813.Constants.OperatorConstants.MANUAL_INTAKE_PIVOT_POS;

import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.commands.LockFunctionCommand;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.encoders.CancoderWrapper;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.subsystems.MotorSubsystem;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.DoublePublisher;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Time;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.InstantCommand;

/**
 * This is the Intake Pivot. Her name is Sophie. Please be kind to her and say hi. Have a nice day!
 */
class IntakePivotSubsystem extends MotorSubsystem<IntakePivotSubsystem.Rotations>
    implements IntakePivot {
  private static final Time MOVEMENT_TIMEOUT = Units.Seconds.of(2);

  IntakePivotSubsystem(NetworkTableInstance networkTableInstance) {
    super(
        new MotorSubsystemConfiguration(
                pivotMotor(), new CancoderWrapper(com.team2813.Constants.INTAKE_ENCODER))
            .acceptableError(0.03)
            .startingPosition(Rotations.INTAKE)
            .rotationUnit(Units.Rotations)
            .controlMode(ControlMode.VOLTAGE)
            .PID(19.875, 0, 0.4));
    // Logging
    NetworkTable networkTable = networkTableInstance.getTable("IntakePivot");
    intakePivotPosition = networkTable.getDoubleTopic("position").publish();
    atPosition = networkTable.getBooleanTopic("at position").publish();

    setDefaultCommand(new ManualIntakePivot(this, () -> -MANUAL_INTAKE_PIVOT_POS.getAsDouble()));
  }

  @Override
  public Command setSetpointCommand(Rotations position) {
    return new InstantCommand(() -> setSetpoint(position), this);
  }

  @Override
  public Command moveToPositionCommand(Rotations position) {
    return new LockFunctionCommand(this::atPosition, () -> this.setSetpoint(position), this)
        .withTimeout(MOVEMENT_TIMEOUT);
  }

  @Override
  public Command disableCommand() {
    return new InstantCommand(this::disable);
  }

  @Override
  protected void useOutput(double output, double setPoint) {
    super.useOutput(output, setPoint);
  }

  private static PIDMotor pivotMotor() {
    TalonFXWrapper pivotMotor =
        new TalonFXWrapper(com.team2813.Constants.INTAKE_PIVOT, InvertType.COUNTER_CLOCKWISE);
    pivotMotor.setNeutralMode(NeutralModeValue.Brake);

    return pivotMotor;
  }

  private final DoublePublisher intakePivotPosition;
  private final BooleanPublisher atPosition;

  @Override
  public void periodic() {
    super.periodic();
    intakePivotPosition.set(getPositionMeasure().in(Units.Rotations));
    atPosition.set(atPosition());
  }
}
