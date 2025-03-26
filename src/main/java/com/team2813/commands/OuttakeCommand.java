package com.team2813.commands;

import com.team2813.subsystems.GroundIntake;
import com.team2813.subsystems.GroundIntakePivot;
import com.team2813.subsystems.intake.Intake;
import edu.wpi.first.wpilibj2.command.*;

public class OuttakeCommand extends Command {
  private final Intake intake;
  private final GroundIntake groundIntake;
  private final GroundIntakePivot groundIntakePivot;
  private final SequentialCommandGroup commandGroup;

  public OuttakeCommand(
      Intake intake, GroundIntake groundIntake, GroundIntakePivot groundIntakePivot) {
    commandGroup =
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                intake.outakeCoralCommand(),
                new ParallelCommandGroup(
                    new InstantCommand(
                        () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.TOP),
                        groundIntakePivot)),
                new SequentialCommandGroup(
                    new WaitCommand(0.13),
                    new InstantCommand(groundIntake::outtakeCoral, groundIntake))),
            new WaitCommand(0.25),
            new InstantCommand(groundIntake::stopGroundIntakeMotor, groundIntake),
            new ParallelCommandGroup(
                new SequentialCommandGroup(
                    new WaitCommand(0.25),
                    new InstantCommand(
                        () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP),
                        groundIntakePivot)),
                new SequentialCommandGroup(
                    new WaitCommand(0.15), intake.stopIntakeMotorCommand())));
    this.intake = intake;
    this.groundIntake = groundIntake;
    this.groundIntakePivot = groundIntakePivot;
    addRequirements(intake.asSubsystem(), groundIntake, groundIntakePivot);
  }

  @Override
  public void initialize() {
    commandGroup.initialize();
  }

  @Override
  public void execute() {
    commandGroup.execute();
  }

  @Override
  public boolean isFinished() {
    return commandGroup.isFinished();
  }

  @Override
  public void end(boolean interrupted) {
    commandGroup.end(interrupted);
    intake.stopIntakeMotorNow();
    groundIntake.stopGroundIntakeMotor();
    groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP);
  }
}
