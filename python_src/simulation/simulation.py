import numpy
import vectormath

type Handle = int

NONE_HANDLE: Handle = 0
TICK_INTERVAL: float = 0.1

class Scene:
    def __init__(self):
        self.entities: list = []
        self.current_tick: int = 0
        self.unique_handle: Handle = 1
    
    def new_handle(self):
        self.unique_handle += 1

        return self.unique_handle
    
    def get_entity(self, needle):
        for entity in self.entities:
            if entity.handle != handle:
                continue
            
            return entity

class Entity:
    def __init__(self, handle: Handle):
        self.handle: Handle = handle
        self.children: list[Handle] = [NONE_HANDLE]
        self.parent = NONE_HANDLE

class Transform:
    def __init__(self):
        self.position = vectormath.Vector3(0, 0, 0)
        #self.basis

class Point(Entity):
    def __init__(self, handle):
        super.__init__(handle)
        
        self.position = vectormath.Vector3(0, 0, 0)
        