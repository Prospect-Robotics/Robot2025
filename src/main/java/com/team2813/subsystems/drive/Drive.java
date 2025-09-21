package com.team2813.subsystems.drive;

import com.team2813.sysid.SubsystemRegistry;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj2.command.Command;

public interface Drive extends AutoCloseable {

  static Drive create(NetworkTableInstance networkTableInstance, SubsystemRegistry registry) {
    DriveSubsystem drive = new DriveSubsystem(networkTableInstance);
    registry.addSubsystem(drive);
    return drive;
  }

  static boolean onRed() {
    return DriverStation.getAlliance()
        .map(alliance -> alliance == DriverStation.Alliance.Red)
        .orElse(false);
  }

  void configurePathPlanner();

  void setPose(Pose2d pose2d);

  @Override
  void close();

  Command enableSlowModeCommand(boolean enable);

  Command resetPoseCommand();
}
