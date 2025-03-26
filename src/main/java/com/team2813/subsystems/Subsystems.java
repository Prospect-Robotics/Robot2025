package com.team2813.subsystems;

import com.team2813.subsystems.climb.Climb;
import com.team2813.subsystems.elevator.Elevator;
import dagger.BindsInstance;
import dagger.Component;
import edu.wpi.first.networktables.NetworkTableInstance;
import javax.inject.Singleton;

@Component(modules = {SubsystemsModule.class})
@Singleton
public interface Subsystems {
  Elevator elevator();

  Climb climb();

  @Component.Builder
  interface Builder {
    @BindsInstance
    Builder networkTableInstance(NetworkTableInstance instance);

    Subsystems build();
  }

  static Builder builder() {
    return DaggerSubsystems.builder();
  }
}
