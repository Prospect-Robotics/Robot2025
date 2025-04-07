package com.team2813.vision;

import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.networktables.StructTopic;
import edu.wpi.first.networktables.TimestampedObject;
import edu.wpi.first.wpilibj.TimedRobot;
import java.util.List;
import java.util.function.Supplier;

/** Publishes timestamped data to a network tables topic. */
final class TimestampedStructPublisher<S> {
  private static final long MICROS_PER_SECOND = 1_000_000;
  static final long EXPECTED_UPDATE_FREQUENCY_MICROS =
      (long) (TimedRobot.kDefaultPeriod * MICROS_PER_SECOND);
  static final long PUBLISHED_VALUE_VALID_MICROS = 2 * EXPECTED_UPDATE_FREQUENCY_MICROS;

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

  /**
   * Publishes the values to network tables.
   *
   * @param values Timestamped data, with the timestamps in FPGA millis.
   */
  public void publish(List<TimestampedObject<S>> values) {
    if (values.isEmpty()) {
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
      for (TimestampedObject<S> object : values) {
        long timestampMicros = object.timestamp;
        lastUpdateTimeMicros = Math.max(lastUpdateTimeMicros, timestampMicros);
        publisher.set(object.value, timestampMicros);
      }
      publishedZeroValue = false;
    }
  }

  private long currentTimeMicros() {
    return (long) (fpgaTimestampSupplier.get() * MICROS_PER_SECOND);
  }
}
