# This file contains generic simulation stuff

import utils
import vectormath

NONE_HANDLE: int = 0
TICK_INTERVAL: float = 0.1

ROOT_ENTITY: int = 1

def get_entity_in_handle_list(entity_list, query_handle):
    for entity in entity_list:
            if entity.handle != query_handle:
                continue
            
            return entity

class Scene:
    """
    This is an instance of a simulation.

    To use the simulation, you have to create an object of this class
    """
    def __init__(self):
        self.entities: list = []
        self.current_tick: int = 0
        self.unique_handle: int = NONE_HANDLE

        self.new_entity() # Root entity
    
    def new_handle(self):
        """
        Creates a unique handle to keep objects separate
        """
        self.unique_handle += 1

        return self.unique_handle
    
    def new_entity(self):
        """
        Creates a new entity and assigns it a handle
        """
        
        res = Entity(self.unique_handle(), self)

        return res
    
    def get_entity(self, query_handle):
        """
        Returns entity by handle
        """
        
        return get_entity_in_handle_list(self.entities, query_handle)

    
    def scene_root(self):
        return self.get_entity(ROOT_ENTITY)

class Entity:
    """
    Generic entity class that has children, a parent, and handles.
    This has to be a component of any object in the scene
    """
    def __init__(self, handle: int, scene: Scene):
        self.handle: int = handle
        self.children: list[int] = [NONE_HANDLE]
        self.parent = NONE_HANDLE
        self.scene = scene
    
    def reparent(self, new_parent):
        self.parent = new_parent
    
    def get_child(self, query_handle):
        return get_entity_in_handle_list(self.children, query_handle)

    def get_parent(self):
        if self.parent == NONE_HANDLE:
            return

        return self.scene.get_entity(self.parent)

class Point(Entity):
    """
    A point is an entity which contains a transform
    """
    def __init__(self, handle):
        super.__init__(handle)
        
        self.transform = utils.Transform()