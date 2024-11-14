# This contains functions specific to an ROV

import scene_builder
import utils
import vectormath

class Thruster(scene_builder.Entity):
    """
    Thruster object, pairs nicely with the `ROV`.

    Transform is in local space to the ROV
    """

    def __init__(self, handle, transform: utils.Transform, max_force: float, thrust_direction: vectormath.Vector3):
        super.__init__(handle)

        self.transform: utils.Transform = transform
        self.max_force: int = max_force #kgf
        self.current_throttle: float = 0.0 # Out of 1.0
        self.thrust_direction = vectormath.vector.Vector3()

    def current_force(self):
        return self.max_force * self.current_throttle

class ROV(scene_builder.Entity):
    """
    The ROV class is the actual robot; it contains motors and whatnot.

    Doubles as a physics body without collisions.

    Center of Mass is the origin!
    """

    def __init__(self, handle):
        super.__init__(handle)

        self.thrusters: list[Thruster] = []
    
    def create_thruster(self, x, y, z, rx, ry, rz, max_force):
        rotation_quat = utils.Quaternion.from_euler(rx, ry, rz)

        new_thruster = Thruster(
            self.scene.unique_handle(),

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
    
    def update():
        """
        Updates the transform and velocity of the ROV.
        """

        pass

        