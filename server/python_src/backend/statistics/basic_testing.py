import backend.scene_builder as scene_builder
import backend.rov as rov
import vectormath

scene = scene_builder.Scene()
main_rov = rov.ROV(scene.new_handle(), scene)

main_rov.reparent(scene.get_scene_root())

thruster_a = main_rov.create_thruster(0, 3, 0, 0, 0, 0, 2)
#thruster_b = main_rov.create_thruster(0, 0, 0, 0, 0, 0, 500)

thruster_a.set_throttle(100)

print("Torque force", thruster_a.current_torque_force())
print("What force required to achieve this?", thruster_a.auto_throttle_rotational_target_force(vectormath.Vector3(0, -3, 0)))

#print(thruster_a.auto_throttle_linear_target_force(vectormath.Vector3(0, 0, 0)))

scene.print_hierarchy()