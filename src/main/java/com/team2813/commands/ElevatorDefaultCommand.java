package com.team2813.commands;

import com.team2813.lib2813.control.ControlMode;
import com.team2813.subsystems.Elevator;
import edu.wpi.first.wpilibj2.command.Command;
import java.util.function.DoubleSupplier;

public class ElevatorDefaultCommand extends Command {
  private final Elevator elevator;
  private final DoubleSupplier movement;

  public ElevatorDefaultCommand(Elevator elevator, DoubleSupplier movement) {
    this.elevator = elevator;
    this.movement = movement;
    addRequirements(elevator);
  }

  @Override
  public void execute() {
    double val = movement.getAsDouble();
    if (Math.abs(val) > 0.1) {
      elevator.set(ControlMode.DUTY_CYCLE, val);
    } else if (!elevator.isEnabled()) {
      // An InstantCommand initiated the motor, and
      // PID controller is disabled; stop the elevator motors, potentially sliding down.
      elevator.set(ControlMode.DUTY_CYCLE, 0);
    } // ..else an InstantCommand initiated the motor. Leave it running ast the current speed
  }
}
