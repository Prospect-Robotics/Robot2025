package com.team2813.subsystems.intake;

import com.team2813.lib2813.control.ControlMode;
import edu.wpi.first.wpilibj2.command.Command;
import java.util.function.DoubleSupplier;

class ManualIntakePivot extends Command {

  private final IntakePivotSubsystem intakePivot;
  private final DoubleSupplier rotation;

  ManualIntakePivot(IntakePivotSubsystem intakePivot, DoubleSupplier rotation) {
    this.intakePivot = intakePivot;
    this.rotation = rotation;
    addRequirements(intakePivot);
  }

  public void execute() {
    double val = rotation.getAsDouble();
    if (Math.abs(val) > 0.1) {
      intakePivot.set(ControlMode.DUTY_CYCLE, val * .1);
    } else if (!intakePivot.isEnabled()) {
      // An InstantCommand initiated the motor, and
      // PID controller is disabled; stop the elevator motors, potentially sliding down.
      intakePivot.set(ControlMode.DUTY_CYCLE, 0);
    } // ..else an InstantCommand initiated the motor. Leave it running ast the current speed
  }
}
