package com.team2813.vision;

import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Transform3d;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.StructArrayPublisher;
import edu.wpi.first.networktables.StructPublisher;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Consumer;
import org.photonvision.EstimatedRobotPose;
import org.photonvision.PhotonCamera;
import org.photonvision.PhotonPoseEstimator;

public class MultiPhotonPoseEstimator implements AutoCloseable {
  private final Map<PhotonCamera, PhotonPoseEstimator> estimators = new HashMap<>();
  private final Map<PhotonCamera, StructArrayPublisher<Pose3d>> publishers = new HashMap<>();

  public static class Builder {
    private final Map<String, Transform3d> cameras = new HashMap<>();
    private final AprilTagFieldLayout fieldTags;
    private final NetworkTableInstance ntInstance;
    private final PhotonPoseEstimator.PoseStrategy poseStrategy;

    public Builder(
        NetworkTableInstance ntInstance,
        AprilTagFieldLayout fieldTags,
        PhotonPoseEstimator.PoseStrategy poseStrategy) {
      this.fieldTags = fieldTags;
      this.ntInstance = ntInstance;
      this.poseStrategy = poseStrategy;
    }

    public Builder addCamera(String name, Transform3d transform) {
      cameras.put(name, transform);
      return this;
    }

    public MultiPhotonPoseEstimator build() {
      return new MultiPhotonPoseEstimator(this);
    }
  }

  private MultiPhotonPoseEstimator(Builder builder) {
    for (Map.Entry<String, Transform3d> entry : builder.cameras.entrySet()) {
      PhotonCamera camera = new PhotonCamera(builder.ntInstance, entry.getKey());
      PhotonPoseEstimator estimator =
          new PhotonPoseEstimator(builder.fieldTags, builder.poseStrategy, entry.getValue());

      publishers.put(camera, createPosePublisher(builder.ntInstance, camera));
      estimators.put(camera, estimator);
    }
  }
  
  private static final Pose3d[] EMPTY_ARRAY = new Pose3d[0];

  public void update(Consumer<? super EstimatedRobotPose> apply) {
    for (Map.Entry<PhotonCamera, PhotonPoseEstimator> entry : estimators.entrySet()) {
      PhotonCamera camera = entry.getKey();
      List<EstimatedRobotPose> poses =
          camera.getAllUnreadResults().stream()
              .map(entry.getValue()::update)
              .flatMap(Optional::stream)
              .toList();
      poses.forEach(apply);
      StructArrayPublisher<Pose3d> publisher = publishers.get(camera);
      if (publisher != null) {
        if (poses.isEmpty()) {
          publisher.set(EMPTY_ARRAY);
        } else {
          for (EstimatedRobotPose pose : poses) {
            // under normal circumstances the NT time is the FPGA time converted into microseconds, so this should be sound
            publisher.set(new Pose3d[] {pose.estimatedPose}, (long) (pose.timestampSeconds * 1e6));
          }
        }
      }
    }
  }

  @Override
  public void close() {
    for (PhotonCamera camera : estimators.keySet()) {
      camera.close();
    }
    estimators.clear();
  }

  private static StructArrayPublisher<Pose3d> createPosePublisher(
      NetworkTableInstance ntInstance, PhotonCamera camera) {
    NetworkTable table = ntInstance.getTable("photonvision/" + camera.getName());
    return table.getStructArrayTopic("pose", Pose3d.struct).publish();
  }
}
