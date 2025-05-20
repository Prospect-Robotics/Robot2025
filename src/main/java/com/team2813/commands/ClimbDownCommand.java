package com.team2813.commands;

import com.team2813.subsystems.Climb;
import com.team2813.subsystems.IntakePivot;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.Command;

public class ClimbDownCommand extends Command {
  private final Climb climb;
  private final IntakePivot intakePivot;
  private double startTime;

  public ClimbDownCommand(Climb climb, IntakePivot intakePivot) {
    this.climb = climb;
    this.intakePivot = intakePivot;
    addRequirements(this.climb, this.intakePivot);
  }

  @Override
  public void end(boolean interrupted) {
    climb.stop();
  }

  @Override
  public void initialize() {
    intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP);
    startTime = Timer.getFPGATimestamp();
  }

  @Override
  public void execute() {
    if (intakePivot.atPosition() || Timer.getFPGATimestamp() - startTime > 1) {
      climb.lower();
    }
  }
}
