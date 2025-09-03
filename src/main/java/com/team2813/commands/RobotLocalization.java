package com.team2813.commands;

import static com.team2813.vision.VisionNetworkTables.HAS_DATA_TOPIC;
import static com.team2813.vision.VisionNetworkTables.VISIBLE_APRIL_TAG_POSES_TOPIC;

import com.pathplanner.lib.auto.AutoBuilder;
import com.pathplanner.lib.path.GoalEndState;
import com.pathplanner.lib.path.PathConstraints;
import com.pathplanner.lib.path.PathPlannerPath;
import com.pathplanner.lib.path.Waypoint;
import com.team2813.lib2813.preferences.PersistedConfiguration;
import com.team2813.subsystems.Drive;
import com.team2813.vision.VisionNetworkTables;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.networktables.*;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructArrayPublisher;
import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import org.json.simple.parser.ParseException;

/*
TODO:
  8/8/2025:
  * Make robot localization use photonvision,
    as now since I deleted the limelight impl. it is useless.
 */
public class RobotLocalization {
  private static final Pose3d[] EMPTY_POSE3D_ARRAY = new Pose3d[0];
  private final Configuration config;
  private final StructPublisher<Pose2d> lastPosePublisher;
  private final BooleanPublisher hasDataPublisher;
  private final StructArrayPublisher<Pose3d> visibleAprilTagPosesPublisher;

  /** Holder for all configuration for {@link RobotLocalization}. */
  public record Configuration(boolean useAutoAlignWaypoints) {

    /** Creates an instance from preference values stored in the robot's flash memory. */
    public static Configuration fromPreferences() {
      return PersistedConfiguration.fromPreferences("RobotLocalization", Configuration.class);
    }
  }

  public RobotLocalization(NetworkTableInstance networkTableInstance) {
    this(networkTableInstance, Configuration.fromPreferences());
  }

  RobotLocalization(NetworkTableInstance networkTableInstance, Configuration config) {
    this.config = config;

    lastPosePublisher =
        networkTableInstance.getStructTopic("Auto Align to", Pose2d.struct).publish();
    NetworkTable limelightNetworkTable =
        VisionNetworkTables.getTableForLimelight(networkTableInstance);
    hasDataPublisher = limelightNetworkTable.getBooleanTopic(HAS_DATA_TOPIC).publish();
    visibleAprilTagPosesPublisher =
        limelightNetworkTable
            .getStructArrayTopic(VISIBLE_APRIL_TAG_POSES_TOPIC, Pose3d.struct)
            .publish();
  }

  /** TODO: Dummy method, implement sometime. */
  public void visionLocation() {
    //    LocationalData locationalData = limelight.getLocationalData();
    //    hasDataPublisher.accept(locationalData.isValid());
    //
    //    Collection<Pose3d> visibleAprilTagPoses =
    // locationalData.getVisibleAprilTagPoses().values();
    //    visibleAprilTagPosesPublisher.accept(visibleAprilTagPoses.toArray(EMPTY_POSE3D_ARRAY));
    //
    //    Optional<BotPoseEstimate> optionalEstimate = botPoseEstimateBlue(locationalData);
    //    limelightPosePublisher.publish(optionalEstimate);
    //
    //    return optionalEstimate;
  }

  // TODO: Dummy method, implement sometime.
  private static void botPoseEstimateBlue(/*LocationalData locationalData*/ ) {
    //    return locationalData.getBotPoseEstimate().map(RobotContainer::toBotposeBlue);
  }

  private static List<Pose2d> positions() {
    List<Pose2d> arrayOfPos = new ArrayList<>();

    arrayOfPos.add(new Pose2d(3.194, 4.189, Rotation2d.fromDegrees(0))); // *
    arrayOfPos.add(new Pose2d(3.223, 3.852, Rotation2d.fromDegrees(0))); // 1r *

    arrayOfPos.add(new Pose2d(3.988, 5.215, Rotation2d.fromDegrees(-60))); // 2l *
    arrayOfPos.add(new Pose2d(3.704, 5.051, Rotation2d.fromDegrees(-60))); // 2r *

    arrayOfPos.add(new Pose2d(5.283, 5.042, Rotation2d.fromDegrees(-120))); // 3l *
    arrayOfPos.add(new Pose2d(4.994, 5.225, Rotation2d.fromDegrees(-120))); // 3r*

    arrayOfPos.add(new Pose2d(5.8, 4.186, Rotation2d.fromDegrees(180))); // 4l*
    arrayOfPos.add(new Pose2d(5.8, 3.857, Rotation2d.fromDegrees(180))); // 4r *

    arrayOfPos.add(new Pose2d(5.286, 3.017, Rotation2d.fromDegrees(120))); // 5l*
    arrayOfPos.add(new Pose2d(4.988, 2.838, Rotation2d.fromDegrees(120))); // 5r *

    arrayOfPos.add(new Pose2d(3.699, 3.004, Rotation2d.fromDegrees(60))); // 6l *
    arrayOfPos.add(new Pose2d(3.981, 2.840, Rotation2d.fromDegrees(60))); // 6r*

    return arrayOfPos;
  }

  private static List<Pose2d> leftPositions() {
    List<Pose2d> positions = positions();
    int size = positions.size();
    List<Pose2d> arrayOfPos = new ArrayList<>(size / 2);
    for (int i = 0; i < size; i += 2) {
      arrayOfPos.add(positions.get(i));
    }
    return arrayOfPos;
  }

  private static List<Pose2d> rightPositions() {
    List<Pose2d> positions = positions();
    int size = positions.size();
    List<Pose2d> arrayOfPos = new ArrayList<>(size / 2);
    for (int i = 1; i < size; i += 2) {
      arrayOfPos.add(positions.get(i));
    }
    return arrayOfPos;
  }

  /**
   * Creates a command from the current position to the nearest target.
   *
   * @param drivePosSupplier Provides the current robot position (in the blue coordinate system).
   * @param targets Locations to place coral, one for each of the sides of the coral reef.
   */
  private Command createPath(Supplier<Pose2d> drivePosSupplier, List<Pose2d> targets) {
    Pose2d currentPose = drivePosSupplier.get();
    if (Drive.onRed()) {
      currentPose =
          new Pose2d(
              17.55 - currentPose.getX(),
              8.052 - currentPose.getY(),
              currentPose.getRotation().plus(new Rotation2d(Math.PI)));
    }

    Pose2d newPosition = currentPose.nearest(targets);
    lastPosePublisher.set(newPosition);

    List<Waypoint> waypoints = PathPlannerPath.waypointsFromPoses(currentPose, newPosition);

    PathConstraints constraints = new PathConstraints(3.0, 3.0, 2 * Math.PI, 4 * Math.PI);

    PathPlannerPath path =
        new PathPlannerPath(
            waypoints, constraints, null, new GoalEndState(0.0, newPosition.getRotation())
            // new GoalEndState(0.0, newPosition.getRotation())
            );
    return AutoBuilder.followPath(path);
  }

  public Command getLeftAutoAlignCommand(Supplier<Pose2d> drivePosSupplier) {
    if (config.useAutoAlignWaypoints) {
      return createPath(drivePosSupplier, leftPositions());
    } else {
      // TODO: be able to use left ones only
      return createPathfindCommand();
    }
  }

  public Command getRightAutoAlignCommand(Supplier<Pose2d> drivePosSupplier) {
    if (config.useAutoAlignWaypoints) {
      return createPath(drivePosSupplier, rightPositions());
    } else {
      // TODO: be able to use right ones only
      return createPathfindCommand();
    }
  }

  private Command createPathfindCommand() {
    // TODO: use more than this command
    String pathName = "aaaalign";
    PathPlannerPath path;
    try {
      path = PathPlannerPath.fromPathFile(pathName);
    } catch (IOException | ParseException e) {
      return Commands.print(
          String.format("An error occurred when reading the path file \"%s\": ", e.getMessage()));
    }

    PathConstraints constraints = new PathConstraints(3.0, 3.0, 2 * Math.PI, 4 * Math.PI);
    return AutoBuilder.pathfindThenFollowPath(path, constraints);
  }
}
