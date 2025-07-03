package com.team2813;

import edu.wpi.first.networktables.NetworkTableInstance;
import org.junit.jupiter.api.extension.AfterEachCallback;
import org.junit.jupiter.api.extension.Extension;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.ExtensionContext.Namespace;
import org.junit.jupiter.api.extension.ExtensionContext.Store;
import org.junit.jupiter.api.extension.ParameterContext;
import org.junit.jupiter.api.extension.ParameterResolutionException;
import org.junit.jupiter.api.extension.ParameterResolver;

/**
 * JUnit Jupiter extension for providing an isolated NetworkTableInstance to tests.
 *
 * <p>Example use:
 *
 * <pre>{@code
 * @ExtendWith(IsolatedNetworkTablesExtension.class)
 * public final class IntakeTest {
 *
 *   @Test
 *   public void intakeCoral(NetworkTableInstance ntInstance)  {
 *     // Do something with ntInstance
 *   }
 * }
 * }</pre>
 */
public final class IsolatedNetworkTablesExtension
    implements Extension, AfterEachCallback, ParameterResolver {
  private static final String NETWORK_TABLE_INSTANCE_KEY = "networkTableInstance";

  @Override
  public void afterEach(ExtensionContext context) throws Exception {
    var networkTableInstance =
        getStore(context).get(NETWORK_TABLE_INSTANCE_KEY, NetworkTableInstance.class);
    if (networkTableInstance != null) {
      networkTableInstance.close();
    }
  }

  @Override
  public boolean supportsParameter(
      ParameterContext parameterContext, ExtensionContext extensionContext)
      throws ParameterResolutionException {
    return NetworkTableInstance.class.equals(parameterContext.getParameter().getType());
  }

  @Override
  public NetworkTableInstance resolveParameter(
      ParameterContext parameterContext, ExtensionContext extensionContext)
      throws ParameterResolutionException {
    Store store = getStore(extensionContext);
    return store.getOrComputeIfAbsent(
        NETWORK_TABLE_INSTANCE_KEY,
        key -> NetworkTableInstance.create(),
        NetworkTableInstance.class);
  }

  private Store getStore(ExtensionContext context) {
    return context.getStore(Namespace.create(getClass(), context.getRequiredTestMethod()));
  }
}
