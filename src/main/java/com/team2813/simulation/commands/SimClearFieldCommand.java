package com.team2813.simulation.commands;

import edu.wpi.first.wpilibj2.command.Command;
import org.ironmaple.simulation.SimulatedArena;

public class SimClearFieldCommand extends Command {
    private final SimulatedArena simulatedArena;

    public SimClearFieldCommand(
            SimulatedArena simulatedArena
    )
    {
        this.simulatedArena = simulatedArena;
    }

    @Override
    public void execute() {
        // Should clear the game pieces and place new ones.
        // [ ] TODO: Ensure the placing of new pieces works.

        simulatedArena.clearGamePieces();
        andThen(simulatedArena::placeGamePiecesOnField);
    }
}
