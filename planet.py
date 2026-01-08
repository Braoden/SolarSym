# planet.py
from objects import Objects
from star import Star
from trail import Trail

from panda3d.core import Vec3
from direct.showbase.MessengerGlobal import messenger
from math import pi, sin , cos, radians

from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton

class Planet(Objects):
    def __init__(self,name, base, mass:float, radius:float, position:Vec3, velocity:Vec3, in_orbit:bool, orbital_period:float, orbital_tilt:float, tilt:float, angular_velocity:float, model_path:str, star:Star):
        super().__init__(base,name,mass,radius,tilt,angular_velocity,model_path)
        
        self.star = star
        self.in_orbit = in_orbit
        self.orbital_tilt = orbital_tilt
        
        if in_orbit:
            self.orbital_period = orbital_period
            self.orbital_radius = ((self.G_constant * self.star.mass * (orbital_period*24*60*60)**2)/(4 * pi**2))**(1/3)
            self.orbital_velocity = ((self.G_constant * self.star.mass) / self.orbital_radius)**(1/2)
             
            #always spawns on right side.
            self.pos = Vec3(0,
                            (self.orbital_radius + self.star.radius) * cos(radians(self.orbital_tilt)),
                            (self.orbital_radius + self.star.radius) * sin(radians(self.orbital_tilt)))
            self.vel = Vec3(-self.orbital_velocity * cos(radians(self.orbital_tilt)),
                            0,self.orbital_velocity * sin(radians(self.orbital_tilt)))
            self.acc = None
        else:
            self.pos = position
            self.vel = velocity
            self.acc = None
        
        self.trail = Trail(self.base, self)

    def create_ui(self):
        self.ui = DirectFrame(
            frameColor=(0, 0, 0, 0.8),
            frameSize=(-0.5, 0.5, -0.3, 0.3),
            pos=(0.8, 0, 0)
        )

        DirectLabel(
            parent=self.ui,
            text=self.name,
            scale=0.07,
            pos=(0, 0, 0.2)
        )

        DirectButton(
            parent=self.ui,
            text="Close",
            scale=0.05,
            pos=(0, 0, -0.2),
            command=self.close_ui
        )

    def close_ui(self):
        self.ui.destroy()
        self.base.deselect_object(self)

