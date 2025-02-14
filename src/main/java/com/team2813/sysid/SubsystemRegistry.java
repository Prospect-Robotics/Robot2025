package com.team2813.sysid;

import edu.wpi.first.wpilibj2.command.Subsystem;

import java.util.*;

public final class SubsystemRegistry {
  private final Map<Class<? extends Subsystem>, Subsystem> subsystems;

  public SubsystemRegistry(Collection<? extends Subsystem> subsystems) {
    Map<Class<? extends Subsystem>, Subsystem> subsystemMap = new HashMap<>();
    for (Subsystem subsystem : subsystems) {
      subsystemMap.put(subsystem.getClass(), subsystem);
    }
    this.subsystems = subsystemMap;
  }

  public <T extends Subsystem> T getSubsystem(Class<? extends T> cls) {
    return Objects.requireNonNull(cls.cast(this.subsystems.get(cls)));
  }

  public Set<? extends Subsystem> allSubsystems() {
    return Set.copyOf(subsystems.values());
  }
}
