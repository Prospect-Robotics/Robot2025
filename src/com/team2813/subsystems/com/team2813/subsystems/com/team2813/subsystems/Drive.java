package com.team2813.subsystems;

import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveDrivetrainConstants;

// Also add all the nescesary imports for constants and other things




public class Drive extends SubsystemBase {

    SwerveDrivetrain drivetrain;


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
    // See above comment, do not delete past this line.

    Drive() {
        
        double FLSteerOffset = 0.0;
        double FRSteerOffset = 0.0;
        double BLSteerOffset = 0.0;
        double BRSteerOffset = 0.0;


        SwerveDrivetrainConstants drivetrainConstants = new SwerveDrivetrainConstants().withPigeon2Id(PIGEON_ID).withCANbusName("rio"); // README: tweak to actual pigeon and CanBusName

        SwerveDrivetrainConstants constantCreator = new SwerveDrivetrainConstants()
            // WARNING: TUNE ALL OF THESE THINGS!!!!!!
            .withDriveMotorGearRatio(6.75)
            .withSteerMotorGearRatio(150.0 / 7)
            .withWheelRadius(1.75)
            .withSlipCurrent(90)
            .withSteerMotorGains(steerGains)
            .withDriveMotorGains(driveGains)
            .withDriveMotorClosedLoopOutput(ClosedLoopOutputType.TorqueCurrentFOC) // Tune this. (Important to tune ↓)
            .withSteerMotorClosedLoopOutput(ClosedLoopOutputType.Voltage) // Tune this.
            .withSpeedAt12VoltsMps(5) // Tune this.
            .withFeedbackSource(SteerFeedbackType.FusedCANcoder) // Tune this.
            .withCouplingGearRatio(3.5)
            .withSteerMotorInverted(true);


            SwerveModuleConstants frontLeft =
            constantCreator.createModuleConstants(
                FRONT_LEFT_STEER_ID,
                FRONT_LEFT_DRIVE_ID,
                FRONT_LEFT_ENCODER_ID,
                FLSteerOffset,
                frontDist,
                leftDist,
                true);
        SwerveModuleConstants frontRight =
            constantCreator.createModuleConstants(
                FRONT_RIGHT_STEER_ID,
                FRONT_RIGHT_DRIVE_ID,
                FRONT_RIGHT_ENCODER_ID,
                FRSteerOffset,
                frontDist,
                -leftDist,
                true);
        SwerveModuleConstants backLeft =
            constantCreator.createModuleConstants(
                BACK_LEFT_STEER_ID,
                BACK_LEFT_DRIVE_ID,
                BACK_LEFT_ENCODER_ID,
                BLSteerOffset,
                -frontDist,
                leftDist,
                true);
        SwerveModuleConstants backRight =
            constantCreator.createModuleConstants(
                BACK_RIGHT_STEER_ID,
                BACK_RIGHT_DRIVE_ID,
                BACK_RIGHT_ENCODER_ID,
                BRSteerOffset,
                -frontDist,
                -leftDist,
                true);

        // .withPigeon2Id(kPigeonId)
        // .withPigeon2Configs(pigeonConfigs);

        // private static final SwerveModuleConstantsFactory<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration> ConstantCreator =
        //     new SwerveModuleConstantsFactory<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>()
        //         .withDriveMotorGearRatio(kDriveGearRatio)
        //         .withSteerMotorGearRatio(kSteerGearRatio)
        //         .withCouplingGearRatio(kCoupleRatio)
        //         .withWheelRadius(kWheelRadius)
        //         .withSteerMotorGains(steerGains)
        //         .withDriveMotorGains(driveGains)
        //         .withSteerMotorClosedLoopOutput(kSteerClosedLoopOutput)
        //         .withDriveMotorClosedLoopOutput(kDriveClosedLoopOutput)
        //         .withSlipCurrent(kSlipCurrent)
        //         .withSpeedAt12Volts(kSpeedAt12Volts)
        //         .withDriveMotorType(kDriveMotorType)
        //         .withSteerMotorType(kSteerMotorType)
        //         .withFeedbackSource(kSteerFeedbackType)
        //         .withDriveMotorInitialConfigs(driveInitialConfigs)
    }

    // TODO: Implement

}
