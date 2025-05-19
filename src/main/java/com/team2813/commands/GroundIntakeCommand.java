package com.team2813.commands;

import com.team2813.subsystems.GroundIntake;
import com.team2813.subsystems.GroundIntakePivot;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.Command;

public class GroundIntakeCommand extends Command {
  GroundIntakePivot groundIntakePivot;
  GroundIntake groundIntake;
  double startTime;

  public GroundIntakeCommand(GroundIntakePivot groundIntakePivot, GroundIntake groundIntake) {
    addRequirements(groundIntakePivot, groundIntake);
    this.groundIntakePivot = groundIntakePivot;
    this.groundIntake = groundIntake;
  }

  @Override
  public void initialize() {
    groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.BOTTOM);
    startTime = Timer.getFPGATimestamp();
  }

  @Override
  public void execute() {
    if (groundIntakePivot.atPosition() || Timer.getFPGATimestamp() - startTime > 1.0) {
      groundIntake.intakeCoral();
    }
  }

  @Override
  public void end(boolean interrupted) {
    groundIntake.stopGroundIntakeMotor();
    groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP);
  }
}
