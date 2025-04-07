package com.team2813.vision;

import com.ctre.phoenix6.Utils;
import com.team2813.lib2813.limelight.BotPoseEstimate;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructTopic;
import edu.wpi.first.networktables.TimestampedObject;
import edu.wpi.first.wpilibj.Timer;
import java.util.Optional;
import java.util.function.Supplier;

public final class LimelightPosePublisher {
  public static final String TABLE_NAME = "limelight";
  private static final long MICROS_PER_SECOND = 1_000_000;
  private final TimestampedStructPublisher<Pose2d> publisher;
  private final double timestampOffset;

  public LimelightPosePublisher(NetworkTableInstance ntInstance) {
    this(ntInstance, Clocks.SYSTEM);
  }

  LimelightPosePublisher(NetworkTableInstance ntInstance, Clocks clocks) {
    timestampOffset =
        clocks.fpgaTimestampSupplier().get() - clocks.currentTimestampSupplier().get();
    StructTopic<Pose2d> topic =
        ntInstance.getTable(TABLE_NAME).getStructTopic("pose", Pose2d.struct);
    publisher = new TimestampedStructPublisher<>(topic, Pose2d.kZero, clocks.fpgaTimestampSupplier);
  }

  /**
   * Publishes the estimated position to network tables.
   *
   * @param poseEstimate The estimated location (with the blue driver station as the origin).
   */
  public void publish(Optional<BotPoseEstimate> poseEstimate) {
    publisher.publish(poseEstimate.stream().map(this::toTimestampedObject).toList());
  }

  private TimestampedObject<Pose2d> toTimestampedObject(BotPoseEstimate estimate) {
    return new TimestampedObject<>(timestampMicros(estimate), 0, estimate.pose());
  }

  private long timestampMicros(BotPoseEstimate estimate) {
    double fpgaTimestampSeconds = currentTimeToFpgaTime(estimate.timestampSeconds());
    return (long) (fpgaTimestampSeconds * MICROS_PER_SECOND);
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
