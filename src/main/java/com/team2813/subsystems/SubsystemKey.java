package com.team2813.subsystems;

import static java.lang.annotation.RetentionPolicy.RUNTIME;

import dagger.MapKey;
import edu.wpi.first.wpilibj2.command.Subsystem;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

/** A {@link MapKey} annotation for maps with {@code Class<? extends Subsystem>} keys. */
@Target(ElementType.METHOD)
@Retention(RUNTIME)
@MapKey
public @interface SubsystemKey {
  Class<? extends Subsystem> value();
}
