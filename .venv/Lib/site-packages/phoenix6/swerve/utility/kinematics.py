"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

try:
    from wpimath.kinematics import (
        SwerveModuleState as SwerveModuleState,
        SwerveModulePosition as SwerveModulePosition,
        ChassisSpeeds as ChassisSpeeds
    )

except ImportError:
    import math
    from phoenix6.units import *
    from phoenix6.swerve.utility.geometry import *

    class SwerveModuleState:
        def __init__(self, speed: meters_per_second = 0, angle: Rotation2d = Rotation2d()):
            self.speed = speed
            self.angle = angle

        @staticmethod
        def optimize(desiredState: 'SwerveModuleState', currentAngle: Rotation2d) -> 'SwerveModuleState':
            delta = desiredState.angle - currentAngle
            if math.fabs(delta.degrees()) > 90:
                return SwerveModuleState(-desiredState.speed, desiredState.angle + Rotation2d.fromDegrees(180))
            else:
                return desiredState

        def __eq__(self, other: 'SwerveModuleState') -> bool:
            return (
                math.fabs(self.speed - other.speed) < 1E-9 and
                self.angle == other.angle
            )

    class SwerveModulePosition:
        def __init__(self, distance: meter = 0, angle: Rotation2d = Rotation2d()):
            self.distance = distance
            self.angle = angle

        def interpolate(self, endValue: 'SwerveModulePosition', t: second) -> 'SwerveModulePosition':
            return SwerveModulePosition(
                lerp(self.distance, endValue.distance, t),
                lerp(self.angle, endValue.angle, t)
            )

        def __eq__(self, other: 'SwerveModulePosition') -> bool:
            return (
                math.fabs(self.distance - other.distance) < 1E-9 and
                self.angle == other.angle
            )

    class ChassisSpeeds:
        def __init__(self, vx: meters_per_second = 0, vy: meters_per_second = 0, omega: radians_per_second = 0):
            self.vx = vx
            self.vy = vy
            self.omega = omega

        @staticmethod
        def discretize(continuousSpeeds: 'ChassisSpeeds', dt: second) -> 'ChassisSpeeds':
            desiredDeltaPose = Pose2d(continuousSpeeds.vx * dt, continuousSpeeds.vy * dt, continuousSpeeds.omega * dt)
            twist = Pose2d().log(desiredDeltaPose)
            return ChassisSpeeds(twist.dx / dt, twist.dy / dt, twist.dtheta / dt)

        @staticmethod
        def fromFieldRelativeSpeeds(fieldRelativeSpeeds: 'ChassisSpeeds', robotAngle: Rotation2d) -> 'ChassisSpeeds':
            rotated = Translation2d(fieldRelativeSpeeds.vx, fieldRelativeSpeeds.vy).rotateBy(-robotAngle)
            return ChassisSpeeds(rotated.x, rotated.y, fieldRelativeSpeeds.omega)

        @staticmethod
        def fromRobotRelativeSpeeds(robotRelativeSpeeds: 'ChassisSpeeds', robotAngle: Rotation2d) -> 'ChassisSpeeds':
            rotated = Translation2d(robotRelativeSpeeds.vx, robotRelativeSpeeds.vy).rotateBy(robotAngle)
            return ChassisSpeeds(rotated.x, rotated.y, robotRelativeSpeeds.omega)

        def __neg__(self) -> 'ChassisSpeeds':
            return ChassisSpeeds(-self.vx, -self.vy, -self.omega)
        def __add__(self, other: 'ChassisSpeeds') -> 'ChassisSpeeds':
            return ChassisSpeeds(self.vx + other.vx, self.vy + other.vy, self.omega + other.omega)
        def __sub__(self, other: 'ChassisSpeeds') -> 'ChassisSpeeds':
            return self + (-other)
        def __mul__(self, scalar: float) -> 'ChassisSpeeds':
            return ChassisSpeeds(scalar * self.vx, scalar * self.vy, scalar * self.omega)
        def __truediv__(self, scalar: float) -> 'ChassisSpeeds':
            return self * (1.0 / scalar)

        def __eq__(self, other: 'ChassisSpeeds') -> bool:
            return self.vx == other.vx and self.vy == other.vy and self.omega == other.omega
