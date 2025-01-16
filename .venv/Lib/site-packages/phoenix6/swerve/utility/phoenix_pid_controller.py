"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import math
from phoenix6.error_reporting import report_status_code
from phoenix6.status_code import StatusCode
from phoenix6.units import *

def input_modulus(input: float, minimum_input: float, maximum_input: float) -> float:
    """
    Returns modulus of input.

    :param input:         Input value to wrap.
    :type input:          float
    :param minimum_input: The minimum value expected from the input.
    :type minimum_input:  float
    :param maximum_input: The maximum value expected from the input.
    :type minimum_input:  float
    """
    modulus = maximum_input - minimum_input

    # Wrap input if it's above the maximum input
    num_max = int((input - minimum_input) / modulus)
    input -= num_max * modulus

    # Wrap input if it's below the minimum input
    num_min = int((input - maximum_input) / modulus)
    input -= num_min * modulus

    return input

class PhoenixPIDController:
    """
    Phoenix-centric PID controller taken from WPI's PIDController class.

    This class differs from the WPI implementation by using explicit timestamps for
    integral/derivative calculations. Ideally, these timestamps come from the StatusSignal.

    :param Kp:     The proportional coefficient. Must be >= 0.
    :type Kp:      float
    :param Ki:     The integral coefficient. Must be >= 0.
    :type Ki:      float
    :param Kd:     The derivative coefficient. Must be >= 0.
    :type Kd:      float
    """

    def __init__(self, Kp: float, Ki: float, Kd: float):
        # Factor for "proportional" control
        self._kp = Kp
        # Factor for "integral" control
        self._ki = Ki
        # Factor for "derivative" control
        self._kd = Kd

        # The error range where "integral" control applies
        self._i_zone = math.inf

        self._maximum_integral = 1.0
        self._minimum_integral = -1.0

        self._maximum_input = 0.0
        self._minimum_input = 0.0

        # Do the endpoints wrap around? eg. Absolute encoder
        self._continuous = False

        # The error at the time of the most recent call to Calculate()
        self._position_error = 0.0
        self._velocity_error = 0.0

        # The error at the time of the second-most-recent call to Calculate() (used
        # to compute velocity)
        self._prev_error = 0.0
        # The sum of the errors for use in the integral calc
        self._total_error = 0.0

        # The error that is considered at setpoint.
        self._position_tolerance = 0.05
        self._velocity_tolerance = math.inf

        self._setpoint = 0.0
        self._measurement = 0.0
        self._have_setpoint = False
        self._have_measurement = False

        self._last_applied_output = 0.0

        # The last timestamp acquired when performing a calculation
        self._last_timestamp: second = 0.0

    def setPID(self, Kp: float, Ki: float, Kd: float):
        """
        Sets the PID Controller gain parameters.
        
        Sets the proportional, integral, and differential coefficients.
        
        :param Kp: The proportional coefficient. Must be >= 0.
        :type Kp: float
        :param Ki: The integral coefficient. Must be >= 0.
        :type Ki: float
        :param Kd: The differential coefficient. Must be >= 0.
        :type Kd: float
        """
        self._kp = Kp
        self._ki = Ki
        self._kd = Kd

    def setP(self, Kp: float):
        """
        Sets the proportional coefficient of the PID controller gain.
        
        :param Kp: The proportional coefficient. Must be >= 0.
        :type Kp: float
        """
        self._kp = Kp

    def setI(self, Ki: float):
        """
        Sets the integral coefficient of the PID controller gain.
        
        :param Ki: The integral coefficient. Must be >= 0.
        :type Ki: float
        """
        self._ki = Ki

    def setD(self, Kd: float):
        """
        Sets the differential coefficient of the PID controller gain.
        
        :param Kd: The differential coefficient. Must be >= 0.
        :type Kd: float
        """
        self._kd = Kd

    def setIZone(self, iZone: float):
        """
        Sets the IZone range. When the absolute value of the position error is
        greater than IZone, the total accumulated error will reset to zero,
        disabling integral gain until the absolute value of the position error is
        less than IZone. This is used to prevent integral windup. Must be
        non-negative. Passing a value of zero will effectively disable integral
        gain. Passing a value of infinity disables IZone functionality.
        
        :param iZone: Maximum magnitude of error to allow integral control. Must be
                      >= 0.
        :type iZone: float
        """
        if iZone < 0:
            report_status_code(StatusCode.INVALID_PARAM_VALUE, "PhoenixPIDController.setIZone")
        self._i_zone = iZone

    def getP(self) -> float:
        """
        Gets the proportional coefficient.
        
        :returns: proportional coefficient
        :rtype: float
        """
        return self._kp

    def getI(self) -> float:
        """
        Gets the integral coefficient.
        
        :returns: integral coefficient
        :rtype: float
        """
        return self._ki

    def getD(self) -> float:
        """
        Gets the differential coefficient.
        
        :returns: differential coefficient
        :rtype: float
        """
        return self._kd

    def getIZone(self) -> float:
        """
        Get the IZone range.
        
        :returns: Maximum magnitude of error to allow integral control
        :rtype: float
        """
        return self._i_zone

    def getPositionTolerance(self) -> float:
        """
        Gets the position tolerance of this controller.
        
        :returns: The position tolerance of the controller
        :rtype: float
        """
        return self._position_tolerance

    def getVelocityTolerance(self) -> float:
        """
        Gets the velocity tolerance of this controller.
        
        :returns: The velocity tolerance of the controller
        :rtype: float
        """
        return self._velocity_tolerance

    def getSetpoint(self) -> float:
        """
        Returns the current setpoint of the PIDController.
        
        :returns: The current setpoint
        :rtype: float
        """
        return self._setpoint

    def atSetpoint(self) -> bool:
        """
        Returns true if the error is within the tolerance of the setpoint.
        
        This will return false until at least one input value has been computed.

        :returns: True if the error is within the tolerance of the setpoint
        :rtype: bool
        """
        return (
            self._have_measurement and
            self._have_setpoint and
            math.fabs(self._position_error) < self._position_tolerance and
            math.fabs(self._velocity_error) < self._velocity_tolerance
        )

    def enableContinuousInput(self, minimumInput: float, maximumInput: float):
        """
        Enables continuous input.
        
        Rather then using the max and min input range as constraints, it considers
        them to be the same point and automatically calculates the shortest route
        to the setpoint.
        
        :param minimumInput: The minimum value expected from the input.
        :type minimumInput: float
        :param maximumInput: The maximum value expected from the input.
        :type maximumInput: float
        """
        self._continuous = True
        self._minimum_input = minimumInput
        self._maximum_input = maximumInput

    def disableContinuousInput(self):
        """
        Disables continuous input.
        """
        self._continuous = False

    def isContinuousInputEnabled(self) -> bool:
        """
        Returns true if continuous input is enabled.

        :returns: True if continuous input is enabled
        :rtype: bool
        """
        return self._continuous

    def setIntegratorRange(self, minimumIntegral: float, maximumIntegral: float):
        """
        Sets the minimum and maximum values for the integrator.
        
        When the cap is reached, the integrator value is added to the controller
        output rather than the integrator value times the integral gain.
        
        :param minimumIntegral: The minimum value of the integrator.
        :type minimumIntegral: float
        :param maximumIntegral: The maximum value of the integrator.
        :type maximumIntegral: float
        """
        self._minimum_integral = minimumIntegral
        self._maximum_integral = maximumIntegral

    def setTolerance(self, positionTolerance: float, velocityTolerance: float = math.inf):
        """
        Sets the error which is considered tolerable for use with AtSetpoint().
        
        :param positionTolerance: Position error which is tolerable.
        :type positionTolerance: float
        :param velocityTolerance: Velocity error which is tolerable.
        :type velocityTolerance: float
        """
        self._position_tolerance = positionTolerance
        self._velocity_tolerance = velocityTolerance

    def getPositionError(self) -> float:
        """
        Returns the difference between the setpoint and the measurement.

        :returns: The position error
        :rtype: float
        """
        return self._position_error

    def getVelocityError(self) -> float:
        """
        Returns the velocity error.

        :returns: The velocity error
        :rtype: float
        """
        return self._velocity_error

    def calculate(self, measurement: float, setpoint: float, currentTimestamp: second) -> float:
        """
        Returns the next output of the PID controller.
        
        :param measurement: The current measurement of the process variable
        :type measurement: float
        :param setpoint: The new setpoint of the controller
        :type setpoint: float
        :param currentTimestamp: The current timestamp to use for calculating integral/derivative error
        :type currentTimestamp: second
        :returns: The next output
        :rtype: float
        """
        self._setpoint = setpoint
        self._have_setpoint = True
        self._measurement = measurement
        self._have_measurement = True
        self._prev_error = self._position_error

        this_period = currentTimestamp - self._last_timestamp
        self._last_timestamp = currentTimestamp

        if self._continuous:
            error_bound = (self._maximum_input - self._minimum_input) / 2.0
            self._position_error = input_modulus(self._setpoint - self._measurement, -error_bound, error_bound)
        else:
            self._position_error = self._setpoint - self._measurement

        self._velocity_error = (self._position_error - self._prev_error) / this_period

        # If the absolute value of the position error is greater than IZone, reset the total error
        if math.fabs(self._position_error) > self._i_zone:
            self._total_error = 0
        elif self._ki != 0.0:
            self._total_error = math.max(
                self._minimum_integral / self._ki,
                math.min(
                    self._total_error + self._position_error * this_period,
                    self._maximum_integral / self._ki
                )
            )

        self._last_applied_output = self._kp * self._position_error + self._ki * self._total_error + self._kd * self._velocity_error
        return self._last_applied_output

    def getLastAppliedOutput(self) -> float:
        """
        Returns the last applied output from this PID controller.

        :returns: The last applied output
        :rtype: float
        """
        return self._last_applied_output

    def reset(self):
        """
        Reset the previous error, the integral term, and disable the controller.
        """
        self._position_error = 0.0
        self._prev_error = 0.0
        self._total_error = 0.0
        self._velocity_error = 0.0
        self._have_measurement = False