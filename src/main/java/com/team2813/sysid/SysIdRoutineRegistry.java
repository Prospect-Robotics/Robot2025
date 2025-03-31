package com.team2813.sysid;

import edu.wpi.first.wpilibj2.command.Subsystem;
import java.util.*;
import java.util.stream.Stream;
import javax.inject.Inject;

public final class SysIdRoutineRegistry {
  private final Map<Subsystem, List<DropdownEntry>> registeredEntries = new HashMap<>();

  @Inject
  SysIdRoutineRegistry() {}

  public void registerRoutines(Subsystem subsystem, Iterable<DropdownEntry> additionalEntries) {
    registeredEntries.compute(
        subsystem,
        (_key, curEntries) -> {
          if (curEntries == null) {
            curEntries = new ArrayList<DropdownEntry>();
          }
          List<DropdownEntry> entries = curEntries;
          String prefix = subsystem.getName() + "-";
          additionalEntries.forEach(
              entry -> {
                entries.add(new DropdownEntry(prefix + entry.name(), entry.routine()));
              });
          return entries;
        });
  }

  Set<? extends Subsystem> allSubsystems() {
    return registeredEntries.keySet();
  }

  Stream<DropdownEntry> entries() {
    return registeredEntries.values().stream().flatMap(List::stream);
  }
}
