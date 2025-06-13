package com.team2813.simulation;

import static edu.wpi.first.units.Units.*;

import edu.wpi.first.math.system.plant.DCMotor;
import edu.wpi.first.units.measure.Distance;
import edu.wpi.first.units.measure.Mass;
import org.ironmaple.simulation.drivesims.COTS;
import org.ironmaple.simulation.drivesims.configs.DriveTrainSimulationConfig;

/**
 * More so a utility class that assists with the creation of drive train instances/configurations
 * for simulation.
 */
public class SimulatedDriveConfigurator {
  private SimulatedDriveConfigurator() {}

  /**
   * @return The configured DriveTrainSimulationConfig, based on our 2025 robot, Maelstrom.
   */
  public static DriveTrainSimulationConfig getDriveConfigs() {
    Mass robotMass = Pounds.of(115); // Robot weighs about 115 kg.

    Distance bumperLengthAndWidth = Centimeters.of(81.5); // Maelstrom is square.
    Distance robotLengthAndWidth = Centimeters.of(65.5); // Maelstrom is square.

    DriveTrainSimulationConfig driveTrainSimulationConfig =
        new DriveTrainSimulationConfig(
            robotMass,
            bumperLengthAndWidth,
            bumperLengthAndWidth,
            robotLengthAndWidth,
            robotLengthAndWidth,
            COTS.ofPigeon2(),
            COTS.ofMark4i(
                DCMotor.getKrakenX60(1), // Difference between KrakenX60FOC unknown.
                DCMotor.getKrakenX60(1),
                COTS.WHEELS.DEFAULT_NEOPRENE_TREAD.cof, // About: 1.426
                2));

    return driveTrainSimulationConfig;
  }
}
