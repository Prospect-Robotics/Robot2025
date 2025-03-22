package com.team2813.gradle;

import com.squareup.javapoet.ClassName;
import com.squareup.javapoet.MethodSpec;
import com.squareup.javapoet.TypeSpec;

import javax.lang.model.element.Modifier;
import java.lang.reflect.Type;
import java.util.Optional;

/** Data object for a network tables entry in {@code networktables.json}. */
class NetworkTableEntry {
    private static final ClassName PREFERENCES_CLASS = ClassName.get("edu.wpi.first.wpilibj", "Preferences");
    private static final String PREFERENCE_NAME_PREFIX = "/Preferences/";

    private String name;
    private String type;
    private Object value;

    enum ValueType {
        BOOLEAN(Boolean.TYPE) {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String key, Object value) {
                builder.addStatement("$T.initBoolean(\"$L\", $L)", PREFERENCES_CLASS, key, (Boolean) value);
            }
            @Override
            protected void addGetter(MethodSpec.Builder builder, String key) {
                builder.returns(type)
                        .addStatement("return $T.getBoolean(\"$L\", false)", PREFERENCES_CLASS, key)
                        .build();
            }
        },
        STRING(String.class) {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String key, Object value) {
                builder.addStatement("$T.initString(\"$L\", \"$L\")", PREFERENCES_CLASS, key, (String) value);
            }

            @Override
            protected void addGetter(MethodSpec.Builder builder, String key) {
                builder.returns(type)
                        .addStatement("return $T.getString(\"$L\", \"\")", PREFERENCES_CLASS, key)
                        .build();
            }
        },
        LONG(Long.TYPE) {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String key, Object value) {
                long intValue = Math.round((Double) value);
                builder.addStatement("$T.initLong(\"$L\", $L)", PREFERENCES_CLASS, key, intValue);
            }

            @Override
            protected void addGetter(MethodSpec.Builder builder, String key) {
                builder.returns(type)
                        .addStatement("return $T.getLong(\"$L\", 0)", PREFERENCES_CLASS, key)
                        .build();
            }
        },
        INT(Integer.TYPE) {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String key, Object value) {
                long intValue = Math.round((Double) value);
                builder.addStatement("$T.initInt(\"$L\", $L)", PREFERENCES_CLASS, key, intValue);
            }

            @Override
            protected void addGetter(MethodSpec.Builder builder, String key) {
                builder.returns(type)
                        .addStatement("return $T.getInt(\"$L\", 0)", PREFERENCES_CLASS, key)
                        .build();
            }
        },
        DOUBLE(Double.TYPE) {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String key, Object value) {
                builder.addStatement("$T.initDouble(\"$L\", $L)", PREFERENCES_CLASS, key, (Double) value);
            }

            @Override
            protected void addGetter(MethodSpec.Builder builder, String key) {
                builder.returns(type)
                        .addStatement("return $T.getDouble(\"$L\", 0)", PREFERENCES_CLASS, key)
                        .build();
            }
        },
        FLOAT(Float.TYPE) {
            @Override
            protected void addInitializer(MethodSpec.Builder builder, String key, Object value) {
                builder.addStatement("$T.initFloat(\"$L\", $Lf)", PREFERENCES_CLASS, key, (Double) value);
            }

            @Override
            protected void addGetter(MethodSpec.Builder builder, String key) {
                builder.returns(type)
                        .addStatement("return $T.getFloat(\"$L\", 0)", PREFERENCES_CLASS, key)
                        .build();
            }
        };

        protected final Type type;

        ValueType(Type type) {
            this.type = type;
        }

        abstract protected void addInitializer(MethodSpec.Builder builder, String name, Object value);
        abstract protected void addGetter(MethodSpec.Builder builder, String key);
    }

    Optional<String> getPreferenceKey() {
        if (!name.startsWith(PREFERENCE_NAME_PREFIX)) {
            return Optional.empty();
        }
        String key = name.substring(PREFERENCE_NAME_PREFIX.length());
        return key.isEmpty() ? Optional.empty() : Optional.of(key);
    }

    private ValueType getType() {
        return ValueType.valueOf(type.toUpperCase());
    }

    void addInitializer(MethodSpec.Builder builder) {
        getPreferenceKey().ifPresent(key -> getType().addInitializer(builder, key, value));
    }

    void addGetter(TypeSpec.Builder classBuilder) {
        getPreferenceKey().ifPresent(key -> {
            String getterName = "get" + Character.toUpperCase(key.charAt(0)) + key.substring(1);
            MethodSpec.Builder builder = MethodSpec.methodBuilder(getterName)
                    .addModifiers(Modifier.PUBLIC, Modifier.STATIC)
                    .addJavadoc("Gets the value of \"$L\" from Preferences.", key);
            getType().addGetter(builder, key);
            classBuilder.addMethod(builder.build());
        });
    }
}
