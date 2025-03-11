package com.team2813.commands;

import edu.wpi.first.wpilibj2.command.Subsystem;
import edu.wpi.first.wpilibj2.command.WaitUntilCommand;
import java.util.function.BooleanSupplier;

/** A command that runs a {@link Runnable}, and then finishes when a condition comes true. */
public class LockFunctionCommand extends WaitUntilCommand {

  private final Runnable function;

  /**
   * Create a new {@link LockFunctionCommand} with no requirements
   *
   * @param condition The check for if this command should end
   * @param function The function to call on command initialization
   */
  public LockFunctionCommand(BooleanSupplier condition, Runnable function) {
    super(condition);
    this.function = function;
  }

  /**
   * Create a new {@link LockFunctionCommand} with a list of requirements
   *
   * @param condition The check for if this command should end
   * @param function The function to call on command initialization
   * @param requirements The requirements for this command
   */
  public LockFunctionCommand(
      BooleanSupplier condition, Runnable function, Subsystem... requirements) {
    super(condition);
    this.function = function;
    addRequirements(requirements);
  }

  @Override
  public void initialize() {
    function.run();
  }
}
