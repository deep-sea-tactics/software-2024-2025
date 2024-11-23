# This contains functions specific to an ROV

import backend.scene_builder as scene_builder
import backend.utils as utils
import vectormath
import math

class Thruster(scene_builder.Entity):
    """
    Thruster object, pairs nicely with `ROV`.

    Transform is in local space to the ROV
    """

    def __init__(self, handle, scene, transform: utils.Transform, max_force: float): #, thrust_direction: vectormath.Vector3):
        super().__init__(handle, scene)

        self.transform: utils.Transform = transform
        self.max_force: int = max_force #kgf
        self.current_throttle: float = 0.0 # Out of 1.0
        self.thrust_direction = vectormath.vector.Vector3()

    def current_force(self):
        """
        Returns the current force applied from this thruster
        """

        return self.max_force * self.current_throttle

    def torque_force(self):
        """
        Returns a vector3 containing all components of the torque force for this thruster and its current throttle.

        https://en.wikipedia.org/wiki/Torque
        """

        global_thrust_direction = self.get_parent().transform.rotation.vec_to_local_quat(self.thrust_direction)

        # Wikipedia once again saves the day

        R = utils.vector3_sub( self.transform.position, self.get_parent().transform.position )
        r = R.as_length()
        F = self.current_force()

        # Provides a vector of the thrust relative to the ROV

        theta_xz = math.atan2(global_thrust_direction.x, global_thrust_direction.z)
        theta_yx = math.atan2(global_thrust_direction.x, global_thrust_direction.y)
        theta_yz = math.atan2(global_thrust_direction.z, global_thrust_direction.y)

        torque_yz = r * F * math.sin(theta_yz)
        torque_yx = r * F * math.sin(theta_yx)
        torque_xz = r * F * math.sin(theta_xz)

        res = vectormath.vector.Vector3(torque_yx, torque_yz, torque_xz) # order of these might be off

        return res
        
        

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
    
    def create_thruster(self, x, y, z, rx, ry, rz, max_force):
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
    
    def update():
        """
        Updates the transform and velocity of the ROV.
        """

        pass

        