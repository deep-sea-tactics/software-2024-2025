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

    UP = vectormath.Vector3(0, 1, 0)
    DOWN = vectormath.Vector3(0, -1, 0)

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
    
    def glob_thrust_direction(self):
        rov_position = self.get_parent().transform.position
        point_on_thruster = utils.vector3_out_of_parent_point(self.thrust_direction, self.transform.position)

        return utils.vector3_out_of_parent_point(point_on_thruster, rov_position)

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
        r = utils.vector3_out_of_parent_point( self.transform.position, rov_position )

        F_magnitude = self.current_thrust()

        F = self.thrust_direction * vectormath.Vector3(F_magnitude, F_magnitude, F_magnitude)

        rx = r[0]
        ry = r[1]
        rz = r[2]

        # Componentize the third dimensional vectors and then calculate the torque force for each axis

        rxy = vectormath.Vector2(rx, ry).length
        rxz = vectormath.Vector2(rx, rz).length
        rzy = vectormath.Vector2(rz, ry).length

        Fxy = vectormath.Vector2(rx, ry).length
        Fxz = vectormath.Vector2(rx, rz).length
        Fzy = vectormath.Vector2(rz, ry).length

        theta_xy = math.atan2(ry, rx)
        theta_xz = math.atan2(rz, rx)
        theta_zy = math.atan2(ry, rz)

        txy = rxy * Fxy * math.sin(theta_xy)
        txz = rxz * Fxz * math.sin(theta_xz)
        tzy = rzy * Fzy * math.sin(theta_zy)

        torque = vectormath.Vector3(txy, txz, tzy)

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