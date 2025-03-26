package com.team2813.subsystems.elevator;

import dagger.Binds;
import dagger.Module;

@Module
public interface ElevatorModule {

  @Binds
  Elevator bindElevator(ElevatorSubsystem elevatorSubsystem);
}
