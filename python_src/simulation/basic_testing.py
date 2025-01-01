import backend.scene_builder as scene_builder
import backend.rov as rov

scene = scene_builder.Scene()
main_rov = rov.ROV(scene.new_handle(), scene)

main_rov.reparent(scene.scene_root())

thruster_a = main_rov.create_thruster(2, 1, 0, 0, 0, 0, 500)
thruster_b = main_rov.create_thruster(-2, 0, 0, 0, 0, 0, 5)

thruster_a.set_throttle(50)

print(thruster_a.torque_force())

scene.print_hierarchy()