package com.team2813;

import static edu.wpi.first.util.ErrorMessages.requireNonNullParam;

import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;

import java.util.concurrent.atomic.AtomicInteger;

public class FakeShuffleboardTabs implements ShuffleboardTabs {
  public static final FakeShuffleboardTabs INSTANCE = new FakeShuffleboardTabs();
  private static final AtomicInteger nextValue = new AtomicInteger(1);

  private FakeShuffleboardTabs() {}

  @Override
  public ShuffleboardTab getTab(String title) {
    requireNonNullParam(title, "title", "getTab");
    int value = nextValue.getAndIncrement();
    return Shuffleboard.getTab("f" + value + title);
  }
}
