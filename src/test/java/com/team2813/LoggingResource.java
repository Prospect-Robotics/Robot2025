package com.team2813;

import edu.wpi.first.wpilibj.DataLogManager;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.List;
import org.junit.rules.ExternalResource;

public class LoggingResource extends ExternalResource {

  private List<DefaultValue> values;

  record DefaultValue(Field field, Object object) {}

  @Override
  protected void before() throws Exception {
    List<DefaultValue> values = new ArrayList<>();
    for (Field field : DataLogManager.class.getDeclaredFields()) {
      if (!Modifier.isFinal(field.getModifiers())) {
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
    DriverStationSim.resetData();
    DriverStationSim.notifyNewData();
  }
}
