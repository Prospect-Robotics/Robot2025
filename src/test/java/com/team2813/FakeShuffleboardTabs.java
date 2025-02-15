package com.team2813;

import static edu.wpi.first.util.ErrorMessages.requireNonNullParam;

import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;

import java.util.concurrent.atomic.AtomicInteger;

public class FakeShuffleboardTabs implements ShuffleboardTabs {
  private static final AtomicInteger nextValue = new AtomicInteger(1);
  private final String prefix;

  public FakeShuffleboardTabs() {
    prefix = "f" + nextValue.getAndIncrement();
  }

  @Override
  public ShuffleboardTab getTab(String title) {
    requireNonNullParam(title, "title", "getTab");
    return Shuffleboard.getTab(prefix + title);
  }

  @Override
  public void selectTab(String title) {
    requireNonNullParam(title, "title", "getTab");
    Shuffleboard.selectTab(prefix + title);
  }
}
