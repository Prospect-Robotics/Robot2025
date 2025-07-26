package com.team2813.subsystems;

import com.ctre.phoenix6.configs.SoftwareLimitSwitchConfigs;
import com.ctre.phoenix6.configs.TalonFXConfigurator;
import com.ctre.phoenix6.signals.NeutralModeValue;
import com.ctre.phoenix6.sim.ChassisReference;
import com.ctre.phoenix6.sim.TalonFXSimState;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.util.ConfigUtils;
import edu.wpi.first.math.system.plant.DCMotor;
import edu.wpi.first.math.system.plant.LinearSystemId;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Voltage;
import edu.wpi.first.wpilibj.DigitalInput;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.RobotController;
import edu.wpi.first.wpilibj.simulation.DCMotorSim;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

import static com.team2813.Constants.CLIMB_1;
import static com.team2813.Constants.CLIMB_2;

/** This is the Climb. Her name is Lisa. Please be kind to her and say hi. Have a nice day! */
public class Climb extends SubsystemBase implements AutoCloseable {

  final PIDMotor climbMotor1;
  final DigitalInput limitSwitch;

  public Climb(NetworkTableInstance networkTableInstance) {
    limitSwitch = new DigitalInput(0);
    TalonFXWrapper climbMotor1 = new TalonFXWrapper(CLIMB_1, InvertType.CLOCKWISE);
    climbMotor1.motor().getSimState().Orientation = ChassisReference.Clockwise_Positive;
    climbMotor1.motor().setNeutralMode(NeutralModeValue.Brake);
    TalonFXConfigurator cnf = climbMotor1.motor().getConfigurator();
    ConfigUtils.phoenix6Config(
        () ->
            cnf.apply(
                new SoftwareLimitSwitchConfigs()
                    .withForwardSoftLimitEnable(false)
                    .withForwardSoftLimitThreshold(0)
                    .withReverseSoftLimitEnable(false)
                    .withReverseSoftLimitThreshold(0)));
    this.climbMotor1 = climbMotor1;
    climbMotor1.addFollower(CLIMB_2, InvertType.FOLLOW_MASTER);
    // Logging
    NetworkTable networkTable = networkTableInstance.getTable("Climb");
    limitSwitchPressed = networkTable.getBooleanTopic("limit switch pressed").publish();
  }

  public void raise() {
    if (!limitSwitchPressed()) {
      climbMotor1.set(ControlMode.VOLTAGE, -8);
    }
  }

  public void lower() {
    climbMotor1.set(ControlMode.VOLTAGE, 8);
  }

  public void stop() {
    climbMotor1.set(ControlMode.VOLTAGE, 0);
  }

  public boolean limitSwitchPressed() {
    return limitSwitch.get();
  }

  private final BooleanPublisher limitSwitchPressed;

  @Override
  public void close() {
    limitSwitch.close();
  }

  @Override
  public void periodic() {
    limitSwitchPressed.set(limitSwitchPressed());
  }

  private static final double gearRatio = 1;

  private final DCMotorSim simModel = new DCMotorSim(
          LinearSystemId.createDCMotorSystem(
                  DCMotor.getKrakenX60(2), 0.001, gearRatio
          ),
          DCMotor.getKrakenX60(2)
  );

  @Override
  public void simulationPeriodic() {
    if (climbMotor1 instanceof TalonFXWrapper wrapper) {
      TalonFXSimState simState = wrapper.motor().getSimState();
      simState.setSupplyVoltage(RobotController.getBatteryVoltage());

      Voltage motorVoltage = simState.getMotorVoltageMeasure();

      simModel.setInputVoltage(motorVoltage.in(Units.Volts));
      simModel.update(0.020);

      simState.setRawRotorPosition(simModel.getAngularPosition().times(gearRatio));
      simState.setRotorVelocity(simModel.getAngularVelocity().times(gearRatio));
    }
  }
}
