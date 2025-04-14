package com.team2813.vision;

import static com.team2813.vision.VisionUtil.getTableForCamera;

import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.StructTopic;
import edu.wpi.first.units.Units;
import edu.wpi.first.wpilibj.Timer;
import java.util.List;
import java.util.function.Supplier;
import java.util.stream.Stream;
import org.photonvision.EstimatedRobotPose;
import org.photonvision.PhotonCamera;

public final class PhotonVisionPosePublisher {
  private final TimestampedStructPublisher<Pose3d> publisher;
  private final TimestampedStructPublisher<Pose3d> tagPublisher;
  private final AprilTagFieldLayout fieldTags;

  public PhotonVisionPosePublisher(PhotonCamera camera, AprilTagFieldLayout fieldTags) {
    this(camera, fieldTags, Timer::getFPGATimestamp);
  }

  public PhotonVisionPosePublisher(
      PhotonCamera camera, AprilTagFieldLayout fieldTags, String topicName) {
    this(camera, fieldTags, topicName, Timer::getFPGATimestamp);
  }

  PhotonVisionPosePublisher(
      PhotonCamera camera, AprilTagFieldLayout fieldTags, Supplier<Double> fpgaTimestampSupplier) {
    this(camera, fieldTags, "poseEstimate", fpgaTimestampSupplier);
  }

  PhotonVisionPosePublisher(
      PhotonCamera camera,
      AprilTagFieldLayout fieldTags,
      String topicName,
      Supplier<Double> fpgaTimestampSupplier) {
    this.fieldTags = fieldTags;
    NetworkTable table = getTableForCamera(camera);
    StructTopic<Pose3d> topic = table.getStructTopic(topicName, Pose3d.struct);
    publisher = new TimestampedStructPublisher<>(topic, Pose3d.kZero, fpgaTimestampSupplier);
    topic = table.getStructTopic("aprilTagPose", Pose3d.struct);
    tagPublisher = new TimestampedStructPublisher<>(topic, Pose3d.kZero, fpgaTimestampSupplier);
  }

  /**
   * Publishes the estimated positions to network tables.
   *
   * @param poseEstimates The estimated locations (with the blue driver station as the origin).
   */
  public void publish(List<EstimatedRobotPose> poseEstimates) {
    publisher.publish(
        poseEstimates.stream()
            .map(PhotonVisionPosePublisher::toRobotPoseTimestampedValue)
            .toList());
    tagPublisher.publish(
        poseEstimates.stream().flatMap(this::toAprilTagPoseTimestampedValue).toList());
  }

  private static TimestampedValue<Pose3d> toRobotPoseTimestampedValue(EstimatedRobotPose pose) {
    return TimestampedValue.withFpgaTimestamp(
        pose.timestampSeconds, Units.Seconds, pose.estimatedPose);
  }

  private Stream<TimestampedValue<Pose3d>> toAprilTagPoseTimestampedValue(EstimatedRobotPose pose) {
    if (pose.targetsUsed.isEmpty()) {
      return Stream.empty();
    }
    return fieldTags
        .getTagPose(pose.targetsUsed.get(0).fiducialId)
        .map(
            tagPose ->
                TimestampedValue.withFpgaTimestamp(pose.timestampSeconds, Units.Seconds, tagPose))
        .stream();
  }
}
