"""
Base class for device configurators
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.hardware.device_identifier import DeviceIdentifier
from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
from phoenix6.error_reporting import report_status_code
from phoenix6.units import *
from phoenix6.utils import get_current_time_seconds
import ctypes
from threading import RLock

class ParentConfigurator:
    def __init__(self, device_identifier: DeviceIdentifier):
        self.__device_identifier = device_identifier
        self.__lock = RLock()

        self.__creation_time = get_current_time_seconds()
        self.__last_config_time = self.__creation_time
        self.__freq_config_start = 0.0

    def _report_if_frequent(self):
        current_time = get_current_time_seconds()
        last_config_time = self.__last_config_time
        self.__last_config_time = current_time

        if current_time - self.__creation_time < 5.0:
            # this was constructed recently, do not warn
            return

        if current_time - last_config_time < 1.0:
            # we should not see multiple configs within a second
            if self.__freq_config_start == 0.0:
                # this is the first frequent config, capture the time we started seeing them
                self.__freq_config_start = last_config_time
        else:
            # this is not a frequent config, reset the start time
            self.__freq_config_start = 0.0

        if self.__freq_config_start > 0.0 and current_time - self.__freq_config_start > 3.0:
            # we've been seeing frequent config calls continuously for a few seconds, warn user
            location = str(self.__device_identifier) + " Config"
            report_status_code(StatusCode.FREQUENT_CONFIG_CALLS, location)

    def _set_configs_private(self, serial_string: str, timeout_seconds: second, future_proof_configs: bool, override_if_duplicate: bool):
        with self.__lock:
            status = StatusCode(Native.instance().c_ctre_phoenix6_set_configs(
                0,
                ctypes.c_char_p(bytes(self.__device_identifier.network, encoding='utf-8')),
                self.__device_identifier.device_hash,
                timeout_seconds,
                ctypes.c_char_p(bytes(serial_string, 'utf-8')),
                len(serial_string),
                future_proof_configs,
                override_if_duplicate,
                False
            ))
            self._report_if_frequent()

        if not status.is_ok() and status != StatusCode.TIMEOUT_CANNOT_BE_ZERO:
            location = str(self.__device_identifier) + " Apply Config"
            report_status_code(status, location)
        return status

    def _get_configs_private(self, timeout_seconds: second) -> tuple[StatusCode, str]:
        values = ctypes.c_char_p()
        with self.__lock:
            status = StatusCode(Native.instance().c_ctre_phoenix6_get_configs(
                0,
                ctypes.c_char_p(bytes(self.__device_identifier.network, encoding='utf-8')),
                self.__device_identifier.device_hash,
                timeout_seconds,
                ctypes.byref(values),
                False
            ))
            self._report_if_frequent()

        to_return = ""

        if values.value is not None:
            # Value is not none, so bring it over and free it
            to_return = str(values.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(values))
        if not status.is_ok():
            location = str(self.__device_identifier) + " Refresh Config"
            report_status_code(status, location)
        return (status, to_return)
