package com.team2813.util;

import java.util.Optional;

import com.team2813.RobotContainer;
import com.team2813.subsystems.Drive;
import com.team2813.util.LimelightValues;
import com.team2813.util.LimelightValues.LedState;

import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

public class Limelight extends SubsystemBase {

      private final LimelightValues values = new LimelightValues();

    private static final double MOUNT_ANGLE = 0;    //degrees
    private static final double MOUNT_HEIGHT = 0;    //inches
    private static final double TARGET_HEIGHT = 0;    //inches

    private Limelight() {
          
    }

    public static final Limelight instance = new Limelight();

    public static Limelight getInstance() {
        return instance;
    }

    public LimelightValues getValues() {
          return values;
      }
  
      public void setLights(boolean enable) {
          values.setLedState(enable ? LedState.DEFAULT : LedState.OFF);
      }
  
      public void setStream(int stream) {
          values.getStream().setNumber(stream);
      }
  
      public void setPipeline(int pipelineIndex) {
          values.getPipelineIndexEntry().setNumber(pipelineIndex);
      }

    /**
     * Gets the position on the playing field using build-in robot localization
     */
       //Do the output how you want to. (but make it make sense)
      public Optional<Pose2d> getPosition() {
          if (values.hasTargets()) {
              Double[] location = values.getFieldLocation();
              location[0] = location[0] + 0.0;
              location[1] = location[1] + 0.30506;
              Pose2d pose = new Pose2d(location[0], location[1], Rotation2d.fromDegrees(location[5]));
              return Optional.of(pose);
          } else {
              return Optional.empty();
          }
      }
  
      @Override
      public void periodic() {
          getPosition().ifPresent((Pose2d position) -> {
              SmartDashboard.putNumber("x position (meters):", position.getX());
              SmartDashboard.putNumber("y position (meters):", position.getY());
              SmartDashboard.putNumber("robot heading (degrees):", position.getRotation().getDegrees());
              if (!DriverStation.isAutonomousEnabled()) {
                     //Possibly update the driver station?
              }
          });
          SmartDashboard.putBoolean("Valid apriltag", values.hasTargets());
          SmartDashboard.putNumber("Id of primary AprilTag", values.primaryApriltag());
  
          SmartDashboard.putNumber("LED Mode", values.getLedStateNum());
      }
}
