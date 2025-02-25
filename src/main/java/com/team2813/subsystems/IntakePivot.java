package com.team2813.subsystems;

import com.ctre.phoenix6.signals.NeutralModeValue;
import com.team2813.ShuffleboardTabs;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.PIDMotor;
import com.team2813.lib2813.control.encoders.CancoderWrapper;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import com.team2813.lib2813.subsystems.MotorSubsystem;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Angle;
import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

import java.util.function.Supplier;
/**
* This is the Intake Pivot. Her name is Sophie.
* Please be kind to her and say hi.
* Have a nice day!
*/
public class IntakePivot extends MotorSubsystem<IntakePivot.Rotations> {
  
    public IntakePivot(ShuffleboardTabs shuffleboard) {
        super(new MotorSubsystemConfiguration(
            pivotMotor(),
            new CancoderWrapper(com.team2813.Constants.INTAKE_ENCODER))
            .acceptableError(0.03)
            .startingPosition(Rotations.INTAKE)
            .rotationUnit(Units.Rotations)
            .controlMode(ControlMode.VOLTAGE)
            .PID(19.875, 0,0.4)
        );
        shuffleboard.getTab("Testing").addBoolean("Intakepivot pos", this::atPosition);
    }

    @Deprecated
    public void resetPosition() {
        encoder.setPosition(Rotations.HARD_STOP.get());
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

    public enum Rotations implements Supplier<Angle>{
        //0.754883
        //0.695801
        //0.448721
        //0.695801
        OUTTAKE(Units.Rotations.of(0.723389)), // TODO: NEEDS TUNING
        INTAKE(Units.Rotations.of(0.448721)), // TODO: NEEDSTUNING
        ALGAE_BUMP(Units.Rotations.of(1.108418)),
        HARD_STOP(Units.Rotations.of(0.438721)); // TODO: NEEDS TUNING

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
