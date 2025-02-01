package com.team2813.commands;

import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Translation2d;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import com.team2813.util.Limelight;
import com.pathplanner.lib.path.GoalEndState;
import com.pathplanner.lib.path.PathPlannerPath;
import com.pathplanner.lib.path.Waypoint;

import java.util.List;
import java.util.Optional;

import com.pathplanner.lib.path.PathConstraints;

public class RobotLocalization {
    private Limelight limelight;

    public RobotLocalization(Limelight limelight) {
        this.limelight = limelight;
    }

    public Pose2d getRobotPose() {
        Optional<Pose2d> botpose = limelight.getPosition();
        if (!botpose.isPresent()) return new Pose2d();
        Pose2d botpose2 = (Pose2d) botpose.get();
        return new Pose2d(new Translation2d(botpose2.getX(), botpose2.getY()), botpose2.getRotation());
    }

    Pose2d currentPose = getRobotPose();

    List<Waypoint> waypoints = PathPlannerPath.waypointsFromPoses(
            currentPose,
            new Pose2d(currentPose.getX() + 2.0, currentPose.getY(), Rotation2d.fromDegrees(0)),
            new Pose2d(currentPose.getX() + 4.0, currentPose.getY(), Rotation2d.fromDegrees(0))
    );

    PathConstraints constraints = new PathConstraints(3.0, 3.0, 2 * Math.PI, 4 * Math.PI);

    PathPlannerPath path = new PathPlannerPath(
            waypoints,
            constraints,
            null,
            new GoalEndState(0.0, Rotation2d.fromDegrees(-90))
    );
    
    public void updateDashboard() {
        Pose2d pose = getRobotPose();
        SmartDashboard.putNumber("Robot X", pose.getX());
        SmartDashboard.putNumber("Robot Y", pose.getY());
        SmartDashboard.putNumber("Robot Rotation", pose.getRotation().getDegrees());
    }
}