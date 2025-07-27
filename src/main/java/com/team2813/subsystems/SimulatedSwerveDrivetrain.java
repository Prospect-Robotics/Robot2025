package com.team2813.subsystems;

import com.ctre.phoenix6.Utils;
import com.ctre.phoenix6.hardware.ParentDevice;
import com.ctre.phoenix6.hardware.traits.CommonTalon;
import com.ctre.phoenix6.swerve.SimSwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveModule;
import com.ctre.phoenix6.swerve.SwerveModuleConstants;
import com.ctre.phoenix6.swerve.SwerveRequest;
import edu.wpi.first.math.Matrix;
import edu.wpi.first.math.estimator.SwerveDrivePoseEstimator;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Rotation3d;
import edu.wpi.first.math.kinematics.SwerveDriveKinematics;
import edu.wpi.first.math.kinematics.SwerveModulePosition;
import edu.wpi.first.math.numbers.N1;
import edu.wpi.first.math.numbers.N3;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.wpilibj.RobotController;
import java.util.Arrays;

final class SimulatedSwerveDrivetrain<
        DriveMotorT extends CommonTalon,
        SteerMotorT extends CommonTalon,
        EncoderT extends ParentDevice>
    extends SimSwerveDrivetrain implements Drivetrain<DriveMotorT, SteerMotorT, EncoderT> {
  private final SwerveDrivetrain<DriveMotorT, SteerMotorT, EncoderT> drivetrain;
  private final StructPublisher<Pose2d> simCurrentPose;
  private final SwerveDrivePoseEstimator poseEstimator;
  private Pose2d simPose;
  private double lastSimUpdateSeconds;

  SimulatedSwerveDrivetrain(
      NetworkTable networkTable,
      SwerveDrivetrain<DriveMotorT, SteerMotorT, EncoderT> drivetrain,
      SwerveModuleConstants<?, ?, ?>... moduleConstants) {
    super(drivetrain.getModuleLocations(), drivetrain.getPigeon2().getSimState(), moduleConstants);
    this.drivetrain = drivetrain;
    simPose = drivetrain.getState().Pose;
    this.simCurrentPose = networkTable.getStructTopic("simulated pose", Pose2d.struct).publish();

    Rotation2d gyroAngle = drivetrain.getPigeon2().getRotation2d();
    SwerveModulePosition[] modulePositions = getModulePositions(drivetrain);
    poseEstimator =
        new SwerveDrivePoseEstimator(
            drivetrain.getKinematics(), gyroAngle, modulePositions, drivetrain.getState().Pose);
  }

  private static SwerveModulePosition[] getModulePositions(SwerveDrivetrain<?, ?, ?> drivetrain) {
    return Arrays.stream(drivetrain.getModules())
        .map(SwerveModule::getCachedPosition)
        .toArray(SwerveModulePosition[]::new);
  }

  public Pose2d getSimulatedPose() {
    return simPose;
  }

  @Override
  public Rotation3d getRotation3d() {
    return new Rotation3d(simPose.getRotation());
  }

  /**
   * Sets the pose, in the blue coordinate system.
   *
   * <p>This is called when the robot is being controlled by path planner. It assumes that the
   * passed-in pose is correct.
   */
  @Override
  public void resetPose(Pose2d pose) {
    drivetrain.resetPose(pose);
    simPose = pose;
    poseEstimator.resetPose(pose);
  }

  @Override
  public void addVisionMeasurement(
      Pose2d visionRobotPoseMeters,
      double timestampSeconds,
      Matrix<N3, N1> visionMeasurementStdDevs) {
    drivetrain.addVisionMeasurement(
        visionRobotPoseMeters, timestampSeconds, visionMeasurementStdDevs);
  }

  @Override
  public SwerveDrivetrain.SwerveDriveState getState() {
    return drivetrain.getState();
  }

  @Override
  public SwerveDriveKinematics getKinematics() {
    return drivetrain.getKinematics();
  }

  @Override
  public SwerveModule<DriveMotorT, SteerMotorT, EncoderT> getModule(int index) {
    return drivetrain.getModule(index);
  }

  @Override
  public void setControl(SwerveRequest request) {
    drivetrain.setControl(request);
  }

  @Override
  public void seedFieldCentric() {
    drivetrain.seedFieldCentric();
  }

  public void periodic() {
    double now = Utils.getCurrentTimeSeconds();
    if (lastSimUpdateSeconds == 0) {
      lastSimUpdateSeconds = now;
    }
    update(
        now - lastSimUpdateSeconds, RobotController.getBatteryVoltage(), drivetrain.getModules());
    lastSimUpdateSeconds = now;

    // TODO: Revisit this. Should be able to get data from the simulator...
    Rotation2d gyroAngle = drivetrain.getState().Pose.getRotation();
    SwerveModulePosition[] wheelPositions = getModulePositions(drivetrain);

    poseEstimator.update(gyroAngle, wheelPositions);
    simPose = poseEstimator.getEstimatedPosition();
    simCurrentPose.set(simPose);
  }

  @Override
  public void close() {}
}
