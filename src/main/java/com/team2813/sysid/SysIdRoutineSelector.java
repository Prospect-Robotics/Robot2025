package com.team2813.sysid;

import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.Subsystem;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;

public class SysIdRoutineSelector {
  private final SendableChooser<SysIdRoutine> routineSelector = new SendableChooser<>();
  private final SendableChooser<SysIdRequestType> requestTypeSelector = new SendableChooser<>();
  private final SendableChooser<SysIdRoutine.Direction> directionSelector = new SendableChooser<>();
  
  private final Set<? extends Subsystem> requirements;
  
  public SysIdRoutineSelector(SubsystemRegistry registry, Function<SubsystemRegistry, List<DropdownEntry>> routineSupplier) {
    requirements = registry.allSubsystems();
    for (DropdownEntry entry : routineSupplier.apply(registry)) {
      routineSelector.addOption(entry.name(), entry.routine());
    }
    for (SysIdRequestType requestType : SysIdRequestType.values()) {
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
    SysIdRoutine routine = routineSelector.getSelected();
    SysIdRequestType requestType = requestTypeSelector.getSelected();
    SysIdRoutine.Direction direction = directionSelector.getSelected();
    if (routine == null || requestType == null || direction == null) {
      return Commands.print(String.format("Some value was not selected! routine: %s, requestType: %s, direction: %s", routine, requestType, direction));
    }
    return getCommand(routine, requestType, direction);
  }
  
  public Set<Subsystem> getRequirements() {
    return Set.copyOf(requirements);
  }
  
  Command getCommand(SysIdRoutine routine, SysIdRequestType requestType, SysIdRoutine.Direction direction) {
    return requestType.createCommand(routine, direction);
  }
}
