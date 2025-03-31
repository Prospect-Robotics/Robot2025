package com.team2813.subsystems.intake;

import com.team2813.lib2813.control.ControlMode;
import edu.wpi.first.wpilibj2.command.Command;
import java.util.function.DoubleSupplier;

public class ManualIntakePivot extends Command {

  private final IntakePivotSubsystem intakepivot;
  private final DoubleSupplier rotation;

  public ManualIntakePivot(IntakePivotSubsystem intakepivot, DoubleSupplier rotation) {
    this.intakepivot = intakepivot;
    this.rotation = rotation;
    addRequirements(intakepivot);
  }

  public void execute() {
    double val = rotation.getAsDouble();
    if (Math.abs(val) > 0.1) {
      intakepivot.set(ControlMode.DUTY_CYCLE, val * .1);
    } else if (!intakepivot.isEnabled()) {
      // An InstantCommand initiated the motor, and
      // PID controller is disabled; stop the elevator motors, potentially sliding down.
      intakepivot.set(ControlMode.DUTY_CYCLE, 0);
    } // ..else an InstantCommand initiated the motor. Leave it running ast the current speed
  }
}
