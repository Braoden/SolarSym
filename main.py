#main.py

from direct.showbase.ShowBase import ShowBase
from camera import Camera_Control
from objects import Objects
from planet import Planet
from star import Star
from moon import Moon
from selector import Selector
from trail import Trail
from slider import Slider

from direct.showbase.MessengerGlobal import messenger
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton

from panda3d.core import Vec3, Point3, LineSegs, NodePath, ClockObject

"""

fix:


implement:
- make the sun seem more vibrant / animated
- asteroid belt
- saturn's ring
- speed of gravity (?)

- solar system minimap
- shaders and lighting
- slider for time_scale
- implement menu gui: 
  - adding objects with custom dimensions wherever
- other objects (asteroids, comets)

storyboard:
- models made of "pixels" that dispurse on collision


"""

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()

        #self.setBackgroundColor(0, 0, 0.1)
        
        skybox = self.loader.load_model("models/backdrop.glb")
        skybox.reparent_to(self.render)
        skybox.set_scale(-3000)
        skybox.set_light_off()
        skybox.set_shader_off()
        skybox.set_two_sided(True)
        skybox.set_compass()

        # Create camera controller
        self.camera_control = Camera_Control(self, Point3(35000,20000,7500))
        self.cam.node().get_lens().set_far(600000)

        #create
        self.all_objects = []

        self.solarSystem()

        #selector
        self.object_selected = None
        self.selector = Selector(self)

        #slider 
        self.slider = Slider()

        #create grid
        self.grid = self.create_grid(size=500000, spacing=1000, zoffset=-self.star.node.getBounds().getRadius())
        
        #acceptors
        self.accept("mouse1", self.on_mouse1)
        
        self.taskMgr.add(self.update, "update-physics")

    
    def update(self, task):
        for object in self.all_objects:
            object.reset_acc()

        for object in self.all_objects:
            for other in self.all_objects:
                if object is not other:
                    object.gravity(other)

        for object in self.all_objects:
            # Note: Due to integration being a riemann sum with n = dt, a larger time_scale will 
            # result in a less accurate calculation of acceleration, affecting the simulation's physics.
            # This change, depending on the frame rate should be fine at time_scale < 1e5 (unsure).
            if (object != self.star):
                dt = ClockObject.getGlobalClock().getDt() * object.time_scale
                object.update_physics(dt)
                object.sync_node()

        return task.cont

    def create_grid(self, size, spacing, zoffset):
        lines = LineSegs()
        lines.setThickness(2)
        lines.setColor(0.3, 0.3, 0.3, 0.5)

        for x in range(-size, size+1, spacing):
            lines.moveTo(x, -size, zoffset)
            lines.drawTo(x, size, zoffset)

        for y in range(-size, size+1, spacing):
            lines.moveTo(-size, y, zoffset)
            lines.drawTo(size, y, zoffset)

        np = NodePath(lines.create())
        np.setTransparency(True)
        np.reparentTo(self.render)

        return np

    def on_mouse1(self):
        if self.object_selected == None:
            self.node = self.selector.select()
            if not self.node: return
            self.tag_node = self.node.findNetPythonTag("object")
            if self.tag_node.isEmpty(): return
            object = self.tag_node.getPythonTag("object")
            if object is None: return
            
            self.select_object(object)

    def select_object(self,object): 
        self.object_selected = object
        object.create_ui()
        self.camera_control.distance = 15*object.node.getBounds().getRadius()
    def deselect_object(self, object):
        self.object_selected = None
        self.camera_control.target = self.camera_control.move_camera_backward(object.node.getBounds().getRadius())
        self.camera_control.distance = 10

    def solarSystem(self):
        self.star = Star( base=self, name="Sun", 
            mass=1.98847e30, radius = 6.9634e8, angular_velocity=1.7,
            model_path="models/sun8.glb")
        
        # --------------- PLANETS ----------------

        self.mercury = Planet( base=self, name="Mercury", 
            mass = 3.305e23, radius = 2.44e6,
            position=None, velocity=None,
            in_orbit=True, orbital_period=87.97, orbital_tilt=7, 
            tilt=0.03 ,angular_velocity=7.1e-5 ,
            model_path="models/mercury2.glb", star=self.star )

        self.venus = Planet( base=self, name="Venus", 
            mass = 4.87e24, radius = 6.0518e6,
            position=None, velocity=None,
            in_orbit=True, orbital_period=224.7, orbital_tilt=3.39, 
            tilt=177.4 ,angular_velocity=-1.7e-5 ,
            model_path="models/venus.glb", star=self.star )
        
        self.earth = Planet( base=self, name="Earth",
            mass = 5.9722e24, radius = 6.371e6,
            position=None, velocity=None,
            in_orbit=True, orbital_period=365, orbital_tilt=0, 
            tilt=23.44 ,angular_velocity=4.178e-3 ,
            model_path="models/earth2.glb", star=self.star )
        # orbital radius = 149,597,870,700 m , orbital velocity = 29785
        self.moon = Moon( base=self, name="Moon", 
            mass = 7.34767309e22, radius = 1.737e6, 
            orbital_period=27.32, orbital_tilt=5.145, 
            tilt=6.68 ,angular_velocity=1.525e-4 ,
            model_path="models/moon.glb", planet=self.earth )

        self.mars = Planet( base=self, name="Mars", 
            mass = 6.42e23, radius = 3.3895e6,
            position=None, velocity=None,
            in_orbit=True, orbital_period=696.98, orbital_tilt=1.85, 
            tilt=25.19 ,angular_velocity=4.071e-3 ,
            model_path="models/mars.glb", star=self.star )
        
        #asteroid belt

        self.jupiter = Planet( base=self, name="Jupiter", 
            mass = 1.898e27, radius = 6.911e7,
            position=None, velocity=None,
            in_orbit=True, orbital_period=4332.59, orbital_tilt=1.31, 
            tilt=3.13 ,angular_velocity=1.0123e-2 ,
            model_path="models/jupiter2.glb", star=self.star )
        
        self.saturn = Planet( base=self, name="Saturn", 
            mass = 5.68e26, radius = 5.8232e7,
            position=None, velocity=None,
            in_orbit=True, orbital_period=10759.22, orbital_tilt=2.49, 
            tilt=26.73 ,angular_velocity=9.446e-3 ,
            model_path="models/saturn8.glb", star=self.star )
        
        self.uranus = Planet( base=self, name="Uranus", 
            mass = 8.68e25, radius = 2.5362e7,
            position=None, velocity=None,
            in_orbit=True, orbital_period=30799.2,
            tilt=97.77 ,angular_velocity=-5.803e-3 , orbital_tilt=0.77, 
            model_path="models/uranus2.glb", star=self.star )
        
        self.neptune = Planet( base=self, name="Neptune", 
            mass = 1.02e26, radius = 2.4622e7,
            position=None, velocity=None,
            in_orbit=True, orbital_period=59800, orbital_tilt=1.77, 
            tilt=29.32 ,angular_velocity=6.214e-3 ,
            model_path="models/neptune.glb", star=self.star )

        

app = MyApp()
app.run()