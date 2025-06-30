package com.team2813.subsystems;

import com.google.auto.value.AutoBuilder;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

class ParameterizedIntakeSubsystem extends SubsystemBase implements AutoCloseable {
  private final PIDMotor intakeMotor;
  private final Params params;
  private double demand = 0.0;

  public record Params(ControlMode controlMode, double intakeDemand, double outtakeDemand) {

    public static Params.Builder builder() {
      return new AutoBuilder_ParameterizedIntakeSubsystem_Params_Builder()
          .setControlMode(ControlMode.VOLTAGE);
    }

    @AutoBuilder
    public interface Builder {
      Builder setControlMode(ControlMode controlMode);

      Builder setIntakeDemand(double demand);

      Builder setOuttakeDemand(double demand);

      Params build();
    }

    public Params {
      if (controlMode == null) {
        throw new IllegalArgumentException("controlMode cannot be null");
      }
      if (isEssentiallyZero(intakeDemand)) {
        throw new IllegalArgumentException("intakeDemand cannot be zero");
      }
      if (isEssentiallyZero(outtakeDemand)) {
        throw new IllegalArgumentException("outtakeDemand cannot be zero");
      }
      if (Math.signum(intakeDemand) == Math.signum(outtakeDemand)) {
        throw new IllegalArgumentException(
            "intakeDemand should be the opposite sign of outtakeDemand");
      }
    }
  }

  public ParameterizedIntakeSubsystem(PIDMotor intakeMotor, Params params) {
    this.intakeMotor = intakeMotor;
    this.params = params;
  }

  final boolean intaking() {
    return motorRunning() && Math.signum(params.intakeDemand) == Math.signum(demand);
  }

  private boolean motorRunning() {
    return !isEssentiallyZero(demand);
  }

  public final Command intakeItemCommand() {
    return new InstantCommand(this::intakeGamePiece, this);
  }

  public final Command outtakeItemCommand() {
    return new InstantCommand(this::outtakeGamePiece, this);
  }

  public final Command stopMotorCommand() {
    return new InstantCommand(this::stopMotor, this);
  }

  /** Makes intake wheels spin in the intake direction. */
  protected final void intakeGamePiece() {
    // FIXME: Maybe add a check that the wheels are not stalled.
    setMotorDemand(params.intakeDemand);
  }

  /** Makes intake wheels spin in the outtake direction. */
  protected final void outtakeGamePiece() {
    setMotorDemand(params.outtakeDemand);
  }

  /**
   * Runs the motor with the provided demand value.
   *
   * @param demand Demand of the motor. Meaning depends on the {@code ControlMode}.
   */
  protected final void setMotorDemand(double demand) {
    intakeMotor.set(params.controlMode, demand);
    this.demand = demand;
  }

  /**
   * Returns a command that runs the motor with the provided demand value.
   *
   * @param demand Demand of the motor. Meaning depends on the {@code ControlMode}.
   */
  protected final Command setMotorDemandCommand(double demand) {
    return new InstantCommand(() -> setMotorDemand(demand), this);
  }

  /** Stops the motor. */
  public final void stopMotor() {
    setMotorDemand(0.0);
  }

  @Override
  public void close() {}

  private static boolean isEssentiallyZero(double value) {
    return Math.abs(value) < 0.001;
  }
}
