package com.team2813.subsystems;

import com.team2813.ShuffleboardTabs;
import com.team2813.subsystems.climb.Climb;
import com.team2813.subsystems.drive.Drive;
import com.team2813.subsystems.elevator.Elevator;
import com.team2813.subsystems.intake.Intake;
import com.team2813.subsystems.intake.IntakePivot;
import com.team2813.sysid.SysIdRoutineSelector;
import dagger.BindsInstance;
import dagger.Component;
import edu.wpi.first.networktables.NetworkTableInstance;
import javax.inject.Singleton;

@Component(modules = {SubsystemsModule.class})
@Singleton
public interface Subsystems {

  static Subsystems create(NetworkTableInstance ntInstance, ShuffleboardTabs sbInstance) {
    return DaggerSubsystems.factory().createSubsystems(ntInstance, sbInstance);
  }

  Drive drive();

  Elevator elevator();

  Climb climb();

  Intake intake();

  IntakePivot intakePivot();

  SysIdRoutineSelector sysIdSelector();

  @Component.Factory
  interface Factory {

    Subsystems createSubsystems(
        @BindsInstance NetworkTableInstance ntInstance, @BindsInstance ShuffleboardTabs sbInstance);
  }
}
