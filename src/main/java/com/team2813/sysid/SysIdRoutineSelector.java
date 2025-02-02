package com.team2813.sysid;

import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;

public class SysIdRoutineSelector {
  private final SendableChooser<SysIdRoutines> routineSelector = new SendableChooser<>();
  private final SendableChooser<SysIdRoutines.SysIdRequestType> requestTypeSelector = new SendableChooser<>();
  private final SendableChooser<SysIdRoutine.Direction> directionSelector = new SendableChooser<>();
  
  public SysIdRoutineSelector() {
    for (SysIdRoutines routine : SysIdRoutines.values()) {
      routineSelector.addOption(routine.toString(), routine);
    }
    for (SysIdRoutines.SysIdRequestType requestType : SysIdRoutines.SysIdRequestType.values()) {
      requestTypeSelector.addOption(requestType.toString(), requestType);
    }
    for (SysIdRoutine.Direction direction : SysIdRoutine.Direction.values()) {
      directionSelector.addOption(direction.toString(), direction);
    }
    ShuffleboardTab tab = Shuffleboard.getTab("SysId");
    tab.add("SysId Routine", routineSelector);
    tab.add("Request Type", requestTypeSelector);
    tab.add("Direction", directionSelector);
  }
  
  public Command getSelected() {
    SysIdRoutines routine = routineSelector.getSelected();
    SysIdRoutines.SysIdRequestType requestType = requestTypeSelector.getSelected();
    SysIdRoutine.Direction direction = directionSelector.getSelected();
    if (routine == null || requestType == null || direction == null) {
      return Commands.print(String.format("Some value was not selected! routine: %s, requestType: %s, direction: %s", routine, requestType, direction));
    }
    return routine.getCommand(requestType, direction);
  }
}
