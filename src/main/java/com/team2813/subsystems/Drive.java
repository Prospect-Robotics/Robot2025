package com.team2813.subsystems;

import static com.team2813.Constants.*;
import static com.team2813.Constants.DriverConstants.DRIVER_CONTROLLER;
import static com.team2813.lib2813.util.ControlUtils.deadband;
import static edu.wpi.first.units.Units.Rotations;

import com.ctre.phoenix6.Utils;
import com.ctre.phoenix6.configs.CANcoderConfiguration;
import com.ctre.phoenix6.configs.CurrentLimitsConfigs;
import com.ctre.phoenix6.configs.Slot0Configs;
import com.ctre.phoenix6.configs.TalonFXConfiguration;
import com.ctre.phoenix6.hardware.CANcoder;
import com.ctre.phoenix6.hardware.TalonFX;
import com.ctre.phoenix6.swerve.SwerveDrivetrain;
import com.ctre.phoenix6.swerve.SwerveDrivetrainConstants;
import com.ctre.phoenix6.swerve.SwerveModule;
import com.ctre.phoenix6.swerve.SwerveModuleConstants;
import com.ctre.phoenix6.swerve.SwerveModuleConstants.ClosedLoopOutputType;
import com.ctre.phoenix6.swerve.SwerveModuleConstants.SteerFeedbackType;
import com.ctre.phoenix6.swerve.SwerveModuleConstantsFactory;
import com.ctre.phoenix6.swerve.SwerveRequest.ApplyRobotSpeeds;
import com.ctre.phoenix6.swerve.SwerveRequest.FieldCentric;
import com.ctre.phoenix6.swerve.SwerveRequest.FieldCentricFacingAngle;
import com.google.auto.value.AutoBuilder;
import com.team2813.commands.DefaultDriveCommand;
import com.team2813.commands.RobotLocalization;
import com.team2813.lib2813.limelight.BotPoseEstimate;
import com.team2813.lib2813.preferences.PreferencesInjector;
import com.team2813.sysid.SwerveSysidRequest;
import com.team2813.vision.MultiPhotonPoseEstimator;
import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.apriltag.AprilTagFields;
import edu.wpi.first.math.Matrix;
import edu.wpi.first.math.Nat;
import edu.wpi.first.math.geometry.*;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.math.kinematics.SwerveModuleState;
import edu.wpi.first.math.numbers.N1;
import edu.wpi.first.math.numbers.N3;
import edu.wpi.first.networktables.*;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.AngularVelocity;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.RobotBase;
import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import java.util.List;
import java.util.Optional;
import java.util.function.DoubleSupplier;
import java.util.stream.IntStream;
import org.photonvision.EstimatedRobotPose;
import org.photonvision.PhotonPoseEstimator;
import org.photonvision.simulation.SimCameraProperties;
import org.photonvision.simulation.VisionSystemSim;
import org.photonvision.targeting.PhotonTrackedTarget;

/** This is the Drive. His name is Gary. Please be kind to him and say hi. Have a nice day! */
public class Drive extends SubsystemBase implements AutoCloseable {
  private static final double DEFAULT_MAX_VELOCITY_METERS_PER_SECOND = 6;
  private static final double DEFAULT_MAX_ROTATIONS_PER_SECOND = 1.2;
  private static final Matrix<N3, N1> PHOTON_MULTIPLE_TAG_STD_DEVS =
      new Matrix<>(Nat.N3(), Nat.N1(), new double[] {0.1, 0.1, 0.1});
  private final RobotLocalization localization;
  private final SwerveDrivetrain<TalonFX, TalonFX, CANcoder> drivetrain;
  private final SimulatedSwerveDrivetrain simDrivetrain;
  private final VisionSystemSim simVisionSystem;
  private final DriveConfiguration config;
  private final MultiPhotonPoseEstimator photonPoseEstimator;

  private final StructArrayPublisher<SwerveModuleState> expectedStatePublisher;
  private final StructArrayPublisher<SwerveModuleState> actualStatePublisher;
  private final StructPublisher<Pose2d> currentPosePublisher;
  private final DoubleArrayPublisher modulePositionsPublisher;
  private final DoublePublisher ambiguityPublisher =
      NetworkTableInstance.getDefault().getDoubleTopic("Ambiguity").publish();

  /** This measurement is <em>IN INCHES</em> */
  private static final double WHEEL_RADIUS_IN = 1.875;

  private double multiplier = 1;
  private double lastVisionEstimateTime = -1;

  static final double FRONT_DIST = 0.330200;
  static final double LEFT_DIST = 0.330200;

  /**
   * The transformation for the {@code captain-barnacles} PhotonVision camera. This camera faces the
   * front
   */
  private static final Transform3d captBarnaclesTransform =
      new Transform3d(
          0.1688157406,
          0.2939800826,
          0.1708140348,
          new Rotation3d(0, -0.1745329252, -0.5235987756));

  /**
   * The transformation for the {@code professor-inking} PhotonVision camera. This camera faces the
   * back
   */
  private static final Transform3d professorInklingTransform =
      new Transform3d(
          0.0584240386, 0.2979761884, 0.1668812004, new Rotation3d(0, 0, 0.1745329252 + Math.PI));

  // See above comment, do not delete past this line.

  /**
   * Configurable values for the {@code Drive} subsystem
   *
   * <p>Thee values here can be updated in the SmartDashboard/Shuffleboard UI, and will have keys
   * starting with {@code "subsystems.Drive.DriveConfiguration."}.
   */
  public record DriveConfiguration(
      boolean addLimelightMeasurement,
      boolean usePhotonVisionLocation,
      boolean usePnpDistanceTrigSolveStrategy,
      double maxLimelightDifferenceMeters,
      DoubleSupplier maxRotationsPerSecond,
      DoubleSupplier maxVelocityInMetersPerSecond) {

    public DriveConfiguration {
      if (maxLimelightDifferenceMeters <= 0) {
        throw new IllegalArgumentException("maxLimelightDifferenceMeters must be positive");
      }
    }

    double maxRadiansPerSecond() {
      return maxRotationsPerSecond.getAsDouble() * Math.PI * 2;
    }

    double maxVelocity() {
      return maxVelocityInMetersPerSecond.getAsDouble();
    }

    PhotonPoseEstimator.PoseStrategy poseStrategy() {
      return usePnpDistanceTrigSolveStrategy
          ? PhotonPoseEstimator.PoseStrategy.PNP_DISTANCE_TRIG_SOLVE
          : PhotonPoseEstimator.PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR;
    }

    /** Creates a builder for {@code DriveConfiguration} with default values. */
    public static Builder builder() {
      return new AutoBuilder_Drive_DriveConfiguration_Builder()
          .addLimelightMeasurement(true)
          .usePhotonVisionLocation(false)
          .maxRotationsPerSecond(DEFAULT_MAX_ROTATIONS_PER_SECOND)
          .maxVelocityInMetersPerSecond(DEFAULT_MAX_VELOCITY_METERS_PER_SECOND)
          .usePnpDistanceTrigSolveStrategy(false)
          .maxLimelightDifferenceMeters(1.0);
    }

    /** Creates an instance from preference values stored in the robot's flash memory. */
    public static DriveConfiguration fromPreferences() {
      DriveConfiguration defaultConfig = builder().build();
      return PreferencesInjector.DEFAULT_INSTANCE.injectPreferences(defaultConfig);
    }

    @AutoBuilder
    public interface Builder {
      Builder addLimelightMeasurement(boolean enabled);

      Builder usePhotonVisionLocation(boolean enabled);

      Builder maxRotationsPerSecond(DoubleSupplier value);

      default Builder maxRotationsPerSecond(double value) {
        return maxRotationsPerSecond(() -> value);
      }

      Builder maxVelocityInMetersPerSecond(DoubleSupplier value);

      default Builder maxVelocityInMetersPerSecond(double value) {
        return maxVelocityInMetersPerSecond(() -> value);
      }

      Builder maxLimelightDifferenceMeters(double value);

      Builder usePnpDistanceTrigSolveStrategy(boolean enabled);

      DriveConfiguration build();
    }
  }

  public Drive(NetworkTableInstance networkTableInstance, RobotLocalization localization) {
    this(networkTableInstance, localization, DriveConfiguration.fromPreferences());
  }

  public Drive(
      NetworkTableInstance networkTableInstance,
      RobotLocalization localization,
      DriveConfiguration config) {
    this.localization = localization;

    var aprilTagFieldLayout = AprilTagFieldLayout.loadField(AprilTagFields.k2025ReefscapeWelded);
    photonPoseEstimator =
        new MultiPhotonPoseEstimator.Builder(
                networkTableInstance, aprilTagFieldLayout, config.poseStrategy())
            // should have named our batteries after Octonauts characters >:(
            .addCamera("capt-barnacles", captBarnaclesTransform, "Front PhotonVision camera")
            .addCamera("professor-inkling", professorInklingTransform, "Back PhotonVision camera")
            .build();
    this.config = config;

    double FLSteerOffset = 0.22021484375;
    double FRSteerOffset = -0.085693359375;
    double BLSteerOffset = -0.367919921875;
    double BRSteerOffset = -0.258544921875;

    Slot0Configs steerGains =
        new Slot0Configs()
            .withKP(50)
            .withKI(0)
            .withKD(3.0889) // Tune this.
            .withKS(0.21041)
            .withKV(2.68)
            .withKA(0.084645); // Tune this.

    // l: 0 h: 10
    Slot0Configs driveGains =
        new Slot0Configs()
            .withKP(2.5)
            .withKI(0)
            .withKD(0) // Tune this.
            .withKS(6.4111)
            .withKV(0.087032)
            .withKA(0); // Tune this.

    SwerveDrivetrainConstants drivetrainConstants =
        new SwerveDrivetrainConstants()
            .withPigeon2Id(PIGEON_ID)
            .withCANBusName("swerve"); // README: tweak to actual pigeon and CanBusName

    SwerveModuleConstantsFactory<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>
        constantCreator =
            new SwerveModuleConstantsFactory<
                    TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>()
                // WARNING: TUNE ALL OF THESE THINGS!!!!!!
                .withDriveMotorGearRatio(6.75)
                .withSteerMotorGearRatio(150.0 / 7)
                .withWheelRadius(Units.Inches.of(WHEEL_RADIUS_IN))
                .withSlipCurrent(90)
                .withSteerMotorGains(steerGains)
                .withDriveMotorGains(driveGains)
                .withDriveMotorClosedLoopOutput(
                    ClosedLoopOutputType
                        .TorqueCurrentFOC) // Tune this. (Important to tune values below)
                .withSteerMotorClosedLoopOutput(ClosedLoopOutputType.Voltage) // Tune this.
                .withSpeedAt12Volts(6) // Tune this.
                .withFeedbackSource(SteerFeedbackType.FusedCANcoder) // Tune this.
                .withCouplingGearRatio(3.5);

    SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>
        frontLeft =
            constantCreator.createModuleConstants(
                FRONT_LEFT_STEER_ID,
                FRONT_LEFT_DRIVE_ID,
                FRONT_LEFT_ENCODER_ID,
                FLSteerOffset,
                FRONT_DIST,
                LEFT_DIST,
                true, // May need to change later.
                true, // May need to change later.
                false); // May need to change later.
    SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>
        frontRight =
            constantCreator.createModuleConstants(
                FRONT_RIGHT_STEER_ID,
                FRONT_RIGHT_DRIVE_ID,
                FRONT_RIGHT_ENCODER_ID,
                FRSteerOffset,
                FRONT_DIST,
                -LEFT_DIST,
                true, // May need to change later.
                true, // May need to change later.
                false); // May need to change later.
    SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>
        backLeft =
            constantCreator.createModuleConstants(
                BACK_LEFT_STEER_ID,
                BACK_LEFT_DRIVE_ID,
                BACK_LEFT_ENCODER_ID,
                BLSteerOffset,
                -FRONT_DIST,
                LEFT_DIST,
                true, // May need to change later.
                true, // May need to change later.
                false); // May need to change later.
    SwerveModuleConstants<TalonFXConfiguration, TalonFXConfiguration, CANcoderConfiguration>
        backRight =
            constantCreator.createModuleConstants(
                BACK_RIGHT_STEER_ID,
                BACK_RIGHT_DRIVE_ID,
                BACK_RIGHT_ENCODER_ID,
                BRSteerOffset,
                -FRONT_DIST,
                -LEFT_DIST,
                true, // May need to change later.
                true, // May need to change later.
                false); // May need to change later.
    SwerveModuleConstants<?, ?, ?>[] modules = {frontLeft, frontRight, backLeft, backRight};
    drivetrain =
        new SwerveDrivetrain<>(
            TalonFX::new, TalonFX::new, CANcoder::new, drivetrainConstants, modules);

    // Logging
    NetworkTable networkTable = networkTableInstance.getTable("Drive");
    expectedStatePublisher =
        networkTable.getStructArrayTopic("expected state", SwerveModuleState.struct).publish();
    actualStatePublisher =
        networkTable.getStructArrayTopic("actual state", SwerveModuleState.struct).publish();
    currentPosePublisher = networkTable.getStructTopic("current pose", Pose2d.struct).publish();
    modulePositionsPublisher = networkTable.getDoubleArrayTopic("module positions").publish();

    setDefaultCommand(createDefaultCommand());

    for (int i = 0; i < 4; i++) {
      drivetrain
          .getModule(i)
          .getDriveMotor()
          .getConfigurator()
          .apply(
              new CurrentLimitsConfigs()
                  .withSupplyCurrentLimit(60)
                  .withSupplyCurrentLimitEnable(true)
                  .withStatorCurrentLimitEnable(false));
    }

    // Simulation code.
    // See https://docs.wpilib.org/en/stable/docs/software/wpilib-tools/robot-simulation/
    if (RobotBase.isSimulation()) {
      simDrivetrain = new SimulatedSwerveDrivetrain(networkTable, drivetrain, modules);

      // See https://docs.photonvision.org/en/latest/docs/simulation/simulation-java.html
      simVisionSystem = new VisionSystemSim("main");
      simVisionSystem.addAprilTags(aprilTagFieldLayout);
      photonPoseEstimator.addToSim(
          simVisionSystem, cameraName -> SimCameraProperties.PERFECT_90DEG());
    } else {
      simDrivetrain = null;
      simVisionSystem = null;
    }
  }

  private Rotation3d getRotation3d() {
    if (simDrivetrain != null) {
      return simDrivetrain.getRotation3d();
    }
    return drivetrain.getRotation3d();
  }

  private Command createDefaultCommand() {
    return new DefaultDriveCommand(
        this,
        () -> -modifyAxis(DRIVER_CONTROLLER.getLeftY()) * config.maxVelocity(),
        () -> -modifyAxis(DRIVER_CONTROLLER.getLeftX()) * config.maxVelocity(),
        () -> -modifyAxis(DRIVER_CONTROLLER.getRightX()) * config.maxRadiansPerSecond());
  }

  private static double modifyAxis(double value) {
    value = deadband(value, 0.1);
    value = Math.copySign(value * value, value);
    return value;
  }

  private double getPosition(int moduleId) {
    return drivetrain
        .getModule(moduleId)
        .getEncoder()
        .getAbsolutePosition()
        .getValue()
        .in(Rotations);
  }

  private final ApplyRobotSpeeds applyRobotSpeedsApplier = new ApplyRobotSpeeds();
  /*
   * IT IS ABSOLUTELY IMPERATIVE THAT YOU USE ApplyRobotSpeeds() RATHER THAN THE DEMENTED ApplyFieldSpeeds() HERE!
   * If ApplyFieldSpeeds() is used, pathplanner & all autonomous paths will not function properly.
   * This is because pathplanner knows where the robot is, but needs to use ApplyRobotSpeeds() in order to convert knowledge
   * of where the robot is on the field, to instruction centered on the robot.
   * Or something like this, I'm still not to sure how this works.
   */
  private final FieldCentricFacingAngle fieldCentricFacingAngleApplier =
      new FieldCentricFacingAngle();
  private final FieldCentric fieldCentricApplier =
      new FieldCentric().withDriveRequestType(SwerveModule.DriveRequestType.Velocity);

  public static boolean onRed() {
    return DriverStation.getAlliance()
        .map(alliance -> alliance == DriverStation.Alliance.Red)
        .orElse(false);
  }

  private boolean correctRotation = false;

  // Note: This is used for teleop drive.
  public void drive(double xSpeed, double ySpeed, double rotation) {
    double multiplier = onRed() && correctRotation ? -this.multiplier : this.multiplier;
    drivetrain.setControl(
        fieldCentricApplier
            .withVelocityX(xSpeed * multiplier)
            .withVelocityY(ySpeed * multiplier)
            .withRotationalRate(
                rotation * this.multiplier)); // Note: might not work, will need testing.
  }

  public void runSysIdRequest(SwerveSysidRequest request) {
    drivetrain.setControl(request);
  }

  // Note: This is used for auto drive.
  public void drive(ChassisSpeeds demand) {
    drivetrain.setControl(applyRobotSpeedsApplier.withSpeeds(demand));
  }

  public void turnToFace(Rotation2d rotation) {
    drivetrain.setControl(fieldCentricFacingAngleApplier.withTargetDirection(rotation));
  }

  /**
   * Sets the rotation velocity of the robot
   *
   * @param rotationRate rotation rate in radians per second
   * @deprecated Unsafe; use {@link #setRotationVelocity(AngularVelocity)}, and specify the unit you
   *     are using
   */
  @Deprecated
  public void setRotationVelocityDouble(double rotationRate) { // Radians per second
    drivetrain.setControl(fieldCentricApplier.withRotationalRate(rotationRate));
  }

  /**
   * Sets the rotation velocity of the robot
   *
   * @param rotationRate rotation rate in units as defined by the WPIlib unit library.
   */
  public void setRotationVelocity(AngularVelocity rotationRate) {
    drivetrain.setControl(fieldCentricApplier.withRotationalRate(rotationRate));
  }

  public Pose2d getPose() {
    return drivetrain.getState().Pose;
  }

  /** Makes the current orientation of the robot "forward" for field-centric maneuvers. */
  public void resetPose() {
    this.correctRotation = false;
    this.drivetrain.seedFieldCentric();
  }

  /**
   * Sets the pose, in the blue coordinate system.
   *
   * <p>This is called by PathPlanner when it starts controlling the robot. It assumes that the
   * passed-in pose is correct.
   */
  public void setPose(Pose2d pose) {
    correctRotation = true;
    if (pose != null) {
      drivetrain.resetPose(pose);
      if (config.usePnpDistanceTrigSolveStrategy) {
        photonPoseEstimator.resetHeadingData(Timer.getTimestamp(), pose.getRotation());
      }
      if (simDrivetrain != null) {
        simDrivetrain.resetPose(pose);
      }
    } else {
      DriverStation.reportError(
          "setPose() passed null! Possibly unintended behavior may occur!",
          false); // The 'false' parameter keeps this from printing the stack trace.
    }
  }

  public ChassisSpeeds getRobotRelativeSpeeds() {
    return this.drivetrain.getKinematics().toChassisSpeeds(this.drivetrain.getState().ModuleStates);
  }

  private static final Matrix<N3, N1> LIMELIGHT_STD_DEVS =
      new Matrix<>(Nat.N3(), Nat.N1(), new double[] {0.9, 0.9, 0.9});

  public void addVisionMeasurement(BotPoseEstimate estimate) {
    double estimateTimestamp = estimate.timestampSeconds();
    if (estimateTimestamp > lastVisionEstimateTime) {
      // Per the JavaDoc for addVisionMeasurement(), only add vision measurements that are already
      // within one meter or so of the current odometry pose estimate.
      Pose2d drivePose = getPose();
      var distance = drivePose.getTranslation().getDistance(estimate.pose().getTranslation());
      if (Math.abs(distance) <= config.maxLimelightDifferenceMeters()) {
        drivetrain.addVisionMeasurement(estimate.pose(), estimateTimestamp, LIMELIGHT_STD_DEVS);
        lastVisionEstimateTime = estimateTimestamp;
      }
    }
  }

  private void handlePhotonPose(EstimatedRobotPose estimate) {
    if (!config.usePhotonVisionLocation) {
      return;
    }

    Matrix<N3, N1> stdDevs;
    List<PhotonTrackedTarget> targets = estimate.targetsUsed;
    if (targets.isEmpty()) {
      return;
    } else if (targets.size() == 1) {
      PhotonTrackedTarget target = targets.get(0);
      double ambiguity = (1.0 / target.area);
      ambiguityPublisher.accept(ambiguity);
      stdDevs = new Matrix<>(Nat.N3(), Nat.N1(), new double[] {ambiguity, ambiguity, ambiguity});
    } else {
      // We see multiple tags.
      // TODO: Calculate the pooled standard deviation.
      // See https://www.statisticshowto.com/pooled-standard-deviation/
      stdDevs = PHOTON_MULTIPLE_TAG_STD_DEVS;
    }
    drivetrain.addVisionMeasurement(
        estimate.estimatedPose.toPose2d(),
        Utils.fpgaToCurrentTime(estimate.timestampSeconds),
        stdDevs);
  }

  @Override
  public void periodic() {
    // If the limelight has a position, send it to SwerveDrivetrain.addVisionMeasurement().
    //
    // Note: we call limelightLocation() even if config.addLimelightMeasurement is false so
    // the position is published to network tables, which allows us to view the limelight's
    // pose estimate in AdvantageScope.
    Optional<BotPoseEstimate> limelightEstimate = localization.limelightLocation();
    if (config.addLimelightMeasurement) {
      limelightEstimate.ifPresent(this::addVisionMeasurement);
    }

    // Publish data to NetworkTables
    expectedStatePublisher.set(drivetrain.getState().ModuleTargets);
    actualStatePublisher.set(drivetrain.getState().ModuleStates);
    if (config.usePnpDistanceTrigSolveStrategy) {
      photonPoseEstimator.addHeadingData(Timer.getTimestamp(), getRotation3d());
    }
    photonPoseEstimator.update(this::handlePhotonPose);
    Pose2d drivePose = getPose();
    currentPosePublisher.set(drivePose);
    photonPoseEstimator.setDrivePose(drivePose);

    modulePositionsPublisher.accept(IntStream.range(0, 4).mapToDouble(this::getPosition).toArray());
  }

  @Override
  public void simulationPeriodic() {
    if (simDrivetrain == null || simVisionSystem == null) {
      return; // We should never get here, but just in case...
    }

    simDrivetrain.periodic();
    Pose2d drivePose = simDrivetrain.getPose();
    simVisionSystem.update(drivePose);
  }

  public void enableSlowMode(boolean enable) {
    multiplier = enable ? 0.3 : 1;
  }

  @Override
  public void close() {
    drivetrain.close();
    photonPoseEstimator.close();
  }
}
