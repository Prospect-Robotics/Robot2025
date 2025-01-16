"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

try:
    from typing import Callable
    from wpilib import MotorSafety

    class MotorSafetyImplem(MotorSafety):
        """
        Implem of MotorSafety interface from WPILib. This allows
        late/lazy construction of WPILib's motor safety object.

        :param stop_motor: Lambda to stop the motor
        :type stop_motor: Callable[[], None]
        :param description: Description of motor controller
        :type description: str
        """
        def __init__(self, stop_motor: Callable[[], None], description: str):
            self.__stop_motor = stop_motor
            self.__description = description

        def stopMotor(self):
            """
            Stops the controller
            """
            self.__stop_motor()

        def getDescription(self) -> str:
            """
            :returns: Description of motor controller
            :rtype: str
            """
            return self.__description

except ImportError:
    pass
