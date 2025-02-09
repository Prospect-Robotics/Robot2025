package com.team2813.subsystems;

import java.util.function.Supplier;

import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.encoders.CancoderWrapper;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.subsystems.MotorSubsystem;

import edu.wpi.first.units.BaseUnits;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.util.sendable.Sendable;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

public class IntakePivot extends MotorSubsystem<IntakePivot.Rotations> {

    public IntakePivot() {
        super(new MotorSubsystemConfiguration(
            pivotMotor(),
            new CancoderWrapper(com.team2813.Constants.INTAKE_ENCODER))
            .acceptableError(0.5)
            .startingPosition(Rotations.INTAKE)
        );
        
    }

    public void resetPosition() {
        encoder.setPosition(Angle.ofBaseUnits(0, null));
    }
    @Override
    protected void useOutput(double output, double setPoint) {
        if (output < 0) {
            output -= -0.02;
        }
        super.useOutput(output, setPoint);
    }
    private static PIDMotor pivotMotor() {
        TalonFXWrapper pivotMotor = new TalonFXWrapper(com.team2813.Constants.INTAKE_PIVOT, InvertType.CLOCKWISE);
        pivotMotor.setNeutralMode(NeutralModeValue.Brake);

        return pivotMotor;
    }

    @Override
    public void periodic() {
        super.periodic();
        SmartDashboard.putData(
                "Intake Pivot CANCoder Position", 
                (Sendable) encoder.getPositionMeasure());
    }

    public static enum Rotations implements Supplier<Angle>{
        OUTTAKE(BaseUnits.AngleUnit.of(0.825439)), // TODO: NEEDS TUNING
        INTAKE(BaseUnits.AngleUnit.of(0)), // TODO: NEEDS TUNING
        ALGAE_BUMP(BaseUnits.AngleUnit.of(0)); // TODO: NEEDS TUNING

        Rotations(Angle pos) {
            this.pos = pos;
        }

        private final Angle pos;

        @Override
        public Angle get() {
            return pos;
        }
    }
}
