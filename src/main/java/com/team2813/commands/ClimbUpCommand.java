package com.team2813.commands;

import com.team2813.subsystems.Climb;
import edu.wpi.first.wpilibj2.command.Command;
import java.util.function.BooleanSupplier;

public class ClimbUpCommand extends Command {
  private final Climb climb;
  private final BooleanSupplier hasClimbed;

  public ClimbUpCommand(Climb climb, BooleanSupplier hasClimbed) {
    this.climb = climb;
    this.hasClimbed = hasClimbed;
    addRequirements(this.climb);
  }

  @Override
  public void end(boolean interrupted) {
    climb.stop();
  }

  @Override
  public void initialize() {
    if (!hasClimbed.getAsBoolean()) {
      climb.raise();
    }
  }

  @Override
  public boolean isFinished() {
    return hasClimbed.getAsBoolean();
  }
}
