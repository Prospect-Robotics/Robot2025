package com.team2813.subsystems.intake;

import dagger.Binds;
import dagger.Module;

@Module
public interface IntakeModule {

  @Binds
  Intake bindIntake(IntakeSubsystem intakeSubsystem);

  @Binds
  IntakePivot bindIntakePivot(IntakePivotSubsystem intakePivotSubsystem);
}
