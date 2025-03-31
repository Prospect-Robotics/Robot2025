package com.team2813.subsystems.drive;

import com.ctre.phoenix6.SignalLogger;
import com.team2813.sysid.*;
import dagger.Module;
import dagger.Provides;
import edu.wpi.first.units.Units;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Module
public interface DriveModule {
  static final SwerveSysidRequest DRIVE_SYSID =
      new SwerveSysidRequest(MotorType.Drive, RequestType.TorqueCurrentFOC);
  static final SwerveSysidRequest STEER_SYSID =
      new SwerveSysidRequest(MotorType.Swerve, RequestType.VoltageOut);

  @Provides
  static Drive provideDrive(DriveSubsystem driveSubsystem, SysIdRoutineRegistry registry) {
    registry.registerRoutines(driveSubsystem, sysIdRoutines(driveSubsystem));
    return driveSubsystem;
  }

  static List<DropdownEntry> sysIdRoutines(DriveSubsystem driveSubsystem) {
    List<DropdownEntry> routines = new ArrayList<>();
    routines.add(
        new DropdownEntry(
            "Drive Motor",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) -> driveSubsystem.runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    driveSubsystem))));
    routines.add(
        new DropdownEntry(
            "Steer Motor",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) -> driveSubsystem.runSysIdRequest(STEER_SYSID.withVoltage(v)),
                    null,
                    driveSubsystem))));
    routines.add(
        new DropdownEntry(
            "Slip Test (Forward Quasistatic only)",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    Units.Volts.of(0.25).per(Units.Second),
                    null,
                    null,
                    (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) -> driveSubsystem.runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    driveSubsystem))));
    return Collections.unmodifiableList(routines);
  }
}
