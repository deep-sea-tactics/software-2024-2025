import backend.scene_builder as scene_builder
import backend.rov as rov

scene = scene_builder.Scene()
main_rov = rov.ROV(scene.new_handle(), scene)

main_rov.reparent(scene.scene_root())

main_rov.create_thruster(2, 0, 0, 0, 0, 0, 5)
main_rov.create_thruster(-2, 0, 0, 0, 0, 0, 5)

scene.print_hierarchy()