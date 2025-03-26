package com.team2813.subsystems.drive;

import com.ctre.phoenix6.SignalLogger;
import com.team2813.subsystems.SubsystemKey;
import com.team2813.sysid.*;
import dagger.Binds;
import dagger.Module;
import dagger.Provides;
import dagger.multibindings.IntoMap;
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

  @Binds
  Drive bindDrive(DriveSubsystem driveSubsystem);

  @Provides
  @IntoMap
  @SubsystemKey(DriveSubsystem.class)
  static List<DropdownEntry> provideSysIdRoutines(DriveSubsystem driveSubsystem) {
    List<DropdownEntry> routines = new ArrayList<>();
    routines.add(
        new DropdownEntry(
            "Drive-Drive Motor",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) -> driveSubsystem.runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    driveSubsystem))));
    routines.add(
        new DropdownEntry(
            "Drive-Steer Motor",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) -> driveSubsystem.runSysIdRequest(STEER_SYSID.withVoltage(v)),
                    null,
                    driveSubsystem))));
    routines.add(
        new DropdownEntry(
            "Drive-Slip Test (Forward Quasistatic only)",
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
