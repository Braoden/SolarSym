# star.py

import random

from objects import Objects

from panda3d.core import Vec3, Material
from direct.showbase.MessengerGlobal import messenger

from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton

class Star(Objects):
    def __init__(self, base, name:str, mass:float, radius:float, angular_velocity:float, model_path:str):
        super().__init__(base,name,mass,radius,0, angular_velocity, model_path)

        self.pos = Vec3(0,0,0)
        self.vel = Vec3(0,0,0)
        self.acc = None

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

        self.values_label = DirectLabel(
            parent=self.ui,
            text=f"Mass: {self.mass} kg\nRadius: {self.radius / 1000} km",
            scale=0.04,
            pos=(0, 0, 0.06),
            frameSize=(-7, 7, -4.5, 2), 
            textMayChange=True
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

