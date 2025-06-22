package com.team2813;

import com.team2813.subsystems.SubsystemsModule;
import dagger.BindsInstance;
import dagger.Component;
import edu.wpi.first.networktables.NetworkTableInstance;
import javax.inject.Singleton;

@Component(modules = {SubsystemsModule.class})
@Singleton
public interface RobotContainerComponent {

  RobotContainer robotContainer();

  @Component.Factory
  interface Factory {

    RobotContainerComponent createContainer(
        @BindsInstance NetworkTableInstance ntInstance, @BindsInstance ShuffleboardTabs sbInstance);
  }
}
