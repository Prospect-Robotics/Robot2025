package com.team2813.gradle;

import com.google.gson.Gson;
import com.google.gson.JsonParseException;
import com.squareup.javapoet.*;
import org.gradle.api.DefaultTask;
import org.gradle.api.Plugin;
import org.gradle.api.Project;
import org.gradle.api.file.RegularFileProperty;
import org.gradle.api.plugins.JavaPlugin;
import org.gradle.api.plugins.JavaPluginExtension;
import org.gradle.api.tasks.InputFile;
import org.gradle.api.tasks.SourceSet;
import org.gradle.api.tasks.TaskAction;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import javax.lang.model.element.Modifier;

import static java.nio.charset.StandardCharsets.UTF_8;

public abstract class GenPreferences implements Plugin<Project> {
    private static final String EXTENSION_NAME = "gen_preferences";
    private static final String GEN_DIR = "generated/sources/" + EXTENSION_NAME;
    private static final String DEFAULT_JSON_FILENAME = "networktables.json";
    private static final String GEN_SRCS_TASK_NAME = "createPreferencesFile";
    private static final Gson gson = new Gson();

    interface GenPreferencesExtension {
        RegularFileProperty getJsonFile();
    }

    @Override
    public void apply(Project project) {
        // Make extension configurable.
        var extension = project.getExtensions().create(EXTENSION_NAME, GenPreferencesExtension.class);
        extension.getJsonFile().convention(project.getLayout().getProjectDirectory().file(DEFAULT_JSON_FILENAME));

        // Create task to generate Java source files.
        var taskProvider = project.getTasks().register(GEN_SRCS_TASK_NAME, GenerateSources.class);
        taskProvider.configure(task -> {
            task.getJsonFile().set(extension.getJsonFile());
            task.onlyIf(t -> extension.getJsonFile().getAsFile().get().exists());
        });
        // ... and make sure all Java tasks dend on this task.
        project.getTasks().getByName(JavaPlugin.COMPILE_JAVA_TASK_NAME).dependsOn(taskProvider);

        var sourceSets = project.getExtensions().getByType(JavaPluginExtension.class).getSourceSets();
        var generatedSourcesDir = project.getLayout().getBuildDirectory().dir(GEN_DIR);
        sourceSets.getByName(SourceSet.MAIN_SOURCE_SET_NAME).getJava().srcDirs(generatedSourcesDir);
    }

    static abstract class GenerateSources extends DefaultTask {

        public GenerateSources() {}

        @InputFile
        abstract RegularFileProperty getJsonFile();

        @TaskAction
        void generateSources() {
            Project project = getProject();
            File file = getJsonFile().getAsFile().get();
            JavaFile javaFile = generateJavaFileFromJson(project, file);

            File genDir = project.getLayout().getBuildDirectory().dir(GEN_DIR).get().getAsFile();
            if (!genDir.exists()) {
                if (!genDir.mkdirs()) {
                    throw new RuntimeException("Could not create " + genDir);
                }
            }

            try {
                javaFile.writeTo(genDir);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        private JavaFile generateJavaFileFromJson(Project project, File file) {
            ClassName preferencesClass = ClassName.get("edu.wpi.first.wpilibj", "Preferences");

            TypeSpec.Builder builder = TypeSpec.classBuilder("RobotPreferences")
                    .addModifiers(Modifier.PUBLIC, Modifier.FINAL)
                    .addJavadoc(CodeBlock.builder()
                            .add("Provides access to preferences which are configured via a JSON file.\n\n")
                            .add("<p>Generated from {@code ./$L} by GenPreferences.",
                                    project.getProjectDir().toPath().relativize(file.toPath()))
                            .build());

            FieldSpec initializedField = FieldSpec.builder(
                    Boolean.TYPE, "initialized", Modifier.PRIVATE, Modifier.STATIC).build();
            builder.addField(initializedField);

            MethodSpec.Builder initializeMethod = MethodSpec.methodBuilder("initialize")
                    .addModifiers(Modifier.PUBLIC, Modifier.STATIC)
                    .addJavadoc("Initializes preferences provided by this class with {@link $T}.", preferencesClass)
                    .returns(void.class);

            initializeMethod.beginControlFlow("if (!$N)", initializedField);
            for (NetworkTableEntry entry : parseJson(file)) {
                entry.getPreferenceKey().ifPresent(key -> {
                    entry.addGetter(builder);
                    initializeMethod.beginControlFlow("if (!$T.containsKey(\"$L\"))", preferencesClass, key);
                    entry.addInitializer(initializeMethod);
                    initializeMethod.endControlFlow();
                });
            }

            initializeMethod.addCode("\n");
            initializeMethod.addStatement("$N = true", initializedField);
            initializeMethod.endControlFlow();
            builder.addMethod(initializeMethod.build());

            builder.addMethod(MethodSpec.constructorBuilder().addModifiers(Modifier.PRIVATE).build());

            return JavaFile.builder("com.team2813", builder.build()).indent("  ").build();
        }

        private NetworkTableEntry[] parseJson(File file) {
            if (!file.exists()) {
                throw new IllegalStateException("Input file does not exist: " + file);
            }

            try (var reader = new FileReader(file, UTF_8)) {
                return gson.fromJson(reader, NetworkTableEntry[].class);
            } catch (IOException e) {
                throw new RuntimeException("Could not read input file: " + file.getPath(), e);
            } catch (JsonParseException e) {
                throw new RuntimeException("Could not parse input file: " + file.getPath(), e);
            }
        }
    }
}
