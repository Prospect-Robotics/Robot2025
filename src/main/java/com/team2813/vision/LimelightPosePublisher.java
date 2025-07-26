package com.team2813.vision;

import static com.team2813.vision.VisionNetworkTables.POSE_ESTIMATE_TOPIC;
import static com.team2813.vision.VisionNetworkTables.VISIBLE_APRIL_TAG_POSES_TOPIC;
import static com.team2813.vision.VisionNetworkTables.getTableForLimelight;

import com.ctre.phoenix6.Utils;
import com.team2813.RobotContainer;
import com.team2813.lib2813.limelight.BotPoseEstimate;
import com.team2813.lib2813.limelight.LocationalData;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructTopic;
import edu.wpi.first.units.Units;
import edu.wpi.first.wpilibj.Timer;
import java.util.Optional;
import java.util.function.Supplier;

public final class LimelightPosePublisher {
  private final TimestampedStructPublisher<Pose2d> publisher;
  private final TimestampedStructArrayPublisher<Pose3d> tagPublisher;
  private final double timestampOffset;

  public LimelightPosePublisher(NetworkTableInstance ntInstance) {
    this(ntInstance, Clocks.SYSTEM);
  }

  LimelightPosePublisher(NetworkTableInstance ntInstance, Clocks clocks) {
    timestampOffset =
        clocks.fpgaTimestampSupplier().get() - clocks.currentTimestampSupplier().get();
    NetworkTable limelightNetworkTable = getTableForLimelight(ntInstance);
    StructTopic<Pose2d> topic =
        limelightNetworkTable.getStructTopic(POSE_ESTIMATE_TOPIC, Pose2d.struct);
    publisher = new TimestampedStructPublisher<>(topic, Pose2d.kZero, clocks.fpgaTimestampSupplier);
    tagPublisher =
        new TimestampedStructArrayPublisher<>(
            limelightNetworkTable.getStructArrayTopic(VISIBLE_APRIL_TAG_POSES_TOPIC, Pose3d.struct),
            clocks.fpgaTimestampSupplier);
  }

  /**
   * Publishes the estimated position to network tables.
   *
   * @param poseEstimate The estimated location (with the blue driver station as the origin).
   */
  public void publish(Optional<BotPoseEstimate> poseEstimate) {
    publisher.publish(poseEstimate.stream().map(this::toTimestampedValue).toList());
  }

  /**
   * Publishes the locational data to network tables.
   *
   * @param locationalData The locational data.
   */
  public void publish(LocationalData locationalData) {
    Optional<BotPoseEstimate> optionalEstimate = botPoseEstimateBlue(locationalData);
    publish(optionalEstimate);

    optionalEstimate.ifPresentOrElse(
        estimate -> {
          double fpgaTimestampSecs = currentTimeToFpgaTime(estimate.timestampSeconds());
          long fpgaTimestampMicros =
              (long) Units.Microseconds.convertFrom(fpgaTimestampSecs, Units.Seconds);
          tagPublisher.publish(
              locationalData.getVisibleAprilTagPoses().values(), fpgaTimestampMicros);
        },
        tagPublisher::publishHasNoValues);
  }

  private static Optional<BotPoseEstimate> botPoseEstimateBlue(LocationalData locationalData) {
    return locationalData.getBotPoseEstimate().map(RobotContainer::toBotposeBlue);
  }

  private TimestampedValue<Pose2d> toTimestampedValue(BotPoseEstimate estimate) {
    return TimestampedValue.withFpgaTimestamp(
        currentTimeToFpgaTime(estimate.timestampSeconds()), Units.Seconds, estimate.pose());
  }

  /**
   * Converts a timestamp reported by {@link Utils#getCurrentTimeSeconds()} to an FPGA timestamp.
   *
   * <p>This conversion is the inverse of the one done by {@link Utils#fpgaToCurrentTime(double)}.
   */
  private double currentTimeToFpgaTime(double currentTimeSeconds) {
    return timestampOffset + currentTimeSeconds;
  }

  record Clocks(Supplier<Double> fpgaTimestampSupplier, Supplier<Double> currentTimestampSupplier) {
    static final Clocks SYSTEM = new Clocks(Timer::getFPGATimestamp, Utils::getCurrentTimeSeconds);
  }
}
