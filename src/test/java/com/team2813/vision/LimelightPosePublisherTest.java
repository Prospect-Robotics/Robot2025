package com.team2813.vision;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.vision.TimestampedStructPublisher.PUBLISHED_VALUE_VALID_MICROS;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.team2813.NetworkTableResource;
import com.team2813.RobotContainer;
import com.team2813.lib2813.limelight.BotPoseEstimate;
import com.team2813.lib2813.limelight.LocationalData;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Rotation3d;
import edu.wpi.first.networktables.*;
import edu.wpi.first.units.Units;
import java.util.*;
import org.junit.After;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;

/** Tests for {@link LimelightPosePublisher}. */
public class LimelightPosePublisherTest {
  private static final Pose3d[] EMPTY_POSE3D_ARRAY = new Pose3d[0];
  private static final double FAKE_TIMESTAMP_OFFSET = 0.25;
  private static final Pose2d DEFAULT_POSE = new Pose2d(28, 13, Rotation2d.fromDegrees(45));
  private static final String EXPECTED_TABLE_NAME = "Vision/limelight";

  @Rule public final NetworkTableResource networkTable = new NetworkTableResource();

  private final FakeClocks fakeClocks = new FakeClocks();
  private StructSubscriber<Pose2d> poseSubscriber;
  private StructArraySubscriber<Pose3d> aprilTagSubscriber;

  @Before
  public void createSubscribers() {
    NetworkTable table = networkTable.getNetworkTableInstance().getTable(EXPECTED_TABLE_NAME);
    poseSubscriber = table.getStructTopic("poseEstimate", Pose2d.struct).subscribe(DEFAULT_POSE);
    aprilTagSubscriber =
        table
            .getStructArrayTopic("visibleAprilTagPoses", Pose3d.struct)
            .subscribe(EMPTY_POSE3D_ARRAY);
  }

  @After
  public void closeSubscribers() {
    aprilTagSubscriber.close();
    poseSubscriber.close();
  }

  @Test
  public void publish_withPose() {
    // Arrange
    LimelightPosePublisher publisher = createPublisher();
    long firstFpgaTimestampSeconds = 25;
    Pose2d estimatedPoseCenter = new Pose2d(7.35, 0.708, Rotation2d.fromDegrees(30));
    Pose3d aprilTag1Pose =
        new Pose3d(
            28, 13, 25, new Rotation3d(Math.toRadians(28), Math.toRadians(13), Math.toRadians(25)));
    Pose3d aprilTag2Pose =
        new Pose3d(
            13, 20, 52, new Rotation3d(Math.toRadians(82), Math.toRadians(31), Math.toRadians(52)));
    BotPoseEstimate botPoseEstimateCenter =
        new BotPoseEstimate(
            estimatedPoseCenter, fpgaSecondsToCurrentTime(firstFpgaTimestampSeconds), Set.of(3));
    LocationalData locationalData = mock(LocationalData.class);
    Map<Integer, Pose3d> aprilTagPoses = new HashMap<>();
    aprilTagPoses.put(1, aprilTag1Pose);
    aprilTagPoses.put(2, aprilTag2Pose);
    when(locationalData.getBotPoseEstimate()).thenReturn(Optional.of(botPoseEstimateCenter));
    when(locationalData.getVisibleAprilTagPoses()).thenReturn(aprilTagPoses);

    // Act
    publisher.publish(locationalData);

    // Assert - published pose
    Pose2d expectedPose = RobotContainer.toBotposeBlue(estimatedPoseCenter);
    List<TimestampedPose> publishedPoses = TimestampedPose.fromSubscriberQueue(poseSubscriber);
    long expectedTimestamp =
        (long) Units.Microseconds.convertFrom(firstFpgaTimestampSeconds, Units.Seconds);
    TimestampedPose expectedTimestampedPose = new TimestampedPose(expectedPose, expectedTimestamp);
    assertThat(publishedPoses).containsExactly(expectedTimestampedPose);

    // Assert - published AprilTags
    List<TimestampedPoses> publishedAprilTags =
        TimestampedPoses.fromSubscriberQueue(aprilTagSubscriber);
    assertThat(publishedAprilTags)
        .containsExactly(
            new TimestampedPoses(List.of(aprilTag1Pose, aprilTag2Pose), expectedTimestamp));
  }

  @Test
  public void publish_withoutPose() {
    // Arrange
    LimelightPosePublisher publisher = createPublisher();
    long firstFpgaTimestampSeconds = 25;
    Pose2d estimatedPose = new Pose2d(7.35, 0.708, Rotation2d.fromDegrees(30));
    BotPoseEstimate estimate =
        new BotPoseEstimate(estimatedPose, fpgaSecondsToCurrentTime(firstFpgaTimestampSeconds));
    publisher.publish(Optional.of(estimate));
    fakeClocks.setFpgaTimestampSeconds(firstFpgaTimestampSeconds);
    fakeClocks.incrementFpgaTimestampMicros(PUBLISHED_VALUE_VALID_MICROS - 1);
    LocationalData locationalData = mock(LocationalData.class);
    when(locationalData.getBotPoseEstimate()).thenReturn(Optional.empty());

    // Act
    publisher.publish(locationalData);

    // Assert - published pose
    List<TimestampedPose> publishedPoses = TimestampedPose.fromSubscriberQueue(poseSubscriber);
    TimestampedPose expectedPose =
        new TimestampedPose(
            estimatedPose,
            (long) Units.Microseconds.convertFrom(firstFpgaTimestampSeconds, Units.Seconds));
    assertThat(publishedPoses).containsExactly(expectedPose);

    // Assert - published AprilTags
    List<TimestampedPoses> publishedAprilTags =
        TimestampedPoses.fromSubscriberQueue(aprilTagSubscriber);
    assertThat(publishedAprilTags).isEmpty();
  }

  private LimelightPosePublisher createPublisher() {
    return new LimelightPosePublisher(
        networkTable.getNetworkTableInstance(), fakeClocks.asClocks());
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

  private record TimestampedPoses(Collection<Pose3d> poses, long timestamp) {

    static TimestampedPoses fromTimestampedObject(TimestampedObject<Pose3d[]> object) {
      List<Pose3d> poses = Arrays.asList(object.value);
      return new TimestampedPoses(new ArrayList<>(poses), object.timestamp);
    }

    static List<TimestampedPoses> fromSubscriberQueue(StructArraySubscriber<Pose3d> subscriber) {
      return Arrays.stream(subscriber.readQueue())
          .map(TimestampedPoses::fromTimestampedObject)
          .toList();
    }
  }
}
