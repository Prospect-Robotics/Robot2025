package com.team2813;

import edu.wpi.first.hal.AllianceStationID;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.simulation.DriverStationSim;
import java.util.Optional;
import java.util.OptionalDouble;
import java.util.OptionalInt;
import org.junit.rules.ExternalResource;

public class DriverStationSimResource extends ExternalResource {

  public static class ModificationBuilder {
    private Optional<Boolean> enabled = Optional.empty();
    private Optional<Boolean> autonomous = Optional.empty();
    private Optional<Boolean> test = Optional.empty();
    private Optional<Boolean> eStop = Optional.empty();
    private Optional<Boolean> fmsAttached = Optional.empty();
    private Optional<Boolean> dsAttached = Optional.empty();
    private Optional<AllianceStationID> allianceStationId = Optional.empty();
    private OptionalDouble matchTime = OptionalDouble.empty();
    private Optional<Boolean> sendError = Optional.empty();
    private Optional<Boolean> sendConsoleLine = Optional.empty();
    private Optional<String> eventName = Optional.empty();
    private Optional<DriverStation.MatchType> matchType = Optional.empty();
    private OptionalInt matchNumber = OptionalInt.empty();
    private OptionalInt replayNumber = OptionalInt.empty();

    public ModificationBuilder enabled(boolean enabled) {
      this.enabled = Optional.of(enabled);
      return this;
    }

    public ModificationBuilder autonomous(boolean autonomous) {
      this.autonomous = Optional.of(autonomous);
      return this;
    }

    public ModificationBuilder test(boolean test) {
      this.test = Optional.of(test);
      return this;
    }

    public ModificationBuilder eStop(boolean eStop) {
      this.eStop = Optional.of(eStop);
      return this;
    }

    public ModificationBuilder fmsAttached(boolean fmsAttached) {
      this.fmsAttached = Optional.of(fmsAttached);
      return this;
    }

    public ModificationBuilder dsAttahced(boolean dsAttahced) {
      this.dsAttached = Optional.of(dsAttahced);
      return this;
    }

    public ModificationBuilder allianceStationId(AllianceStationID allianceStationId) {
      this.allianceStationId = Optional.of(allianceStationId);
      return this;
    }

    public ModificationBuilder matchTime(double matchTime) {
      this.matchTime = OptionalDouble.of(matchTime);
      return this;
    }

    public ModificationBuilder sendError(boolean sendError) {
      this.sendError = Optional.of(sendError);
      return this;
    }

    public ModificationBuilder sendConsoleLine(boolean sendConsoleLine) {
      this.sendConsoleLine = Optional.of(sendConsoleLine);
      return this;
    }

    public ModificationBuilder eventName(String eventName) {
      this.eventName = Optional.of(eventName);
      return this;
    }

    public ModificationBuilder matchType(DriverStation.MatchType matchType) {
      this.matchType = Optional.of(matchType);
      return this;
    }

    public ModificationBuilder matchNumber(int matchNumber) {
      this.matchNumber = OptionalInt.of(matchNumber);
      return this;
    }

    public ModificationBuilder replayNumber(int replayNumber) {
      this.replayNumber = OptionalInt.of(replayNumber);
      return this;
    }

    public void perform() {
      this.enabled.ifPresent(DriverStationSim::setEnabled);
      this.autonomous.ifPresent(DriverStationSim::setAutonomous);
      this.test.ifPresent(DriverStationSim::setTest);
      this.eStop.ifPresent(DriverStationSim::setEStop);
      this.fmsAttached.ifPresent(DriverStationSim::setFmsAttached);
      this.dsAttached.ifPresent(DriverStationSim::setDsAttached);
      this.allianceStationId.ifPresent(DriverStationSim::setAllianceStationId);
      this.matchTime.ifPresent(DriverStationSim::setMatchTime);
      this.sendError.ifPresent(DriverStationSim::setSendError);
      this.sendConsoleLine.ifPresent(DriverStationSim::setSendConsoleLine);
      this.eventName.ifPresent(DriverStationSim::setEventName);
      this.matchType.ifPresent(DriverStationSim::setMatchType);
      this.matchNumber.ifPresent(DriverStationSim::setMatchNumber);
      this.replayNumber.ifPresent(DriverStationSim::setMatchNumber);
      DriverStationSim.notifyNewData();
    }
  }

  public static ModificationBuilder modificationBuilder() {
    return new ModificationBuilder();
  }

  @Override
  protected void after() {
    DriverStationSim.resetData();
    DriverStationSim.notifyNewData();
  }
}
