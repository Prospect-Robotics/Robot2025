package com.team2813.subsystems;

import static edu.wpi.first.units.Units.*;

import com.team2813.simulation.SimulatedDriveConfigurator;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Translation2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.wpilibj.smartdashboard.Field2d;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.ironmaple.simulation.SimulatedArena;
import org.ironmaple.simulation.drivesims.SelfControlledSwerveDriveSimulation;
import org.ironmaple.simulation.drivesims.SwerveDriveSimulation;

// Legally Distinct from SimulatedSwerveDriveTrain
public class MapleSimDrive implements DriveInterface {
  private final SelfControlledSwerveDriveSimulation simulatedDrive;
  private final Field2d field2d;

  public MapleSimDrive(/*NetworkTableInstance networkTableInstance*/ ) {
    var config = SimulatedDriveConfigurator.getDriveConfigs();

    this.simulatedDrive =
        new SelfControlledSwerveDriveSimulation(
            new SwerveDriveSimulation(
                config, new Pose2d(Meters.of(2), Meters.of(2), new Rotation2d(Degrees.of(180)))));

    SimulatedArena.getInstance().addDriveTrainSimulation(simulatedDrive.getDriveTrainSimulation());

    field2d = new Field2d();
    SmartDashboard.putData("simulation field", field2d);
  }

  @Override
  public void drive(ChassisSpeeds demand) {
    this.simulatedDrive.runChassisSpeeds(
        demand,
        new Translation2d(), // NOTE: We may need to mess with the Translation 2d stuff and other
        // inputs.
        true,
        true);
  }

  @Override
  public void drive(double xSpeed, double ySpeed, double rotation) {
    ChassisSpeeds demand = new ChassisSpeeds(xSpeed, ySpeed, rotation);

    this.simulatedDrive.runChassisSpeeds(
        demand,
        new Translation2d(), // NOTE: We may need to mess with the Translation 2d stuff and other
        // inputs.
        true,
        true);
  }

  @Override
  public Pose2d getPose() {
    return simulatedDrive.getOdometryEstimatedPose();
  }

  @Override
  public void resetPose() {
    Pose2d originalPose = simulatedDrive.getOdometryEstimatedPose();
    Pose2d seededPose = new Pose2d(originalPose.getTranslation(), new Rotation2d(Radians.of(0)));
    simulatedDrive.setSimulationWorldPose(seededPose);
  }

  @Override
  public void setPose(Pose2d pose) {
    simulatedDrive.setSimulationWorldPose(pose);
    simulatedDrive.resetOdometry(pose);
  }

  @Override
  public ChassisSpeeds getRobotRelativeSpeeds() {
    return simulatedDrive.getActualSpeedsFieldRelative();
  }

  @Override
  public void enableSlowMode(boolean enable) {
    // TODO: add slow mode implementation someday.
  }

  @Override
  public void close() {
    // Note: This likely won't have anything in it unless we do photonVision.
    // Note: Holy crap, I was wrong.
    field2d.close();
  }
}
