import vectormath

class Quaternion:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.vector3 = vectormath.Vector3(x, y, z)
        self.w = w