package com.team2813.vision;

import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.math.geometry.Transform3d;
import edu.wpi.first.networktables.NetworkTableInstance;
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
  private final Map<String, PhotonVisionPosePublisher> posePublishers = new HashMap<>();

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
      if (cameras.put(name, transform) != null) {
        throw new IllegalArgumentException(String.format("Already a camera with name '%s'", name));
      }
      return this;
    }

    public MultiPhotonPoseEstimator build() {
      return new MultiPhotonPoseEstimator(this);
    }
  }

  private MultiPhotonPoseEstimator(Builder builder) {
    for (Map.Entry<String, Transform3d> entry : builder.cameras.entrySet()) {
      String cameraName = entry.getKey();
      PhotonCamera camera = new PhotonCamera(builder.ntInstance, cameraName);
      PhotonPoseEstimator estimator =
          new PhotonPoseEstimator(builder.fieldTags, builder.poseStrategy, entry.getValue());

      posePublishers.put(cameraName, new PhotonVisionPosePublisher(camera));
      estimators.put(camera, estimator);
    }
  }

  public void update(Consumer<? super EstimatedRobotPose> apply) {
    for (Map.Entry<PhotonCamera, PhotonPoseEstimator> entry : estimators.entrySet()) {
      PhotonCamera camera = entry.getKey();
      List<EstimatedRobotPose> poses =
          camera.getAllUnreadResults().stream()
              .map(entry.getValue()::update)
              .flatMap(Optional::stream)
              .toList();

      poses.forEach(apply);

      PhotonVisionPosePublisher posePublisher = posePublishers.get(camera.getName());
      if (posePublisher != null) {
        posePublisher.publish(poses);
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
}
