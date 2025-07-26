package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.Constants.OperatorConstants.OPERATOR_CONTROLLER;

import com.ctre.phoenix6.hardware.TalonFX;
import com.ctre.phoenix6.sim.ChassisReference;
import com.ctre.phoenix6.sim.TalonFXSimState;
import com.team2813.*;
import com.team2813.lib2813.control.Motor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.simulation.DIOSim;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import edu.wpi.first.wpilibj.simulation.PS4ControllerSim;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

@ExtendWith({CommandTesterExtension.class, IsolatedNetworkTablesExtension.class})
public class ClimbTest {
  private final ShuffleboardTabs shuffleboardTabs = new FakeShuffleboardTabs();

  private static final double TOLERANCE = 0.1;

  private TalonFXSimState getMotorSim(Motor motor) {
    assertThat(motor).isInstanceOf(TalonFXWrapper.class);
    TalonFXWrapper wrapper = (TalonFXWrapper) motor;
    TalonFX talon = wrapper.motor();
    return talon.getSimState();
  }

  @Test
  public void extend(NetworkTableInstance ntInstance, CommandTester commandTester) {
    try (RobotContainer robotContainer = new RobotContainer(shuffleboardTabs, ntInstance)) {
      // Setup
      Climb climb = robotContainer.climb;
      DIOSim dioSim = new DIOSim(climb.limitSwitch);
      TalonFXSimState simState = getMotorSim(climb.climbMotor1);
      dioSim.setValue(false);
      dioSim.setInitialized(true);
      simState.Orientation = ChassisReference.Clockwise_Positive;
      PS4ControllerSim controllerSim = new PS4ControllerSim(OPERATOR_CONTROLLER.getHID());
      DriverStationSim.setEnabled(true);
      DriverStationSim.setAutonomous(false);
      DriverStationSim.notifyNewData();
      // Lower intake
      IntakePivot intakePivot = robotContainer.intakePivot;
      intakePivot.setPosition(IntakePivot.Rotations.ALGAE_BUMP.get());

      assertThat(simState.getMotorVoltage()).isWithin(TOLERANCE).of(0);

      // Set POV Down
      controllerSim.setPOV(180);
      controllerSim.notifyNewData();
      // Advance time 2 seconds
      for (int i = 0; i < 2 / 0.02; i++) {
        CommandScheduler.getInstance().run();
      }
      assertThat(simState.getMotorVoltage()).isWithin(TOLERANCE).of(8);

      // Release POV Down
      controllerSim.setPOV(-1);
      controllerSim.notifyNewData();
      // Advance time 2 seconds
      for (int i = 0; i < 2 / 0.02; i++) {
        CommandScheduler.getInstance().run();
      }
      assertThat(simState.getMotorVoltage()).isWithin(TOLERANCE).of(0);
    }
  }

  @Test
  public void extendWithLimitSwitch(NetworkTableInstance ntInstance) {
    try (RobotContainer robotContainer = new RobotContainer(shuffleboardTabs, ntInstance)) {
      // Setup
      Climb climb = robotContainer.climb;
      DIOSim dioSim = new DIOSim(climb.limitSwitch);
      TalonFXSimState simState = getMotorSim(climb.climbMotor1);
      dioSim.setValue(true);
      dioSim.setInitialized(true);
      simState.Orientation = ChassisReference.Clockwise_Positive;
      PS4ControllerSim controllerSim = new PS4ControllerSim(OPERATOR_CONTROLLER.getHID());
      DriverStationSim.setEnabled(true);
      DriverStationSim.setAutonomous(false);
      DriverStationSim.notifyNewData();
      // Lower intake
      IntakePivot intakePivot = robotContainer.intakePivot;
      intakePivot.setPosition(IntakePivot.Rotations.ALGAE_BUMP.get());

      assertThat(simState.getMotorVoltage()).isWithin(TOLERANCE).of(0);

      // Set POV Down
      controllerSim.setPOV(180);
      controllerSim.notifyNewData();
      // Advance time 2 seconds
      for (int i = 0; i < 2 / 0.02; i++) {
        CommandScheduler.getInstance().run();
      }
      assertThat(simState.getMotorVoltage()).isWithin(TOLERANCE).of(8);

      // Release POV Down
      controllerSim.setPOV(-1);
      controllerSim.notifyNewData();
      // Advance time 2 seconds
      for (int i = 0; i < 2 / 0.02; i++) {
        CommandScheduler.getInstance().run();
      }
      assertThat(simState.getMotorVoltage()).isWithin(TOLERANCE).of(0);
    }
  }
}
