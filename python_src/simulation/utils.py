# Script containing helpful functions and MATH!

import vectormath
import math

class Transform:
    """
    Combination between position and rotation
    """
    def __init__(self, x, y, z, rx, ry, rz, rw):
        self.position = vectormath.vector.Vector3(x, y, z)
        self.rotation = Quaternion(rx, ry, rz, rw)

class Quaternion: 
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    def zero():
        return Quaternion(
            0,
            0,
            0,
            0
        )

    def conjugate(self):
        """
        Returns the mathematical conjugation of the quaternion.
        """
        res = self.deepcopy()

        res.y *= -1
        res.z *= -1
        res.x *= -1

        return res

    def __mult__(self, rhs):
        """
        Thanks, Wikipedia!

        Operator overload which returns the hamilton product of a quaternion
        """

        res = Quaternion(
            ((self.x * rhs.x) - (self.y * rhs.y) - (self.z * rhs.z) - (self.w * rhs.w)),
            ((self.x * rhs.y) + (self.y * rhs.x) + (self.z * rhs.w) - (self.w * rhs.z)),
            ((self.x * rhs.z) - (self.y * rhs.w) + (self.z * rhs.x) + (self.w * rhs.y)),
            ((self.x * rhs.w) + (self.y * rhs.z) - (self.z * rhs.y) + (self.w * rhs.x))
        )

        return res
    
    def vec_to_local_quat(self):
        """
        Transforms a vector from the global plane to the local plane of the quaternion
        """
        pass

    def to_vec(self):
        """
        Convenience that returns the quaternion as a 3D vector
        """

        pass

    def from_euler(roll: float, pitch: float, yaw: float):
        """
        Create a quaternion from euler angles.
        """

        cos_roll: float = math.cos(roll * 0.5)
        sin_roll: float = math.sin(roll * 0.5)
        cos_pitch: float = math.cos(pitch * 0.5)
        sin_pitch: float = math.sin(pitch * 0.5)
        cos_yaw: float = math.cos(yaw * 0.5)
        sin_yaw: float = math.sin(yaw * 0.5)

        res = Quaternion(
            cos_roll * cos_pitch * cos_yaw + sin_roll * sin_pitch * sin_yaw,
            sin_roll * cos_pitch * cos_yaw - cos_roll * sin_pitch * sin_yaw,
            cos_roll * sin_pitch * cos_yaw + sin_roll * cos_pitch * sin_yaw,
            cos_roll * cos_pitch * sin_yaw - sin_roll * sin_pitch * cos_yaw
        )

        return res
