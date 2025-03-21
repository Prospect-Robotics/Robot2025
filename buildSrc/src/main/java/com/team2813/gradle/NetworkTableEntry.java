package com.team2813.gradle;

import com.squareup.javapoet.ClassName;
import com.squareup.javapoet.MethodSpec;

import java.util.Optional;

/** Data object for a network tables entry in {@code networktables.json}. */
class NetworkTableEntry {
    private static final ClassName PREFERENCES_CLASS = ClassName.get("edu.wpi.first.wpilibj", "Preferences");
    private static final String PREFERENCE_NAME_PREFIX = "/Preferences/";

    private String name;
    private String type;
    private Object value;

    enum Type {
        BOOLEAN {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String name, Object value) {
                builder.addStatement("$T.initBoolean(\"$L\", $L)", PREFERENCES_CLASS,name, (Boolean) value);
            }
        },
        INT {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String name, Object value) {
                long intValue = Math.round((Double) value);
                builder.addStatement("$T.initInt(\"$L\", $L)", PREFERENCES_CLASS,name, intValue);
            }
        },
        DOUBLE {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String name, Object value) {
                builder.addStatement("$T.initDouble(\"$L\", $L)", PREFERENCES_CLASS,name, (Double) value);
            }
        };

        abstract protected void addInitializer(MethodSpec.Builder builder, String name, Object value);
    }

    Optional<String> getPreferenceKey() {
        if (!name.startsWith(PREFERENCE_NAME_PREFIX)) {
            return Optional.empty();
        }
        return Optional.of(name.substring(PREFERENCE_NAME_PREFIX.length()));
    }

    String getName() {
        return name;
    }

    Type getType() {
        return Type.valueOf(type.toUpperCase());
    }

    void addInitializer(MethodSpec.Builder builder) {
        getPreferenceKey().ifPresent(key -> getType().addInitializer(builder, key, value));
    }
}
