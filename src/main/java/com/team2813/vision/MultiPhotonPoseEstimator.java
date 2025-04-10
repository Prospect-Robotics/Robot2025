package com.team2813.vision;

import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.math.geometry.Transform3d;
import edu.wpi.first.networktables.NetworkTableInstance;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Consumer;
import org.photonvision.EstimatedRobotPose;
import org.photonvision.PhotonCamera;
import org.photonvision.PhotonPoseEstimator;

public class MultiPhotonPoseEstimator implements AutoCloseable {
  private final List<CameraData> cameraDatas = new ArrayList<>();

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

  private record CameraData(
      PhotonCamera camera, PhotonPoseEstimator estimator, PhotonVisionPosePublisher publisher) {}

  private MultiPhotonPoseEstimator(Builder builder) {
    for (Map.Entry<String, Transform3d> entry : builder.cameras.entrySet()) {
      String cameraName = entry.getKey();
      PhotonCamera camera = new PhotonCamera(builder.ntInstance, cameraName);
      Transform3d robotToCamera = entry.getValue();
      PhotonPoseEstimator estimator =
          new PhotonPoseEstimator(builder.fieldTags, builder.poseStrategy, robotToCamera);
      var publisher = new PhotonVisionPosePublisher(camera);

      cameraDatas.add(new CameraData(camera, estimator, publisher));
    }
  }

  public void update(Consumer<? super EstimatedRobotPose> apply) {
    for (CameraData cameraData : cameraDatas) {
      List<EstimatedRobotPose> poses =
          cameraData.camera.getAllUnreadResults().stream()
              .map(cameraData.estimator::update)
              .flatMap(Optional::stream)
              .toList();

      poses.forEach(apply);
      cameraData.publisher.publish(poses);
    }
  }

  @Override
  public void close() {
    for (CameraData cameraData : cameraDatas) {
      cameraData.camera.close();
    }
    cameraDatas.clear();
  }
}
