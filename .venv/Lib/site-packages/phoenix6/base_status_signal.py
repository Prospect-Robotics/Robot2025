"""
Common base class for StatusSignals
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from typing import Callable, TYPE_CHECKING
from phoenix6.phoenix_native import Native, SignalValues, ReturnValues, NetworkSignals
from phoenix6.timestamp import Timestamp, TimestampSource
from phoenix6.all_timestamps import AllTimestamps
from phoenix6.status_code import StatusCode
from phoenix6.error_reporting import report_status_code
from phoenix6.units import second, hertz
from abc import ABC, abstractmethod
import ctypes

if TYPE_CHECKING:
    from phoenix6.hardware.device_identifier import DeviceIdentifier
    from phoenix6.status_signal import StatusSignal


class BaseStatusSignal(ABC):
    """
    Common parent type for the :ref:StatusSignal: object.

    This can be used for a collection of :ref:StatusSignal: objects,
    but we recommend using the derived class instead when possible
    """

    def __init__(self, device_identifer: 'DeviceIdentifier', spn: int, signal_name: str, report_if_old_func: Callable[[], None]):
        """
        Normal Constructor for a BaseStatusSignal

        :param device_identifer: Identifier of the device this signal is associated to
        :type device_identifer: DeviceIdentifier
        :param spn: SPN Index of this signal
        :type spn: int
        :param signal_name: Name of this signal
        :type signal_name: str
        :param report_if_old_func: Function to call if device is too old
        :type report_if_old_func: Callable[[], None]
        """
        from phoenix6.hardware.device_identifier import DeviceIdentifier

        self.__last_timestamp: second = 0
        self._spn: int = spn
        self._value: float = 0
        self._identifier: DeviceIdentifier = device_identifer
        self._status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        self._all_timestamps: AllTimestamps = AllTimestamps()
        self._name: str = signal_name
        self._report_if_old_func: Callable[[], None] = report_if_old_func

        # Get the units for this signal
        rets: ReturnValues = ReturnValues()
        Native.instance().c_ctre_phoenix6_get_rets(self._spn, 2, ctypes.byref(rets))

        self._units = rets.units.decode("utf-8")

    @property
    def name(self) -> str:
        """
        The name of this signal.

        :return: The name of this signal
        :rtype: str
        """
        return self._name

    @property
    def units(self) -> str:
        """
        The units associated with this signal.

        :return: Units associated with this signal
        :rtype: str
        """
        return self._units

    @property
    def value_as_double(self) -> float:
        """
        Gets the value as a double instead of the generic
        type. This may be helpful when working with the
        base class.

        :return: Signal as a double
        :rtype: float
        """
        return self._value

    @property
    def all_timestamps(self) -> AllTimestamps:
        """
        All the timestamps associated with this signal.

        :return: All the timestamps associated with this signal
        :rtype: AllTimestamps
        """
        return self._all_timestamps

    @property
    def timestamp(self) -> Timestamp:
        """
        The most accurate timestamp available for this signal.

        The timestamp sources from most to least accurate are:

            - TimestampSource.Device
            - TimestampSource.CANivore
            - TimestampSource.System

        Note that some of these sources may not be available.

        :return: The most accurate timestamp available for this signal
        :rtype: Timestamp
        """
        return self._all_timestamps.get_best_timestamp()

    @property
    def status(self) -> StatusCode:
        """
        The status of the last time this signal was updated.

        :return: Status of the last time this signal was updated
        :rtype: StatusCode
        """
        return self._status

    @property
    def has_updated(self) -> bool:
        """
        Check whether the signal has been updated since the last check.

        Note that the signal must be refreshed before calling this routine.

        :return: True if the signal has updated since the previous call of this routine
        :rtype: bool
        """
        retval = False
        timestamp = self.all_timestamps.get_system_timestamp()
        if timestamp.is_valid:
            if self.__last_timestamp != timestamp.time:
                self.__last_timestamp = timestamp.time
                retval = True
        return retval

    @staticmethod
    def wait_for_all(timeout_seconds: second, *signals: 'BaseStatusSignal | list[BaseStatusSignal]') -> StatusCode:
        """
        Waits for new data on all provided signals up to timeout.
        This API is typically used with CANivore Bus signals as they will be synced using the
        CANivore Timesync feature and arrive simultaneously. Signals on a roboRIO bus cannot
        be synced and may require a significantly longer blocking call to receive all signals.

        Note that CANivore Timesync requires Phoenix Pro.

        This can also be used with a timeout of zero to refresh many signals at once, which
        is faster than calling refresh() on every signal. This is equivalent to calling refresh_all.

        If a signal arrives multiple times while waiting, such as when *not* using CANivore
        Timesync, the newest signal data is fetched. Additionally, if this function times out,
        the newest signal data is fetched for all signals (when possible). We recommend checking
        the individual status codes using self.status when this happens.

        :param timeout_seconds: Maximum time to wait for new data in seconds.
                                Pass zero to refresh all signals without blocking.
        :type timeout_seconds: second
        :param signals: Signals to wait for new data against
        :type signals: tuple[BaseStatusSignal | list[BaseStatusSignal], ...]
        :returns:   An InvalidParamValue if signals array is empty,
                    InvalidNetwork if signals are on different CAN bus networks,
                    RxTimeout if it took longer than timeoutSeconds to receive all the signals,
                    MultiSignalNotSupported if using the roboRIO bus with more than one signal and a non-zero timeout.
                    An OK status code means that all signals arrived within timeoutSeconds and they are all OK.

                    Any other value represents the StatusCode of the first failed signal.
                    Check the status of each signal to determine which ones failed.
        :rtype: StatusCode"""
        return BaseStatusSignal.__wait_for_all_impl("BaseStatusSignal.wait_for_all", timeout_seconds, BaseStatusSignal.__flatten_signals(*signals))

    @staticmethod
    def refresh_all(*signals: 'BaseStatusSignal | list[BaseStatusSignal]') -> StatusCode:
        """
        Performs a non-blocking refresh on all provided signals.

        This provides a performance improvement over separately
        calling refresh() on each signal.

        :param signals: Signals to refresh
        :type signals: tuple[BaseStatusSignal | list[BaseStatusSignal], ...]
        :returns:   An InvalidParamValue if signals array is empty,
                    InvalidNetwork if signals are on different CAN bus networks.
                    An OK status code means that all signals are OK.

                    Any other value represents the StatusCode of the first failed signal.
                    Check the status of each signal to determine which ones failed.
        :rtype: StatusCode
        """
        return BaseStatusSignal.__wait_for_all_impl("BaseStatusSignal.refresh_all", 0, BaseStatusSignal.__flatten_signals(*signals))

    @staticmethod
    def get_latency_compensated_value(signal: 'StatusSignal[float]', signal_slope: 'StatusSignal[float]', max_latency_seconds: second = 0.300) -> float:
        """
        Performs latency compensation on signal using the signalSlope and signal's latency to determine
        the magnitude of compensation. The caller must refresh these StatusSignals beforehand;
        this function only does the math required for latency compensation.

        Important: The signalSlope must be the rate of change of the signal. If it is not the latency
        compensation may not perform as expected.

        Example: compensatedTurns = BaseStatusSignal.get_latency_compensated_value(fx.get_position(), fx.get_velocity())

        :param signal:  Signal to be latency compensated. Caller must make sure this signal is up to date
                        either by calling StatusSignal.refresh() or StatusSignal.wait_for_update(double).
        :type signal: StatusSignal[float]
        :param signal_slope:    Derivative of signal that informs compensation magnitude. Caller must make sure this
                                signal is up to date either by calling StatusSignal.refresh() or StatusSignal.wait_for_update(double).
        :type signal: StatusSignal[float]
        :param max_latency_seconds: The maximum amount of latency to compensate for in seconds. A negative or zero
                                    value disables the max latency cap. This is used to cap the contribution of
                                    latency compensation for stale signals, such as after the device has been
                                    disconnected from the CAN bus.
        :type max_latency_seconds: second
        :returns: Latency compensated value from the signal StatusSignal.
        :rtype: float
        """
        non_compensated_signal = signal.value
        change_in_signal = signal_slope.value
        latency = signal.timestamp.get_latency()
        if max_latency_seconds > 0 and latency > max_latency_seconds:
            latency = max_latency_seconds
        return non_compensated_signal + (change_in_signal * latency)

    @staticmethod
    def is_all_good(*signals: 'BaseStatusSignal | list[BaseStatusSignal]') -> bool:
        """
        Checks if all signals have an OK error code.
        :param signals: Signals to check error code of
        :type signals: tuple[BaseStatusSignal | list[BaseStatusSignal], ...]
        :returns: True if all are good, False otherwise
        :rtype: bool
        """
        for sig in BaseStatusSignal.__flatten_signals(*signals):
            if not sig.status.is_ok():
                return False
        return True

    @staticmethod
    def set_update_frequency_for_all(frequency_hz: hertz, *signals: 'BaseStatusSignal | list[BaseStatusSignal]') -> StatusCode:
        """
        Sets the update frequency of all specified status signals to the provided common frequency.

        A frequency of 0 Hz will turn off the signal. Otherwise, the minimum supported signal
        frequency is 4 Hz, and the maximum is 1000 Hz.

        If other StatusSignals in the same status frame have been set to an update frequency,
        the fastest requested update frequency will be applied to the frame.

        This will wait up to 0.100 seconds (100ms) for each signal.

        :param frequency_hz: Rate to publish the signal in Hz
        :type frequency_hz: hertz
        :param signals: Signals to apply the update frequency to
        :type signals: tuple[BaseStatusSignal | list[BaseStatusSignal], ...]
        :returns: Status code of the first failed update frequency set call, or OK if all succeeded
        :rtype: StatusCode
        """
        signals = BaseStatusSignal.__flatten_signals(*signals)
        count = len(signals)
        sigs = (NetworkSignals * count)()
        for (i, sig) in enumerate(signals):
            sigs[i].signal.devicehash = sig._identifier.device_hash
            sigs[i].signal.spn = sig._spn
            sigs[i].network = ctypes.c_char_p(bytes(sig._identifier.network, 'utf-8'))
        return StatusCode(Native.instance().c_ctre_phoenix6_SetUpdateFrequencyForAll(0, sigs, count, frequency_hz, 0.100))

    def set_update_frequency(self, frequency_hz: hertz, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Sets the rate at which the device will publish this signal.

        A frequency of 0 Hz will turn off the signal. Otherwise, the minimum supported signal
        frequency is 4 Hz, and the maximum is 1000 Hz.

        If other StatusSignals in the same status frame have been set to an update frequency,
        the fastest requested update frequency will be applied to the frame.

        :param frequency_hz: Rate to publish the signal in Hz
        :type frequency_hz: hertz
        :param timeout_seconds: Maximum amount of time to wait when performing the action
        :type timeout_seconds: second
        :returns: Status code of setting the update frequency
        :rtype: StatusCode
        """
        network = ctypes.c_char_p(bytes(self._identifier.network, 'utf-8'))
        return StatusCode(Native.instance().c_ctre_phoenix6_SetUpdateFrequency(0, network, self._identifier.device_hash, self._spn, frequency_hz, timeout_seconds))

    def get_applied_update_frequency(self) -> hertz:
        """
        Gets the rate at which the device will publish this signal.

        This is typically the last value passed into set_update_frequency. The returned value
        may be higher if another StatusSignal in the same status frame has been set to a higher
        update frequency.

        :returns: Applied update frequency of the signal in Hz
        :rtype: hertz
        """
        network = ctypes.c_char_p(bytes(self._identifier.network, 'utf-8'))
        return Native.instance().c_ctre_phoenix6_GetUpdateFrequency(network, self._identifier.device_hash, self._spn)

    @staticmethod
    def __wait_for_all_impl(location: str, timeout_seconds: second, signals: list['BaseStatusSignal']) -> StatusCode:
        count = len(signals)
        if count < 1:
            report_status_code(StatusCode.INVALID_PARAM_VALUE.value, location)
            return StatusCode.INVALID_PARAM_VALUE

        network = signals[0]._identifier.network
        for signal in signals[1:]:
            if signal._identifier.network != network:
                # Networks don't match, return early
                status = StatusCode.INVALID_NETWORK
                report_status_code(status, location)
                return status

        for signal in signals:
            # Report if any device firmware versions are too old
            signal._report_if_old_func()

        # Now wait for all the signals
        sigs = (SignalValues * count)()
        rets = (ReturnValues * count)()
        for (i, signal) in enumerate(signals):
            sigs[i].devicehash = signal._identifier.device_hash
            sigs[i].spn = signal._spn

        status = StatusCode(Native.instance().c_ctre_phoenix6_get_signal(count, sigs, rets, ctypes.c_char_p(bytes(network, 'utf-8')), True, timeout_seconds))

        for (signal, ret) in zip(signals, rets):
            signal._status = StatusCode(ret.error)
            signal._value = ret.outValue
            signal._all_timestamps.update(
                ret.swtimestampseconds, TimestampSource.System, True,
                ret.hwtimestampseconds, TimestampSource.CANivore, True,
                ret.ecutimestampseconds, TimestampSource.Device, ret.ecutimestampseconds != 0.0
            )
            signal._update_units(ret.unitsKey)

        # error reporting
        if not status.is_ok():
            report_status_code(status, location)

        return status

    @staticmethod
    def __flatten_signals(*signals: 'BaseStatusSignal | list[BaseStatusSignal]') -> list['BaseStatusSignal']:
        sigs: list['BaseStatusSignal'] = []
        for sig in signals:
            if isinstance(sig, list):
                sigs.extend(sig)
            else:
                sigs.append(sig)
        return sigs

    @abstractmethod
    def _update_units(self, spn: int):
        pass
