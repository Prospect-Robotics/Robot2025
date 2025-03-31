package com.team2813.subsystems.drive;

import com.team2813.sysid.SubsystemRegistry;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Subsystem;

public interface Drive extends AutoCloseable {

  static Drive create(NetworkTableInstance networkTableInstance, SubsystemRegistry registry) {
    RobotLocalization localization = new RobotLocalization(networkTableInstance);
    DriveSubsystem drive = new DriveSubsystem(networkTableInstance, localization);
    registry.addSubsystem(drive);
    return drive;
  }

  static boolean onRed() {
    return DriverStation.getAlliance()
        .map(alliance -> alliance == DriverStation.Alliance.Red)
        .orElse(false);
  }

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
