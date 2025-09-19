package com.team2813.vision;

import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.networktables.StructTopic;
import edu.wpi.first.wpilibj.TimedRobot;
import java.util.List;
import java.util.function.Supplier;

/** Publishes timestamped data to a network tables topic. */
final class TimestampedStructPublisher<S> {
  private static final long MICROS_PER_SECOND = 1_000_000;
  static final long EXPECTED_UPDATE_FREQUENCY_MICROS =
      (long) (TimedRobot.kDefaultPeriod * MICROS_PER_SECOND);
  // PhotonVision appears to produce estimates every 80ms, so treat values older than 0.1s as stale.
  static final long PUBLISHED_VALUE_VALID_MICROS = MICROS_PER_SECOND / 10;

  private final StructPublisher<S> publisher;
  private final Supplier<Double> fpgaTimestampSupplier;
  private final S zeroValue;
  private long lastUpdateTimeMicros;
  private boolean publishedZeroValue;

  /**
   * Creates a publisher.
   *
   * @param topic Topic to publish to.
   * @param zeroValue Value to publish when data is determined to be stale.
   * @param fpgaTimestampSupplier Supplies FPGA timestamps in seconds.
   */
  TimestampedStructPublisher(
      StructTopic<S> topic, S zeroValue, Supplier<Double> fpgaTimestampSupplier) {
    this.fpgaTimestampSupplier = fpgaTimestampSupplier;
    this.zeroValue = zeroValue;
    this.publisher = topic.publish();
    this.publisher.set(zeroValue, 1);
    publishedZeroValue = true;
  }

  /** Publishes the values to network tables. */
  public void publish(List<TimestampedValue<S>> timestampedValues) {
    if (timestampedValues.isEmpty()) {
      if (!publishedZeroValue) {
        long currentTimeMicros = currentTimeMicros();
        long microsSinceLastUpdate = currentTimeMicros - lastUpdateTimeMicros;
        if (microsSinceLastUpdate > PUBLISHED_VALUE_VALID_MICROS) {
          long timestamp = lastUpdateTimeMicros + EXPECTED_UPDATE_FREQUENCY_MICROS;
          publisher.set(zeroValue, timestamp);
          publishedZeroValue = true;
        }
      }
    } else {
      for (var timestampedValue : timestampedValues) {
        long timestampMicros = timestampedValue.networkTablesTimestampMicros();
        lastUpdateTimeMicros = Math.max(lastUpdateTimeMicros, timestampMicros);
        publisher.set(timestampedValue.value(), timestampMicros);
      }
      publishedZeroValue = false;
    }
  }

  private long currentTimeMicros() {
    return (long) (fpgaTimestampSupplier.get() * MICROS_PER_SECOND);
  }
}
