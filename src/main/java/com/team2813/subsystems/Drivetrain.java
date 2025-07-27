package com.team2813.subsystems;

import com.ctre.phoenix6.Utils;
import com.ctre.phoenix6.hardware.ParentDevice;
import com.ctre.phoenix6.hardware.traits.CommonTalon;
import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveModule;
import com.ctre.phoenix6.swerve.SwerveRequest;
import edu.wpi.first.math.Matrix;
import edu.wpi.first.math.estimator.SwerveDrivePoseEstimator;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation3d;
import edu.wpi.first.math.kinematics.SwerveDriveKinematics;
import edu.wpi.first.math.numbers.N1;
import edu.wpi.first.math.numbers.N3;

interface Drivetrain<
    DriveMotorT extends CommonTalon,
    SteerMotorT extends CommonTalon,
    EncoderT extends ParentDevice> {

  /**
   * Gets the current state of the swerve drivetrain. This includes information such as the pose
   * estimate, module states, and chassis speeds.
   *
   * @return Current state of the drivetrain
   */
  SwerveDrivetrain.SwerveDriveState getState();

  /**
   * Gets the current orientation of the robot as a {@link Rotation3d} from the Pigeon 2 quaternion
   * values.
   *
   * @return The robot orientation as a {@link Rotation3d}
   */
  Rotation3d getRotation3d();

  /**
   * Gets a reference to the kinematics used for the drivetrain.
   *
   * @return Swerve kinematics
   */
  SwerveDriveKinematics getKinematics();

  /**
   * Get a reference to the module at the specified index. The index corresponds to the module
   * described in the constructor.
   *
   * @param index Which module to get
   * @return Reference to SwerveModule
   */
  SwerveModule<DriveMotorT, SteerMotorT, EncoderT> getModule(int index);

  /**
   * Applies the specified control request to this swerve drivetrain.
   *
   * @param request Request to apply
   */
  void setControl(SwerveRequest request);

  /**
   * Resets the rotation of the robot pose to 0 from the {@link
   * SwerveRequest.ForwardPerspectiveValue#OperatorPerspective} perspective. This makes the current
   * orientation of the robot X forward for field-centric maneuvers.
   */
  void seedFieldCentric();

  /**
   * Resets the pose of the robot. The pose should be from the {@link
   * SwerveRequest.ForwardPerspectiveValue#BlueAlliance} perspective.
   *
   * @param pose Pose to make the current pose
   */
  void resetPose(Pose2d pose);

  /**
   * Adds a vision measurement to the Kalman Filter. This will correct the odometry pose estimate
   * while still accounting for measurement noise.
   *
   * <p>This method can be called as infrequently as you want, as long as you are calling {@link
   * SwerveDrivePoseEstimator#update} every loop.
   *
   * <p>To promote stability of the pose estimate and make it robust to bad vision data, we
   * recommend only adding vision measurements that are already within one meter or so of the
   * current pose estimate.
   *
   * <p>Note that the vision measurement standard deviations passed into this method will continue
   * to apply to future measurements until a subsequent call to {@link
   * SwerveDrivePoseEstimator#setVisionMeasurementStdDevs(Matrix)} or this method.
   *
   * @param visionRobotPoseMeters The pose of the robot as measured by the vision camera.
   * @param timestampSeconds The timestamp of the vision measurement in seconds. Note that you must
   *     use a timestamp with an epoch since system startup (i.e., the epoch of this timestamp is
   *     the same epoch as {@link Utils#getCurrentTimeSeconds}). This means that you should use
   *     {@link Utils#getCurrentTimeSeconds} as your time source or sync the epochs. An FPGA
   *     timestamp can be converted to the correct timebase using {@link Utils#fpgaToCurrentTime}.
   * @param visionMeasurementStdDevs Standard deviations of the vision pose measurement (x position
   *     in meters, y position in meters, and heading in radians). Increase these numbers to trust
   *     the vision pose measurement less.
   */
  void addVisionMeasurement(
      Pose2d visionRobotPoseMeters,
      double timestampSeconds,
      Matrix<N3, N1> visionMeasurementStdDevs);

  void close();
}
