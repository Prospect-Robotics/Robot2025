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
import edu.wpi.first.math.controller.PIDController;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.units.Units;

import java.util.function.Supplier;

public class Elevator extends MotorSubsystem<Elevator.Position> {

    // You see a message written in blood on the wall...
    // It reads: "THIS CODE WILL LIKELY HAVE TO BE *MAJORLY* REFACTORED 
    // AND TESTED AS IT WAS JUST COPIED FROM FENDER BENDER WITH MINIMUM CHANGES."
    // HERE BE DRAGONS.
    // Your companion notes: "...jeez... that is a lot of blood... couldn't they just leave a paper taped to the wall, rather than raid a blood donation clinic."
    // Another message appears...
    // It reads: "This is the Elevator. His name is Pablo. Treat him with respect."
    public Elevator() {
        super(
                new MotorSubsystemConfiguration(
                        getMotor())
                        .controlMode(ControlMode.VOLTAGE)
                        .acceptableError(2.5)
                        .controller(getPIDController())
                        .rotationUnit(Units.Radians));
        ((TalonFXWrapper) motor).addFollower(ELEVATOR_2, "swerve", InvertType.OPPOSE_MASTER); // TODO: See if the motors need to be reversed.
    }
    
    private static TalonFXWrapper getMotor() {
        TalonFXWrapper wrapper = new TalonFXWrapper(ELEVATOR_1, "swerve", InvertType.COUNTER_CLOCKWISE); // TODO: See if the motors need to be reversed.
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
        // TODO: Once we have a working elevator, tune this.
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
