package com.team2813.subsystems.drive;

import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Subsystem;

public interface Drive extends AutoCloseable {

  static boolean onRed() {
    return DriverStation.getAlliance()
        .map(alliance -> alliance == DriverStation.Alliance.Red)
        .orElse(false);
  }

  RobotLocalization localization();

  Subsystem asSubsystem();

  Pose2d getPose();

  void setPose(Pose2d pose2d);

  ChassisSpeeds getRobotRelativeSpeeds();

  /** Handles autonomous driving. */
  void drive(ChassisSpeeds chassisSpeeds);

  @Override
  void close();

  Command enableSlowModeCommand(boolean enable);

  Command resetPoseCommand();

  Command rightAutoAlignCommand();

  Command leftAutoAlignCommand();
}
