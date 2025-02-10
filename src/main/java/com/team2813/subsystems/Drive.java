package com.team2813.subsystems;

import com.ctre.phoenix6.configs.Pigeon2Configuration;
import com.ctre.phoenix6.configs.Slot0Configs;
import com.ctre.phoenix6.configs.TalonFXConfiguration;
import com.ctre.phoenix6.hardware.TalonFX;
import com.ctre.phoenix6.hardware.core.CorePigeon2;
import com.ctre.phoenix6.swerve.SwerveRequest.FieldCentricFacingAngle;
import com.ctre.phoenix6.swerve.SwerveRequest.FieldCentric;
import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveDrivetrainConstants;
import com.ctre.phoenix6.swerve.SwerveModuleConstants;
import com.ctre.phoenix6.swerve.SwerveModuleConstants.ClosedLoopOutputType; // Might be inproper import.
import com.ctre.phoenix6.swerve.SwerveModuleConstants.SteerFeedbackType; // Might be inproper import.
import com.ctre.phoenix6.swerve.SwerveRequest.ApplyFieldSpeeds;
import com.ctre.phoenix6.swerve.SwerveModuleConstantsFactory;

import static com.team2813.Constants.*;

import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.units.measure.AngularVelocity;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

// Also add all the nescesary imports for constants and other things




public class Drive extends SubsystemBase {

    private final SwerveDrivetrain<TalonFX, TalonFX, CorePigeon2> drivetrain;

	// This is Bartholomew Jaquavious DeMarcus Jr Jr the 3rd. He is the Climb subsystem of the robot.
	// Treat him with respect.
    

    static double frontDist = 0;
    static double leftDist = 0;
    // See above comment, do not delete past this line.

    public Drive() {
        
        double FLSteerOffset = 0.0;
        double FRSteerOffset = 0.0;
        double BLSteerOffset = 0.0;
        double BRSteerOffset = 0.0;

        Slot0Configs steerGains = new Slot0Configs()
			.withKP(50).withKI(0).withKD(0.2)// Tune this.
			.withKS(0).withKV(1.5).withKA(0);// Tune this.

        Slot0Configs driveGains = new Slot0Configs()
			.withKP(2.5).withKI(0).withKD(0)// Tune this.
			.withKS(0).withKV(0).withKA(0);// Tune this.


        SwerveDrivetrainConstants drivetrainConstants = new SwerveDrivetrainConstants().withPigeon2Id(PIGEON_ID).withCANBusName("rio"); // README: tweak to actual pigeon and CanBusName

        SwerveModuleConstantsFactory<TalonFXConfiguration, TalonFXConfiguration, Pigeon2Configuration>  constantCreator = new SwerveModuleConstantsFactory<TalonFXConfiguration, TalonFXConfiguration, Pigeon2Configuration>()
            // WARNING: TUNE ALL OF THESE THINGS!!!!!!
            .withDriveMotorGearRatio(6.75)
            .withSteerMotorGearRatio(150.0 / 7)
            .withWheelRadius(1.75)
            .withSlipCurrent(90)
            .withSteerMotorGains(steerGains)
            .withDriveMotorGains(driveGains)
            .withDriveMotorClosedLoopOutput(ClosedLoopOutputType.TorqueCurrentFOC) // Tune this. (Important to tune ↓)
            .withSteerMotorClosedLoopOutput(ClosedLoopOutputType.Voltage) // Tune this.
            .withSpeedAt12Volts(5) // Tune this.
            .withFeedbackSource(SteerFeedbackType.FusedCANcoder) // Tune this.
            .withCouplingGearRatio(3.5);



            SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, Pigeon2Configuration> frontLeft =
                constantCreator.createModuleConstants(
                    FRONT_LEFT_STEER_ID,
                    FRONT_LEFT_DRIVE_ID,
                    FRONT_LEFT_ENCODER_ID,
                    FLSteerOffset,
                    frontDist,
                    leftDist,
                    true, // May need to change later.
                    true, // May need to change later.
                    false); // May need to change later.
            SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, Pigeon2Configuration> frontRight =
                constantCreator.createModuleConstants(
                    FRONT_RIGHT_STEER_ID,
                    FRONT_RIGHT_DRIVE_ID,
                    FRONT_RIGHT_ENCODER_ID,
                    FRSteerOffset,
                    frontDist,
                    -leftDist,
                    true, // May need to change later.
                    true, // May need to change later.
                    false); // May need to change later.
            SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, Pigeon2Configuration> backLeft =
                constantCreator.createModuleConstants(
                    BACK_LEFT_STEER_ID,
                    BACK_LEFT_DRIVE_ID,
                    BACK_LEFT_ENCODER_ID,
                    BLSteerOffset,
                    -frontDist,
                    leftDist,
                    true, // May need to change later.
                    true, // May need to change later.
                    false); // May need to change later.
            SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, Pigeon2Configuration> backRight =
                constantCreator.createModuleConstants(
                    BACK_RIGHT_STEER_ID,
                    BACK_RIGHT_DRIVE_ID,
                    BACK_RIGHT_ENCODER_ID,
                    BRSteerOffset,
                    -frontDist,
                    -leftDist,
                    true, // May need to change later.
                    true, // May need to change later.
                    false); // May need to change later.

            drivetrain = new SwerveDrivetrain<>(
                TalonFX::new, TalonFX::new, CorePigeon2::new, drivetrainConstants, frontLeft, frontRight, backLeft, backRight);
    }


    private final ApplyFieldSpeeds applyFieldSpeedsApplier = new ApplyFieldSpeeds(); // Looks stupid, but ApplyFieldSpeeds needs to be instanced.
    private final FieldCentricFacingAngle fieldCentricFacingAngleApplier = new FieldCentricFacingAngle(); // Same as above
    private final FieldCentric fieldCentricApplier = new FieldCentric();

    public void drive(double xSpeed, double ySpeed, double rotation) {
        drivetrain.setControl(fieldCentricApplier
            .withVelocityX(xSpeed)
            .withVelocityY(ySpeed)
            .withRotationalRate(rotation)
            ); // Note: might not work, will need testing.
    }
    
    public void drive(ChassisSpeeds demand) {
        drivetrain.setControl(applyFieldSpeedsApplier.withSpeeds(demand));
    }

    public void turnToFace(Rotation2d rotation) {
        drivetrain.setControl(fieldCentricFacingAngleApplier.withTargetDirection(rotation));
    }

    /**
     * Sets the rotation velocity of the robot
     * @param rotationRate rotation rate in radians per second
     * @deprecated unsafe; use {@link #setRotationVelocity(AngularVelocity)}, and specify the unit you are using
     */
    @Deprecated
    public void setRotationVelocityDouble(double rotationRate) { // Radians per second
        drivetrain.setControl(fieldCentricApplier.withRotationalRate(rotationRate));
    }

    public void setRotationVelocity(AngularVelocity rotationRate) { // Uses WPIlib units library.
        drivetrain.setControl(fieldCentricApplier.withRotationalRate(rotationRate));
    }
    public Pose2d getPose() {
        return null;
        // insert robot getPose here
    }
    public void resetPose() {
        // insert robot odometry reset here
    }
    public ChassisSpeeds getCurrentSpeeds() {
        return null;
        // insert robot getSpeeds here
    }
}
