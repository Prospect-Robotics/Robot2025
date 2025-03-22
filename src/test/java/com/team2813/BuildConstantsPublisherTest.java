package com.team2813;

import static com.google.common.truth.Fact.fact;
import static com.google.common.truth.Fact.simpleFact;
import static com.google.common.truth.Truth.assertAbout;
import static com.google.common.truth.Truth.assertThat;

import com.google.common.truth.FailureMetadata;
import com.google.common.truth.Subject;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import org.junit.Test;

public class BuildConstantsPublisherTest {

  /**
   * A Truth {@link Subject} for asserting properties of strings that should parse as {@link
   * LocalDateTime}.
   *
   * <p>Composed with the help of Gemini: https://g.co/gemini/share/d8db68a8fbaf
   */
  private class DateTimeStringSubject extends Subject {

    private final String actual;
    private final DateTimeFormatter formatter =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss z");

    private DateTimeStringSubject(FailureMetadata metadata, String actual) {
      super(metadata, actual);
      this.actual = actual;
    }

    public void parsesAsLocalDateTime() {
      if (actual == null) {
        failWithActual(simpleFact("expected to parse as LocalDateTime, but was null"));
        return;
      }

      try {
        LocalDateTime.parse(actual, formatter);
      } catch (DateTimeParseException e) {
        failWithActual(
            fact("expected to parse as LocalDateTime with format", formatter),
            fact("but parsing failed with", e.getMessage()));
      }
    }
  }

  /**
   * Returns the value of the given key in the given table, or an empty string if the key is not
   * present.
   */
  private String getStringEntryOrEmpty(NetworkTable table, String key) {
    return table.getStringTopic(key).getEntry("").get();
  }

  private Long getIntegerEntryOrDefault(NetworkTable table, String key, long defaultValue) {
    return table.getIntegerTopic(key).getEntry(defaultValue).get();
  }

  @Test
  public void publishesBuildConstantsToNetworkTables() {
    // Arrange.
    NetworkTableInstance ntInstance = NetworkTableInstance.create();
    BuildConstantsPublisher publisher = new BuildConstantsPublisher(ntInstance);
    NetworkTable table = ntInstance.getTable(BuildConstantsPublisher.TABLE_NAME);

    // Act.
    publisher.publish();

    // Assert.
    assertThat(table).isNotNull();
    assertThat(table.getKeys())
        .containsExactly(
            "MavenName",
            "GitRevision",
            "GitSha",
            "GitDate",
            "GitBranch",
            "BuildUnixTime",
            "BuildDate",
            "Dirty");
    assertThat(getStringEntryOrEmpty(table, "MavenName")).isEqualTo("Robot2025");

    assertThat(getIntegerEntryOrDefault(table, "GitRevision", 0)).isGreaterThan(0);
    assertThat(getStringEntryOrEmpty(table, "GitSha")).isNotEmpty();
    assertThat(getStringEntryOrEmpty(table, "GitDate")).isNotEmpty();
    assertThat(getStringEntryOrEmpty(table, "GitBranch")).isNotEmpty();

    assertThat(getIntegerEntryOrDefault(table, "BuildUnixTime", 0)).isNotEqualTo(0);
    assertThat(getStringEntryOrEmpty(table, "BuildDate")).isNotEmpty();
    assertAbout(DateTimeStringSubject::new)
        .that(getStringEntryOrEmpty(table, "BuildDate"))
        .parsesAsLocalDateTime();
    assertThat(getIntegerEntryOrDefault(table, "Dirty", -1)).isAnyOf(0l, 1l);
  }
}
