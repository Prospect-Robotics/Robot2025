package com.team2813.subsystems;

import static com.team2813.Constants.ELEVATOR_1;
import static com.team2813.Constants.ELEVATOR_2;
import static edu.wpi.first.units.Units.Rotations;

import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.subsystems.MotorSubsystem;
import edu.wpi.first.math.MathUtil;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.DoublePublisher;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.units.measure.Current;
import java.util.function.Supplier;

/** This is the Elevator. His name is Pablo. Please be kind to him and say hi. Have a nice day! */
public class Elevator extends MotorSubsystem<Elevator.Position> {

  // You see a message written in blood on the wall...
  // It reads: "THIS CODE WILL LIKELY HAVE TO BE *MAJORLY* REFACTORED
  // AND TESTED AS IT WAS JUST COPIED FROM FENDER BENDER WITH MINIMUM CHANGES."
  // HERE BE DRAGONS.
  // Your companion notes: "...jeez... that is a lot of blood... couldn't they just leave a paper
  // taped to the wall, rather than raid a blood donation clinic."
  public Elevator(NetworkTableInstance networkTableInstance) {
    super(
        new MotorSubsystemConfiguration(getMotor())
            .controlMode(ControlMode.VOLTAGE)
            .acceptableError(1.7)
            .PID(0.2, 0.001, 0.001)
            .rotationUnit(Units.Radians));
    NetworkTable networkTable = networkTableInstance.getTable("Elevator");
    atPosition = networkTable.getBooleanTopic("at position").publish();
    position = networkTable.getDoubleTopic("position").publish();
  }

  private static TalonFXWrapper getMotor() {
    TalonFXWrapper wrapper = new TalonFXWrapper(ELEVATOR_1, InvertType.CLOCKWISE);
    wrapper.setNeutralMode(NeutralModeValue.Brake);
    wrapper.addFollower(ELEVATOR_2, InvertType.FOLLOW_MASTER);
    return wrapper;
  }

  @Override
  protected void useOutput(double output, double setpoint) {
    super.useOutput(MathUtil.clamp(output, -6, 6), setpoint);
  }

  @Override
  public Current getAppliedCurrent() {
    return motor.getAppliedCurrent();
  }

  public enum Position implements Supplier<Angle> {
    BOTTOM(-0.212500),
    TEST(10),
    TOP(16.358496);

    private final Angle position;

    Position(double position) {
      this.position = Rotations.of(position);
    }

    @Override
    public Angle get() {
      return position;
    }
  }

  private final BooleanPublisher atPosition;
  private final DoublePublisher position;

  @Override
  public void periodic() {
    super.periodic();
    atPosition.set(atPosition());
    position.set(getMeasurement());
  }
}
