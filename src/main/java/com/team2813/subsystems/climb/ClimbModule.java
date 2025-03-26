package com.team2813.subsystems.climb;

import dagger.Binds;
import dagger.Module;

@Module
public interface ClimbModule {

  @Binds
  Climb bindElevator(ClimbSubsystem climbSubsystem);
}
