package com.team2813.subsystems;

import static com.team2813.Constants.OperatorConstants.OPERATOR_CONTROLLER;

import com.team2813.subsystems.climb.ClimbModule;
import com.team2813.subsystems.drive.DriveModule;
import com.team2813.subsystems.elevator.ElevatorControl;
import com.team2813.subsystems.elevator.ElevatorModule;
import com.team2813.subsystems.intake.IntakeModule;
import dagger.Module;
import dagger.Provides;
import java.util.function.DoubleSupplier;

@Module(
    includes = {
      ClimbModule.class,
      DriveModule.class,
      ElevatorModule.class,
      IntakeModule.class,
    })
class SubsystemsModule {

  @Provides
  @ElevatorControl
  static DoubleSupplier provideElevatorControl() {
    return () -> -OPERATOR_CONTROLLER.getRightY();
  }
}
