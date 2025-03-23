package com.team2813.subsystems;

import static com.team2813.Constants.*;
import static com.team2813.Constants.DriverConstants.DRIVER_CONTROLLER;
import static com.team2813.lib2813.util.ControlUtils.deadband;
import static edu.wpi.first.units.Units.Rotations;

import com.ctre.phoenix6.Utils;
import com.ctre.phoenix6.configs.CANcoderConfiguration;
import com.ctre.phoenix6.configs.Slot0Configs;
import com.ctre.phoenix6.configs.TalonFXConfiguration;
import com.ctre.phoenix6.hardware.CANcoder;
import com.ctre.phoenix6.hardware.TalonFX;
import com.ctre.phoenix6.swerve.*;
import com.ctre.phoenix6.swerve.SwerveModuleConstants.ClosedLoopOutputType;
import com.ctre.phoenix6.swerve.SwerveModuleConstants.SteerFeedbackType;
import com.ctre.phoenix6.swerve.SwerveRequest.ApplyRobotSpeeds;
import com.ctre.phoenix6.swerve.SwerveRequest.FieldCentric;
import com.ctre.phoenix6.swerve.SwerveRequest.FieldCentricFacingAngle;
import com.google.auto.value.AutoBuilder;
import com.team2813.AllPreferences;
import com.team2813.Constants.*;
import com.team2813.commands.DefaultDriveCommand;
import com.team2813.commands.RobotLocalization;
import com.team2813.lib2813.limelight.BotPoseEstimate;
import com.team2813.lib2813.limelight.Limelight;
import com.team2813.lib2813.limelight.LocationalData;
import com.team2813.lib2813.preferences.PreferencesInjector;
import com.team2813.sysid.SwerveSysidRequest;
import com.team2813.vision.MultiPhotonPoseEstimator;
import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.apriltag.AprilTagFields;
import edu.wpi.first.math.geometry.*;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.math.kinematics.SwerveModuleState;
import edu.wpi.first.networktables.*;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.AngularVelocity;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.SubsystemBase;
import java.util.Collection;
import java.util.stream.IntStream;
import org.photonvision.PhotonPoseEstimator;

/** This is the Drive. His name is Gary. Please be kind to him and say hi. Have a nice day! */
public class Drive extends SubsystemBase implements AutoCloseable {
  private static final double MAX_VELOCITY = 6;
  private static final double MAX_ROTATION = Math.PI * 2;
  private final RobotLocalization localization;
  private final SwerveDrivetrain<TalonFX, TalonFX, CANcoder> drivetrain;
  private final DriveConfiguration config;
  private final MultiPhotonPoseEstimator estimator;

  /** This measurement is <em>IN INCHES</em> */
  private static final double WHEEL_RADIUS_IN = 1.875;

  private double multiplier = 1;
  private double lastVisionEstimateTime = -1;

  static double frontDist = 0.330200;
  static double leftDist = 0.330200;

  private static final Transform3d captBarnaclesTransform =
      new Transform3d(
          0.1688157406,
          0.2939800826,
          0.1708140348,
          new Rotation3d(0, -0.1745329252, -0.5235987756));
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
      boolean addLimelightMeasurement, double maxLimelightDifferenceMeters) {

    public DriveConfiguration {
      if (maxLimelightDifferenceMeters <= 0) {
        throw new IllegalArgumentException("maxLimelightDifferenceMeters must be positive");
      }
    }

    /** Creates a builder for {@code DriveConfiguration} with default values. */
    public static Builder builder() {
      return new AutoBuilder_Drive_DriveConfiguration_Builder()
          .addLimelightMeasurement(true)
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

      Builder maxLimelightDifferenceMeters(double value);

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
    estimator =
        new MultiPhotonPoseEstimator.Builder(
                networkTableInstance,
                AprilTagFieldLayout.loadField(AprilTagFields.k2025ReefscapeWelded),
                PhotonPoseEstimator.PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR)
            // should have named our batteries after Octonauts characters >:(
            .addCamera("capt-barnacles", captBarnaclesTransform)
            .addCamera("professor-inkling", professorInklingTransform)
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
                frontDist,
                leftDist,
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
                frontDist,
                -leftDist,
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
                -frontDist,
                leftDist,
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
                -frontDist,
                -leftDist,
                true, // May need to change later.
                true, // May need to change later.
                false); // May need to change later.
    drivetrain =
        new SwerveDrivetrain<>(
            TalonFX::new,
            TalonFX::new,
            CANcoder::new,
            drivetrainConstants,
            frontLeft,
            frontRight,
            backLeft,
            backRight);

    // Logging
    NetworkTable networkTable = networkTableInstance.getTable("Drive");
    expectedState =
        networkTable.getStructArrayTopic("expected state", SwerveModuleState.struct).publish();
    actualState =
        networkTable.getStructArrayTopic("actual state", SwerveModuleState.struct).publish();
    currentPose = networkTable.getStructTopic("current pose", Pose2d.struct).publish();
    visibleTargetPoses =
        networkTable.getStructArrayTopic("visible target poses", Pose3d.struct).publish();
    modulePositions = networkTable.getDoubleArrayTopic("module positions").publish();
    captPose = networkTable.getStructTopic("Front cam pos", Pose3d.struct).publish();
    professorPose = networkTable.getStructTopic("Back cam pos", Pose3d.struct).publish();

    setDefaultCommand(createDefaultCommand());
  }

  private Command createDefaultCommand() {
    return new DefaultDriveCommand(
        this,
        () -> -modifyAxis(DRIVER_CONTROLLER.getLeftY()) * MAX_VELOCITY,
        () -> -modifyAxis(DRIVER_CONTROLLER.getLeftX()) * MAX_VELOCITY,
        () -> -modifyAxis(DRIVER_CONTROLLER.getRightX()) * MAX_ROTATION);
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

  private static boolean onRed() {
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

  public void resetPose() {
    this.correctRotation = false;
    this.drivetrain.seedFieldCentric();
  }

  public void setPose(Pose2d pose) {
    correctRotation = true;
    if (pose != null) {
      drivetrain.resetPose(pose);
    } else {
      DriverStation.reportError(
          "setPose() passed null! Possibly unintended behavior may occur!",
          false); // The 'false' parameter keeps this from printing the stack trace.
    }
  }

  public ChassisSpeeds getRobotRelativeSpeeds() {
    return this.drivetrain.getKinematics().toChassisSpeeds(this.drivetrain.getState().ModuleStates);
  }

  public void addVisionMeasurement(BotPoseEstimate estimate) {
    double estimateTimestamp = estimate.timestampSeconds();
    if (estimateTimestamp > lastVisionEstimateTime) {
      drivetrain.addVisionMeasurement(estimate.pose(), estimateTimestamp);
      lastVisionEstimateTime = estimateTimestamp;
    }
  }

  private final StructArrayPublisher<SwerveModuleState> expectedState;
  private final StructArrayPublisher<SwerveModuleState> actualState;
  private final StructPublisher<Pose2d> currentPose;
  private final StructArrayPublisher<Pose3d> visibleTargetPoses;
  private final DoubleArrayPublisher modulePositions;
  private final StructPublisher<Pose3d> captPose;
  private final StructPublisher<Pose3d> professorPose;

  private static final Pose3d[] EMPTY_LIST = new Pose3d[0];

  @Override
  public void periodic() {
    Limelight limelight = Limelight.getDefaultLimelight();
    LocationalData locationalData = limelight.getLocationalData();
    if (config.addLimelightMeasurement) {
      // If the limelight has a position that isn't too far from the drive's current estimated
      // position, send it to SwerveDrivetrain.addVisionMeasurement().
      localization.limelightLocation(this::getPose, config).ifPresent(this::addVisionMeasurement);
    }

    // Publish data to NetworkTables
    expectedState.set(drivetrain.getState().ModuleTargets);
    actualState.set(drivetrain.getState().ModuleStates);
    if (AllPreferences.usePhotonVisionLocation().getAsBoolean()) {
      estimator.update(
          (estimate) ->
              drivetrain.addVisionMeasurement(
                  estimate.estimatedPose.toPose2d(),
                  Utils.fpgaToCurrentTime(estimate.timestampSeconds)));
    }
    Pose2d pose = getPose();
    currentPose.set(pose);
    captPose.set(new Pose3d(pose).plus(captBarnaclesTransform));
    professorPose.set(new Pose3d(pose).plus(professorInklingTransform));
    Collection<Pose3d> poses = locationalData.getVisibleAprilTagPoses().values();
    visibleTargetPoses.accept(poses.toArray(EMPTY_LIST));

    modulePositions.accept(IntStream.range(0, 4).mapToDouble(this::getPosition).toArray());

    localization.updateDashboard();
  }

  public void enableSlowMode(boolean enable) {
    multiplier = enable ? 0.3 : 1;
  }

  @Override
  public void close() {
    drivetrain.close();
    estimator.close();
  }
}
