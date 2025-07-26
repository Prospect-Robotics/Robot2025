package com.team2813.vision;

import edu.wpi.first.networktables.StructArrayPublisher;
import edu.wpi.first.networktables.StructArrayTopic;
import edu.wpi.first.util.struct.Struct;
import edu.wpi.first.wpilibj.TimedRobot;
import java.lang.reflect.Array;
import java.util.Collection;
import java.util.Collections;
import java.util.function.Supplier;

/** Publishes timestamped array dataq to a network tables topic. */
final class TimestampedStructArrayPublisher<S> {
  private static final long MICROS_PER_SECOND = 1_000_000;
  static final long EXPECTED_UPDATE_FREQUENCY_MICROS =
      (long) (TimedRobot.kDefaultPeriod * MICROS_PER_SECOND);
  static final long PUBLISHED_VALUE_VALID_MICROS = 2 * EXPECTED_UPDATE_FREQUENCY_MICROS;

  private final StructArrayPublisher<S> publisher;
  private final Supplier<Double> fpgaTimestampSupplier;
  private final S[] emptyArray;
  private long lastUpdateTimeMicros;
  private boolean publishedEmptyValue;

  /**
   * Creates a publisher.
   *
   * @param topic Topic to publish to.
   * @param fpgaTimestampSupplier Supplies FPGA timestamps in seconds.
   */
  TimestampedStructArrayPublisher(
      StructArrayTopic<S> topic, Supplier<Double> fpgaTimestampSupplier) {
    this.fpgaTimestampSupplier = fpgaTimestampSupplier;
    emptyArray = createEmptyArray(topic.getStruct());
    publisher = topic.publish();
    publisher.set(emptyArray, 1);
    publishedEmptyValue = true;
  }

  @SuppressWarnings("unchecked")
  private static <S> S[] createEmptyArray(Struct<S> struct) {
    return (S[]) Array.newInstance(struct.getTypeClass(), 0);
  }

  /** Publishes the values to network tables. */
  public void publishHasNoValues() {
    publish(Collections.emptyList(), currentTimeMicros());
  }

  /** Publishes the values to network tables. */
  public void publish(Collection<S> values, long fpgaTimestampMicros) {
    if (values.isEmpty()) {
      if (!publishedEmptyValue) {
        long microsSinceLastUpdate = fpgaTimestampMicros - lastUpdateTimeMicros;
        if (microsSinceLastUpdate > PUBLISHED_VALUE_VALID_MICROS) {
          long timestamp = lastUpdateTimeMicros + EXPECTED_UPDATE_FREQUENCY_MICROS;
          publisher.set(emptyArray, timestamp);
          publishedEmptyValue = true;
        }
      }
    } else {
      publisher.set(values.toArray(emptyArray), fpgaTimestampMicros);
      lastUpdateTimeMicros = fpgaTimestampMicros;
      publishedEmptyValue = false;
    }
  }

  private long currentTimeMicros() {
    return (long) (fpgaTimestampSupplier.get() * MICROS_PER_SECOND);
  }
}
