package com.team2813;

import static com.google.common.truth.Truth.assertThat;

import com.pathplanner.lib.events.EventTrigger;
import java.lang.reflect.Field;
import java.util.Arrays;
import java.util.Collection;
import java.util.Map;
import org.junit.ClassRule;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExternalResource;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;

@RunWith(Parameterized.class)
public class EventTriggerTest {
  private final FakeShuffleboardTabs shuffleboard = new FakeShuffleboardTabs();
  @Rule public final NetworkTableResource networkTable = new NetworkTableResource();

  public static class PathPlannerMap extends ExternalResource {
    private Map<String, Boolean> theMap;

    @Override
    protected void before() throws Throwable {
      Field field = EventTrigger.class.getDeclaredField("eventConditions");
      field.setAccessible(true);
      // should always succeed.
      @SuppressWarnings("unchecked")
      Map<String, Boolean> theMap = (Map<String, Boolean>) field.get(null);
      this.theMap = theMap;
      field.setAccessible(false);
    }

    private Map<String, Boolean> getMap() {
      return theMap;
    }
  }

  @ClassRule public static final PathPlannerMap pathPlannerMapProvider = new PathPlannerMap();

  @Parameterized.Parameters(name = "{0}")
  public static Collection<?> data() {
    return Arrays.asList("PrepareL2", "PrepareL3");
  }

  @Parameterized.Parameter public String eventName;

  @Test
  public void eventExists() {
    try (var container =
        RobotContainer.create(shuffleboard, networkTable.getNetworkTableInstance())) {
      // RobotContainer.create() has a side effect of registering named commands.
      // Sadly, all the methods of NamedCommands are static, so we cannot make this
      // dependency explicit.
      assertThat(pathPlannerMapProvider.getMap().containsKey(eventName)).isTrue();
    }
  }
}
