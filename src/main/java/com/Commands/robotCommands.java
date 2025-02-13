package com.Commands;

import com.team2813.subsystems.Elevator;
import com.team2813.subsystems.Intake;

import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.ParallelCommandGroup;
import edu.wpi.first.wpilibj2.command.ParallelRaceGroup;
import edu.wpi.first.wpilibj2.command.SequentialCommandGroup;
import edu.wpi.first.wpilibj2.command.WaitCommand;

public class robotCommands {
    private final Intake intake;
    private final IntakePivot intakePivot;
    private final Elevator elevator;
    private final Climb climb;
    private final AlgeaIntake algeaIntake;
    public robotCommands(Intake intake,IntakePivot intakePivot, Elevator elevator, Climb climb){
        this.intake = intake;
        this.intakePivot = intakePivot;
        this.elevator = elevator;
        this.climb = climb;
    }
    private volatile static Command placeCoral = null;
    
        private static Command createPlaceCoral() {
                return new SequentialCommandGroup(
                    new ParallelRaceGroup(
                        new Command()::atPosition, () -> intakePivot.setSetpoint(Rotations.INTAKE_DOWN), intakePivot),
                        new WaitCommand(0.5)
                    ),
                    new ParallelCommandGroup(
                        new InstantCommand(intake::outakeCoral, intake),
                    )
                );
            }
        
            public Command placeCoral() {
                if (placeCoral == null) {
                synchronized (robotCommands.class) {
                    if (placeCoral == null) {
                        placeCoral = createPlaceCoral();
				}
			}
		}
		return placeCoral;
	}

    private volatile static Command scoreAlgea = null;
    
        private static Command createScoreAlgea() {
                    return new SequentialCommandGroup(
                        new ParallelRaceGroup(
                            new Command()::atPosition, () -> intakePivot.setSetpoint(Rotations.INTAKE_DOWN), algeaIntake),
                            new WaitCommand(0.5)
                        ),
                        new ParallelCommandGroup(
                            new InstantCommand(algeaIntake::outake, algeaIntake),
                        )
                    );
                }
            
                public Command scoreAlgea() {
                    if (scoreAlgea == null) {
                    synchronized (robotCommands.class) {
                        if (scoreAlgea == null) {
                            scoreAlgea = createScoreAlgea();
				}
			}
		}
        return scoreAlgea;
    }
	}