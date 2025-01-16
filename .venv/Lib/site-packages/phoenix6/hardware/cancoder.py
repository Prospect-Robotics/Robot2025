"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.hardware.core.core_cancoder import CoreCANcoder

try:
    import hal
    from hal import SimDevice, simulation
    from wpilib import RobotBase
    from wpiutil import Sendable, SendableBuilder, SendableRegistry

    from phoenix6 import utils
    from phoenix6.canbus import CANBus
    from phoenix6.phoenix_native import Native
    from phoenix6.sim.device_type import DeviceType
    from phoenix6.wpiutils.auto_feed_enable import AutoFeedEnable
    from phoenix6.wpiutils.replay_auto_enable import ReplayAutoEnable

    import copy
    import ctypes

    class CANcoder(CoreCANcoder, Sendable):
        """
        Constructs a new CANcoder object.

        :param device_id: ID of the device, as configured in Phoenix Tuner.
        :type device_id: int
        :param canbus: Name of the CAN bus this device is on. Possible CAN bus strings are:

            - "rio" for the native roboRIO CAN bus
            - CANivore name or serial number
            - SocketCAN interface (non-FRC Linux only)
            - "*" for any CANivore seen by the program
            - empty string (default) to select the default for the system:

                - "rio" on roboRIO
                - "can0" on Linux
                - "*" on Windows

        :type canbus: str | CANBus, optional
        """

        __SIM_DEVICE_TYPE = DeviceType.P6_CANcoderType

        def __init__(self, device_id: int, canbus: str | CANBus = ""):
            CoreCANcoder.__init__(self, device_id, canbus)
            Sendable.__init__(self)

            # The StatusSignal getters are copies so that calls
            # to the WPI interface do not update any references
            self.__position_getter = copy.deepcopy(self.get_position(False))

            SendableRegistry.addLW(self, "CANcoder (v6) ", device_id)

            if RobotBase.isSimulation():
                # run in both swsim and hwsim
                AutoFeedEnable.get_instance().start()
            if utils.is_replay():
                ReplayAutoEnable.get_instance().start()

            self.__sim_cancoder = SimDevice("CANEncoder:CANcoder (v6)", device_id)

            self.__sim_periodic_before_callback: simulation.SimCB | None = None
            self.__sim_value_changed_callbacks: list[simulation.SimValueCB] = []

            if self.__sim_cancoder:
                self.__sim_periodic_before_callback = simulation.registerSimPeriodicBeforeCallback(self.__on_periodic)

                self.__sim_supply_voltage = self.__sim_cancoder.createDouble("supplyVoltage", SimDevice.Direction.kInput, 12.0)

                self.__sim_position = self.__sim_cancoder.createDouble("position", SimDevice.Direction.kOutput, 0)

                self.__sim_raw_position = self.__sim_cancoder.createDouble("rawPositionInput", SimDevice.Direction.kInput, 0)
                self.__sim_velocity = self.__sim_cancoder.createDouble("velocity", SimDevice.Direction.kInput, 0)

                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_supply_voltage, self.__on_value_changed, True))
                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_raw_position, self.__on_value_changed, True))
                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_velocity, self.__on_value_changed, True))

        def __enter__(self) -> 'CANcoder':
            return self

        def __exit__(self, *_):
            self.close()

        def close(self):
            SendableRegistry.remove(self)
            if self.__sim_periodic_before_callback is not None:
                self.__sim_periodic_before_callback.cancel()
                self.__sim_periodic_before_callback = None

            for callback in self.__sim_value_changed_callbacks:
                callback.cancel()
            self.__sim_value_changed_callbacks.clear()

            AutoFeedEnable.get_instance().stop()
            ReplayAutoEnable.get_instance().stop()

        # ----- Callbacks for Sim -----
        def __on_value_changed(self, name: str, handle: int, _: hal.SimValueDirection, value: hal.Value):
            device_name = simulation.getSimDeviceName(simulation.getSimValueDeviceHandle(handle))
            phys_type = device_name + ":" + name
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes(phys_type, 'utf-8')),
                float(value.value),
            )

        def __on_periodic(self):
            value = ctypes.c_double()
            err: int = 0

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("SupplyVoltage", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_supply_voltage.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("Position", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_position.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("RawPosition", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_raw_position.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("Velocity", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_velocity.set(value.value)

        # ----- Sendable -----
        def initSendable(self, builder: SendableBuilder):
            builder.setSmartDashboardType("CANcoder")
            builder.addDoubleProperty("Position", self.__position_getter.as_supplier(), self.set_position)

except ImportError:
    class CANcoder(CoreCANcoder):
        # Stub class to remove the "Core" string of CANcoder
        pass
