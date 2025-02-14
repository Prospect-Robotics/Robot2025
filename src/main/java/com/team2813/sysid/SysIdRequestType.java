package com.team2813.sysid;

import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;

import java.util.function.BiFunction;

enum SysIdRequestType {
  Quasistatic(SysIdRoutine::quasistatic),
  Dynamic(SysIdRoutine::dynamic);
  private final BiFunction<SysIdRoutine, SysIdRoutine.Direction, Command> commandCreator;
  
  SysIdRequestType(BiFunction<SysIdRoutine, SysIdRoutine.Direction, Command> commandCreator) {
    this.commandCreator = commandCreator;
  }
  
  public Command createCommand(SysIdRoutine routine, SysIdRoutine.Direction direction) {
    return commandCreator.apply(routine, direction);
  }
}
