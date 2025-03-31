package com.team2813.subsystems;

import com.team2813.subsystems.climb.Climb;
import com.team2813.subsystems.elevator.Elevator;
import com.team2813.subsystems.intake.Intake;
import dagger.BindsInstance;
import dagger.Component;
import edu.wpi.first.networktables.NetworkTableInstance;
import javax.inject.Singleton;

@Component(modules = {SubsystemsModule.class})
@Singleton
public interface Subsystems {

  static Subsystems create(NetworkTableInstance instance) {
    return DaggerSubsystems.factory().createSubsystems(instance);
  }

  Elevator elevator();

  Climb climb();

  Intake intake();

  @Component.Factory
  interface Factory {

    Subsystems createSubsystems(@BindsInstance NetworkTableInstance instance);
  }
}
