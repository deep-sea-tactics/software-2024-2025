import backend.scene_builder as scene_builder
import backend.rov as rov
import vectormath

scene = scene_builder.Scene()
main_rov = rov.ROV(scene.new_handle(), scene)

main_rov.reparent(scene.scene_root())

thruster_a = main_rov.create_thruster(0, 0, 0, 0, 0, 0, 500)
thruster_b = main_rov.create_thruster(0, 0, 0, 0, 0, 0, 500)

thruster_a.set_throttle(100)

print(thruster_a.torque_force())

print(thruster_a.auto_throttle_linear_target_force(vectormath.Vector3(250, 0, 0)))

scene.print_hierarchy()