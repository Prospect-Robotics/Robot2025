package com.team2813.subsystems;

import com.ctre.phoenix6.configs.Pigeon2Configuration;
import com.ctre.phoenix6.configs.Slot0Configs;
import com.ctre.phoenix6.configs.TalonFXConfiguration;
import com.ctre.phoenix6.hardware.TalonFX;
import com.ctre.phoenix6.hardware.core.CorePigeon2;
import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveDrivetrainConstants;
import com.ctre.phoenix6.swerve.SwerveModuleConstants;
import com.ctre.phoenix6.swerve.SwerveModuleConstants.ClosedLoopOutputType; // Might be inproper import.
import com.ctre.phoenix6.swerve.SwerveModuleConstants.SteerFeedbackType; // Might be inproper import.
import com.ctre.phoenix6.swerve.SwerveModuleConstantsFactory;

import edu.wpi.first.wpilibj2.command.SubsystemBase;

// Also add all the nescesary imports for constants and other things




public class Drive extends SubsystemBase {

    private final SwerveDrivetrain<TalonFX, TalonFX, CorePigeon2> drivetrain; // TODO: Create a drive train...


    // These variables below should be removed and replaced, they are here solely untill a drivetrain is created. 
    public static final int FRONT_RIGHT_STEER_ID = 1;
    public static final int FRONT_RIGHT_ENCODER_ID = 2;
    public static final int FRONT_RIGHT_DRIVE_ID = 3;
    // Back Right swerve module
    public static final int BACK_RIGHT_STEER_ID = 4;
    public static final int BACK_RIGHT_ENCODER_ID = 5;
    public static final int BACK_RIGHT_DRIVE_ID = 6;
    // Back Left swerve module
    public static final int BACK_LEFT_STEER_ID = 7;
    public static final int BACK_LEFT_ENCODER_ID = 8;
    public static final int BACK_LEFT_DRIVE_ID = 9;
    // Front Left swerve module
    public static final int FRONT_LEFT_STEER_ID = 10;
    public static final int FRONT_LEFT_ENCODER_ID = 11;
    public static final int FRONT_LEFT_DRIVE_ID = 12;
    public static final int PIGEON_ID = 13; // Usually in robot constants.

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

            drivetrain = new SwerveDrivetrain<TalonFX, TalonFX, CorePigeon2>(
                TalonFX::new, TalonFX::new, CorePigeon2::new, drivetrainConstants, frontLeft, frontRight, backLeft, backRight);
    }
}
