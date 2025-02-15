package com.team2813;

import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;

/**
 * Wrapper around {@link Shuffleboard#getTab}, for providing a seam for testing.
 */
public interface ShuffleboardTabs {
  ShuffleboardTab getTab(String title);
  void selectTab(String title);

  static ShuffleboardTabs forDefaultNetworkTableInstance() {
    return new ShuffleboardTabs() {
      @Override
      public ShuffleboardTab getTab(String title) {
        return Shuffleboard.getTab(title);
      }

      @Override
      public void selectTab(String title) {
        Shuffleboard.selectTab(title);
      }
    };
  }
}
