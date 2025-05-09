# Binding the simulation component to DSS
import server.python_src.frontend.dss.deep_seashell as dss
import backend.scene_builder as scene_builder
import backend.rov as rov

class ROVSimulation:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.scene = scene_builder.Scene()
        self.rov = rov.ROV(self.scene.new_handle(), self.scene)
        self.rov.reparent(self.scene.get_scene_root())

simulations: list[ROVSimulation] = []

def _find_sim(id: str):
    global simulations

    for sim in simulations:
        if sim.session_id != id:
            continue
        
        return sim

def cmd_def_simulation(args: list[str]) -> int:
    global simulations
    
    MIN_ARGS = 1 
    if len(args < MIN_ARGS): return 1

    simulations.append(ROVSimulation(args[0]))

    return 0

def cmd_thruster(args: list[str]) -> int:
    MIN_ARGS = 9
    if len(args < MIN_ARGS): return 1

    simulation = _find_sim(args[0])

    return 0

NAMESPACE = "sim::"

def define_dss_commands():
    dss.Define.define(
        cmd_def_simulation,
        NAMESPACE + "simulation",
        """
        Creates an instance of the simulation.

        Arguments: <name>
        """
    )