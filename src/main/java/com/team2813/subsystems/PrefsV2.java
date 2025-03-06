package com.team2813.subsystems;

import com.team2813.lib2813.preferences.*;

import java.lang.reflect.Field;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.RecordComponent;
import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.Map;
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

  private static final Map<Type, BiFunction<RecordComponent, Object, Object>> TYPE_TO_RESOLVERS = new HashMap<>();

  static {
    SimpleBooleanPref.registerResolvers();
    SimpleDoublePref.registerResolvers();
    SimpleIntPref.registerResolvers();
    SimpleLongPref.registerResolvers();
    SimpleStringPref.registerResolvers();
  }

  private static class SimpleBooleanPref extends SimplePref implements BooleanPreference {
    private final boolean defaultValue;

    SimpleBooleanPref(RecordComponent component, boolean defaultValue) {
      super(component.getDeclaringRecord(), component.getName());
      this.defaultValue = defaultValue;
    }

    @Override
    public boolean defaultValue() {
      return defaultValue;
    }

    static void registerResolvers() {
      TYPE_TO_RESOLVERS.put(Boolean.TYPE, (component, value) -> {
        boolean defaultValue = (Boolean) value;
        var pref = new SimpleBooleanPref(component, defaultValue);
        pref.initialize();
        return pref.get();
      });
      TYPE_TO_RESOLVERS.put(BooleanSupplier.class, (component, value) -> {
        boolean defaultValue = ((BooleanSupplier) value).getAsBoolean();
        var pref = new SimpleBooleanPref(component, defaultValue);
        pref.initialize();
        return pref.asSupplier();
      });
    }
  }

  private static class SimpleDoublePref extends SimplePref implements DoublePreference {
    private final double defaultValue;

    SimpleDoublePref(RecordComponent component, double defaultValue) {
      super(component.getDeclaringRecord(), component.getName());
      this.defaultValue = defaultValue;
    }

    @Override
    public double defaultValue() {
      return defaultValue;
    }

    static void registerResolvers() {
      TYPE_TO_RESOLVERS.put(Double.TYPE, (component, value) -> {
        double defaultValue = (Double) value;
        var pref = new SimpleDoublePref(component, defaultValue);
        pref.initialize();
        return pref.get();
      });
      TYPE_TO_RESOLVERS.put(DoubleSupplier.class, (component, value) -> {
        double defaultValue = ((DoubleSupplier) value).getAsDouble();
        var pref = new SimpleDoublePref(component, defaultValue);
        pref.initialize();
        return pref.asSupplier();
      });
    }
  }

  private static class SimpleIntPref extends SimplePref implements IntPreference {
    private final int defaultValue;

    SimpleIntPref(RecordComponent component, int defaultValue) {
      super(component.getDeclaringRecord(), component.getName());
      this.defaultValue = defaultValue;
    }

    @Override
    public int defaultValue() {
      return defaultValue;
    }

    static void registerResolvers() {
      TYPE_TO_RESOLVERS.put(Integer.TYPE, (component, value) -> {
        int defaultValue = (Integer) value;
        var pref = new SimpleIntPref(component, defaultValue);
        pref.initialize();
        return pref.get();
      });
      TYPE_TO_RESOLVERS.put(IntSupplier.class, (component, value) -> {
        int defaultValue = ((IntSupplier) value).getAsInt();
        var pref = new SimpleIntPref(component, defaultValue);
        pref.initialize();
        return pref.asSupplier();
      });
    }
  }

  private static class SimpleLongPref extends SimplePref implements LongPreference {
    private final long defaultValue;

    SimpleLongPref(RecordComponent component, long defaultValue) {
      super(component.getDeclaringRecord(), component.getName());
      this.defaultValue = defaultValue;
    }

    @Override
    public long defaultValue() {
      return defaultValue;
    }

    static void registerResolvers() {
      TYPE_TO_RESOLVERS.put(Long.TYPE, (component, value) -> {
        long defaultValue = (Long) value;
        var pref = new SimpleLongPref(component, defaultValue);
        pref.initialize();
        return pref.get();
      });
      TYPE_TO_RESOLVERS.put(LongSupplier.class, (component, value) -> {
        long defaultValue = ((LongSupplier) value).getAsLong();
        var pref = new SimpleLongPref(component, defaultValue);
        pref.initialize();
        return pref.asSupplier();
      });
    }
  }

  private static class SimpleStringPref extends SimplePref implements StringPreference {
    private final String defaultValue;

    SimpleStringPref(RecordComponent component, String defaultValue) {
      super(component.getDeclaringRecord(), component.getName());
      this.defaultValue = defaultValue;
    }

    @Override
    public String defaultValue() {
      return defaultValue;
    }

    static void registerResolvers() {
      TYPE_TO_RESOLVERS.put(String.class, (component, value) -> {
        String defaultValue = (String) value;
        var pref = new SimpleStringPref(component, defaultValue);
        pref.initialize();
        return pref.get();
      });
      TYPE_TO_RESOLVERS.put(Supplier.class, (component, value) -> {
        Type supplierType = ((ParameterizedType) component.getGenericType()).getActualTypeArguments()[0];
        if (!supplierType.equals(String.class)) {
          throw new IllegalArgumentException(String.format("Unsupported type for '%s': %s", component.getName(), component.getGenericType()));
        }
        Object defaultValue = ((Supplier<?>) value).get();
        if (defaultValue == null) {
          throw new IllegalArgumentException(String.format("Default value for '%s' cannot be null", component.getName()));
        }
        var pref = new SimpleStringPref(component, (String) defaultValue);
        pref.initialize();
        return pref.asSupplier();
      });
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
        Field defaultValueField = clazz.getDeclaredField(name);
        defaultValueField.setAccessible(true);
        Class<?> type = component.getType();
        types[i] = type;

        var resolver = TYPE_TO_RESOLVERS.get(type);
        if (resolver != null) {
          Object defaultValue = defaultValueField.get(configWithDefaults);
          params[i] = resolver.apply(component, defaultValue);
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
