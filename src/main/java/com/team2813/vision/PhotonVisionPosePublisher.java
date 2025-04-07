package com.team2813.vision;

import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.networktables.StructTopic;
import edu.wpi.first.networktables.TimestampedObject;
import edu.wpi.first.wpilibj.Timer;
import java.util.List;
import java.util.function.Supplier;
import org.photonvision.EstimatedRobotPose;
import org.photonvision.PhotonCamera;

public final class PhotonVisionPosePublisher {
  private static final long MICROS_PER_SECOND = 1_000_000;
  private final TimestampedStructPublisher<Pose3d> publisher;

  public PhotonVisionPosePublisher(PhotonCamera camera) {
    this(camera, Timer::getFPGATimestamp);
  }

  PhotonVisionPosePublisher(PhotonCamera camera, Supplier<Double> fpgaTimestampSupplier) {
    StructTopic<Pose3d> topic = camera.getCameraTable().getStructTopic("pose", Pose3d.struct);
    publisher = new TimestampedStructPublisher<>(topic, Pose3d.kZero, fpgaTimestampSupplier);
  }

  /**
   * Publishes the estimated positions to network tables.
   *
   * @param poseEstimates The estimated locations (with the blue driver station as the origin).
   */
  public void publish(List<EstimatedRobotPose> poseEstimates) {
    publisher.publish(
        poseEstimates.stream().map(PhotonVisionPosePublisher::toTimestampedObject).toList());
  }

  private static TimestampedObject<Pose3d> toTimestampedObject(EstimatedRobotPose pose) {
    return new TimestampedObject<>(
        (long) (pose.timestampSeconds * MICROS_PER_SECOND), 0, pose.estimatedPose);
  }
}
