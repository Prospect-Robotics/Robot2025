package com.team2813;

import static edu.wpi.first.util.ErrorMessages.requireNonNullParam;

import com.team2813.lib2813.util.ShuffleboardTabs;
import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;
import java.util.concurrent.atomic.AtomicInteger;

public final class FakeShuffleboardTabs implements ShuffleboardTabs {
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
    requireNonNullParam(title, "title", "selectTab");
    Shuffleboard.selectTab(prefix + title);
  }
}
