package com.team2813;

import edu.wpi.first.networktables.IntegerPublisher;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StringPublisher;

/**
 * Publishes build constants to NetworkTables.
 *
 * <p>This class is used to publish build constants to NetworkTables during robot operation. This
 * information is important when iterating on robot code and diagnosing issues observed in the field
 * - it helps the main developer and any other developers assisting with the troubleshooting to
 * confirm what (and whos) version of the code is running on the robot.
 *
 * <p>Build constants need to be published only once, typically during robot initialization.
 *
 * <p>The constants are published under the {@code "/BuildConstants"} table in NetworkTables.
 *
 * <p>The build constants class, {@code BuildConstants}, is generated for the robot library by
 * enabling the `gversion` plugin in the gradle build file. {@code BuildConstantsPublisher} will
 * fail to compile if the {@code BuildConstants} class is not generated.
 *
 * <pre>{@code
 * plugins {
 *   ...
 *   // Plugin needed for Git Build Info
 *   // (see https://docs.wpilib.org/en/stable/docs/software/advanced-gradlerio/deploy-git-data.html)
 *   id 'com.peterabeles.gversion' version '1.10'
 *   ...
 * }
 * ...
 * // Generates a BuildConstants file.
 * // https://docs.wpilib.org/en/stable/docs/software/advanced-gradlerio/deploy-git-data.html
 * project.compileJava.dependsOn(createVersionFile)
 * def BUILD_CONSTANTS_AUTOGEN_PATH = 'build/generated/sources/build_constants/'
 * gversion {
 *     // Build inside build/ (so that it will be ignored by git due to .gitignore)
 *     // and inside build/generated/ (so that it will be ignored by our Spotless
 *     // rules).
 *     srcDir       = BUILD_CONSTANTS_AUTOGEN_PATH
 *     classPackage = 'com.team2813'
 *     className    = 'BuildConstants'
 *     dateFormat   = 'yyyy-MM-dd HH:mm:ss z'
 *     timeZone     = 'America/Los_Angeles' // Use preferred time zone
 *     indent       = '  '
 * }
 * sourceSets.main.java.srcDirs += BUILD_CONSTANTS_AUTOGEN_PATH
 * ...
 * }</pre>
 */
public class BuildConstantsPublisher {
  public static final String TABLE_NAME = "Metadata";
  // No publisher for BuildConstants.MAVEN_GROUP because it is always empty.
  private StringPublisher m_mavenNamePublisher;
  // No publisher for BuildConstants.VERSION because it is always "unspecified".
  private IntegerPublisher m_gitRevisionPublisher;
  private StringPublisher m_gitShaPublisher;
  private StringPublisher m_gitDatePublisher;
  private StringPublisher m_gitBranchPublisher;
  private StringPublisher m_buildDatePublisher;
  private IntegerPublisher m_buildUnixTimePublisher;
  private IntegerPublisher m_dirtyPublisher;

  /**
   * Constructs a BuildConstantsPublisher.
   *
   * <p>This constructor creates publishers for each build constant and publishes them to the
   * provided network table instance.
   *
   * @param ntInstance
   */
  public BuildConstantsPublisher(NetworkTableInstance ntInstance) {
    NetworkTable table = ntInstance.getTable(TABLE_NAME);
    m_mavenNamePublisher = table.getStringTopic("MavenName").publish();
    m_gitRevisionPublisher = table.getIntegerTopic("GitRevision").publish();
    m_gitShaPublisher = table.getStringTopic("GitSha").publish();
    m_gitDatePublisher = table.getStringTopic("GitDate").publish();
    m_gitBranchPublisher = table.getStringTopic("GitBranch").publish();
    m_buildUnixTimePublisher = table.getIntegerTopic("BuildUnixTime").publish();
    m_buildDatePublisher = table.getStringTopic("BuildDate").publish();
    m_dirtyPublisher = table.getIntegerTopic("Dirty").publish();
  }

  /**
   * Publishes build constants to NetworkTables.
   *
   * <p>This is typically called once during robot initialization.
   */
  public void publish() {
    m_mavenNamePublisher.set(BuildConstants.MAVEN_NAME);
    m_gitRevisionPublisher.set(BuildConstants.GIT_REVISION);
    m_gitShaPublisher.set(BuildConstants.GIT_SHA);
    m_gitDatePublisher.set(BuildConstants.GIT_DATE);
    m_gitBranchPublisher.set(BuildConstants.GIT_BRANCH);
    m_buildDatePublisher.set(BuildConstants.BUILD_DATE);
    m_buildUnixTimePublisher.set(BuildConstants.BUILD_UNIX_TIME);
    m_dirtyPublisher.set(BuildConstants.DIRTY);
  }
}
