package com.team2813.sysid;

import com.ctre.phoenix6.SignalLogger;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Subsystem;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;

import java.util.HashMap;
import java.util.Map;
import java.util.function.BiFunction;

enum SysIdRoutines {
  Drive(new SysIdRoutine(
          new SysIdRoutine.Config(null, null, null, (s) -> SignalLogger.writeString("State", s.toString())),
          new SysIdRoutine.Mechanism(
                  (volts) -> SUBSYSTEMS.get(com.team2813.subsystems.Drive.class).
          )
  ));
  private static final Map<Class<? extends Subsystem>, Subsystem> SUBSYSTEMS = new HashMap<>();
  private final SysIdRoutine routine;
  
  SysIdRoutines(SysIdRoutine routine) {
    this.routine = routine;
  }
  
  public Command getCommand(SysIdRequestType requestType, SysIdRoutine.Direction direction) {
    return requestType.createCommand(routine, direction);
  }
  
  public enum SysIdRequestType {
    Quasistatic(SysIdRoutine::quasistatic),
    Dynamic(SysIdRoutine::dynamic);
    private final BiFunction<SysIdRoutine, SysIdRoutine.Direction, Command> commandCreator;
    
    SysIdRequestType(BiFunction<SysIdRoutine, SysIdRoutine.Direction, Command> commandCreator) {
      this.commandCreator = commandCreator;
    }
    
    private Command createCommand(SysIdRoutine routine, SysIdRoutine.Direction direction) {
      return commandCreator.apply(routine, direction);
    }
  }
}
