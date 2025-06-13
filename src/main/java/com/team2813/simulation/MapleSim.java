package com.team2813.simulation;

import com.team2813.subsystems.MapleSimDrive;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructArrayPublisher;
import edu.wpi.first.networktables.StructPublisher;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.ironmaple.simulation.SimulatedArena;

public class MapleSim extends SubsystemBase {

  private final SimulatedArena simulatedArena;
  public final MapleSimDrive mapleSimDrive;
  private final NetworkTableInstance networkTableInstance;
  final StructArrayPublisher<Pose3d> gamePiecePublisher;
  final StructPublisher<Pose2d> drivePublisher;

  public MapleSim(SimulatedArena simulatedArena, NetworkTableInstance networkTableInstance) {
    this.simulatedArena = simulatedArena;

    this.networkTableInstance = networkTableInstance;

    NetworkTable simTable = networkTableInstance.getTable("MapleSim");
    this.gamePiecePublisher = simTable.getStructArrayTopic("Coral Poses", Pose3d.struct).publish();
    this.drivePublisher = simTable.getStructTopic("Drive Pose", Pose2d.struct).publish();

    this.mapleSimDrive = new MapleSimDrive();
  }

  //  private final StructArrayPublisher<Pose3d> notesPoses =
  // NetworkTableInstance.getDefault().getStructArrayTopic("MyPoseArray", Pose3d.struct).publish();

  @Override
  public void periodic() {
    gamePiecePublisher.accept(SimulatedArena.getInstance().getGamePiecesArrayByType("Coral"));
    publish();
  }

  private void publish() {
    //    drivePublisher.set(selfControlledSwerveDriveSimulation.getActualPoseInSimulationWorld());
  }
}
