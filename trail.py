#trail.py

from random import choice 
from objects import Objects 
from panda3d.core import Vec4 , ClockObject
from math import pi 
from direct.motiontrail.MotionTrail import MotionTrail

class Trail(): 
    def __init__(self, base, object:Objects): 
        self.base = base 
        self.object = object 

        

        if not hasattr(self, "self.trail"):
            self.trail = MotionTrail("trail", self.object.node) 
            self.trail.geom_node_path.reparent_to(self.base.render) 
            self.trail.register_motion_trail()
            self.trail.geom_node_path.setTransparency(True)
        
        self.trail.setGlobalEnable(True)
        
        self.trail.sampling_time = 0.4
        #make the trail update every n seconds. set high as a low value causes extreme lag
        
        if hasattr(object, "in_orbit") and object.in_orbit:
            # Length of self.trail 
            self.trail.time_window = 32 * (2 * pi * (object.orbital_radius**3 / (object.G_constant * object.base.star.mass))**0.5) * 3.17e-8 * 1e6 / object.time_scale 
            #Math is to ensure self.trail can complete a full loop no matter the planet. also accounts for time_scale.
            #doesn't even work
        else: 
            self.trail.time_window = 5e6 / object.time_scale 
        
        
        center = self.base.render.attach_new_node("center") 
        around = center.attach_new_node("around") 
        around.set_y(0.2)
        res = 4 # Amount of angles in "circle". Higher is smoother. 
        for i in range(res + 1): 
            center.set_p((360 / res) * i) 
            vertex_pos = around.get_pos(self.base.render) 
            self.trail.add_vertex(vertex_pos)

        center.remove_node()
        around.remove_node()

        for i in range(res + 1):
            self.trail.set_vertex_color(i, Vec4(1, 1, 1, 1),Vec4(1, 1, 1, 0.8))
        self.trail.update_vertices()

