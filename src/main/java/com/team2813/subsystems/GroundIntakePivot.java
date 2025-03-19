package com.team2813.subsystems;

import static com.team2813.Constants.GROUND_INTAKE_PIVOT;
import static edu.wpi.first.units.Units.Radians;
import static edu.wpi.first.units.Units.Rotations;

import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.subsystems.MotorSubsystem;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.DoublePublisher;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Angle;
import java.util.function.Supplier;

// TODO: TUNE ALL THE THINGS!!1! AND ALSO SET UP THE POSITIONS ENUM PROPERLY.

public class GroundIntakePivot extends MotorSubsystem<GroundIntakePivot.Positions> {

  private final DoublePublisher groundIntakePivot;
  private final BooleanPublisher atPosition;

  public GroundIntakePivot(NetworkTableInstance networkTableInstance) {
    super(
        new MotorSubsystemConfiguration(pivotMotor())
            .controlMode(ControlMode.VOLTAGE)
            .PID(0, 0, 0) // TODO: Configure the PID. Maybe I should try this on my own.
            .rotationUnit(Radians)
            .acceptableError(1.0) // TODO: Tune this as well.
        );

    NetworkTable networkTable = networkTableInstance.getTable("GroundIntakePivot");
    groundIntakePivot = networkTable.getDoubleTopic("position").publish();
    atPosition = networkTable.getBooleanTopic("at position").publish();
  }

  private static PIDMotor pivotMotor() {
    TalonFXWrapper pivotMotor =
        new TalonFXWrapper(com.team2813.Constants.GROUND_INTAKE_PIVOT, InvertType.COUNTER_CLOCKWISE);
    pivotMotor.setNeutralMode(NeutralModeValue.Brake);

    return pivotMotor;
  }

  @Override
  public void periodic() {
    super.periodic();
    groundIntakePivot.set(getPositionMeasure().in(Units.Rotations));
    atPosition.set(atPosition());
  }

  public enum Positions implements Supplier<Angle> {
    BOTTOM(0.0), // FIXME: SET THESE UP TO THE PROPER POSITIONS.
    TEST(5),
    TOP(0.0); // FIXME: SET THESE UP TO THE PROPER POSITIONS.

    private final Angle position;

    Positions(double position) {
      this.position = Rotations.of(position);
    }

    @Override
    public Angle get() {
      return position;
    }
  }
}
