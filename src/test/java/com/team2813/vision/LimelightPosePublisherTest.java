package com.team2813.vision;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.vision.TimestampedStructPublisher.PUBLISHED_VALUE_VALID_MICROS;

import com.team2813.lib2813.limelight.BotPoseEstimate;
import com.team2813.lib2813.testing.junit.jupiter.IsolatedNetworkTablesExtension;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.networktables.*;
import edu.wpi.first.units.Units;
import java.util.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

/** Tests for {@link LimelightPosePublisher}. */
@ExtendWith(IsolatedNetworkTablesExtension.class)
public class LimelightPosePublisherTest {
  private static final double FAKE_TIMESTAMP_OFFSET = 0.25;
  private static final Pose2d DEFAULT_POSE = new Pose2d(28, 13, Rotation2d.fromDegrees(45));
  private static final String EXPECTED_TABLE_NAME = "Vision/limelight";

  private final FakeClocks fakeClocks = new FakeClocks();

  @Test
  public void publish_withPose(NetworkTableInstance ntInstance) {
    // Arrange
    var topic = getTopic(ntInstance);

    try (StructSubscriber<Pose2d> subscriber = topic.subscribe(DEFAULT_POSE)) {
      LimelightPosePublisher publisher = createPublisher(ntInstance);
      long firstFpgaTimestampSeconds = 25;
      Pose2d estimatedPose = new Pose2d(7.35, 0.708, Rotation2d.fromDegrees(30));
      BotPoseEstimate estimate =
          new BotPoseEstimate(estimatedPose, fpgaSecondsToCurrentTime(firstFpgaTimestampSeconds));

      // Act
      publisher.publish(Optional.of(estimate));

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
  public void publish_withoutPose(NetworkTableInstance ntInstance) {
    // Arrange
    var topic = getTopic(ntInstance);

    try (StructSubscriber<Pose2d> subscriber = topic.subscribe(DEFAULT_POSE)) {
      LimelightPosePublisher publisher = createPublisher(ntInstance);
      long firstFpgaTimestampSeconds = 25;
      Pose2d estimatedPose = new Pose2d(7.35, 0.708, Rotation2d.fromDegrees(30));
      BotPoseEstimate estimate =
          new BotPoseEstimate(estimatedPose, fpgaSecondsToCurrentTime(firstFpgaTimestampSeconds));
      publisher.publish(Optional.of(estimate));
      fakeClocks.setFpgaTimestampSeconds(firstFpgaTimestampSeconds);
      fakeClocks.incrementFpgaTimestampMicros(PUBLISHED_VALUE_VALID_MICROS - 1);

      // Act
      publisher.publish(Optional.empty());

      // Assert
      List<TimestampedPose> publishedValues = TimestampedPose.fromSubscriberQueue(subscriber);
      TimestampedPose expectedPose =
          new TimestampedPose(
              estimatedPose,
              (long) Units.Microseconds.convertFrom(firstFpgaTimestampSeconds, Units.Seconds));
      assertThat(publishedValues).containsExactly(expectedPose);
    }
  }

  private LimelightPosePublisher createPublisher(NetworkTableInstance ntInstance) {
    return new LimelightPosePublisher(ntInstance, fakeClocks.asClocks());
  }

  private StructTopic<Pose2d> getTopic(NetworkTableInstance ntInstance) {
    NetworkTable table = ntInstance.getTable(EXPECTED_TABLE_NAME);
    return table.getStructTopic("poseEstimate", Pose2d.struct);
  }

  private static double fpgaSecondsToCurrentTime(double fpgaTimeSeconds) {
    return fpgaTimeSeconds - FAKE_TIMESTAMP_OFFSET;
  }

  private static class FakeClocks {
    private double fpgaTimestampSeconds = 2.0;

    private LimelightPosePublisher.Clocks asClocks() {
      return new LimelightPosePublisher.Clocks(this::getFPGATimestamp, this::getCurrentTimeSeconds);
    }

    double getFPGATimestamp() {
      return fpgaTimestampSeconds;
    }

    double getCurrentTimeSeconds() {
      return fpgaSecondsToCurrentTime(fpgaTimestampSeconds);
    }

    void setFpgaTimestampSeconds(double seconds) {
      fpgaTimestampSeconds = seconds;
    }

    void incrementFpgaTimestampMicros(double micros) {
      fpgaTimestampSeconds += Units.Seconds.convertFrom(micros, Units.Microseconds);
    }
  }

  private record TimestampedPose(Pose2d pose, long timestamp) {

    static TimestampedPose fromTimestampedObject(TimestampedObject<Pose2d> object) {
      return new TimestampedPose(object.value, object.timestamp);
    }

    static List<TimestampedPose> fromSubscriberQueue(StructSubscriber<Pose2d> subscriber) {
      return Arrays.stream(subscriber.readQueue())
          .map(TimestampedPose::fromTimestampedObject)
          .toList();
    }
  }
}
