"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.hardware.core.core_pigeon2 import CorePigeon2

try:
    import hal
    from hal import SimDevice, simulation
    from wpilib import RobotBase
    from wpimath.geometry import Rotation2d, Rotation3d, Quaternion
    from wpiutil import Sendable, SendableBuilder, SendableRegistry

    from phoenix6 import utils
    from phoenix6.base_status_signal import BaseStatusSignal
    from phoenix6.canbus import CANBus
    from phoenix6.phoenix_native import Native
    from phoenix6.sim.device_type import DeviceType
    from phoenix6.wpiutils.auto_feed_enable import AutoFeedEnable
    from phoenix6.wpiutils.replay_auto_enable import ReplayAutoEnable

    import copy
    import ctypes

    class Pigeon2(CorePigeon2, Sendable):
        """
        Constructs a new Pigeon 2 sensor object.

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

        __SIM_DEVICE_TYPE = DeviceType.P6_Pigeon2Type

        def __init__(self, device_id: int, canbus: str | CANBus = ""):
            CorePigeon2.__init__(self, device_id, canbus)
            Sendable.__init__(self)

            # The StatusSignal getters are copies so that calls
            # to the WPI interface do not update any references
            self.__yaw_getter = copy.deepcopy(self.get_yaw(False))
            self.__quat_w_getter = copy.deepcopy(self.get_quat_w(False))
            self.__quat_x_getter = copy.deepcopy(self.get_quat_x(False))
            self.__quat_y_getter = copy.deepcopy(self.get_quat_y(False))
            self.__quat_z_getter = copy.deepcopy(self.get_quat_z(False))

            SendableRegistry.addLW(self, "Pigeon 2 (v6) ", device_id)

            if RobotBase.isSimulation():
                # run in both swsim and hwsim
                AutoFeedEnable.get_instance().start()
            if utils.is_replay():
                ReplayAutoEnable.get_instance().start()

            self.__sim_pigeon = SimDevice("CANGyro:Pigeon 2 (v6)", device_id)

            self.__sim_periodic_before_callback: simulation.SimCB | None = None
            self.__sim_value_changed_callbacks: list[simulation.SimValueCB] = []

            if self.__sim_pigeon:
                # Simulated Pigeon2 LEDs change if it's enabled, so make sure we enable it
                self.__sim_periodic_before_callback = simulation.registerSimPeriodicBeforeCallback(self.__on_periodic)

                self.__sim_supply_voltage = self.__sim_pigeon.createDouble("supplyVoltage", SimDevice.Direction.kInput, 12.0)

                self.__sim_yaw = self.__sim_pigeon.createDouble("yaw", SimDevice.Direction.kOutput, 0)

                self.__sim_raw_yaw = self.__sim_pigeon.createDouble("rawYawInput", SimDevice.Direction.kInput, 0)
                self.__sim_pitch = self.__sim_pigeon.createDouble("pitch", SimDevice.Direction.kInput, 0)
                self.__sim_roll = self.__sim_pigeon.createDouble("roll", SimDevice.Direction.kInput, 0)
                self.__sim_angular_velocity_x = self.__sim_pigeon.createDouble("angularVelX", SimDevice.Direction.kInput, 0)
                self.__sim_angular_velocity_y = self.__sim_pigeon.createDouble("angularVelY", SimDevice.Direction.kInput, 0)
                self.__sim_angular_velocity_z = self.__sim_pigeon.createDouble("angularVelZ", SimDevice.Direction.kInput, 0)

                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_supply_voltage, self.__on_value_changed, True))
                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_raw_yaw, self.__on_value_changed, True))
                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_pitch, self.__on_value_changed, True))
                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_roll, self.__on_value_changed, True))

        def __enter__(self) -> 'Pigeon2':
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
                ctypes.c_char_p(bytes("Yaw", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_yaw.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("RawYaw", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_raw_yaw.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("Pitch", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_pitch.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("Roll", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_roll.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("AngularVelocityX", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_angular_velocity_x.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("AngularVelocityY", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_angular_velocity_y.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("AngularVelocityZ", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_angular_velocity_z.set(value.value)

        # ----- WPILib Gyro Interface -----
        # WPILib no longer has a Gyro interface, but these methods are standard in FRC.

        def reset(self):
            """
            Resets the Pigeon 2 to a heading of zero.

            This can be used if there is significant drift in the gyro,
            and it needs to be recalibrated after it has been running.
            """
            self.set_yaw(0)

        def getRotation2d(self) -> Rotation2d:
            """
            Returns the heading of the robot as a Rotation2d.

            The angle increases as the Pigeon 2 turns counterclockwise when
            looked at from the top. This follows the NWU axis convention.

            The angle is continuous; that is, it will continue from 360 to
            361 degrees. This allows for algorithms that wouldn't want to
            see a discontinuity in the gyro output as it sweeps past from
            360 to 0 on the second time around.

            :returns: The current heading of the robot as a Rotation2d
            :rtype: Rotation2d
            """
            return Rotation2d.fromDegrees(self.__yaw_getter.refresh().value)

        def getRotation3d(self) -> Rotation3d:
            """
            Returns the orientation of the robot as a Rotation3d
            created from the quaternion signals.

            :returns: The current orientation of the robot as a Rotation3d
            :rtype: Rotation3d
            """
            BaseStatusSignal.refresh_all(
                self.__quat_w_getter,
                self.__quat_x_getter,
                self.__quat_y_getter,
                self.__quat_z_getter
            )
            return Rotation3d(Quaternion(
                self.__quat_w_getter.value,
                self.__quat_x_getter.value,
                self.__quat_y_getter.value,
                self.__quat_z_getter.value
            ))

        # ----- Sendable -----
        def initSendable(self, builder: SendableBuilder):
            builder.setSmartDashboardType("Gyro")
            builder.addDoubleProperty("Value", self.__yaw_getter.as_supplier(), self.set_yaw)

except ImportError:
    class Pigeon2(CorePigeon2):
        # Stub class to remove the "Core" string of Pigeon2
        pass
