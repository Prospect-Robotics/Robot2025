package com.team2813.vision;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.vision.TimestampedStructPublisher.EXPECTED_UPDATE_FREQUENCY_MICROS;
import static com.team2813.vision.TimestampedStructPublisher.PUBLISHED_VALUE_VALID_MICROS;

import com.team2813.NetworkTableResource;
import edu.wpi.first.math.geometry.*;
import edu.wpi.first.networktables.*;
import edu.wpi.first.units.Units;
import java.util.*;
import java.util.function.Supplier;
import org.junit.Rule;
import org.junit.Test;

/** Tests for {@link TimestampedStructPublisher}. */
public class TimestampedStructPublisherTest {
  private static final Translation2d DEFAULT_VALUE = new Translation2d(28, 13);
  private static final String TABLE_NAME = "gearHeads";
  private static final String TOPIC_NAME = "championships";

  @Rule public final NetworkTableResource networkTable = new NetworkTableResource();

  private final FakeClock fakeClock = new FakeClock();

  private TimestampedStructPublisher<Translation2d> createPublisher() {
    NetworkTable table = networkTable.getNetworkTableInstance().getTable(TABLE_NAME);
    return new TimestampedStructPublisher<>(
        table.getStructTopic(TOPIC_NAME, Translation2d.struct), Translation2d.kZero, fakeClock);
  }

  @Test
  public void constructorPublishesZeroValue() {
    // Arrange
    var topic = getTopic();

    try (StructSubscriber<Translation2d> subscriber = topic.subscribe(DEFAULT_VALUE)) {
      // Act
      createPublisher();

      // Assert
      List<TimestampedValue> publishedValues = TimestampedValue.fromSubscriberQueue(subscriber);
      TimestampedValue expectedPose = new TimestampedValue(Translation2d.kZero, 1);
      assertThat(publishedValues).containsExactly(expectedPose);
    }
  }

  @Test
  public void publish_withOnePose() {
    // Arrange
    var topic = getTopic();

    try (StructSubscriber<Translation2d> subscriber = topic.subscribe(DEFAULT_VALUE)) {
      TimestampedStructPublisher<Translation2d> publisher = createPublisher();
      long firstFpgaTimestampMicros = 25;
      Translation2d value = new Translation2d(7.35, 0.708);
      TimestampedObject<Translation2d> object =
          new TimestampedObject<>(firstFpgaTimestampMicros, 0, value);

      // Act
      publisher.publish(List.of(object));

      // Assert
      List<TimestampedValue> publishedValues = TimestampedValue.fromSubscriberQueue(subscriber);
      TimestampedValue expectedValue = new TimestampedValue(value, firstFpgaTimestampMicros);
      assertThat(publishedValues).containsExactly(expectedValue);
    }
  }

  @Test
  public void publish_withManyPoses() {
    // Arrange
    var topic = getTopic();

    try (StructSubscriber<Translation2d> subscriber =
        topic.subscribe(DEFAULT_VALUE, PubSubOption.pollStorage(5))) {
      TimestampedStructPublisher<Translation2d> publisher = createPublisher();
      long firstFpgaTimestampMicros = 25;

      List<TimestampedObject<Translation2d>> valuesToPublish = new ArrayList<>(3);
      for (int i = 0; i < 3; i++) {
        Translation2d value = new Translation2d(7.35 + i, 0.708);
        TimestampedObject<Translation2d> object =
            new TimestampedObject<>(firstFpgaTimestampMicros + i * 10, 0, value);
        valuesToPublish.add(object);
      }
      assertThat(subscriber.readQueue()).hasLength(1);

      // Act
      publisher.publish(valuesToPublish);

      // Assert
      List<TimestampedValue> publishedValues = TimestampedValue.fromSubscriberQueue(subscriber);
      List<TimestampedValue> expectedValues =
          valuesToPublish.stream().map(TimestampedValue::fromTimestampedObject).toList();

      assertThat(publishedValues).containsExactlyElementsIn(expectedValues);
    }
  }

  @Test
  public void publish_withNoPoses_withStalePreviousPose() {
    // Arrange
    var topic = getTopic();

    try (StructSubscriber<Translation2d> subscriber =
        topic.subscribe(DEFAULT_VALUE, PubSubOption.pollStorage(5))) {
      TimestampedStructPublisher<Translation2d> publisher = createPublisher();
      long firstFpgaTimestampMicros = 25;
      Translation2d value = new Translation2d(7.35, 0.708);
      TimestampedObject<Translation2d> object =
          new TimestampedObject<>(firstFpgaTimestampMicros, 0, value);
      assertThat(subscriber.readQueue()).hasLength(1);
      publisher.publish(List.of(object));
      assertThat(subscriber.readQueue()).hasLength(1);
      fakeClock.setFpgaTimestampMicros(firstFpgaTimestampMicros);
      fakeClock.incrementFpgaTimestampMicros(PUBLISHED_VALUE_VALID_MICROS + 1);

      // Act
      publisher.publish(List.of());

      // Assert
      List<TimestampedValue> publishedValues = TimestampedValue.fromSubscriberQueue(subscriber);
      assertThat(publishedValues).hasSize(1);
      TimestampedValue publishedValue = publishedValues.get(0);
      TimestampedValue expectedPose =
          new TimestampedValue(
              Translation2d.kZero, firstFpgaTimestampMicros + EXPECTED_UPDATE_FREQUENCY_MICROS);
      assertThat(publishedValues).containsExactly(expectedPose);
    }
  }

  @Test
  public void publish_withNoPoses_withNonStalePreviousPose() {
    // Arrange
    var topic = getTopic();

    try (StructSubscriber<Translation2d> subscriber =
        topic.subscribe(DEFAULT_VALUE, PubSubOption.pollStorage(5))) {
      TimestampedStructPublisher<Translation2d> publisher = createPublisher();
      long firstFpgaTimestampMicros = 25;

      Translation2d value = new Translation2d(7.35, 0.708);
      TimestampedObject<Translation2d> object =
          new TimestampedObject<>(firstFpgaTimestampMicros, 0, value);
      assertThat(subscriber.readQueue()).hasLength(1);
      publisher.publish(List.of(object));
      assertThat(subscriber.readQueue()).hasLength(1);
      fakeClock.setFpgaTimestampMicros(firstFpgaTimestampMicros);
      fakeClock.incrementFpgaTimestampMicros(PUBLISHED_VALUE_VALID_MICROS - 1);

      // Act
      publisher.publish(List.of());

      // Assert
      List<TimestampedValue> publishedValues = TimestampedValue.fromSubscriberQueue(subscriber);
      assertThat(publishedValues).isEmpty();
    }
  }

  private StructTopic<Translation2d> getTopic() {
    NetworkTable table = networkTable.getNetworkTableInstance().getTable(TABLE_NAME);
    return table.getStructTopic(TOPIC_NAME, Translation2d.struct);
  }

  private static class FakeClock implements Supplier<Double> {
    private double fpgaTimestampSeconds = 2.0;

    public Double get() {
      return fpgaTimestampSeconds;
    }

    void setFpgaTimestampMicros(long micros) {
      fpgaTimestampSeconds = Units.Seconds.convertFrom(micros, Units.Microseconds);
    }

    void incrementFpgaTimestampMicros(double micros) {
      fpgaTimestampSeconds += Units.Seconds.convertFrom(micros, Units.Microseconds);
    }
  }

  private record TimestampedValue(Translation2d value, long timestamp) {

    static TimestampedValue fromTimestampedObject(TimestampedObject<Translation2d> object) {
      return new TimestampedValue(object.value, object.timestamp);
    }

    static List<TimestampedValue> fromSubscriberQueue(StructSubscriber<Translation2d> subscriber) {
      return Arrays.stream(subscriber.readQueue())
          .map(TimestampedValue::fromTimestampedObject)
          .toList();
    }
  }
}
