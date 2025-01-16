"""
Base class for Phoenix Hardware Devices
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import copy
import ctypes
from threading import RLock
from typing import Protocol, Callable, TypeVar
from phoenix6.phoenix_native import Native
from phoenix6.hardware.device_identifier import DeviceIdentifier
from phoenix6.controls.empty_control import EmptyControl
from phoenix6.spns.spn_value import SpnValue
from phoenix6.status_signal import StatusSignal
from phoenix6.status_code import StatusCode
from phoenix6.unmanaged import get_api_compliancy
from phoenix6.error_reporting import report_status_code
from phoenix6.utils import get_current_time_seconds
from phoenix6.units import hertz, second

DEFAULT_CONTROL_RATE_PERIOD_SEC = 0.010

class SupportsSendRequest(Protocol):
    """
    Represents any type that can be used to
    send a control request to a device.
    """

    @property
    def name(self) -> str:
        pass

    @property
    def control_info(self) -> dict:
        pass

    def _send_request(self, network: str, device_hash: int) -> StatusCode:
        pass

    def with_update_freq_hz(self, new_update_freq_hz: hertz) -> 'SupportsSendRequest':
        pass

T = TypeVar("T")

class ParentDevice:
    """
    Base class of Phoenix devices.
    This holds the base information for the devices, and
    can be used as a generic type to hold onto a collection
    of multiple devices.
    """

    __empty_control = EmptyControl()

    def __init__(self, device_id: int, model: str, canbus: str):
        """
        Constructor for a device

        :param deviceId: ID of the device
        :type deviceId: int
        :param model: Model of the device
        :type model: str
        :param canbus: CANbus the device is on
        :type canbus: str
        """
        self._device_identifier = DeviceIdentifier(device_id, model, canbus)

        self.__signal_values: dict[int, StatusSignal] = {}
        self.__control_request = ParentDevice.__empty_control
        self.__control_request_lck = RLock()

        self.__creation_time = get_current_time_seconds()

        self.__is_initialized = False
        self.__version_status = StatusCode.COULD_NOT_RETRIEVEV6_FIRMWARE
        self.__time_to_refresh_version = get_current_time_seconds()

        self.__compliancy = self._common_lookup(SpnValue.COMPLIANCY_VERSION.value, None, "Compliancy", int, False, True)
        self.__reset_signal = self._common_lookup(SpnValue.STARTUP_RESET_FLAGS.value, None, "ResetFlags", int, False, True)

        self.__is_initialized = True

    @property
    def device_id(self) -> int:
        """
        Gets the ID of this device.

        :return: ID of this device
        :rtype: int
        """
        return self._device_identifier.device_id

    @property
    def network(self) -> str:
        """
        Gets the name of the network this device is on.

        :return: Name of the network this device is on
        :rtype: str
        """
        return self._device_identifier.network

    @property
    def device_hash(self) -> int:
        """
        Gets a number unique for this device's hardware type and ID.
        This number is not unique across networks.

        This can be used to easily reference hardware devices on
        the same network in collections such as maps.

        :return: Hash of this device
        :rtype: int
        """
        return self._device_identifier.device_hash

    @property
    def control_request(self) -> SupportsSendRequest:
        """
        Get the latest applied control.

        :returns: Latest applied control
        :rtype: SupportsSendRequest
        """
        return self.__control_request

    @property
    def has_reset_occurred(self) -> bool:
        """
        Check if the device has reset since the previous call to this routine

        :return: True if device has reset
        :rtype: bool
        """
        return self.__reset_signal.refresh(False).has_updated

    def get_reset_occurred_checker(self) -> Callable[[], bool]:
        """
        Get a lambda that checks for device resets.

        :return: A lambda that checks for device resets
        :rtype: Callable[[], bool]
        """
        reset_signal = copy.deepcopy(self.__reset_signal)
        return lambda: reset_signal.refresh(False).has_updated

    @property
    def is_connected(self, max_latency_seconds: second = 0.5) -> bool:
        """
        Returns whether the device is still connected to the robot.
        This is equivalent to refreshing and checking the latency of the
        Version status signal.

        :param max_latency_seconds: The maximum latency of the Version status signal
                                    before the device is reported as disconnected
        :type max_latency_seconds: float
        :returns: True if the device is connected
        :rtype: bool
        """
        return self.__compliancy.refresh(False).timestamp.get_latency() <= max_latency_seconds

    def optimize_bus_utilization(self, optimized_freq_hz: hertz = 0.0, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Optimizes the device's bus utilization by reducing the
        update frequencies of its status signals.

        All status signals that have not been explicitly gven an
        update frequency using BaseStatusSignal.set_update_frequency
        will be disabled. Note that if other status signals in the
        same frame have been given an update frequency, the update
        frequency will be honored for the entire frame.

        This function only needs to be called once on this device
        in the robot program. Additionally, this method does not
        necessarily need to be called after setting the update
        frequencies of other signals.

        To restore the default status update frequencies, call
        reset_signal_frequencies. Alternatively, remove this method
        call, redeploy the robot application, and power-cycle the
        device on the bus. The user can also override individual
        status update frequencies using BaseStatusSignal.set_update_frequency.

        :param optimized_freq_hz:   The update frequency to apply to
                                    the optimized status signals. A
                                    frequency of 0 Hz (default) will
                                    turn off the signals. Otherwise,
                                    the minimum supported signal
                                    frequency is 4 Hz.
        :type optimized_freq_hz: hertz, optional
        :param timeout_seconds: Maximum amount of time to wait
                                for each status frame when
                                performing the action
        :type timeout_seconds: second, optional
        :return:    Status code of the first failed update frequency
                    set call, or OK if all succeeded.
        :rtype: StatusCode
        """
        network = ctypes.c_char_p(bytes(self.network, 'utf-8'))
        return StatusCode(Native.instance().c_ctre_phoenix6_OptimizeUpdateFrequencies(0, network, self.device_hash, optimized_freq_hz, timeout_seconds))

    @staticmethod
    def optimize_bus_utilization_for_all(*devices: 'ParentDevice | list[ParentDevice]', optimized_freq_hz: hertz = 0.0) -> StatusCode:
        """
        Optimizes the bus utilization of the provided devices by
        reducing the update frequencies of their status signals.

        All status signals that have not been explicitly given an
        update frequency using BaseStatusSignal.set_update_frequency
        will be disabled. Note that if other status signals in the
        same status frame have been given an update frequency, the
        update frequency will be honored for the entire frame.

        This function only needs to be called once in the robot
        program for the provided devices. Additionally, this method
        does not necessarily need to be called after setting the
        update frequencies of other signals.

        To restore the default status update frequencies, call
        reset_signal_frequencies_for_all. Alternatively, remove this
        method call, redeploy the robot application, and power-cycle
        the devices on the bus. The user can also override individual
        status update frequencies using BaseStatusSignal.set_update_frequency.

        This will wait up to 0.100 seconds (100ms) for each status frame.

        :param devices: Devices for which to optimize bus utilization.
        :type devices: tuple[ParentDevice | list[ParentDevice], ...]
        :param optimized_freq_hz:   The update frequency to apply to
                                    the optimized status signals. A
                                    frequency of 0 Hz (default) will
                                    turn off the signals. Otherwise,
                                    the minimum supported signal
                                    frequency is 4 Hz. This must be
                                    specified using a named parameter
                                    at the end of the parameter list.
        :type optimized_freq_hz: hertz, optional
        :returns:   Status code of the first failed optimize call,
                    or OK if all succeeded
        :rtype: StatusCode
        """
        retval = StatusCode.OK
        for device in ParentDevice.__flatten_devices(*devices):
            err = device.optimize_bus_utilization(optimized_freq_hz)
            if err.is_ok():
                retval = err
        return retval

    def reset_signal_frequencies(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Resets the update frequencies of all the device's status signals
        to the defaults.

        This restores the default update frequency of all status signals,
        including status signals explicitly given an update frequency using
        BaseStatusSignal.set_update_frequency and status signals optimized
        out using optimize_bus_utilization.

        :param timeout_seconds: Maximum amount of time to wait
                                for each status frame when
                                performing the action
        :type timeout_seconds: second, optional
        :return:    Status code of the first failed update frequency
                    set call, or OK if all succeeded.
        :rtype: StatusCode
        """
        network = ctypes.c_char_p(bytes(self.network, 'utf-8'))
        return StatusCode(Native.instance().c_ctre_phoenix6_ResetUpdateFrequencies(0, network, self.device_hash, timeout_seconds))

    @staticmethod
    def reset_signal_frequencies_for_all(*devices: 'ParentDevice | list[ParentDevice]') -> StatusCode:
        """
        Resets the update frequencies of all the devices' status signals
        to the defaults.

        This restores the default update frequency of all status signals,
        including status signals explicitly given an update frequency using
        BaseStatusSignal.set_update_frequency and status signals optimized
        out using optimize_bus_utilization_for_all.

        This will wait up to 0.100 seconds (100ms) for each status frame.

        :param devices: Devices for which to restore default update frequencies.
        :type devices: tuple[ParentDevice | list[ParentDevice], ...]
        :returns:   Status code of the first failed restore call,
                    or OK if all succeeded
        :rtype: StatusCode
        """
        retval = StatusCode.OK
        for device in ParentDevice.__flatten_devices(*devices):
            err = device.reset_signal_frequencies()
            if err.is_ok():
                retval = err
        return retval

    def __report_if_too_old(self):
        # if version is correct, no more checking
        if self.__version_status.is_ok():
            return
        # If we're not initialized, we can't even check the versions
        if not self.__is_initialized:
            return

        # get fresh data if enough time has passed
        current_time = get_current_time_seconds()
        if current_time >= self.__time_to_refresh_version:
            # Try to refresh again after 250ms
            self.__time_to_refresh_version = current_time + 0.25
            # Refresh versions, don't print out if there's an error with refreshing
            self.__compliancy.refresh(False)

            # process the fetched version
            code = StatusCode.OK

            # First check if we have good versions or not
            if self.__compliancy.status.is_ok():
                firmware_compliancy = self.__compliancy.value
                api_compliancy = get_api_compliancy()

                if api_compliancy > firmware_compliancy:
                    code = StatusCode.FIRMWARE_TOO_OLD
                elif api_compliancy < firmware_compliancy:
                    code = StatusCode.API_TOO_OLD
            else:
                # don't care why we couldn't get message, just report we didn't get it
                code = StatusCode.COULD_NOT_RETRIEVEV6_FIRMWARE

            # how much time has passed
            delta_time_sec = current_time - self.__creation_time

            if code.is_ok():
                # version is retrieved and healthy
                pass
            elif (code is StatusCode.FIRMWARE_TOO_OLD or code is StatusCode.API_TOO_OLD) or delta_time_sec >= 3.0:
                # report error
                report_status_code(code, str(self._device_identifier))
            else:
                # don't start reporting COULD_NOT_RETRIEVEV6_FIRMWARE yet, device was likely recently constructed
                pass
            # save the status code
            self.__version_status = code

    def _set_control_private(self, request: SupportsSendRequest) -> StatusCode:
        """
        Sets the control request to this device

        :param request: Control request to set
        :type request: SupportsSendRequest
        """
        with self.__control_request_lck:
            self.__report_if_too_old()
            if not self.__version_status.is_ok() and self.__compliancy.status.is_ok():
                # version mismatch, cancel controls and report the error
                self.__control_request = ParentDevice.__empty_control
                ParentDevice.__empty_control._send_request(self.network, self.device_hash)
                status = self.__version_status
            else:
                # send the request
                self.__control_request = request
                status = request._send_request(self.network, self.device_hash)

        if not status.is_ok():
            location = str(self._device_identifier) + " Set Control " + request.name
            report_status_code(status, location)
        return status

    def _common_lookup(self, spn: int, generator: Callable[[], dict[int, str]], signal_name: str, signal_type: type[T], report_on_construction: bool, refresh: bool) -> StatusSignal[T]:
        # Lookup and return if found
        if spn in self.__signal_values:
            # Found it, save it under to_find
            to_find = self.__signal_values[spn]
            # Since we didn't construct, report errors
            report_on_construction = True
        else:
            # Insert into map
            if generator is None:
                self.__signal_values[spn] = StatusSignal(None, self._device_identifier, spn, self.__report_if_too_old, None, signal_name, signal_type)
            else:
                self.__signal_values[spn] = StatusSignal(None, self._device_identifier, spn, self.__report_if_too_old, generator, signal_name, signal_type)

            # Lookup and return
            to_find = self.__signal_values[spn]

        # Refresh and return
        if refresh:
            to_find.refresh(report_on_construction)
        return to_find

    @staticmethod
    def __flatten_devices(*devices: 'ParentDevice | list[ParentDevice]') -> list['ParentDevice']:
        devs: list['ParentDevice'] = []
        for dev in devices:
            if isinstance(dev, list):
                devs.extend(dev)
            else:
                devs.append(dev)
        return devs
