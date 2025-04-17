package com.team2813.subsystems;

import com.ctre.phoenix6.Utils;
import com.ctre.phoenix6.swerve.SimSwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveModule;
import com.ctre.phoenix6.swerve.SwerveModuleConstants;
import edu.wpi.first.math.estimator.SwerveDrivePoseEstimator;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.kinematics.SwerveModulePosition;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.wpilibj.RobotController;
import java.util.Arrays;

final class SimulatedSwerveDrivetrain extends SimSwerveDrivetrain {
  private final SwerveDrivetrain<?, ?, ?> realDrivetrain;
  private final StructPublisher<Pose2d> simCurrentPosePublisher;
  private final SwerveDrivePoseEstimator nonCorrectedPoseEstimator;
  private Pose2d simPose;
  private double lastSimUpdateSeconds;

  SimulatedSwerveDrivetrain(
      NetworkTable networkTable,
      SwerveDrivetrain<?, ?, ?> drivetrain,
      SwerveModuleConstants<?, ?, ?>... moduleConstants) {
    super(drivetrain.getModuleLocations(), drivetrain.getPigeon2().getSimState(), moduleConstants);
    this.realDrivetrain = drivetrain;
    simPose = drivetrain.getState().Pose;
    this.simCurrentPosePublisher =
        networkTable.getStructTopic("simulated pose", Pose2d.struct).publish();

    Rotation2d gyroAngle = drivetrain.getPigeon2().getRotation2d();
    SwerveModulePosition[] modulePositions = getModulePositions(drivetrain);
    nonCorrectedPoseEstimator =
        new SwerveDrivePoseEstimator(
            drivetrain.getKinematics(), gyroAngle, modulePositions, drivetrain.getState().Pose);
  }

  private static SwerveModulePosition[] getModulePositions(SwerveDrivetrain<?, ?, ?> drivetrain) {
    return Arrays.stream(drivetrain.getModules())
        .map(SwerveModule::getCachedPosition)
        .toArray(SwerveModulePosition[]::new);
  }

  /**
   * Sets the pose, in the blue coordinate system.
   *
   * <p>This is called when the robot is being controlled by path planner. It assumes that the
   * passed-in pose is correct.
   */
  public void resetPose(Pose2d pose) {
    simPose = pose;
    nonCorrectedPoseEstimator.resetPose(pose);
  }

  /** Gets the robot position, excluding corrections from vision. ( */
  public Pose2d getPose() {
    return simPose;
  }

  public void periodic() {
    double now = Utils.getCurrentTimeSeconds();
    if (lastSimUpdateSeconds == 0) {
      lastSimUpdateSeconds = now;
    }
    update(
        now - lastSimUpdateSeconds,
        RobotController.getBatteryVoltage(),
        realDrivetrain.getModules());
    lastSimUpdateSeconds = now;

    Rotation2d gyroAngle = realDrivetrain.getState().Pose.getRotation();
    SwerveModulePosition[] wheelPositions = getModulePositions(realDrivetrain);

    nonCorrectedPoseEstimator.update(gyroAngle, wheelPositions);
    simPose = nonCorrectedPoseEstimator.getEstimatedPosition();
    simCurrentPosePublisher.set(simPose);
  }
}
