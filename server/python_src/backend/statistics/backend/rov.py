# This contains functions specific to an ROV

import backend.scene_builder as scene_builder
import backend.utils as utils
import vectormath
import math
import numpy

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

    def __init__(self, handle, scene, transform: utils.Transform, max_force: float, name: str = "unnamed"): #, thrust_direction: vectormath.Vector3):
        super().__init__(handle, scene)

        self.name = name
        self.transform: utils.Transform = transform # in local space to parent ROV
        self.max_force: float = max_force #kgf
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

    def auto_throttle(self, target_force: vectormath.Vector3, effective_direction: vectormath.Vector3, force_scale: float = 1.0):
        """
        How much should this thruster fire in order to achieve the intended force vector?

        This function answers that question by returning a throttle value from 0.0 to 1.0
        """

        # For safety, because apparently `vectormath` doesn't like `as_length()`-ing zero vectors
        if target_force.length == 0:
            return

        #F_dir = self.thrust_vec() #self.thrust_vec()
        target_direction = target_force.as_length(1) # Why? vectormath.Vector3.normalize() modifies the vector, doesn't copy it. Wow.

        # Determines how parallel the target and thruster's direction are
        parallel_scalar_modifier = abs(utils.vector3_dot(effective_direction, target_direction))

        # Max force possibly produced in this direction.
        parallel_scalar = self.max_force * parallel_scalar_modifier * force_scale

        # Don't want the thrusters to overshoot tiny manuevers, clamp the values perfectly to the target force
        parallel_scalar = numpy.clip(parallel_scalar, 0, target_force.length)

        throttle = parallel_scalar / self.max_force
        throttle /= force_scale # `force_scale` is for cases where the force produced vs the max thrust of this thruster are different
        throttle = numpy.clip(throttle, 0.0, 1.0) # Throttle must be in range 0.0 to 1.0

        return throttle

    def linear_force(self):
        """
        Returns the summation of linear forces and the correct direction for the output of this thruster
        """

        F_dir = self.thrust_vec()
        F_magnitude = self.current_thrust()

        F = vectormath.Vector3.as_length(F_dir, F_magnitude)

        return F

    def auto_throttle_rotational_target_force(self, torque: vectormath.Vector3) -> float:
        """
        Whatever the `torque`, figure out the original linear force applied at the rotational axis.

        In the thruster's case, this value should (?) be a scalar quantity
        
        Recall: Torque = radius * force * sin(theta)
        """
        r: float = self.transform.position.length
        torque_direction: vectormath.Vector3 = self.torque(1)

        print(torque)
        roll = torque[0]
        pitch = torque[1]
        yaw = torque[2]

        roll_linear = roll/(r * math.sin(torque_direction[0]))
        pitch_linear = pitch/(r * math.sin(torque_direction[1]))
        yaw_linear = yaw/(r * math.sin(torque_direction[2]))

        print("Pitch: " + pitch_linear)

        linear_force = vectormath.Vector3(roll_linear, pitch_linear, yaw_linear)
        print(linear_force)
        #print("RADIUS: " + str(r))
        #print("DIRECTION: " + str(torque_direction))

        return self.auto_throttle(linear_force, torque_direction, r)
    
    def current_torque_force(self):
        """
        Returns the torque force currently produced by this thruster
        """

        return self.torque(self.current_thrust())

    def torque(self, input_force_scalar):
        """
        Returns torque force in the direction of this thruster

        In units of newton-meter

        https://en.wikipedia.org/wiki/Torque
        """

        r = self.transform.position

        F = self.linear_force()

        if F.length == 0:
            return
        
        F = F.as_unit()
        F = F.as_length(input_force_scalar)

        torque = utils.vector3_cross(r, F)

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
    
    def create_thruster(self, x: float, y: float, z: float, roll: float, pitch: float, yaw: float, max_force: float, name: str = "unnamed") -> Thruster:
        """
        Creates (and returns a reference to) a new thruster on this ROV.
        """

        rotation_quat = utils.Quaternion.from_euler(roll, pitch, yaw)

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

            max_force,

            name
        )

        self.thrusters.append(new_thruster)
        new_thruster.reparent(self)

        return new_thruster
    
    def get_thruster_by_name(self, name: str):
        for thruster in self.thrusters:
            if thruster.name != name: continue

            return thruster

    def update(self):
        """
        Updates the transform and velocity of the ROV.
        """

        # Rotate and translate each thruster by the current transform and rotation
        for thruster in self.thrusters:
            thruster.transform.position = self.transform.rotation.vec_to_local_quat(thruster.transform.position)
            thruster.transform.rotation = self.transform.rotation

