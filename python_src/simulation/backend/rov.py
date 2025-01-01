# This contains functions specific to an ROV

import backend.scene_builder as scene_builder
import backend.utils as utils
import vectormath
import math

UNIT = 1

class THRUSTER_DIRECTION:
    """
    Constant unit vectors representing directions of thrust
    """

    UP = vectormath.Vector3(1, 0, 0)
    DOWN = vectormath.Vector3(-1, 0, 0)

class Thruster(scene_builder.Entity):
    """
    Thruster object, pairs nicely with `ROV`.

    Transform is in local space to the ROV
    """

    def __init__(self, handle, scene, transform: utils.Transform, max_force: float): #, thrust_direction: vectormath.Vector3):
        super().__init__(handle, scene)

        self.transform: utils.Transform = transform # in local space to parent ROV
        self.max_force: int = max_force #kgf
        self.current_throttle: float = 0.0 # Out of 1.0
        self.thrust_direction = THRUSTER_DIRECTION.UP

    def set_throttle(self, percent: float):
        """
        Set the throttle of this thruster using a percentage (out of 100)
        """

        self.current_throttle = percent / 100
    
    def thrust_vec(self):
        """
        Returns a unit vector representing the location of force in the scope of the thruster
        """
        rotated = self.transform.rotation.vec_to_local_quat(self.thrust_direction)

        return rotated

    def current_thrust(self):
        """
        Returns the current force applied from this thruster
        """

        return self.max_force * self.current_throttle

    def auto_throttle_for_linear_motion(self):
        pass

    def torque_force(self):
        """
        Returns a vector3 containing all components of the torque force produced by this thruster.

        In units of newton-meter

        https://en.wikipedia.org/wiki/Torque
        """

        rov_position = self.get_parent().transform.position
        r = self.transform.position


        rx = r[0]
        ry = r[1]
        rz = r[2]

        # Componentize the third dimensional vectors and then calculate the torque force for each axis

        rzy = vectormath.Vector2(rz, ry).length
        rxy = vectormath.Vector2(rx, ry).length
        rxz = vectormath.Vector2(rx, rz).length

        euler_eq: tuple[float] = self.transform.rotation.to_euler()

        F_dir = self.thrust_vec()
        F_magnitude = self.current_thrust()

        F = vectormath.Vector3.as_length(F_dir, F_magnitude)

        print("that would be", F.x, F.y, F.z)

        theta_zy = euler_eq[0] # Roll
        theta_xy = euler_eq[1] # Pitch
        theta_xz = euler_eq[2] # Yaw

        tx = rzy * F.x
        ty = rxy * F.y
        tz = rxz * F.z
        
        print(tx)
        print(ty)
        print(tz)

        torque = vectormath.Vector3(tx, ty, tz)

        return torque

class ROV(scene_builder.Entity):
    """
    The ROV class is the actual robot; it contains motors and whatnot.

    Doubles as a physics body without collisions.

    Center of Mass is the origin!
    """

    def __init__(self, handle, scene):
        super().__init__(handle, scene)

        self.thrusters: list[Thruster] = []
        self.transform = utils.Transform.zero()
        self.mass = 0 #kg
    
    def create_thruster(self, x: float, y: float, z: float, rx: float, ry: float, rz: float, max_force: float) -> Thruster:
        """
        Creates (and returns a reference to) a new thruster on this ROV.
        """

        rotation_quat = utils.Quaternion.from_euler(rx, ry, rz)

        new_thruster = Thruster(
            self.scene.new_handle(),

            self.scene,

            utils.Transform(
                x,
                y,
                z,
                rotation_quat.x,
                rotation_quat.y,
                rotation_quat.z,
                rotation_quat.w
            ),

            max_force
        )

        self.thrusters.append(new_thruster)
        new_thruster.reparent(self)

        return new_thruster
    
    def update(self):
        """
        Updates the transform and velocity of the ROV.
        """

        # Rotate and translate each thruster by the current transform and rotation
        for thruster in self.thrusters:
            thruster.transform.position = self.transform.rotation.vec_to_local_quat(thruster.transform.position)
            thruster.transform.rotation = self.transform.rotation