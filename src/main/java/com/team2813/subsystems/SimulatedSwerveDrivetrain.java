package com.team2813.subsystems;

import com.ctre.phoenix6.Utils;
import com.ctre.phoenix6.swerve.SimSwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveModuleConstants;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.wpilibj.RobotController;

final class SimulatedSwerveDrivetrain extends SimSwerveDrivetrain {
  private final SwerveDrivetrain<?, ?, ?> drivetrain;
  private final StructPublisher<Pose2d> simCurrentPose;
  private double lastSimUpdateSeconds;

  SimulatedSwerveDrivetrain(
      NetworkTable networkTable,
      SwerveDrivetrain<?, ?, ?> drivetrain,
      SwerveModuleConstants<?, ?, ?>... moduleConstants) {
    super(drivetrain.getModuleLocations(), drivetrain.getPigeon2().getSimState(), moduleConstants);
    this.drivetrain = drivetrain;
    this.simCurrentPose = networkTable.getStructTopic("simulated pose", Pose2d.struct).publish();
  }

  public Pose2d getPose() {
    return drivetrain.getState().Pose;
  }

  public void periodic() {
    double now = Utils.getCurrentTimeSeconds();
    if (lastSimUpdateSeconds == 0) {
      lastSimUpdateSeconds = now;
    }
    update(
        now - lastSimUpdateSeconds, RobotController.getBatteryVoltage(), drivetrain.getModules());
    lastSimUpdateSeconds = now;

    simCurrentPose.set(getPose());
  }
}
