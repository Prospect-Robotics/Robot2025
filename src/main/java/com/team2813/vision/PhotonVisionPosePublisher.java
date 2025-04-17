package com.team2813.vision;

import static com.team2813.vision.VisionUtil.getTableForCamera;

import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.StructTopic;
import edu.wpi.first.units.Units;
import edu.wpi.first.wpilibj.Timer;
import java.util.List;
import java.util.function.Supplier;
import org.photonvision.EstimatedRobotPose;
import org.photonvision.PhotonCamera;

public final class PhotonVisionPosePublisher {
  private final TimestampedStructPublisher<Pose3d> publisher;

  public PhotonVisionPosePublisher(PhotonCamera camera) {
    this(camera, Timer::getFPGATimestamp);
  }

  PhotonVisionPosePublisher(PhotonCamera camera, Supplier<Double> fpgaTimestampSupplier) {
    NetworkTable table = getTableForCamera(camera);
    StructTopic<Pose3d> topic = table.getStructTopic("poseEstimate", Pose3d.struct);
    publisher = new TimestampedStructPublisher<>(topic, Pose3d.kZero, fpgaTimestampSupplier);
  }

  /**
   * Publishes the estimated positions to network tables.
   *
   * @param poseEstimates The estimated locations (with the blue driver station as the origin).
   */
  public void publish(List<EstimatedRobotPose> poseEstimates) {
    publisher.publish(
        poseEstimates.stream().map(PhotonVisionPosePublisher::toTimestampedValue).toList());
  }

  private static TimestampedValue<Pose3d> toTimestampedValue(EstimatedRobotPose pose) {
    return TimestampedValue.withFpgaTimestamp(
        pose.timestampSeconds, Units.Seconds, pose.estimatedPose);
  }
}
