"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.hardware.core.core_talon_fxs import CoreTalonFXS

try:
    import hal
    from hal import SimDevice, simulation
    from wpilib import RobotBase
    from wpimath import units
    from wpiutil import Sendable, SendableBuilder, SendableRegistry

    from phoenix6 import configs, controls, signals, utils
    from phoenix6.canbus import CANBus
    from phoenix6.hardware.parent_device import SupportsSendRequest
    from phoenix6.phoenix_native import Native
    from phoenix6.sim.device_type import DeviceType
    from phoenix6.status_code import StatusCode
    from phoenix6.wpiutils.auto_feed_enable import AutoFeedEnable
    from phoenix6.wpiutils.replay_auto_enable import ReplayAutoEnable
    from phoenix6.wpiutils.motor_safety_implem import MotorSafetyImplem

    import copy
    import ctypes
    from threading import RLock

    class TalonFXS(CoreTalonFXS, Sendable):
        """
        Constructs a new Talon FXS motor controller object.

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

        __SIM_DEVICE_TYPE = DeviceType.P6_TalonFXSType

        __DEFAULT_SAFETY_EXPIRATION: units.seconds = 0.1

        def __init__(self, device_id: int, canbus: str | CANBus = ""):
            CoreTalonFXS.__init__(self, device_id, canbus)
            Sendable.__init__(self)

            # The StatusSignal getters are copies so that calls
            # to the WPI interface do not update any references
            self.__duty_cycle = copy.deepcopy(self.get_duty_cycle(False))

            self.__setter_control = controls.DutyCycleOut(0)
            self.__neutral_control = controls.NeutralOut()
            self.__voltage_control = controls.VoltageOut(0)

            self.__configs = configs.MotorOutputConfigs()

            self.__motor_safety = None
            self.__mot_safe_expiration = self.__DEFAULT_SAFETY_EXPIRATION
            self.__motor_safety_lock = RLock()

            self.__description = "Talon FXS (v6) " + str(device_id)
            SendableRegistry.addLW(self, "Talon FXS (v6) ", device_id)

            if RobotBase.isSimulation():
                # run in both swsim and hwsim
                AutoFeedEnable.get_instance().start()
            if utils.is_replay():
                ReplayAutoEnable.get_instance().start()

            self.__sim_motor = SimDevice("CANMotor:Talon FXS (v6)", device_id)

            base = "Talon FXS (v6)[" + str(device_id) + "]/"
            self.__sim_rotor = SimDevice("CANEncoder:" + base + "Rotor Sensor")
            self.__sim_forward_limit = SimDevice("CANDIO:" + base + "Fwd Limit")
            self.__sim_reverse_limit = SimDevice("CANDIO:" + base + "Rev Limit")

            self.__sim_periodic_before_callback: simulation.SimCB | None = None
            self.__sim_value_changed_callbacks: list[simulation.SimValueCB] = []

            if self.__sim_motor:
                self.__sim_periodic_before_callback = simulation.registerSimPeriodicBeforeCallback(self.__on_periodic)

                self.__sim_supply_voltage = self.__sim_motor.createDouble("supplyVoltage", SimDevice.Direction.kInput, 12.0)

                self.__sim_duty_cycle = self.__sim_motor.createDouble("dutyCycle", SimDevice.Direction.kOutput, 0)
                self.__sim_motor_voltage = self.__sim_motor.createDouble("motorVoltage", SimDevice.Direction.kOutput, 0)
                self.__sim_torque_current = self.__sim_motor.createDouble("torqueCurrent", SimDevice.Direction.kOutput, 0)
                self.__sim_supply_current = self.__sim_motor.createDouble("supplyCurrent", SimDevice.Direction.kOutput, 0)

                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_supply_voltage, self.__on_value_changed, True))

            if self.__sim_rotor:
                self.__sim_rotor_pos = self.__sim_rotor.createDouble("position", SimDevice.Direction.kOutput, 0)

                self.__sim_rotor_raw_pos = self.__sim_rotor.createDouble("rawPositionInput", SimDevice.Direction.kInput, 0)
                self.__sim_rotor_vel = self.__sim_rotor.createDouble("velocity", SimDevice.Direction.kInput, 0)
                self.__sim_rotor_accel = self.__sim_rotor.createDouble("acceleration", SimDevice.Direction.kInput, 0)

                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_rotor_raw_pos, self.__on_value_changed, True))
                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_rotor_vel, self.__on_value_changed, True))
                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_rotor_accel, self.__on_value_changed, True))

            if self.__sim_forward_limit:
                self.__sim_forward_limit.createBoolean("init", SimDevice.Direction.kOutput, True)
                self.__sim_forward_limit.createBoolean("input", SimDevice.Direction.kOutput, True)

                self.__sim_forward_limit_value = self.__sim_forward_limit.createBoolean("value", SimDevice.Direction.kBidir, False)

                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_forward_limit_value, self.__on_value_changed, True))

            if self.__sim_reverse_limit:
                self.__sim_reverse_limit.createBoolean("init", SimDevice.Direction.kOutput, True)
                self.__sim_reverse_limit.createBoolean("input", SimDevice.Direction.kOutput, True)

                self.__sim_reverse_limit_value = self.__sim_reverse_limit.createBoolean("value", SimDevice.Direction.kBidir, False)

                self.__sim_value_changed_callbacks.append(simulation.registerSimValueChangedCallback(self.__sim_forward_limit_value, self.__on_value_changed, True))

        def __enter__(self) -> 'TalonFXS':
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
                ctypes.c_char_p(bytes("DutyCycle", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_duty_cycle.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("MotorVoltage", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_motor_voltage.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("TorqueCurrent", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_torque_current.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("SupplyCurrent", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_supply_current.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("RotorPosition", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_rotor_pos.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("RawRotorPosition", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_rotor_raw_pos.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("RotorVelocity", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_rotor_vel.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("RotorAcceleration", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_rotor_accel.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("ForwardLimit", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_forward_limit_value.set(value.value)

            err = Native.instance().c_ctre_phoenix6_platform_sim_get_physics_value(
                self.__SIM_DEVICE_TYPE.value,
                self.device_id,
                ctypes.c_char_p(bytes("ReverseLimit", 'utf-8')),
                ctypes.byref(value),
            )
            if err == 0:
                self.__sim_reverse_limit_value.set(value.value)

        # ----- Set/get routines for WPILIB interfaces -----
        def set(self, speed: float):
            """
            Common interface for setting the speed of a motor controller.
            
            :param speed: The speed to set. Value should be between -1.0 and 1.0.
            :type speed: float
            """
            self.feed()
            self.set_control(self.__setter_control.with_output(speed))

        def setVoltage(self, volts: units.volts):
            """
            Common interface for seting the direct voltage output of a motor controller.

            :param volts: The voltage to output.
            :type volts: units.volts
            """
            self.feed()
            self.set_control(self.__voltage_control.with_output(volts))

        def get(self) -> float:
            """
            Common interface for getting the current set speed of a motor controller.

            :returns: The current set speed. Value is between -1.0 and 1.0.
            :rtype: float
            """
            return self.__duty_cycle.refresh().value

        def _set_control_private(self, request: SupportsSendRequest):
            # intercept the control setter and feed motor-safety
            self.feed()
            return super()._set_control_private(request)

        # ----- Turn-motor-off routines -----
        def disable(self):
            """
            Common interface for disabling a motor controller.
            """
            self.set_control(self.__neutral_control)

        def stopMotor(self):
            """
            Common interface to stop motor movement until set is called again.
            """
            self.disable()

        # ----- Neutral mode routines -----
        def setNeutralMode(self, neutralMode: signals.NeutralModeValue, timeout_seconds: units.seconds = 0.100) -> StatusCode:
            """
            Sets the mode of operation when output is neutral or disabled.

            Since neutral mode is a config, this API is blocking. We recommend
            that users avoid calling this API periodically.

            :param neutralMode: The state of the motor controller bridge
                                when output is neutral or disabled
            :type neutralMode: signals.NeutralModeValue
            :param timeout_seconds: Maximum amount of time to wait when
                                    performing configuration
            :type timeout_seconds: units.seconds
            :returns: Status of refreshing and applying the neutral mode config
            :rtype: StatusCode
            """
            # First read the configs so they're up-to-date
            retval = self.configurator.refresh(self.__configs, timeout_seconds)
            if retval.is_ok():
                # Then set the neutral mode config to the appropriate value
                self.__configs.neutral_mode = neutralMode
                retval = self.configurator.apply(self.__configs, timeout_seconds)
            return retval

        # ----- Sendable -----
        def initSendable(self, builder: SendableBuilder):
            builder.setSmartDashboardType("Motor Controller")
            builder.setActuator(True)
            builder.setSafeState(self.stopMotor)
            builder.addDoubleProperty("Value", self.get, self.set)

        def getDescription(self) -> str:
            """
            :returns: Description of motor
            :rtype: str
            """
            return self.__description

        # ----- Motor Safety -----
        def __get_motor_safety(self) -> MotorSafetyImplem:
            """
            caller must lock appropriately
            """
            if self.__motor_safety is None:
                # newly created MS object
                self.__motor_safety = MotorSafetyImplem(self.stopMotor, self.getDescription())
                self.__motor_safety.setExpiration(self.__mot_safe_expiration)
            return self.__motor_safety

        def feed(self):
            with self.__motor_safety_lock:
                if self.__motor_safety is None:
                    # do nothing, MS features were never enabled
                    pass
                else:
                    self.__get_motor_safety().feed()

        def setExpiration(self, expirationTime: units.seconds):
            """
            Set the expiration time for the corresponding motor
            safety object.
            
            :param expirationTime: The timeout value in seconds.
            :type expirationTime: units.seconds
            """
            with self.__motor_safety_lock:
                # save the value for if/when we do create the MS object
                self.__mot_safe_expiration = expirationTime
                # apply it only if MS object exists
                if self.__motor_safety is None:
                    # do nothing, MS features were never enabled
                    pass
                else:
                    # this call will trigger creating a registered MS object
                    self.__get_motor_safety().setExpiration(self.__mot_safe_expiration)

        def getExpiration(self) -> units.seconds:
            """
            Retrieve the timeout value for the corresponding motor
            safety object.

            :returns: the timeout value in seconds.
            :rtype: units.seconds
            """
            with self.__motor_safety_lock:
                return self.__mot_safe_expiration

        def isAlive(self) -> bool:
            """
            Determine of the motor is still operating or has timed out.

            :returns:   a True value if the motor is still operating normally
                        and hasn't timed out
            :rtype: bool
            """
            with self.__motor_safety_lock:
                if self.__motor_safety is None:
                    # MC is alive - MS features were never enabled to neutral the MC
                    return True
                else:
                    return self.__get_motor_safety().isAlive()

        def setSafetyEnabled(self, enabled: bool):
            """
            Enable/disable motor safety for this device.

            Turn on and off the motor safety option for this object.

            :param enabled: True if motor safety is enforced for this object.
            :type enabled: bool
            """
            with self.__motor_safety_lock:
                if self.__motor_safety is None and not enabled:
                    # Caller wants to disable MS,
                    # but MS features were nevere enabled,
                    # so it doesn't need to be disabled.
                    pass
                else:
                    # MS will be created if it does not exist
                    self.__get_motor_safety().setSafetyEnabled(enabled)

        def isSafetyEnabled(self) -> bool:
            """
            Return the state of the motor safety enabled flag.

            Return if the motor safety is currently enabled for this device.

            :returns: True if motor safety is enforced for this device
            :rtype: bool
            """
            with self.__motor_safety_lock:
                if self.__motor_safety is None:
                    # MS features were never enabled.
                    return False
                else:
                    return self.__get_motor_safety().isSafetyEnabled()

except ImportError:
    class TalonFXS(CoreTalonFXS):
        # Stub class to remove the "Core" string of TalonFXS
        pass
