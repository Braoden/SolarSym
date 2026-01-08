# moon.py
from objects import Objects
from planet import Planet
from trail import Trail

from panda3d.core import Vec3
from math import pi, sin, cos, radians
from direct.showbase.MessengerGlobal import messenger

from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton

class Moon(Objects):
    def __init__(self,name, base, mass:float, radius:float, orbital_period:float, orbital_tilt:float, tilt:float, angular_velocity:float,model_path:str, planet:Planet):
        super().__init__(base,name,mass,radius,tilt, angular_velocity,model_path)

        self.planet = planet
        self.orbital_tilt = orbital_tilt

        self.orbital_period = orbital_period
        self.orbital_radius = ((self.G_constant * self.planet.mass * (orbital_period*24*60*60)**2)/(4 * pi**2))**(1/3)
        self.orbital_velocity = ((self.G_constant * self.planet.mass) / self.orbital_radius)**(1/2)
        
        #spawns above (-x) the earth.
        self.pos = Vec3((-self.orbital_radius - self.planet.radius) * cos(radians(self.orbital_tilt)),
                        self.planet.pos.y,
                        (self.orbital_radius + self.planet.radius) * sin(radians(self.orbital_tilt)))
        self.vel = Vec3(self.planet.vel.x,
                        -self.orbital_velocity * cos(radians(self.orbital_tilt)),
                        self.orbital_velocity * sin(radians(self.orbital_tilt)))
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

