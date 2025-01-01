# Script containing helpful functions and MATH!

import vectormath
import math

def vector3_sub(lhs: vectormath.Vector3, rhs: vectormath.Vector3):
    return vectormath.vector.Vector3(
        lhs.x - rhs.x,
        lhs.y - rhs.y,
        lhs.z - rhs.z
    )

def vector3_out_of_parent_point(child: vectormath.Vector3, parent: vectormath.Vector3):
    """
    Returns `child` (e.g. a thruster) translated out of the parent point, `parent` (e.g. an ROV)
    """

    return child + parent

def vector3_cross(a: vectormath.Vector3, b: vectormath.Vector3):
    """
    https://engineeringstatics.org/cross-product-math.html
    """

    res = vectormath.Vector3(
        (a.x * b.z) - (a.z * b.x),
        (a.x * b.y) - (a.y * b.x),
        (a.y * b.z) - (a.z * b.y),
    )

    return res
    

class Transform:
    """
    Combination between position and rotation
    """
    def __init__(self, x: float, y: float, z: float, rx: float, ry: float, rz: float, rw: float):
        self.position = vectormath.vector.Vector3(x, y, z)
        self.rotation = Quaternion(rx, ry, rz, rw)
    
    def zero():
        return Transform(
            0,
            0,
            0,
            0,
            0,
            0,
            0
        )

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

        res = Quaternion.zero()

        res.x = self.x * -1
        res.y = self.y * -1
        res.z = self.z * -1
        res.w = self.w

        return res

    def __mul__(self, rhs):
        """
        https://en.wikipedia.org/wiki/Quaternion

        Operator overload which returns the hamilton product of a quaternion
        """

        a1 = self.w
        a2 = rhs.w

        b1 = self.x
        b2 = rhs.x

        c1 = self.y
        c2 = rhs.y

        d1 = self.z
        d2 = rhs.z

        res = Quaternion(
            ((a1 * b2) + (b1 * a2) + (c1 * d2) - (d1 * c2)),
            ((a1 * c2) - (b1 * d2) + (c1 * a2) + (d1 * b2)),
            ((a1 * d2) + (b1 * c2) - (c1 * b2) + (d1 * a2)),
            ((a1 * a2) - (b1 * b2) - (c1 * c2) - (d1 * d2))
        )

        return res
    
    def vec_to_local_quat(self, input_vector: vectormath.Vector3) -> vectormath.Vector3:
        """
        Transforms a vector from the global plane to the local plane of the quaternion
        """
        v = Quaternion.from_vec(input_vector)

        print(v.x, v.y, v.z, v.w)
        print(self.x, self.y, self.z, self.w)
        print(self.conjugate().x, self.conjugate().y, self.conjugate().z, self.conjugate().w)

        res = (self * v) * self.conjugate()

        print("vec_to_local_quat result", res.x, res.y, res.z, res.w)

        return res.to_vec()

    def to_vec(self):
        """
        Convenience that returns the quaternion as a 3D vector
        """

        return vectormath.Vector3( self.x, self.y, self.z )

    def from_vec(vector: vectormath.Vector3):
        """
        Vector to quaternion.
        """

        return Quaternion(
            vector.x,
            vector.y,
            vector.z,
            0
        )

    def from_euler(roll: float, pitch: float, yaw: float):
        """
        Create a quaternion from euler angles. Takes numbers in degrees.

        https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
        """

        roll = math.radians(roll)
        yaw = math.radians(yaw)
        pitch = math.radians(pitch)

        cos_roll: float = math.cos(roll * 0.5)
        sin_roll: float = math.sin(roll * 0.5)
        cos_yaw: float = math.cos(yaw * 0.5)
        sin_yaw: float = math.sin(yaw * 0.5)
        cos_pitch: float = math.cos(pitch * 0.5)
        sin_pitch: float = math.sin(pitch * 0.5)

        res = Quaternion(
            sin_roll * cos_yaw * cos_pitch - cos_roll * sin_yaw * sin_pitch,
            cos_roll * sin_yaw * cos_pitch + sin_roll * cos_yaw * sin_pitch,
            cos_roll * cos_yaw * sin_pitch - sin_roll * sin_yaw * cos_pitch,
            cos_roll * cos_yaw * cos_pitch + sin_roll * sin_yaw * sin_pitch
        )

        print("euler to quat:", res.x, res.y, res.z, res.w)

        return res
    
    def to_euler(self) -> tuple[float]:
        roll = math.atan2(
            2 * ((self.w * self.x) + (self.y * self.z)),
            1 - 2 * ((self.x**2) + (self.y**2))
        )

        pitch = math.atan2(
            2 * ((self.w * self.z) + (self.x * self.y)),
            1 - 2 * ((self.y**2) + (self.z**2))
        )

        diff_qwqy_qxqz = ((self.w * self.y) - (self.x * self.z))

        yaw = (-math.pi / 2) + 2 * math.atan2(
            math.sqrt(1 + (2 * diff_qwqy_qxqz)),
            math.sqrt(1 - (2 * diff_qwqy_qxqz))
        )

        res = (math.degrees(roll), math.degrees(pitch), math.degrees(yaw))

        return res
