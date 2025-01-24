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
import edu.wpi.first.math.controller.ElevatorFeedforward;
import edu.wpi.first.math.controller.PIDController;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.units.Measure;
import edu.wpi.first.units.Units;

import java.util.function.Supplier;

public class Elevator extends MotorSubsystem<Elevator.Position> {

    public Elevator() {
        super(
                new MotorSubsystemConfiguration(
                        getMotor())
                        .controlMode(ControlMode.VOLTAGE)
                        .acceptableError(2.5)
                        .controller(getPIDController())
                        .rotationUnit(Units.Radians));
        ((TalonFXWrapper) motor).addFollower(ELEVATOR_2, "swerve", InvertType.OPPOSE_MASTER);
    }
    
    private static TalonFXWrapper getMotor() {
        TalonFXWrapper wrapper = new TalonFXWrapper(ELEVATOR_1, "swerve", InvertType.COUNTER_CLOCKWISE);
        wrapper.setNeutralMode(NeutralModeValue.Brake);
        return wrapper;
    }
    
    private static PIDController getPIDController() {
        PIDController controller = new PIDController(0.051524, 0.01, 0);
        controller.setTolerance(1.5, 23.784);
        return controller;
    }
    
    @Override
    protected void useOutput(double output, double setpoint) {
        if (output > 0) {
            output += 0.40798;
        }
        super.useOutput(MathUtil.clamp(output, -7, 7), setpoint);
    }

    public enum Position implements Supplier<Angle> {
        BOTTOM(0.283203),
        TEST(10),
        TOP(19.644043);

        private final Angle position;

        Position(double position) {
            this.position = Rotations.of(position);
        }

        @Override
        public Angle get() {
            return position;
        }
    }
}