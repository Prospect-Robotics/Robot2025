package com.team2813.vision;

import static com.google.common.truth.Truth.assertThat;

import com.team2813.NetworkTableResource;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation3d;
import edu.wpi.first.networktables.*;
import edu.wpi.first.units.Units;
import java.util.*;
import java.util.function.Supplier;
import org.junit.Rule;
import org.junit.Test;
import org.photonvision.EstimatedRobotPose;
import org.photonvision.PhotonCamera;
import org.photonvision.PhotonPoseEstimator;

/** Tests for {@link PhotonVisionPosePublisher}. */
public class PhotonVisionPosePublisherTest {
  private static final Pose3d DEFAULT_POSE =
      new Pose3d(
          28, 13, 25, new Rotation3d(Math.toRadians(28), Math.toRadians(13), Math.toRadians(25)));
  private static final String CAMERA_NAME = "tweak";
  private static final String EXPECTED_TABLE_NAME = "Vision/tweak";

  @Rule public final NetworkTableResource networkTable = new NetworkTableResource();

  private final FakeClock fakeClock = new FakeClock();

  @Test
  public void publish_withOnePose() {
    // Arrange
    var topic = getTopic();

    try (StructSubscriber<Pose3d> subscriber = topic.subscribe(DEFAULT_POSE)) {
      PhotonVisionPosePublisher publisher = createPublisher();
      long firstFpgaTimestampSeconds = 25;
      Rotation3d rotation =
          new Rotation3d(Math.toRadians(-5.17), Math.toRadians(-24.32), Math.toRadians(-164.63));
      Pose3d estimatedPose = new Pose3d(7.35, 0.708, -3.45, rotation);
      EstimatedRobotPose estimate =
          new EstimatedRobotPose(
              estimatedPose,
              firstFpgaTimestampSeconds,
              List.of(),
              PhotonPoseEstimator.PoseStrategy.AVERAGE_BEST_TARGETS);

      // Act
      publisher.publish(List.of(estimate));

      // Assert
      List<TimestampedPose> publishedValues = TimestampedPose.fromSubscriberQueue(subscriber);
      TimestampedPose expectedPose =
          new TimestampedPose(
              estimatedPose,
              (long) Units.Microseconds.convertFrom(firstFpgaTimestampSeconds, Units.Seconds));
      assertThat(publishedValues).containsExactly(expectedPose);
    }
  }

  @Test
  public void publish_withManyPoses() {
    // Arrange
    var topic = getTopic();

    try (StructSubscriber<Pose3d> subscriber =
        topic.subscribe(DEFAULT_POSE, PubSubOption.pollStorage(5))) {
      PhotonVisionPosePublisher publisher = createPublisher();
      long firstFpgaTimestampSeconds = 25;

      List<EstimatedRobotPose> estimates = new ArrayList<>(3);
      for (int i = 0; i < 3; i++) {
        Rotation3d rotation =
            new Rotation3d(
                Math.toRadians(-5.17 + i), Math.toRadians(-24.32), Math.toRadians(-164.63));
        Pose3d estimatedPose = new Pose3d(7.35 + i, 0.708, -3.45, rotation);
        EstimatedRobotPose estimate =
            new EstimatedRobotPose(
                estimatedPose,
                firstFpgaTimestampSeconds + i * 10,
                List.of(),
                PhotonPoseEstimator.PoseStrategy.AVERAGE_BEST_TARGETS);
        estimates.add(estimate);
      }
      assertThat(subscriber.readQueue()).hasLength(1);

      // Act
      publisher.publish(estimates);

      // Assert
      List<TimestampedPose> publishedValues = TimestampedPose.fromSubscriberQueue(subscriber);
      List<TimestampedPose> expectedValues =
          estimates.stream().map(TimestampedPose::fromEstimatedRobotPose).toList();

      assertThat(publishedValues).containsExactlyElementsIn(expectedValues);
    }
  }

  private StructTopic<Pose3d> getTopic() {
    NetworkTable table = networkTable.getNetworkTableInstance().getTable(EXPECTED_TABLE_NAME);
    return table.getStructTopic("poseEstimate", Pose3d.struct);
  }

  private static class FakeClock implements Supplier<Double> {
    @Override
    public Double get() {
      return 2.0;
    }
  }

  protected PhotonVisionPosePublisher createPublisher() {
    var camera = new PhotonCamera(networkTable.getNetworkTableInstance(), CAMERA_NAME);
    return new PhotonVisionPosePublisher(camera, fakeClock);
  }

  private record TimestampedPose(Pose3d pose, long timestamp) {

    static TimestampedPose fromTimestampedObject(TimestampedObject<Pose3d> object) {
      return new TimestampedPose(object.value, object.timestamp);
    }

    static TimestampedPose fromEstimatedRobotPose(EstimatedRobotPose estimate) {
      return new TimestampedPose(
          estimate.estimatedPose,
          (long) Units.Microseconds.convertFrom(estimate.timestampSeconds, Units.Seconds));
    }

    static List<TimestampedPose> fromSubscriberQueue(StructSubscriber<Pose3d> subscriber) {
      return Arrays.stream(subscriber.readQueue())
          .map(TimestampedPose::fromTimestampedObject)
          .toList();
    }
  }
}
