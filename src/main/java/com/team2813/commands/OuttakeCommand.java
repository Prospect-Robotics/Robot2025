package com.team2813.commands;

import com.team2813.subsystems.GroundIntake;
import com.team2813.subsystems.GroundIntakePivot;
import com.team2813.subsystems.intake.Intake;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.ParallelCommandGroup;
import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import edu.wpi.first.wpilibj2.command.WaitCommand;

public final class OuttakeCommand {

  public static Command create(
      Intake intake, GroundIntake groundIntake, GroundIntakePivot groundIntakePivot) {
    Command commandGroup =
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

    return commandGroup.handleInterrupt(
        () -> {
          groundIntake.stopGroundIntakeMotor();
          groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP);
        });
  }
}
