package com.team2813.gradle;

import javax.lang.model.element.Modifier;

import org.gradle.api.Plugin;
import org.gradle.api.Project;
import com.squareup.javapoet.TypeSpec;
import com.squareup.javapoet.JavaFile;
import org.gradle.api.file.RegularFileProperty;

import java.io.File;
import java.io.IOException;

public abstract class GenPreferences implements Plugin<Project> {

    @Override
    public void apply(Project project) {
        var extension = project.getExtensions().create("genPreferences", GenPreferencesExtension.class);
        extension.getJson().convention(project.getLayout().getProjectDirectory().file("preferences.json"));
        project.afterEvaluate(p -> generateSources(p, extension));
    }

    // See https://discuss.gradle.org/t/how-to-use-javapoet-generate-java-file/42674/1
    private void generateSources(Project project, GenPreferencesExtension extensions) {
        File file = extensions.getJson().getAsFile().get(); // project.file("preferences.json");
        if (!file.exists()) {
            throw new RuntimeException("File not exist: " + file);
        }
        TypeSpec.Builder builder = TypeSpec.classBuilder("MyPreferences")
                .addModifiers(Modifier.PUBLIC, Modifier.FINAL);
        JavaFile javaFile = JavaFile.builder("com.team2813", builder.build()).build();
        File createFile = new File(project.getProjectDir(), "build/generated/sources/gen_preferences");
        if (!createFile.exists()) {
            createFile.mkdirs();
        }
        try {
            javaFile.writeTo(createFile);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    interface GenPreferencesExtension {
        RegularFileProperty getJson();
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
