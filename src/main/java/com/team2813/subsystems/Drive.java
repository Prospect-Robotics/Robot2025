package com.team2813.subsystems;

import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import com.ctre.phoenix6.configs.CANcoderConfiguration;
import com.ctre.phoenix6.configs.Slot0Configs;
import com.ctre.phoenix6.configs.TalonFXConfiguration;
import com.ctre.phoenix6.hardware.CANcoder;
import com.ctre.phoenix6.hardware.TalonFX;
import com.ctre.phoenix6.swerve.*;
import com.ctre.phoenix6.swerve.SwerveModuleConstants.ClosedLoopOutputType; // Might be improper import.
import com.ctre.phoenix6.swerve.SwerveModuleConstants.SteerFeedbackType; // Might be improper import.
import com.ctre.phoenix6.swerve.SwerveRequest.ApplyFieldSpeeds;
import com.ctre.phoenix6.swerve.SwerveRequest.FieldCentric;
import com.ctre.phoenix6.swerve.SwerveRequest.FieldCentricFacingAngle;

import static com.team2813.Constants.*;
import static edu.wpi.first.units.Units.Rotations;

import com.team2813.sysid.SwerveSysidRequest;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Translation2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.math.kinematics.SwerveModuleState;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructArrayPublisher;
import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.units.measure.AngularVelocity;
import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

import com.team2813.commands.RobotLocalization;
import com.team2813.commands.RobotLocalization.*;

/**
* This is the Drive. His name is Gary.
* Please be kind to him and say hi.
* Have a nice day!
*/
public class Drive extends SubsystemBase {
    public static final double MAX_VELOCITY = 6;
    public static final double MAX_ROTATION = Math.PI * 2;
    private final SwerveDrivetrain<TalonFX, TalonFX, CANcoder> drivetrain;
    private static final Translation2d poseOffset = new Translation2d(8.310213, 4.157313);

    static double frontDist = 0.330200;
    static double leftDist = 0.330200;
    // See above comment, do not delete past this line.

    public Drive() {
        
        double FLSteerOffset = 0.16796875;
        double FRSteerOffset = -0.355712890625;
        double BLSteerOffset = -0.367919921875;
        double BRSteerOffset = 0.371337890625;

        Slot0Configs steerGains = new Slot0Configs()
			      .withKP(46.619).withKI(0).withKD(3.0889)// Tune this.
			      .withKS(0.20951).withKV(2.4288).withKA(0.11804);// Tune this.

        // l: 0 h: 2.5
        Slot0Configs driveGains = new Slot0Configs()
			      .withKP(0).withKI(0).withKD(0)// Tune this.
			      .withKS(0).withKV(0).withKA(0);// Tune this.


        SwerveDrivetrainConstants drivetrainConstants = new SwerveDrivetrainConstants().withPigeon2Id(PIGEON_ID).withCANBusName("swerve"); // README: tweak to actual pigeon and CanBusName

        SwerveModuleConstantsFactory<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>  constantCreator = new SwerveModuleConstantsFactory<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>()
            // WARNING: TUNE ALL OF THESE THINGS!!!!!!
            .withDriveMotorGearRatio(6.75)
            .withSteerMotorGearRatio(150.0 / 7)
            .withWheelRadius(1.75)
            .withSlipCurrent(90)
            .withSteerMotorGains(steerGains)
            .withDriveMotorGains(driveGains)
            .withDriveMotorClosedLoopOutput(ClosedLoopOutputType.Voltage) // Tune this. (Important to tune values below)
            .withSteerMotorClosedLoopOutput(ClosedLoopOutputType.Voltage) // Tune this.
            .withSpeedAt12Volts(5) // Tune this.
            .withFeedbackSource(SteerFeedbackType.RemoteCANcoder) // Tune this.
            .withCouplingGearRatio(3.5);



        SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration> frontLeft =
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
        SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration> frontRight =
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
        SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration> backLeft =
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
        SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration> backRight =
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
            TalonFX::new, TalonFX::new, CANcoder::new, drivetrainConstants, frontLeft, frontRight, backLeft, backRight);
        for (int i = 0; i < 4; i++) {
            int temp = i;
            Shuffleboard.getTab("swerve").addDouble(String.format("Module [%d] position", i), () -> getPosition(temp));
        }
    }
    
    private double getPosition(int moduleId) {
        return drivetrain.getModule(moduleId).getEncoder().getAbsolutePosition().getValue().in(Rotations);
    }
    private final ApplyFieldSpeeds applyFieldSpeedsApplier = new ApplyFieldSpeeds(); // Looks stupid, but ApplyFieldSpeeds needs to be instanced.
    private final FieldCentricFacingAngle fieldCentricFacingAngleApplier = new FieldCentricFacingAngle(); // Same as above
    private final FieldCentric fieldCentricApplier = new FieldCentric().withDriveRequestType(SwerveModule.DriveRequestType.Velocity);

    public void drive(double xSpeed, double ySpeed, double rotation) {
        drivetrain.setControl(fieldCentricApplier
            .withVelocityX(xSpeed)
            .withVelocityY(ySpeed)
            .withRotationalRate(rotation)
            ); // Note: might not work, will need testing.
    }
    
    public void runSysIdRequest(SwerveSysidRequest request) {
        drivetrain.setControl(request);
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
        double x = this.drivetrain.getState().Pose.getX() + Drive.poseOffset.getX();
        double y = this.drivetrain.getState().Pose.getY() + Drive.poseOffset.getY();
        return new Pose2d(x,y,this.drivetrain.getState().Pose.getRotation());
    }
    public void resetPose() {
        this.drivetrain.seedFieldCentric();
    }
    public void setPose(Pose2d pose) {
        drivetrain.resetPose(pose);
    }
    public ChassisSpeeds getRobotRelativeSpeeds() {
        return this.drivetrain.getKinematics().toChassisSpeeds(this.drivetrain.getState().ModuleStates);
    }
    
    StructArrayPublisher<SwerveModuleState> expextedState =
            NetworkTableInstance.getDefault().getStructArrayTopic("expected state", SwerveModuleState.struct).publish();
    StructArrayPublisher<SwerveModuleState> actualState =
            NetworkTableInstance.getDefault().getStructArrayTopic("actual state", SwerveModuleState.struct).publish();
    StructPublisher<Pose2d> currentPose =
            NetworkTableInstance.getDefault().getStructTopic("current pose", Pose2d.struct).publish();
    
    @Override
    public void periodic() {
        expextedState.set(drivetrain.getState().ModuleTargets);
        actualState.set(drivetrain.getState().ModuleStates);
        currentPose.set(getPose());
        //RobotLocalization.getRobotPose();
        RobotLocalization.updateDashboard();
    }
}
