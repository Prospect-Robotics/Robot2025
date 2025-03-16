package com.team2813.commands;

import com.pathplanner.lib.auto.AutoBuilder;
import com.pathplanner.lib.path.GoalEndState;
import com.pathplanner.lib.path.PathConstraints;
import com.pathplanner.lib.path.PathPlannerPath;
import com.pathplanner.lib.path.Waypoint;
import com.team2813.AllPreferences;
import com.team2813.RobotContainer;
import com.team2813.lib2813.limelight.Limelight;
import com.team2813.subsystems.Drive;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructArrayPublisher;
import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.BooleanSupplier;
import java.util.function.Supplier;
import org.json.simple.parser.ParseException;

public class RobotLocalization { // TODO: consider making this a subsystem so we can use periodic()
  private static final Limelight limelight = Limelight.getDefaultLimelight();
  private final BooleanSupplier useLimelightLocation;

  public record Location(Pose2d pos, double timestampSeconds) {}

  public RobotLocalization() {
    useLimelightLocation = AllPreferences.useLimelightLocation();
  }

  public Optional<Location> limelightLocation() {
    if (!useLimelightLocation.getAsBoolean()) {
      return Optional.empty();
    }
    return rawLocation();
  }

  private Optional<Location> rawLocation() {
    // TODO: Update lib2813 limelight code to include the time in LocationalData.
    return limelight
        .getLocationalData()
        .getBotpose()
        .map(Pose3d::toPose2d)
        .map(RobotContainer::toBotposeBlue)
        .map(pos -> new Location(pos, System.currentTimeMillis()));
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

    arrayOfPos.add(new Pose2d(4.988, 2.838, Rotation2d.fromDegrees(120))); // 5l*
    arrayOfPos.add(new Pose2d(5.286, 3.017, Rotation2d.fromDegrees(120))); // 5r *

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

  private final StructPublisher<Pose2d> lastPose =
      NetworkTableInstance.getDefault().getStructTopic("Auto Align to", Pose2d.struct).publish();

  private Command createPath(Supplier<Pose2d> drivePosSupplier, List<Pose2d> positions) {

    Pose2d currentPose = drivePosSupplier.get();
    Pose2d newPosition;
    if (Drive.onRed()) {
      Pose2d mirroredPose =
          new Pose2d(
              17.55 - currentPose.getX(),
              8.052 - currentPose.getY(),
              currentPose.getRotation().plus(new Rotation2d(Math.PI)));
      newPosition = mirroredPose.nearest(positions);
      newPosition =
          new Pose2d(
              17.55 - newPosition.getX(),
              8.052 - newPosition.getY(),
              newPosition.getRotation().plus(new Rotation2d(Math.PI)));
    } else {
      newPosition = currentPose.nearest(positions);
    }
    lastPose.set(newPosition);

    List<Waypoint> waypoints = PathPlannerPath.waypointsFromPoses(currentPose, newPosition);

    PathConstraints constraints = new PathConstraints(3.0, 3.0, 2 * Math.PI, 4 * Math.PI);

    PathPlannerPath path =
        new PathPlannerPath(
            waypoints, constraints, null, new GoalEndState(0.0, newPosition.getRotation())
            // new GoalEndState(0.0, newPosition.getRotation())
            );
    return AutoBuilder.followPath(path);
  }

  public Command getAutoAlignCommand(Supplier<Pose2d> drivePosSupplier) {
    if (AllPreferences.useAutoAlignWaypoints().getAsBoolean()) {
      return createPath(drivePosSupplier, positions());
    } else {
      return createPathfindCommand();
    }
  }

  public Command getLeftAutoAlignCommand(Supplier<Pose2d> drivePosSupplier) {
    if (AllPreferences.useAutoAlignWaypoints().getAsBoolean()) {
      return createPath(drivePosSupplier, leftPositions());
    } else {
      // TODO: be able to use left ones only
      return createPathfindCommand();
    }
  }

  public Command getRightAutoAlignCommand(Supplier<Pose2d> drivePosSupplier) {
    if (AllPreferences.useAutoAlignWaypoints().getAsBoolean()) {
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
          String.format("An error occured when reading the path file \"%s\": ", e.getMessage()));
    }

    PathConstraints constraints = new PathConstraints(3.0, 3.0, 2 * Math.PI, 4 * Math.PI);
    return AutoBuilder.pathfindThenFollowPath(path, constraints);
  }

  private final StructArrayPublisher<Pose2d> botpose =
      NetworkTableInstance.getDefault()
          .getStructArrayTopic("Limelight pose", Pose2d.struct)
          .publish();
  private final BooleanPublisher hasData =
      NetworkTableInstance.getDefault().getBooleanTopic("Has Limelight Data").publish();
  private static final Pose2d[] NO_POS = new Pose2d[0];

  public void updateDashboard() {
    botpose.set(rawLocation().map(location -> new Pose2d[] {location.pos()}).orElse(NO_POS));
    hasData.accept(limelight.getJsonDump().isPresent());
  }
}
