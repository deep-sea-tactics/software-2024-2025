# This file contains generic simulation stuff

import backend.utils as utils
import vectormath

NONE_HANDLE: int = 0
TICK_INTERVAL: float = 0.1

ROOT_ENTITY: int = 1

def get_entity_in_handle_list(entity_list, query_handle):
    for entity in entity_list:
        if entity.handle != query_handle:
            continue
            
        return entity

class Entity:
    """
    Generic entity class that has children, a parent, and handles.
    This has to be a component of any object in the scene
    """
    def __init__(self, handle: int, scene):
        self.handle: int = handle
        self.children: list[int] = []
        self.parent = NONE_HANDLE
        self.scene = scene

        list.append(self.scene.entities, self)
    
    def reparent(self, new_parent):
        """
        Reparent this entity to another entity.
        """
        if self.parent != NONE_HANDLE:
            list.remove(self.get_parent().children, self.handle)
            self.parent = NONE_HANDLE

        self.parent = new_parent.handle
        list.append(self.get_parent().children, self.handle)
    
    def get_child(self, query_handle):
        """
        Returns an entity, if it exists, from handle.
        """
        return get_entity_in_handle_list(self.children, query_handle)

    def get_parent(self):
        """
        Returns the parent entity of this entity.
        """

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

class Scene:
    """
    This is an instance of a simulation.

    To use the simulation, you have to create an object of this class
    """
    def __init__(self):
        self.entities: list[Entity] = []
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
        
        res = Entity(self.new_handle(), self)

        return res.handle
    
    def get_entity(self, query_handle) -> Entity:
        """
        Returns entity by handle
        """
        
        return get_entity_in_handle_list(self.entities, query_handle)

    
    def get_scene_root(self) -> Entity:
        """
        Returns the scene root entity
        """
        return self.get_entity(ROOT_ENTITY)
    
    def print_hierarchy(self):
        """
        Outputs every entity and child to console.
        """

        print("There are " + str(len(self.entities)) + " entities present in this scene.")

        for item in self.entities:
            print(str(type(item)) + ", handle: " + str(item.handle) + ", parent: " + str(item.parent))