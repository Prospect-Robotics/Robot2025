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

    @Override
    public void apply(Project project) {
        // Make extension configurable.
        var extension = project.getExtensions().create(EXTENSION_NAME, GenPreferencesExtension.class);
        extension.getJsonFile().convention(project.getLayout().getProjectDirectory().file(DEFAULT_JSON_FILENAME));

        // Create task to generate Java source files.
        var taskProvider = project.getTasks().register(GEN_SRCS_TASK_NAME, GenerateSources.class);
        taskProvider.configure(task -> task.getJsonFile().set(extension.getJsonFile()));
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

            File genDir = new File(project.getProjectDir(), "build/generated/sources/gen_preferences");
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
            if (!file.exists()) {
                throw new RuntimeException("Input file does not exist: " + file);
            }
            NetworkTableEntry[] entries;
            try (var reader = new FileReader(file, UTF_8)) {
                entries = gson.fromJson(reader, NetworkTableEntry[].class);
            } catch (IOException e) {
                throw new RuntimeException("Could not read input file: " + file.getPath(), e);
            } catch (JsonParseException e) {
                throw new RuntimeException("Could not parse input file: " + file.getPath(), e);
            }

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
            for (NetworkTableEntry entry : entries) {
                entry.getPreferenceKey().ifPresent(key -> {
                    entry.addGetter(builder);
                    initializeMethod.beginControlFlow("if (!$T.containsKey(\"$L\"))", preferencesClass, key);
                    entry.addInitializer(initializeMethod);
                    initializeMethod.endControlFlow();
                });
//            if (entry.getType() == NetworkTableEntry.Type.BOOLEAN) {
//                FieldSpec spec = FieldSpec.builder(Boolean.TYPE, entry.getName())
//                        .addModifiers(Modifier.PUBLIC, Modifier.FINAL)
//                        .initializer("$L", entry.getValueAsBoolean())
//                        .build();
//                builder.addField(spec);
//
//                initializeMethod.beginControlFlow("if (!$T.containsKey(\"$L\"))", preferencesClass, entry.getName());
//                initializeMethod.addStatement("$T.initBoolean(\"$L\", $L)", preferencesClass, entry.getName(), entry.getValueAsBoolean());
//                initializeMethod.endControlFlow();
//            }
            }

            initializeMethod.addCode("\n");
            initializeMethod.addStatement("$N = true", initializedField);
            initializeMethod.endControlFlow();
            builder.addMethod(initializeMethod.build());

            builder.addMethod(MethodSpec.constructorBuilder().addModifiers(Modifier.PRIVATE).build());

            return JavaFile.builder("com.team2813", builder.build()).indent("  ").build();
        }
    }

    interface GenPreferencesExtension {
        RegularFileProperty getJsonFile();
    }

//        project.afterEvaluate {
//            //读取配置数据
//            File file = project.file("config.json");
//            if (!file.exists()) {
//                throw new Exception("config.json not exist!");
//            }
//            String json = file.text;
//            JsonSlurper jsonSlurper = new JsonSlurper();
//            def config = (Map<String, Map<String, String>>) jsonSlurper.parseText(json);
//            println("read config result is \n $config");
//            TypeSpec.Builder builder = TypeSpec.classBuilder("UpConfigData")
//                    .addModifiers(Modifier.PUBLIC, Modifier.ABSTRACT)
//            JavaFile javaFile = JavaFile.builder("com.haier.uhome.uplus.plugin.uppermissionplugin.initdemo",
//                    builder.build()).build()
//            File createFile = new File(project.projectDir, "src/main/java")
//            if (!createFile.exists()) {
//                createFile.mkdirs()
//            }
//            javaFile.writeTo(createFile)
//            println "[write to]: ${createFile.absolutePath}"
//        }
}
