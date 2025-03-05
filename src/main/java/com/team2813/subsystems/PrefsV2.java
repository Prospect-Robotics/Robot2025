package com.team2813.subsystems;

import com.team2813.lib2813.preferences.*;

import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.function.*;

class PrefsV2 {

  private static abstract class SimplePref implements Preference {
    private final Class<?> containingClass;
    private final String name;

    SimplePref(Class<?> containingClass, String name) {
      this.containingClass = containingClass;
      this.name = name;
    }

    @Override
    public String name() {
      return name;
    }

    @Override
    public String key() {
      return keyFactory().createKey(containingClass, name());
    }
  }

  private static class SimpleBooleanPref extends SimplePref implements BooleanPreference {
    private final boolean defaultValue;

    SimpleBooleanPref(Class<?> containingClass, String name, boolean defaultValue) {
      super(containingClass, name);
      this.defaultValue = defaultValue;
    }

    @Override
    public boolean defaultValue() {
      return defaultValue;
    }
  }

  private static class SimpleDoublePref extends SimplePref implements DoublePreference {
    private final double defaultValue;

    SimpleDoublePref(Class<?> containingClass, String name, double defaultValue) {
      super(containingClass, name);
      this.defaultValue = defaultValue;
    }

    @Override
    public double defaultValue() {
      return defaultValue;
    }
  }

  private static class SimpleIntPref extends SimplePref implements IntPreference {
    private final int defaultValue;

    SimpleIntPref(Class<?> containingClass, String name, int defaultValue) {
      super(containingClass, name);
      this.defaultValue = defaultValue;
    }

    @Override
    public int defaultValue() {
      return defaultValue;
    }
  }

  private static class SimpleLongPref extends SimplePref implements LongPreference {
    private final long defaultValue;

    SimpleLongPref(Class<?> containingClass, String name, long defaultValue) {
      super(containingClass, name);
      this.defaultValue = defaultValue;
    }

    @Override
    public long defaultValue() {
      return defaultValue;
    }
  }

  private static class SimpleStringPref extends SimplePref implements StringPreference {
    private final String defaultValue;

    SimpleStringPref(Class<?> containingClass, String name, String defaultValue) {
      super(containingClass, name);
      this.defaultValue = defaultValue;
    }

    @Override
    public String defaultValue() {
      return defaultValue;
    }
  }

  /**
   * Creates an instance of the given record class with all fields populated from
   * preferences.
   *
   * <p>The type of the record components can be any of the following:
   * <ul>
   *   <li>{@code boolean} or {@code BooleanSupplier}</li>
   *   <li>{@code int} or {@code IntSupplier}</li>
   *   <li>{@code long} or {@code LongSupplier}</li>
   *   <li>{@code double} or {@code DoubleSupplier}</li>
   *   <li>{@code String} or {@code Supplier<String>}</li>
   * </ul>
   *
   * <p>The values for the components for the passed-in instance will be used
   * as the default value for the preference. If a component is a supplier, the
   * supplier will be called to get the default instance.
   *
   * @param configWithDefaults Record instance with all values set to their preferred default values.
   */
  static <T extends java.lang.Record> T injectPreferences(T configWithDefaults) {
    try {
      @SuppressWarnings("unchecked")
      Class<? extends T> clazz = (Class<? extends T>) configWithDefaults.getClass();

      var components = clazz.getRecordComponents();
      if (components == null) {
        throw new IllegalArgumentException("Must pass in a record class");
      }

      Object[] params = new Object[components.length];
      Class<?>[] types = new Class[components.length];
      int i = 0;
      for (var component : Drive.DriveConfiguration.class.getRecordComponents()) {
        String name = component.getName();
        var defaultValueField = clazz.getDeclaredField(name);
        defaultValueField.setAccessible(true);
        Class<?> type = component.getType();
        types[i] = type;

        if (type.equals(String.class)) {
          String defaultValue = (String) defaultValueField.get(configWithDefaults);
          var pref = new SimpleStringPref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.get();
        } else if (type.equals(Supplier.class)) { // Supplier<String>
          Type supplierType = ((ParameterizedType) component.getGenericType()).getActualTypeArguments()[0];
          if (!supplierType.equals(String.class)) {
            throw new IllegalArgumentException(String.format("Unsupported type for '%s': %s", name, component.getGenericType()));
          }
          Object defaultValue = ((Supplier<?>) defaultValueField.get(configWithDefaults)).get();
          if (defaultValue == null) {
            throw new IllegalArgumentException(String.format("Default value for '%s' cannot be null", name));
          }
          var pref = new SimpleStringPref(clazz, name, (String) defaultValue);
          pref.initialize();
          params[i] = pref.asSupplier();
        } else if (type.equals(Boolean.TYPE)) {
          boolean defaultValue = (Boolean) defaultValueField.get(configWithDefaults);
          var pref = new SimpleBooleanPref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.get();
        } else if (type.equals(BooleanSupplier.class)) {
          boolean defaultValue = ((BooleanSupplier) defaultValueField.get(configWithDefaults)).getAsBoolean();
          var pref = new SimpleBooleanPref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.asSupplier();
        } else if (type.equals(Integer.TYPE)) {
          int defaultValue = (Integer) defaultValueField.get(configWithDefaults);
          var pref = new SimpleIntPref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.get();
        } else if (type.equals(IntSupplier.class)) {
          int defaultValue = ((IntSupplier) defaultValueField.get(configWithDefaults)).getAsInt();
          var pref = new SimpleIntPref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.asSupplier();
        } else if (type.equals(Long.TYPE)) {
          long defaultValue = (Long) defaultValueField.get(configWithDefaults);
          var pref = new SimpleLongPref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.get();
        } else if (type.equals(LongSupplier.class)) {
          long defaultValue = ((LongSupplier) defaultValueField.get(configWithDefaults)).getAsLong();
          var pref = new SimpleLongPref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.asSupplier();
        } else if (type.equals(Double.TYPE)) {
          double defaultValue = (Double) defaultValueField.get(configWithDefaults);
          var pref = new SimpleDoublePref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.get();
        } else if (type.equals(DoubleSupplier.class)) {
          double defaultValue = ((DoubleSupplier) defaultValueField.get(configWithDefaults)).getAsDouble();
          var pref = new SimpleDoublePref(clazz, name, defaultValue);
          pref.initialize();
          params[i] = pref.asSupplier();
        } else {
          throw new IllegalArgumentException(String.format("Unsupported type for '%s': %s", name, type));
        }
        i++;
      }
      return clazz.getConstructor(types).newInstance(params);
    } catch (ReflectiveOperationException e) {
      throw new RuntimeException(e);
    }
  }
}
