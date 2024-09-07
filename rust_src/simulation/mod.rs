use vecmath;

//The simulation is a testing component. It's here to test:
// - Autonomy
// - Stabilization
//..and anything else that requires an ROV to work.

type Handle = usize;

const EMPTY_HANDLE: Handle = 0;

/// Base class for every part of the simulation.
pub struct Entity {
    handle: Handle,
    parent: Handle,
    children: Vec<Handle>,
}
impl Entity {
    fn new(handle: usize) -> Entity {
        Entity {
            handle: handle,
            parent: EMPTY_HANDLE,
            children: vec![],
        }
    }
}

pub struct Simulation {
    
}
impl Simulation {

}