"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

try:
    from wpilib import Notifier, DriverStation
    from threading import RLock
    from phoenix6.signal_logger import SignalLogger
    from phoenix6.unmanaged import feed_enable

    class AutoFeedEnable:
        __instance = None

        def __init__(self):
            self.__enable_notifier = Notifier(self.__run)
            self.__lock = RLock()
            self.__start_count = 0

        def __run(self):
            if DriverStation.isEnabled():
                feed_enable(0.100)

                if DriverStation.isAutonomous():
                    robot_mode = "Autonomous"
                elif DriverStation.isTest():
                    robot_mode = "Test"
                else:
                    robot_mode = "Teleop"
            else:
                robot_mode = "Disabled"
            SignalLogger.write_string("RobotMode", robot_mode)

        @classmethod
        def get_instance(clazz):
            if clazz.__instance is None:
                clazz.__instance = AutoFeedEnable()
            return clazz.__instance

        def start(self):
            """
            Starts feeding the enable signal to CTRE actuators.
            """
            with self.__lock:
                if self.__start_count == 0:
                    # start if we were previously at 0
                    self.__enable_notifier.startPeriodic(0.02)
                self.__start_count += 1

        def stop(self):
            """
            Stops feeding the enable signal to CTRE actuators. The
            enable signal will only be stopped when all actuators
            have requested to stop the enable signal.
            """
            with self.__lock:
                if self.__start_count > 0:
                    self.__start_count -= 1
                    if self.__start_count == 0:
                        self.__enable_notifier.stop()

except ImportError:
    pass
