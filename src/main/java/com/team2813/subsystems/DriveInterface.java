package com.team2813.subsystems;

import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.wpilibj2.command.Subsystem;

/** A bare minimum Drive interface to allow MapleSim's drive to work. */
public interface DriveInterface extends Subsystem, AutoCloseable {

  //    void addVisionMeasurement(BotPoseEstimate estimate);

  void drive(ChassisSpeeds demand);

  void drive(double xSpeed, double ySpeed, double rotation);

  Pose2d getPose();

  void resetPose();

  void setPose(Pose2d pose);

  ChassisSpeeds getRobotRelativeSpeeds();

  void enableSlowMode(boolean enable);

  void close();
}
