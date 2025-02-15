package com.team2813.commands;

import java.util.function.BooleanSupplier;

import edu.wpi.first.wpilibj2.command.Subsystem;
import edu.wpi.first.wpilibj2.command.WaitUntilCommand;

public class LockFunctionCommand extends WaitUntilCommand {

    private final Runnable function;

    public LockFunctionCommand(BooleanSupplier condition, Runnable function) {
        super(condition);
        this.function = function;
    }

    public LockFunctionCommand(BooleanSupplier condition, Runnable function, Subsystem... requirements) {
        super(condition);
        this.function = function;
        addRequirements(requirements);
    }

	@Override
    public void initialize() {
        function.run();
    }
}