package com.team2813.simulation;

import com.ctre.phoenix6.swerve.SimSwerveDrivetrain;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructArrayPublisher;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import org.ironmaple.simulation.SimulatedArena;

public class MapleSim extends SubsystemBase {

//    final SimSwerveDrivetrain simSwerveDrivetrain;

    private final SimulatedArena simulatedArena;

    public MapleSim(/*SimSwerveDrivetrain simSwerveDrivetrain,*/ SimulatedArena simulatedArena) {
//        this.simSwerveDrivetrain = simSwerveDrivetrain;
        this.simulatedArena = simulatedArena;

        }

    private final StructArrayPublisher<Pose3d> notesPoses = NetworkTableInstance.getDefault()
            .getStructArrayTopic("MyPoseArray", Pose3d.struct)
            .publish();

    @Override
    public void periodic() {
        notesPoses.accept(SimulatedArena.getInstance()
                .getGamePiecesArrayByType("Coral"));
    }
}