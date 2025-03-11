package com.team2813.commands;

import com.pathplanner.lib.auto.AutoBuilder;
import com.pathplanner.lib.path.GoalEndState;
import com.pathplanner.lib.path.PathConstraints;
import com.pathplanner.lib.path.PathPlannerPath;
import com.pathplanner.lib.path.Waypoint;
import com.team2813.AllPreferences;
import com.team2813.lib2813.limelight.Limelight;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructArrayPublisher;
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
        .getBotposeBlue()
        .map(Pose3d::toPose2d)
        .map(pos -> new Location(pos, System.currentTimeMillis()));
  }

  /*private static ArrayList<Pose2d> positions() {
      Pose2d one = new Pose2d(2.826,4.008,new Rotation2d(0));
      Pose2d two = new Pose2d(3.666,5.46,new Rotation2d(0));
      Pose2d three = new Pose2d(5.245,5.487,new Rotation2d(0));
      Pose2d four = new Pose2d(6.147,3.995,new Rotation2d(0));
      Pose2d five = new Pose2d(5.343,2.595,new Rotation2d(0));
      Pose2d six = new Pose2d(3.699,2.563,new Rotation2d(0));

      ArrayList<Pose2d> arrayOfPos = new ArrayList<Pose2d>();
      arrayOfPos.add(one);
      arrayOfPos.add(two);
      arrayOfPos.add(three);
      arrayOfPos.add(four);
      arrayOfPos.add(five);
      arrayOfPos.add(six);

      return arrayOfPos;
  }*/

  private static List<Pose2d> positions() {
    List<Pose2d> arrayOfPos = new ArrayList<>();

    arrayOfPos.add(new Pose2d(3.194, 4.189, Rotation2d.fromDegrees(0))); // *
    arrayOfPos.add(new Pose2d(3.223, 3.852, Rotation2d.fromDegrees(0))); // 1r *

    arrayOfPos.add(new Pose2d(3.988, 5.215, Rotation2d.fromDegrees(-60))); // 2l *
    arrayOfPos.add(new Pose2d(3.704, 5.051, Rotation2d.fromDegrees(-60))); // 2r *

    arrayOfPos.add(new Pose2d(5.283, 5.042, Rotation2d.fromDegrees(-120))); // 3l *
    arrayOfPos.add(new Pose2d(4.994, 5.225, Rotation2d.fromDegrees(-120))); // 3r*

    arrayOfPos.add(new Pose2d(5.8, 3.857, Rotation2d.fromDegrees(180))); // 4l *
    arrayOfPos.add(new Pose2d(5.8, 4.186, Rotation2d.fromDegrees(180))); // 4r*

    arrayOfPos.add(new Pose2d(4.988, 2.838, Rotation2d.fromDegrees(120))); // 5l*
    arrayOfPos.add(new Pose2d(5.286, 3.017, Rotation2d.fromDegrees(120))); // 5r *

    arrayOfPos.add(new Pose2d(3.699, 3.004, Rotation2d.fromDegrees(60))); // 6l *
    arrayOfPos.add(new Pose2d(3.981, 2.840, Rotation2d.fromDegrees(60))); // 6r*

    return arrayOfPos;
  }

  private Command createPath(Supplier<Pose2d> drivePosSupplier) {

    // Pose2d currentPose = limelightLocation().map(Location::pos).orElseGet(drivePosSupplier);
    Pose2d currentPose = drivePosSupplier.get();
    System.out.println("currentPose: " + currentPose);
    // Pose2d newPosition = currentPose.nearest(positions());
    Pose2d newPosition = new Pose2d(3.126, 4.196, Rotation2d.fromDegrees(0));

    List<Waypoint> waypoints =
        PathPlannerPath.waypointsFromPoses(
            currentPose,
            // new Pose2d(currentPose.getX(), currentPose.getY(), Rotation2d.fromDegrees(0)),
            // new Pose2d(currentPose.getX(), currentPose.getY(), currentPose.getRotation()),
            // new Pose2d(currentPose.getX(), currentPose.getY(), Rotation2d.fromDegrees(0)),
            // currentPose,
            newPosition);

    /*List<Waypoint> waypoints = PathPlannerPath.waypointsFromPoses(
        currentPose,
        new Pose2d(currentPose.getX(), currentPose.getY(), currentPose.getRotation()),
        new Pose2d(2.826, 4.196, Rotation2d.fromDegrees(179.503)) //*
        //new Pose2d(2.828, 3.866, Rotation2d.fromDegrees(179.503) //1r *

        //new Pose2d(3.784, 5.527, Rotation2d.fromDegrees(121.217)) //2l *
        //new Pose2d(3.497, 5.367, Rotation2d.fromDegrees(121.624)) //2r *

        //new Pose2d(5.147, 5.550, Rotation2d.fromDegrees(61.367)) //3l *
        //new Pose2d(5.456, 5.377, Rotation2d.fromDegrees(60.198)) //3r*

        //new Pose2d(6.148, 4.181, Rotation2d.fromDegrees(-0.564)) //4l *
        //new Pose2d(6.143, 3.857, Rotation2d.fromDegrees(-0.564)) //4r*

        //new Pose2d(5.448, 2.662, Rotation2d.fromDegrees(-60.854)) //5l*
        //new Pose2d(5.166, 2.499, Rotation2d.fromDegrees(-60.854)) //5r *

        //new Pose2d(3.825, 2.492, Rotation2d.fromDegrees(-121.125)) //6l *
        //new Pose2d(3.503, 2.682, Rotation2d.fromDegrees(-121.125)) //6r*
    );*/

    PathConstraints constraints = new PathConstraints(3.0, 3.0, 2 * Math.PI, 4 * Math.PI);

    PathPlannerPath path =
        new PathPlannerPath(
            waypoints, constraints, null, new GoalEndState(0.0, Rotation2d.fromDegrees(0))
            // new GoalEndState(0.0, newPosition.getRotation())
            );
    return AutoBuilder.followPath(path);
  }

  public Command getAutoAlignCommand(Supplier<Pose2d> drivePosSupplier) {
    if (AllPreferences.useAutoAlignWaypoints().getAsBoolean()) {
      return createPath(drivePosSupplier);
    } else {
      return createPathfindCommand();
    }
  }

  private Command createPathfindCommand() {
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
