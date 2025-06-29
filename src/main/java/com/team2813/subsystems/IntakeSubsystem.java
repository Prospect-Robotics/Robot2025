package com.team2813.subsystems;

import com.google.auto.value.AutoBuilder;
import com.team2813.lib2813.control.ControlMode;
import com.team2813.lib2813.control.PIDMotor;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

class IntakeSubsystem extends SubsystemBase implements AutoCloseable {
  protected final PIDMotor intakeMotor;
  private final Params params;
  private double speed = 0.0;

  public record Params(double intakeSpeed, double outtakeSpeed) {

    public static Params.Builder builder() {
      return new AutoBuilder_IntakeSubsystem_Params_Builder();
    }

    @AutoBuilder
    public interface Builder {
      Builder setIntakeSpeed(double speed);

      Builder setOuttakeSpeed(double speed);

      Params build();
    }

    public Params {
      if (isEssentiallyZero(intakeSpeed)) {
        throw new IllegalArgumentException("intakeSpeed cannot be zero");
      }
      if (isEssentiallyZero(outtakeSpeed)) {
        throw new IllegalArgumentException("outtakeSpeed cannot be zero");
      }
      if (Math.signum(intakeSpeed) == Math.signum(outtakeSpeed)) {
        throw new IllegalArgumentException(
            "intakeSpeed should be the opposite sign as outtakeSpeed");
      }
    }
  }

  protected IntakeSubsystem(PIDMotor intakeMotor, Params params) {
    this.intakeMotor = intakeMotor;
    this.params = params;
  }

  final boolean intaking() {
    return motorRunning() && Math.signum(params.intakeSpeed) == Math.signum(speed);
  }

  private boolean motorRunning() {
    return !isEssentiallyZero(speed);
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
    setMotorSpeed(params.intakeSpeed);
  }

  /** Makes intake wheels spin in the outtake direction. */
  protected final void outtakeGamePiece() {
    setMotorSpeed(params.outtakeSpeed);
  }

  /**
   * Runs the motor at a specified speed.
   *
   * @param speed Voltage to apply to the motor.
   */
  protected final void setMotorSpeed(double speed) {
    intakeMotor.set(ControlMode.VOLTAGE, speed);
    this.speed = speed;
  }

  /**
   * Returns a command that runs the motor at a specified speed.
   *
   * @param speed Voltage to apply to the motor.
   */
  protected final Command setMotorSpeedCommand(double speed) {
    return new InstantCommand(() -> setMotorSpeed(speed), this);
  }

  /** Stops the motor. */
  public final void stopMotor() {
    setMotorSpeed(0.0);
  }

  @Override
  public void close() {}

  private static boolean isEssentiallyZero(double value) {
    return Math.abs(value) < 0.001;
  }
}
