package com.team2813.apriltag;

import edu.wpi.first.math.Matrix;
import edu.wpi.first.math.Nat;
import edu.wpi.first.math.geometry.Pose3d;

public class Fiducial {
  private int id;
  private double[] transform;
  public Pose3d getPosition() {
    return new Pose3d(new Matrix<>(Nat.N4(), Nat.N4(), transform));
  }
  public int getId() {
    return id;
  }
}
