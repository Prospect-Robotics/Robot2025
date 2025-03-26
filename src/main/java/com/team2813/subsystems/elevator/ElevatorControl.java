package com.team2813.subsystems.elevator;

import static java.lang.annotation.RetentionPolicy.RUNTIME;

import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import javax.inject.Qualifier;

/**
 * Binding annotation for a {@link java.util.function.DoubleSupplier} that provides data from a
 * controller to control the elevator.
 */
@Qualifier @Documented
@Retention(RUNTIME)
public @interface ElevatorControl {}
