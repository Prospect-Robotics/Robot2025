package com.team2813.subsystems.drive;

import dagger.Binds;
import dagger.Module;

@Module
public interface DriveModule {

  @Binds
  Drive bindDrive(DriveSubsystem elevatorSubsystem);
}
