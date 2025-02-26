package com.team2813.commands;

import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.networktables.BooleanPublisher;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructArrayPublisher;

import com.team2813.lib2813.limelight.Limelight;
import com.team2813.AllPreferences;
import com.pathplanner.lib.path.GoalEndState;
import com.pathplanner.lib.path.PathPlannerPath;
import com.pathplanner.lib.path.Waypoint;

import java.util.*;
import java.util.function.BooleanSupplier;
import java.util.function.DoubleSupplier;
import java.util.function.Supplier;

import com.pathplanner.lib.path.PathConstraints;


public class RobotLocalization { // TODO: consider making this a subsystem so we can use periodic()
    private static final Limelight limelight = Limelight.getDefaultLimelight();
    private final BooleanSupplier useLimelightLocation;
    private final DoubleSupplier maxLimelightError;

    public RobotLocalization() {
        useLimelightLocation = AllPreferences.useLimelightLocation();
        maxLimelightError = AllPreferences.maxLimelightError();
    }

    public Optional<Pose2d> limelightRobotPose() {
        if (!useLimelightLocation.getAsBoolean()) {
            return Optional.empty();
        }
        return rawLimelightRobotPose();
    }

    private Optional<Pose2d> rawLimelightRobotPose() {
        return limelight.getLocationalData().getBotposeBlue().map(Pose3d::toPose2d);
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

        arrayOfPos.add(new Pose2d(2.826, 4.196, Rotation2d.fromDegrees(179.503))); //* 
        arrayOfPos.add(new Pose2d(2.828, 3.866, Rotation2d.fromDegrees(179.503))); //1r * 
        arrayOfPos.add(new Pose2d(3.784, 5.527, Rotation2d.fromDegrees(121.217))); //2l *
        arrayOfPos.add(new Pose2d(3.497, 5.367, Rotation2d.fromDegrees(121.624))); //2r *
        arrayOfPos.add(new Pose2d(5.147, 5.550, Rotation2d.fromDegrees(61.367))); //3l * 
        arrayOfPos.add(new Pose2d(5.456, 5.377, Rotation2d.fromDegrees(60.198))); //3r* 
        arrayOfPos.add(new Pose2d(6.148, 4.181, Rotation2d.fromDegrees(-0.564))); //4l *
        arrayOfPos.add(new Pose2d(6.143, 3.857, Rotation2d.fromDegrees(-0.564))); //4r*
        arrayOfPos.add(new Pose2d(5.448, 2.662, Rotation2d.fromDegrees(-60.854))); //5l*
        arrayOfPos.add(new Pose2d(5.166, 2.499, Rotation2d.fromDegrees(-60.854))); //5r *
        arrayOfPos.add(new Pose2d(3.825, 2.492, Rotation2d.fromDegrees(-121.125))); //6l * 
        arrayOfPos.add(new Pose2d(3.503, 2.682, Rotation2d.fromDegrees(-121.125))); //6r*

        return arrayOfPos;
    }

    public PathPlannerPath createPath(Supplier<Pose2d> drivePosSupplier) {
        Pose2d currentPose = limelightRobotPose().orElseGet(drivePosSupplier);
        //Pose2d newPosition = currentPose.nearest(positions());
        Pose2d newPosition = new Pose2d(2.826, 4.196, Rotation2d.fromDegrees(0));

        List<Waypoint> waypoints = PathPlannerPath.waypointsFromPoses(
            //currentPose,
            //new Pose2d(currentPose.getX(), currentPose.getY(), Rotation2d.fromDegrees(0)),
            //new Pose2d(currentPose.getX(), currentPose.getY(), currentPose.getRotation()),
            new Pose2d(currentPose.getX(), currentPose.getY(), Rotation2d.fromDegrees(0)),
            newPosition
        );

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

        PathPlannerPath path = new PathPlannerPath(
                waypoints,
                constraints,
                null,
                new GoalEndState(0.0, Rotation2d.fromDegrees(179.503))
                //new GoalEndState(0.0, newPosition.getRotation())
        );
        return path;
    }

    private final StructArrayPublisher<Pose2d> botpose = NetworkTableInstance.getDefault().getStructArrayTopic("Limelight pose", Pose2d.struct).publish();
    private final BooleanPublisher hasData = NetworkTableInstance.getDefault().getBooleanTopic("Has Limelight Data").publish();
    private static final Pose2d[] NO_POS = new Pose2d[0];

    public void updateDashboard() {
        botpose.set(rawLimelightRobotPose().map(pos -> new Pose2d[]{pos}).orElse(NO_POS));
        hasData.accept(limelight.getJsonDump().isPresent());
    }

}