package com.team2813.subsystems.elevator;

import static com.team2813.Constants.ELEVATOR_1;
import static com.team2813.Constants.ELEVATOR_2;

import com.ctre.phoenix6.Utils;
import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.commands.LockFunctionCommand;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.subsystems.MotorSubsystem;
import edu.wpi.first.math.MathUtil;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.DoublePublisher;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Time;
import edu.wpi.first.wpilibj2.command.*;
import java.util.Set;
import java.util.function.DoubleSupplier;

/** This is the Elevator. His name is Pablo. Please be kind to him and say hi. Have a nice day! */
class ElevatorSubsystem extends MotorSubsystem<ElevatorSubsystem.Position> implements Elevator {
  private static final Time MOVEMENT_TIMEOUT = Units.Seconds.of(2);
  private double lastSetpointSetTime;

  // You see a message written in blood on the wall...
  // It reads: "THIS CODE WILL LIKELY HAVE TO BE *MAJORLY* REFACTORED
  // AND TESTED AS IT WAS JUST COPIED FROM FENDER BENDER WITH MINIMUM CHANGES."
  // HERE BE DRAGONS.
  // Your companion notes: "...jeez... that is a lot of blood... couldn't they just leave a paper
  // taped to the wall, rather than raid a blood donation clinic."
  ElevatorSubsystem(NetworkTableInstance networkTableInstance, DoubleSupplier movement) {
    super(
        new MotorSubsystemConfiguration(getMotor())
            .controlMode(ControlMode.VOLTAGE)
            .acceptableError(1.7)
            .PID(0.2, 0.001, 0.001)
            .rotationUnit(Units.Radians));
    NetworkTable networkTable = networkTableInstance.getTable("Elevator");
    atPosition = networkTable.getBooleanTopic("at position").publish();
    position = networkTable.getDoubleTopic("position").publish();

    setDefaultCommand(new DefaultCommand(this, movement));
  }

  private static TalonFXWrapper getMotor() {
    TalonFXWrapper wrapper = new TalonFXWrapper(ELEVATOR_1, InvertType.CLOCKWISE);
    wrapper.setNeutralMode(NeutralModeValue.Brake);
    wrapper.addFollower(ELEVATOR_2, InvertType.FOLLOW_MASTER);
    return wrapper;
  }

  @Override
  public Command moveToPositionCommand(Position position) {
    return new LockFunctionCommand(this::atPosition, () -> this.setSetpoint(position), this)
        .withTimeout(MOVEMENT_TIMEOUT);
  }

  @Override
  public Command waitForSetpointCommand() {
    return new DeferredCommand(
        () -> {
          if (atPosition()) {
            return Commands.none();
          }
          double elapsedSecs = Utils.getCurrentTimeSeconds() - lastSetpointSetTime;
          Time timeout = MOVEMENT_TIMEOUT.minus(Units.Seconds.of(elapsedSecs));
          return Commands.waitUntil(this::atPosition).withTimeout(timeout);
        },
        Set.of(this));
  }

  @Override
  public Command setSetpointCommand(Position position) {
    return new InstantCommand(() -> setSetpoint(position), this);
  }

  @Override
  public void setSetpoint(Position position) {
    super.setSetpoint(position);
    lastSetpointSetTime = Utils.getCurrentTimeSeconds();
  }

  @Override
  public Command disableCommand() {
    return new InstantCommand(this::disable, this);
  }

  @Override
  protected void useOutput(double output, double setpoint) {
    super.useOutput(MathUtil.clamp(output, -6, 6), setpoint);
  }

  private final BooleanPublisher atPosition;
  private final DoublePublisher position;

  @Override
  public void periodic() {
    super.periodic();
    atPosition.set(atPosition());
    position.set(getMeasurement());
  }
}
