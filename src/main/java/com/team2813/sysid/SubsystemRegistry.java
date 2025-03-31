package com.team2813.sysid;

import edu.wpi.first.wpilibj2.command.Subsystem;
import java.util.*;

public final class SubsystemRegistry {
  private final Map<Class<? extends Subsystem>, Subsystem> subsystemMap = new HashMap<>();

  public SubsystemRegistry() {}

  public SubsystemRegistry(Collection<? extends Subsystem> subsystems) {
    for (Subsystem subsystem : subsystems) {
      subsystemMap.put(subsystem.getClass(), subsystem);
    }
  }

  public void addSubsystem(Subsystem subsystem) {
    if (subsystemMap.putIfAbsent(subsystem.getClass(), subsystem) != null) {
      throw new IllegalArgumentException("Instance already registered for " + subsystem);
    }
  }

  public <T extends Subsystem> T getSubsystem(Class<? extends T> cls) {
    return Objects.requireNonNull(cls.cast(this.subsystemMap.get(cls)));
  }

  public Set<? extends Subsystem> allSubsystems() {
    return Set.copyOf(subsystemMap.values());
  }
}
