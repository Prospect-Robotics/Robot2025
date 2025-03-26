package com.team2813.subsystems.elevator;

import static edu.wpi.first.units.Units.Rotations;

import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.wpilibj2.command.Command;
import java.util.function.DoubleSupplier;
import java.util.function.Supplier;

public interface Elevator {

  /**
   * Creates an instance.
   *
   * @param movement Controller input.
   */
  static Elevator create(DoubleSupplier movement) {
    return new ElevatorSubsystem(NetworkTableInstance.getDefault(), movement);
  }

  /**
   * Returns a command that sets the setpoint and waits for the elevator to reach that point.
   *
   * @param position The desired position.
   */
  Command moveToPositionCommand(Position position);

  /**
   * Returns a command that sets the setpoint to the given value.
   *
   * <p>The returned command will complete immediately after executing. The default elevator command
   * will move the elevator to the given setpoint.
   *
   * @param position The desired position.
   */
  Command setSetpointCommand(Position position);

  /**
   * Returns a command that waits for the elevator to reach the current setpoint.
   *
   * <p>If the elevator does not reach the setpoint in a reasonable period of time, the returned
   * command will cancel itself.
   */
  Command waitForSetpointCommand();

  Command disableCommand();

  boolean atPosition();

  public enum Position implements Supplier<Angle> {
    BOTTOM(-0.212500),
    TEST(10),
    TOP(16.358496);

    private final Angle position;

    Position(double position) {
      this.position = Rotations.of(position);
    }

    @Override
    public Angle get() {
      return position;
    }
  }
}
