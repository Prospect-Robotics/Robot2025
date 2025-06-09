package com.team2813.simulation;

import edu.wpi.first.math.system.plant.DCMotor;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Distance;
import edu.wpi.first.units.measure.ImmutableDistance;
import edu.wpi.first.units.measure.ImmutableMass;
import edu.wpi.first.units.measure.Mass;
import org.ironmaple.simulation.drivesims.COTS;
import org.ironmaple.simulation.drivesims.GyroSimulation;
import org.ironmaple.simulation.drivesims.configs.DriveTrainSimulationConfig;

// Legally Distinct from SimulatedSwerveDriveTrain
public class SimulatedDrive {
    private SimulatedDrive() {}

    public static DriveTrainSimulationConfig getDriveConfigs() {
        Mass robotMass = new ImmutableMass(115, 0, Units.Kilogram); // Robot weighs about 115 kg.

        Distance bumperLengthAndWidth = new ImmutableDistance(81.5, 0, Units.Centimeter); // Maelstrom is square.
        Distance robotLengthAndWidth = new ImmutableDistance(65.5, 0, Units.Centimeter); // Maelstrom is square.

        DriveTrainSimulationConfig driveTrainSimulationConfig = new DriveTrainSimulationConfig(robotMass,
                bumperLengthAndWidth,
                bumperLengthAndWidth,
                robotLengthAndWidth,
                robotLengthAndWidth,
                COTS.ofPigeon2(),
                COTS.ofMark4i(
                        DCMotor.getKrakenX60(1), // Difference between KrakenX60FOC unknown.
                        DCMotor.getKrakenX60(1),
                        COTS.WHEELS.DEFAULT_NEOPRENE_TREAD.cof, // About: 1.426
                        2)
                );

        return driveTrainSimulationConfig;
    }
}
