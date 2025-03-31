package com.team2813.subsystems;

import com.team2813.subsystems.climb.Climb;
import com.team2813.subsystems.drive.Drive;
import com.team2813.subsystems.elevator.Elevator;
import com.team2813.subsystems.intake.Intake;
import com.team2813.subsystems.intake.IntakePivot;
import com.team2813.sysid.DropdownEntry;
import com.team2813.sysid.SubsystemRegistry;
import dagger.BindsInstance;
import dagger.Component;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj2.command.Subsystem;
import java.util.List;
import java.util.Map;
import javax.inject.Singleton;

@Component(modules = {SubsystemsModule.class})
@Singleton
public interface Subsystems {

  static Subsystems create(NetworkTableInstance instance) {
    return DaggerSubsystems.factory().createSubsystems(instance);
  }

  SubsystemRegistry registry();

  Drive drive();

  Elevator elevator();

  Climb climb();

  Intake intake();

  IntakePivot intakePivot();

  Map<Class<? extends Subsystem>, List<DropdownEntry>> sysIdRoutines();

  @Component.Factory
  interface Factory {

    Subsystems createSubsystems(@BindsInstance NetworkTableInstance instance);
  }
}
