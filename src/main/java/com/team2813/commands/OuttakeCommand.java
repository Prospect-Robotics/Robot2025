package com.team2813.commands;

import com.team2813.subsystems.GroundIntake;
import com.team2813.subsystems.GroundIntakePivot;
import com.team2813.subsystems.Intake;
import edu.wpi.first.wpilibj2.command.*;

public final class OuttakeCommand {

  /** Creates a command that outtakes coral from both intakes at the same time. */
  public static Command create(
      Intake intake, GroundIntake groundIntake, GroundIntakePivot groundIntakePivot) {
    Command command =
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                intake.outtakeItemCommand(),
                new InstantCommand(
                    () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.TOP),
                    groundIntakePivot),
                new SequentialCommandGroup(
                    new WaitCommand(0.13), groundIntake.outtakeItemCommand())),
            new WaitCommand(0.25),
            groundIntake.stopMotorCommand(),
            new WaitCommand(0.15),
            intake.stopMotorCommand(),
            new WaitCommand(0.1));

    return command.finallyDo(
        () -> {
          intake.stopMotor();
          groundIntake.stopMotor();
          groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP);
        });
  }
}
