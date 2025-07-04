package com.team2813;

import java.util.function.Supplier;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.ExtensionContext.Store;

/**
 * A type-safe key for use in a {@link Store}.
 *
 * <p>TODO: Move to lib2813 once we create a testing library there.
 *
 * @param <V> the type for values stored in this store.
 */
final class StoreKey<V> {
  private final Class<V> requiredType;

  /**
   * Creates a key for storing data of the provided type.
   *
   * <p>Values returned from this method should almost always be stored in static final fields.
   */
  public static <V> StoreKey<V> of(Class<V> requiredType) {
    return new StoreKey<>(requiredType);
  }

  private StoreKey(Class<V> requiredType) {
    this.requiredType = requiredType;
  }

  /**
   * Gets the value that is stored under this key.
   *
   * <p>If no value is stored in the current {@link ExtensionContext} for this key, ancestors of the
   * context will be queried for a value with this key in the {@code Namespace} used to create this
   * store.
   *
   * @param store the store to get data from.
   * @see #getOrDefault(Store, V)
   */
  public V get(Store store) {
    return store.get(this, requiredType);
  }

  /**
   * Gets the value of the specified required type that is stored under this key, or the supplied
   * {@code defaultValue} if no value is found for this key in this store or in an ancestor.
   *
   * <p>If no value is stored in the current {@link ExtensionContext} for this, ancestors of the
   * context will be queried for a value with this key in the {@code Namespace} used to create this
   * store.
   *
   * @param store the store to get data from.
   * @param defaultValue the default value.
   * @return the value; potentially {@code null}.
   * @see #get(Store)
   */
  public V getOrDefault(Store store, V defaultValue) {
    return store.getOrDefault(this, requiredType, defaultValue);
  }

  /**
   * Gets the value of the specified required type that is stored under this key.
   *
   * <p>If no value is stored in the current {@link ExtensionContext} for this key, ancestors of the
   * context will be queried for a value with this key in the {@code Namespace} used to create this
   * store. If no value is found for this key a new value will be computed by the {@code
   * valueSupplier}, stored, and returned.
   *
   * <p>If {@code requiredType} implements {@link Store.CloseableResource} or {@link AutoCloseable}
   * (unless the {@code junit.jupiter.extensions.store.close.autocloseable.enabled} configuration
   * parameter is set to {@code false}), then the {@code close()} method will be invoked on the
   * stored object when the store is closed.
   *
   * @param store the store to use to get and store the data.
   * @param valueSupplier the function called to create a new value; never {@code null} but may
   *     return {@code null}.
   * @return the value; potentially {@code null}.
   * @see Store.CloseableResource
   * @see AutoCloseable
   */
  public V getOrComputeIfAbsent(Store store, Supplier<V> valueSupplier) {
    return store.getOrComputeIfAbsent(this, key -> valueSupplier.get(), requiredType);
  }

  /**
   * Stores a {@code value} for later retrieval under this key.
   *
   * <p>A stored {@code value} is visible in child {@link ExtensionContext ExtensionContexts} for
   * the store's {@code Namespace} unless they overwrite it.
   *
   * <p>If the {@code value} is an instance of {@link Store.CloseableResource} or {@link
   * AutoCloseable} (unless the {@code junit.jupiter.extensions.store.close.autocloseable.enabled}
   * configuration parameter is set to {@code false}), then the {@code close()} method will be
   * invoked on the stored object when the store is closed.
   *
   * @param store the store to put data into.
   * @param value the value to store; may be {@code null}.
   * @see Store.CloseableResource
   * @see AutoCloseable
   */
  public void put(Store store, V value) {
    store.put(this, value);
  }

  /**
   * Removes the value of the specified required type that was previously stored under this key.
   *
   * <p>The value will only be removed in the current {@link ExtensionContext}, not in ancestors. In
   * addition, the {@link Store.CloseableResource} and {@link AutoCloseable} API will not be honored
   * for values that are manually removed via this method.
   *
   * @param store the store to remove data from.
   * @return the previous value or {@code null} if no value was present for the specified key.
   */
  public V remove(Store store) {
    return store.remove(this, requiredType);
  }
}
