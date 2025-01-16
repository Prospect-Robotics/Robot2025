"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

try:
    from wpilib import Notifier
    from wpilib.simulation import DriverStationSim
    from threading import RLock
    from phoenix6 import HootReplay

    class ReplayAutoEnable:
        __instance = None

        def __init__(self):
            self.__enable_notifier = Notifier(self.__run)
            self.__lock = RLock()
            self.__start_count = 0

        def __run(self):
            if HootReplay.is_playing():
                enable_sig = HootReplay.get_boolean("RobotEnable")
                if enable_sig.status.is_ok():
                    DriverStationSim.setEnabled(enable_sig.value)

                robot_mode_sig = HootReplay.get_string("RobotMode")
                if robot_mode_sig.status.is_ok():
                    if robot_mode_sig.value == "Autonomous":
                        DriverStationSim.setAutonomous(True)
                        DriverStationSim.setTest(False)
                    elif robot_mode_sig.value == "Test":
                        DriverStationSim.setAutonomous(False)
                        DriverStationSim.setTest(True)
                    else:
                        DriverStationSim.setAutonomous(False)
                        DriverStationSim.setTest(False)

                DriverStationSim.notifyNewData()

        @classmethod
        def get_instance(clazz):
            if clazz.__instance is None:
                clazz.__instance = ReplayAutoEnable()
            return clazz.__instance

        def start(self):
            """
            Starts automatically enabling the robot in replay.
            """
            with self.__lock:
                if self.__start_count == 0:
                    # start if we were previously at 0
                    self.__enable_notifier.startPeriodic(0.02)
                self.__start_count += 1

        def stop(self):
            """
            Stops automatically enabling the robot in replay. The
            replay enable will only be stopped when all actuators
            have requested to stop the replay enable.
            """
            with self.__lock:
                if self.__start_count > 0:
                    self.__start_count -= 1
                    if self.__start_count == 0:
                        self.__enable_notifier.stop()

except ImportError:
    pass
