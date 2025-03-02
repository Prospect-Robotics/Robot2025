package com.team2813.apriltag;

import com.google.gson.Gson;
import edu.wpi.first.wpilibj.Filesystem;

import java.io.*;
import java.util.EnumSet;

public abstract sealed class FiducialRetriever {
  private static FiducialRetriever retriever;
  protected abstract Fiducial[] fiducials();
  static final class FileRetriever extends FiducialRetriever {
    Fiducial[] fiducials;
    private static final Gson gson = new Gson();
    @Override
    protected Fiducial[] fiducials() {
      if (fiducials != null) {
        return fiducials;
      }
      File file = new File(Filesystem.getDeployDirectory(), "apriltag-locations.json");
      try (FileReader reader = new FileReader(file)) {
        FieldMap map = gson.fromJson(reader, FieldMap.class);
        fiducials = map.fiducials;
        return map.fiducials;
      } catch (IOException e) {
        return new Fiducial[0];
      }
    }
  }
  static final class SetRetriever extends FiducialRetriever {
    private final Fiducial[] fiducials;
    SetRetriever(Fiducial[] fiducials) {
      this.fiducials = fiducials;
    }
    @Override
    protected Fiducial[] fiducials() {
      return fiducials;
    }
  }
  public static Fiducial[] getFiducials() {
    if (retriever == null) {
      retriever = new FileRetriever();
    }
    return retriever.fiducials();
  }
  static FiducialRetriever setRetriever(FiducialRetriever retriever) {
    FiducialRetriever old = FiducialRetriever.retriever;
    FiducialRetriever.retriever = retriever;
    return old;
  }
}
