"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.units import *

def lerp(startValue, endValue, t: second):
    return startValue + (endValue - startValue) * t

try:
    from wpimath.geometry import (
        Rotation2d as Rotation2d,
        Translation2d as Translation2d,
        Transform2d as Transform2d,
        Twist2d as Twist2d,
        Pose2d as Pose2d,
    )

except ImportError:
    import math
    from typing import overload

    class Rotation2d:
        @overload
        def __init__(self) -> None: ...

        @overload
        def __init__(self, value: radian) -> None: ...

        @overload
        def __init__(self, x: float, y: float) -> None: ...

        def __init__(self, arg1 = None, arg2 = None):
            if arg1 is None and arg2 is None:
                # Self()
                self._value: radian = 0.0
                self._cos = 1.0
                self._sin = 0.0
            elif isinstance(arg1, (radian, int)) and arg2 is None:
                # Self(value)
                value = radian(arg1)
                self._value: radian = value
                self._cos = math.cos(value)
                self._sin = math.sin(value)
            elif isinstance(arg1, (float, int)) and isinstance(arg2, (float, int)):
                # Self(x, y)
                x = float(arg1)
                y = float(arg2)
                magnitude = math.hypot(x, y)
                if (magnitude > 1e-6):
                    self._cos = x / magnitude
                    self._sin = y / magnitude
                else:
                    self._cos = 1.0
                    self._sin = 0.0
                self._value: radian = math.atan2(self._sin, self._cos)
            else:
                raise TypeError('Invalid arguments for Rotation2d.__init__')

        @staticmethod
        def fromDegrees(value: degree) -> 'Rotation2d':
            return Rotation2d(math.radians(value))

        @staticmethod
        def fromRotations(value: rotation) -> 'Rotation2d':
            return Rotation2d(2 * math.pi * value)

        def radians(self) -> radian:
            return self._value
        def degrees(self) -> degree:
            return math.degrees(self._value)
        def rotations(self) -> rotation:
            return self._value / (2 * math.pi)

        def cos(self) -> float:
            return self._cos
        def sin(self) -> float:
            return self._sin
        def tan(self) -> float:
            return self._sin / self._cos

        def rotateBy(self, other: 'Rotation2d') -> 'Rotation2d':
            return Rotation2d(
                self.cos() * other.cos() - self.sin() * other.sin(),
                self.cos() * other.sin() + self.sin() * other.cos()
            )

        def __neg__(self) -> 'Rotation2d':
            return Rotation2d(-self._value)
        def __add__(self, other: 'Rotation2d') -> 'Rotation2d':
            return self.rotateBy(other)
        def __sub__(self, other: 'Rotation2d') -> 'Rotation2d':
            return self + (-other)
        def __mul__(self, scalar: float) -> 'Rotation2d':
            return Rotation2d(self._value * scalar)
        def __truediv__(self, scalar: float) -> 'Rotation2d':
            return self * (1.0 / scalar)

        def __eq__(self, other: 'Rotation2d') -> bool:
            return math.hypot(self.cos() - other.cos(), self.sin() - other.sin()) < 1E-9

    class Translation2d:
        @overload
        def __init__(self) -> None: ...

        @overload
        def __init__(self, x: meter, y: meter) -> None: ...

        @overload
        def __init__(self, distance: meter, angle: Rotation2d) -> None: ...

        def __init__(self, arg1 = None, arg2 = None):
            if arg1 is None and arg2 is None:
                # Self()
                self._x: meter = 0.0
                self._y: meter = 0.0
            elif isinstance(arg1, (meter, int)) and isinstance(arg2, (meter, int)):
                # Self(x, y)
                self._x: meter = meter(arg1)
                self._y: meter = meter(arg2)
            elif isinstance(arg1, (meter, int)) and isinstance(arg2, Rotation2d):
                # Self(distance, angle)
                distance = meter(arg1)
                angle = arg2
                self._x: meter = distance * angle.sin()
                self._y: meter = distance * angle.cos()
            else:
                raise TypeError('Invalid arguments for Translation2d.__init__')

        @property
        def x(self) -> meter:
            return self._x
        @property
        def y(self) -> meter:
            return self._y

        def norm(self) -> meter:
            return math.hypot(self.x, self.y)
        def angle(self) -> Rotation2d:
            return Rotation2d(self.x, self.y)
        def distance(self, other: 'Translation2d') -> meter:
            return math.hypot(other.x - self.x, other.y - self.y)
        def rotateBy(self, angle: Rotation2d) -> 'Translation2d':
            return Translation2d(
                self.x * angle.cos() - self.y * angle.sin(),
                self.x * angle.sin() + self.y * angle.cos()
            )

        def __neg__(self) -> 'Translation2d':
            return Translation2d(-self.x, -self.y)
        def __add__(self, other: 'Translation2d') -> 'Translation2d':
            return Translation2d(self.x + other.x, self.y + other.y)
        def __sub__(self, other: 'Translation2d') -> 'Translation2d':
            return self + (-other)
        def __mul__(self, scalar: float) -> 'Translation2d':
            return Translation2d(scalar * self.x, scalar * self.y)
        def __truediv__(self, scalar: float) -> 'Translation2d':
            return self * (1.0 / scalar)

        def __eq__(self, other: 'Translation2d') -> bool:
            return (
                math.fabs(self.x - other.x) < 1E-9 and
                math.fabs(self.y - other.y) < 1E-9
            )

    class Transform2d:
        @overload
        def __init__(self) -> None: ...

        @overload
        def __init__(self, translation: Translation2d, rotation: Rotation2d) -> None: ...

        @overload
        def __init__(self, initial: 'Pose2d', final: 'Pose2d') -> None: ...

        def __init__(self, arg1 = None, arg2 = None):
            if arg1 is None and arg2 is None:
                # Self()
                self._translation = Translation2d()
                self._rotation = Rotation2d()
            elif isinstance(arg1, Translation2d) and isinstance(arg2, Rotation2d):
                # Self(translation, rotation)
                self._translation = arg1
                self._rotation = arg2
            elif isinstance(arg1, Pose2d) and isinstance(arg2, Pose2d):
                # Self(initial, final)
                initial: Pose2d = arg1
                final: Pose2d = arg2
                self._translation = (final.translation() - initial.translation()).rotateBy(-initial.rotation())
                self._rotation = final.rotation() - initial.rotation()
            else:
                raise TypeError('Invalid arguments for Transform2d.__init__')

        def translation(self) -> Translation2d:
            return self._translation
        def rotation(self) -> Rotation2d:
            return self._rotation

        @property
        def x(self) -> meter:
            return self._translation.x
        @property
        def y(self) -> meter:
            return self._translation.y

        def inverse(self) -> 'Transform2d':
            return Transform2d(-self._translation.rotateBy(-self._rotation), -self._rotation)

        def __add__(self, other: 'Transform2d') -> 'Transform2d':
            return Transform2d(Pose2d(), Pose2d().transformBy(self).transformBy(other))
        def __mul__(self, scalar: float) -> 'Transform2d':
            return Transform2d(self._translation * scalar, self._rotation * scalar)
        def __truediv__(self, scalar: float) -> 'Transform2d':
            return self * (1.0 / scalar)

        def __eq__(self, other: 'Transform2d') -> bool:
            return (
                self._translation == other._translation and
                self._rotation == other._rotation
            )

    class Twist2d:
        def __init__(self, dx: meter = 0, dy: meter = 0, dtheta: radian = 0):
            self.dx = dx
            self.dy = dy
            self.dtheta = dtheta

        def __mul__(self, scalar: float) -> 'Twist2d':
            return Twist2d(self.dx * scalar, self.dy * scalar, self.dtheta * scalar)

        def __eq__(self, other: 'Twist2d') -> bool:
            return (
                math.fabs(self.dx - other.dx) < 1E-9 and
                math.fabs(self.dy - other.dy) < 1E-9 and
                math.fabs(self.dtheta - other.dtheta) < 1E-9
            )

    class Pose2d:
        @overload
        def __init__(self) -> None: ...

        @overload
        def __init__(self, translation: Translation2d, rotation: Rotation2d) -> None: ...

        @overload
        def __init__(self, x: meter, y: meter, rotation: Rotation2d) -> None: ...

        def __init__(self, arg1 = None, arg2 = None, arg3 = None):
            if arg1 is None and arg2 is None and arg3 is None:
                # Self()
                self._translation = Translation2d()
                self._rotation = Rotation2d()
            elif isinstance(arg1, Translation2d) and isinstance(arg2, Rotation2d) and arg3 is None:
                # Self(translation, rotation)
                self._translation = arg1
                self._rotation = arg2
            elif isinstance(arg1, (meter, int)) and isinstance(arg2, (meter, int)) and isinstance(arg3, Rotation2d):
                # Self(x, y, rotation)
                self._translation = Translation2d(arg1, arg2)
                self._rotation = arg3
            else:
                raise TypeError('Invalid arguments for Pose2d.__init__')

        def translation(self) -> Translation2d:
            return self._translation
        def rotation(self) -> Rotation2d:
            return self._rotation

        @property
        def x(self) -> meter:
            return self._translation.x
        @property
        def y(self) -> meter:
            return self._translation.y

        def rotateBy(self, angle: Rotation2d) -> 'Pose2d':
            return Pose2d(self._translation.rotateBy(angle), self._rotation.rotateBy(angle))

        def transformBy(self, other: Transform2d) -> 'Pose2d':
            return Pose2d(
                self._translation + other.translation().rotateBy(self._rotation),
                other.rotation() + self._rotation
            )

        def relativeTo(self, other: 'Pose2d') -> 'Pose2d':
            transform = Transform2d(other, self)
            return Pose2d(transform.translation(), transform.rotation())

        def exp(self, twist: Twist2d) -> 'Pose2d':
            dx = twist.dx
            dy = twist.dy
            dtheta = twist.dtheta

            sinTheta = math.sin(dtheta)
            cosTheta = math.cos(dtheta)

            if math.fabs(dtheta) < 1E-9:
                s = 1.0 - 1.0 / 6.0 * dtheta * dtheta
                c = 0.5 * dtheta
            else:
                s = sinTheta / dtheta
                c = (1 - cosTheta) / dtheta

            transform = Transform2d(
                Translation2d(dx * s - dy * c, dx * c + dy * s),
                Rotation2d(cosTheta, sinTheta)
            )
            return self + transform

        def log(self, end: 'Pose2d') -> Twist2d:
            transform = end.relativeTo(self)
            dtheta = transform.rotation().radians()
            halfDtheta = dtheta / 2.0

            cosMinusOne = transform.rotation().cos() - 1

            if math.fabs(cosMinusOne) < 1E-9:
                halfThetaByTanOfHalfDtheta = 1.0 - 1.0 / 12.0 * dtheta * dtheta
            else:
                halfThetaByTanOfHalfDtheta = -(halfDtheta * transform.rotation().sin()) / cosMinusOne

            translationPart = (
                transform.translation().rotateBy(
                    Rotation2d(halfThetaByTanOfHalfDtheta, -halfDtheta)
                ) * math.hypot(halfThetaByTanOfHalfDtheta, halfDtheta)
            )
            return Twist2d(translationPart.x, translationPart.y, dtheta)

        def __add__(self, other: Transform2d) -> 'Pose2d':
            return self.transformBy(other)
        def __sub__(self, other: 'Pose2d') -> Transform2d:
            pose = self.relativeTo(other)
            return Transform2d(pose.translation(), pose.rotation())
        def __mul__(self, scalar: float) -> 'Pose2d':
            return Pose2d(self._translation * scalar, self._rotation * scalar)
        def __truediv__(self, scalar: float) -> 'Pose2d':
            return self * (1.0 / scalar)

        def __eq__(self, other: 'Pose2d') -> bool:
            return (
                self._translation == other._translation and
                self._rotation == other._rotation
            )
