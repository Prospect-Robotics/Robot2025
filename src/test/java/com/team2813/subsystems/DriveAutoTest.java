package com.team2813.subsystems;

import static com.google.common.truth.Truth.assertThat;
import static com.team2813.lib2813.testing.truth.Translation2dSubject.assertThat;

import com.pathplanner.lib.auto.AutoBuilder;
import com.pathplanner.lib.path.GoalEndState;
import com.pathplanner.lib.path.IdealStartingState;
import com.pathplanner.lib.path.PathConstraints;
import com.pathplanner.lib.path.PathPlannerPath;
import com.pathplanner.lib.path.Waypoint;
import com.pathplanner.lib.util.FlippingUtil;
import com.team2813.FakeShuffleboardTabs;
import com.team2813.IsolatedNetworkTablesExtension;
import com.team2813.RobotContainer;
import com.team2813.ShuffleboardTabs;
import com.team2813.lib2813.testing.junit.jupiter.CommandTester;
import com.team2813.lib2813.testing.junit.jupiter.WPILibExtension;
import com.team2813.lib2813.testing.truth.Pose2dSubject;
import edu.wpi.first.hal.AllianceStationID;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Translation2d;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructSubscriber;
import edu.wpi.first.networktables.StructTopic;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import edu.wpi.first.wpilibj.simulation.PS4ControllerSim;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.WaitCommand;
import java.util.List;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;

@ExtendWith({IsolatedNetworkTablesExtension.class, WPILibExtension.class})
public class DriveAutoTest {

  public static final Pose2d STARTING_POSE = new Pose2d(5, 1, Rotation2d.k180deg);
  public static final Pose2d ENDING_POSE = new Pose2d(3, 1, Rotation2d.k180deg);

  private static PathPlannerPath createPath() {
    List<Waypoint> waypoints = PathPlannerPath.waypointsFromPoses(STARTING_POSE, ENDING_POSE);
    PathConstraints constraints = PathConstraints.unlimitedConstraints(6);
    IdealStartingState idealStartingState = new IdealStartingState(0, Rotation2d.k180deg);
    GoalEndState goalEndState = new GoalEndState(0, Rotation2d.k180deg);
    return new PathPlannerPath(waypoints, constraints, idealStartingState, goalEndState);
  }

  private final PathPlannerPath path = createPath();
  private final ShuffleboardTabs shuffleboardTabs = new FakeShuffleboardTabs();

  @ParameterizedTest
  @EnumSource(
      value = AllianceStationID.class,
      names = {"Blue1", "Red1"})
  public void auto(
      AllianceStationID stationID, NetworkTableInstance ntInstance, CommandTester commandTester) {
    // Set up DS sim for this test
    DriverStationSim.setAllianceStationId(stationID);
    DriverStationSim.setDsAttached(true);
    DriverStationSim.notifyNewData();
    NetworkTable driveTable = ntInstance.getTable("Drive");
    StructTopic<Pose2d> poseTopic = driveTable.getStructTopic("current pose", Pose2d.struct);
    try (RobotContainer robotContainer = new RobotContainer(shuffleboardTabs, ntInstance);
        StructSubscriber<Pose2d> poseSubscriber = poseTopic.subscribe(null)) {
      // set starting position
      Pose2d startingPose = STARTING_POSE;
      if (stationID == AllianceStationID.Blue1) {
        assertThat(AutoBuilder.shouldFlip()).isFalse();
      } else {
        assertThat(AutoBuilder.shouldFlip()).isTrue();
        startingPose = FlippingUtil.flipFieldPose(startingPose);
      }
      robotContainer.setPose(startingPose);
      commandTester.runUntilComplete(Commands.none());
      // assert that our update succeeded
      Pose2dSubject.assertThat(startingPose).isWithin(1e-6).of(poseSubscriber.get());

      // create and run path
      PathPlannerPath path = createPath();
      assertThat(path.preventFlipping).isFalse();
      Command toRun = AutoBuilder.followPath(path);
      commandTester.runUntilComplete(toRun);
      Pose2d finalPose = poseSubscriber.get();

      // assert we moved left 2 meters
      Translation2d expected = new Translation2d(2, 0);
      if (stationID == AllianceStationID.Red1) {
        expected = expected.unaryMinus();
      }
      assertThat(startingPose.getTranslation().minus(finalPose.getTranslation()))
          .isWithin(0.3)
          .of(expected);
    } finally {
      // clean up even if an exception was thrown
      DriverStationSim.resetData();
      DriverStationSim.notifyNewData();
    }
  }

  @ParameterizedTest
  @EnumSource(
      value = AllianceStationID.class,
      names = {"Blue1", "Red1"})
  public void forward(
      AllianceStationID stationID, NetworkTableInstance ntInstance, CommandTester commandTester) {
    // Set up DS sim for this test
    DriverStationSim.setAllianceStationId(stationID);
    DriverStationSim.setDsAttached(true);
    DriverStationSim.notifyNewData();
    PS4ControllerSim controllerSim = new PS4ControllerSim(0);
    NetworkTable driveTable = ntInstance.getTable("Drive");
    StructTopic<Pose2d> poseTopic = driveTable.getStructTopic("current pose", Pose2d.struct);

    try (RobotContainer robotContainer = new RobotContainer(shuffleboardTabs, ntInstance);
        StructSubscriber<Pose2d> poseSubscriber = poseTopic.subscribe(null)) {
      // Update our starting position (and make sure flipping is working properly)
      Pose2d startingPose = STARTING_POSE;
      if (stationID == AllianceStationID.Blue1) {
        assertThat(AutoBuilder.shouldFlip()).isFalse();
      } else {
        assertThat(AutoBuilder.shouldFlip()).isTrue();
        startingPose = FlippingUtil.flipFieldPose(startingPose);
      }
      robotContainer.setPose(startingPose);
      commandTester.runUntilComplete(Commands.none());
      // assert that our update succeeded
      Pose2dSubject.assertThat(startingPose).isWithin(1e-6).of(poseSubscriber.get());

      // Follow the path
      Command toRun = AutoBuilder.followPath(path).withTimeout(15);
      commandTester.runUntilComplete(toRun);
      startingPose = poseSubscriber.get();

      // hold forward in teleop
      DriverStationSim.setEnabled(true);
      DriverStationSim.notifyNewData();
      controllerSim.setLeftY(-1);
      controllerSim.notifyNewData();

      // run for 4 seconds
      commandTester.runUntilComplete(new WaitCommand(4));
      Pose2d finalPose = AutoBuilder.getCurrentPose();

      if (stationID == AllianceStationID.Blue1) {
        // assert we moved right
        assertThat(startingPose.getX()).isLessThan(finalPose.getX());
      } else {
        // assert we moved left
        assertThat(startingPose.getX()).isGreaterThan(finalPose.getX());
      }
    } finally {
      // clean up even if an exception was thrown
      DriverStationSim.resetData();
      DriverStationSim.notifyNewData();
      controllerSim.setLeftY(0);
      controllerSim.notifyNewData();
    }
  }
}
