#objects.py

from abc import ABC, abstractmethod

from panda3d.core import Vec3, Point3, BitMask32, Quat, LMatrix4f
from math import pi, log, radians,sin,cos

class Objects(ABC):

    #universal scales
    dimension_scale = 1e-6
    distance_scale = 5
    time_scale = 1e5
    size_scale = 3
        
    G_constant = 6.67430e-11

    def __init__(self, base, name:str, mass:float,radius:float, tilt:float, angular_velocity:float, model_path:str):
        self.node = base.loader.loadModel(model_path)
        self.node.reparentTo(base.render)
        self.node.setScale(radius * self.dimension_scale * self.size_scale)
        self.node.setCollideMask(BitMask32.bit(1))

        self.node.setPythonTag("object", self)

        # Keep track of properties
        self.base = base
        self.name = name
        self.mass = mass
        self.radius = radius
        self.tilt = tilt
    
        self.angular_velocity = angular_velocity
        self.angle = 0

        self.model_fix_quat = Quat()
        self.model_fix_quat.set_from_axis_angle(90, Vec3(1, 0, 0))
        self.tilt_quat = Quat()
        self.tilt_quat.set_from_axis_angle(tilt, Vec3(0,1,0))
        self.rotation_quat = Quat()

        self.base.all_objects.append(self)
    def reset_acc(self):
        self.acc = Vec3(0,0,0)

    def gravity(self, other):
        direction = other.pos - self.pos

        r = direction.length()
        if r == 0:
            return
        direction.normalize()
        self.acc += direction * (self.G_constant * other.mass / (r * r))
    
    def update_physics(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        
        self.angle += self.angular_velocity * dt
        self.rotation_quat.set_from_axis_angle(self.angle, Vec3(0,0,1).normalized())
        final_quat = self.model_fix_quat * self.rotation_quat * self.tilt_quat
        self.node.setQuat(final_quat)

    def sync_node(self):
        if self.node.getPos().length() <= 60000:
            self.node.setPos(self.pos * self.dimension_scale / self.distance_scale)
        else: 
            self.node.setPos((self.pos * self.dimension_scale / self.distance_scale / 10) + self.pos.normalized() * 60000)


    @abstractmethod
    def create_ui(self): pass
    @abstractmethod
    def close_ui(self): pass

