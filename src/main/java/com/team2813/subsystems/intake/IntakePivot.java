package com.team2813.subsystems.intake;

import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.wpilibj2.command.Command;
import java.util.function.Supplier;

public interface IntakePivot {
  /**
   * Returns a command that sets the setpoint and waits for the elevator to reach that point.
   *
   * @param position The desired position.
   */
  Command moveToPositionCommand(Rotations position);

  /**
   * Returns a command that sets the setpoint to the given value.
   *
   * <p>The returned command will complete immediately after executing. The default elevator command
   * will move the elevator to the given setpoint.
   *
   * @param position The desired position.
   */
  Command setSetpointCommand(Rotations position);

  Command disableCommand();

  enum Rotations implements Supplier<Angle> {
    OUTTAKE(Units.Rotations.of(0.723389)), // TODO: NEEDS TUNING
    INTAKE(Units.Rotations.of(0.448721)), // TODO: NEEDS TUNING
    ALGAE_BUMP(Units.Rotations.of(1.108418)),
    HARD_STOP(Units.Rotations.of(0.438721)); // TODO: NEEDS TUNING

    Rotations(Angle pos) {
      this.pos = pos;
    }

    private final Angle pos;

    @Override
    public Angle get() {
      return pos;
    }
  }
}
