package com.team2813;

import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;

/**
 * Wrapper around {@link Shuffleboard#getTab}, for providing a seam for testing.
 */
public interface ShuffleboardTabs {
  ShuffleboardTab getTab(String title);
  void selectTab(String title);
}
