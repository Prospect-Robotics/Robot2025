package com.team2813.subsystems;

import java.util.function.Supplier;

import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.encoders.CancoderWrapper;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.subsystems.MotorSubsystem;

import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
/**
* This is the Intake Pivot. Her name is Sophie.
* Please be kind to her and say hi.
* Have a nice day!
*/
public class IntakePivot extends MotorSubsystem<IntakePivot.Position> {
    
    private static final Angle RESET_ANGLE = Units.Rotations.of(0);

    public IntakePivot() {
        super(new MotorSubsystemConfiguration(
            pivotMotor(),
            new CancoderWrapper(com.team2813.Constants.INTAKE_ENCODER))
            .acceptableError(0.5)
            .startingPosition(Position.INTAKE)
        );
        
    }

    @Deprecated
    public void resetPosition() {
        encoder.setPosition(RESET_ANGLE);
    }

    @Override
    protected void useOutput(double output, double setPoint) {
        super.useOutput(output, setPoint);
    }

    private static PIDMotor pivotMotor() {
        TalonFXWrapper pivotMotor = new TalonFXWrapper(com.team2813.Constants.INTAKE_PIVOT, InvertType.COUNTER_CLOCKWISE);
        pivotMotor.setNeutralMode(NeutralModeValue.Brake);

        return pivotMotor;
    }

    @Override
    public void periodic() {
        super.periodic();
        SmartDashboard.putNumber("Intake Pivot CANCoder Position", encoder.getPositionMeasure().in(Units.Rotations));
    }

    public static enum Position implements Supplier<Angle>{
        OUTTAKE(Units.Rotations.of(0.825439)), // TODO: NEEDS TUNING
        INTAKE(Units.Rotations.of(0)), // TODO: NEEDS TUNING
        ALGAE_BUMP(Units.Rotations.of(0)); // TODO: NEEDS TUNING

        Position(Angle pos) {
            this.pos = pos;
        }

        private final Angle pos;

        @Override
        public Angle get() {
            return pos;
        }
    }
}
