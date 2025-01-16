"""
Contains the device identifier class used to identify
a Phoenix hardware device at the low level
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from phoenix6.phoenix_native import Native


class DeviceIdentifier:
    def __init__(self, device_id: int, model: str, canbus: str):
        """
        Constructs a new device identifier with the specified
        parameters

        :param deviceId: ID of the device
        :type deviceId: int
        :param model: Model of the device
        :type model: str
        :param canbus: What CAN bus the device is on
        :type canbus: str
        """

        self.__device_id = device_id
        self.__model = model
        self.__network = canbus

        model_bytes = bytes(model, "utf-8")
        canbus_bytes = bytes(canbus, "utf-8")

        val = ctypes.c_uint32()

        Native.instance().c_ctre_phoenix6_encode_device(
            self.__device_id, ctypes.c_char_p(model_bytes), ctypes.c_char_p(canbus_bytes), ctypes.byref(val)
        )

        self.__device_hash = val.value

    def __str__(self) -> str:
        """
        Override string method

        :return: String representation of this object
        :rtype: str
        """
        return f'{self.__model} {self.__device_id} ("{self.__network}")'

    @property
    def network(self) -> str:
        """
        Gets the network

        :return: Network
        :rtype: str
        """
        return self.__network

    @property
    def model(self) -> str:
        """
        Gets the model

        :return: Model
        :rtype: str
        """
        return self.__model

    @property
    def device_id(self) -> int:
        """
        Gets the device id

        :return: Device ID
        :rtype: int
        """
        return self.__device_id

    @property
    def device_hash(self) -> int:
        """
        Gets the device hash

        :return: Device hash
        :rtype: int
        """
        return self.__device_hash
