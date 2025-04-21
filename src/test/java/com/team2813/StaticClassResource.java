package com.team2813;

import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;
import org.junit.rules.ExternalResource;

/**
 * Resets the non-final static state of a class to it's initial state after each test
 */
public class StaticClassResource extends ExternalResource {

  private final Class<?> theClass;

  public StaticClassResource(Class<?> theClass) {
    this.theClass = theClass;
  }

  private List<DefaultValue> values;

  record DefaultValue(Field field, Object object) {}

  @Override
  protected void before() throws Exception {
    List<DefaultValue> values = new ArrayList<>();
    for (Field field : theClass.getDeclaredFields()) {
      int modifiers = field.getModifiers();
      if (!Modifier.isFinal(modifiers) && Modifier.isStatic(modifiers)) {
        field.setAccessible(true);
        values.add(new DefaultValue(field, field.get(null)));
      }
    }
    this.values = values;
  }

  @Override
  protected void after() {
    for (DefaultValue value : values) {
      try {
        value.field.set(null, value.object);
      } catch (IllegalAccessException e) {
        throw new RuntimeException(e);
      }
    }
  }
}
