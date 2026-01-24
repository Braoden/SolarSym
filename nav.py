# nav.py
from direct.gui.DirectGui import DirectFrame, DirectButton
from direct.showbase.ShowBaseGlobal import render2d
from panda3d.core import (
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
)
from math import cos, sin, radians
from panda3d.core import Point3


class Minimap:
    def __init__(self, base):
        self.base = base
        self.minimap_scale = 420000


        # Create minimap container frame (transparent, just for positioning)
        self.frame = DirectFrame(
            frameColor=(0.3, 0.3, 0.3, 0.5),
            frameSize=(-0.4, 0.4, -0.4, 0.4),  # Size of the minimap box
            pos=(1.4, 0, 0.55)  # Top right position
        )

        # Create black box outline using 4 border frames
        border_width = 0.005  # Thickness of the border
        size = 0.4  # Half-size of the minimap
        
        DirectFrame(
            parent=self.frame,
            frameColor=(0, 0, 0, 1.0),  # Black
            frameSize=(-size, size, size - border_width, size),
            pos=(0, 0, 0)
        )
        DirectFrame(
            parent=self.frame,
            frameColor=(0, 0, 0, 1.0),  # Black
            frameSize=(-size, size, -size, -size + border_width),
            pos=(0, 0, 0)
        )
        DirectFrame(
            parent=self.frame,
            frameColor=(0, 0, 0, 1.0),  # Black
            frameSize=(-size, -size + border_width, -size, size),
            pos=(0, 0, 0)
        )
        DirectFrame(
            parent=self.frame,
            frameColor=(0, 0, 0, 1.0),  # Black
            frameSize=(size - border_width, size, -size, size),
            pos=(0, 0, 0)
        )
        
        icon_radius = 0.01  # Size of planet icons
        spacing = 0.038  # Distance between each planet

        sun_button = DirectButton(
            parent=self.frame,
            frameSize=(-0.015, 0.015, -0.015, 0.015),
            frameColor=(0, 0, 0, 0),  # Transparent hit area
            pos=(0, 0, 0),
            relief=None,
            borderWidth=(0, 0),
            command=self.sun_clicked,
            pressEffect=0,
        )
        
        # Create filled circle for visuals
        sun_circle = self._create_filled_circle(
            radius=0.018,
            segments=40,
            color=(1.0, 0.8, 0.0, 1.0)
        )

        # Define planets with their colors and objects
        planets = [
            ("Mercury", (0.7, 0.7, 0.7, 1.0), lambda: self.base.mercury),  # Gray
            ("Venus", (0.9, 0.7, 0.4, 1.0), lambda: self.base.venus),  # Yellowish
            ("Earth", (0.2, 0.4, 0.8, 1.0), lambda: self.base.earth),  # Blue
            ("Mars", (0.8, 0.3, 0.2, 1.0), lambda: self.base.mars),  # Red
            ("Jupiter", (0.9, 0.7, 0.5, 1.0), lambda: self.base.jupiter),  # Orange-tan
            ("Saturn", (0.9, 0.8, 0.6, 1.0), lambda: self.base.saturn),  # Pale yellow
            ("Uranus", (0.5, 0.8, 0.9, 1.0), lambda: self.base.uranus),  # Cyan
            ("Neptune", (0.2, 0.3, 0.9, 1.0), lambda: self.base.neptune),  # Blue
        ]

        # Create buttons and circles for each celestial body
        self.planet_buttons = {}
        self.planet_circles = {}
        
        for i, (name, color, obj_getter) in enumerate(planets):
            # Calculate position (sun at center, planets to the right)
            x_pos = (i+2) * spacing
            
            # Create transparent button for clicking
            button = DirectButton(
                parent=self.frame,
                frameSize=(-icon_radius, icon_radius, -icon_radius, icon_radius),
                frameColor=(0, 0, 0, 0),  # Transparent hit area
                pos=(x_pos, 0, 0),
                relief=None,
                borderWidth=(0, 0),
                command=lambda obj=obj_getter: self._on_body_clicked(obj),
                pressEffect=0,
            )
            
            # Create filled circle for visuals
            circle = self._create_filled_circle(
                radius=icon_radius,
                segments=40,
                color=color,
            )
            circle.reparentTo(button)
            circle.setPos(0, 0, 0)

            if name == "Earth":
                circle = self._create_filled_circle(
                    radius=icon_radius - 0.003,
                    segments=40,
                    color=(0,0.4,0,1),
                )
                circle.reparentTo(button)
                circle.setPos(0, 0, 0)
            
            self.planet_buttons[name] = button
            self.planet_circles[name] = circle
    
    def sun_clicked(self):
        if self.base.object_selected == None:
            self.base.select_object(self.base.star)

    def _on_body_clicked(self, obj_getter):
        """Handle click on any celestial body in the minimap"""
        obj = obj_getter()
        if obj and self.base.object_selected == None:
            self.base.select_object(obj)

    def _create_filled_circle(self, radius: float, segments: int, color):
        """
        Create a filled circle NodePath in the DirectGUI coordinate space.
        The circle is created as a triangle fan in the X/Z plane (Y is depth).
        """
        fmt = GeomVertexFormat.getV3c4()
        vdata = GeomVertexData("circle", fmt, Geom.UHStatic)
        vwriter = GeomVertexWriter(vdata, "vertex")
        cwriter = GeomVertexWriter(vdata, "color")

        # Center vertex
        vwriter.addData3(0.0, 0.0, 0.0)
        cwriter.addData4f(*color)

        # Ring vertices (duplicate the first at the end to close the loop)
        import math

        for i in range(segments + 1):
            theta = (2.0 * math.pi * i) / segments
            x = radius * math.cos(theta)
            z = radius * math.sin(theta)
            vwriter.addData3(x, 0.0, z)
            cwriter.addData4f(*color)

        tris = GeomTriangles(Geom.UHStatic)
        for i in range(1, segments + 1):
            tris.addVertices(0, i, i + 1)
        tris.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(tris)
        node = GeomNode("circle_node")
        node.addGeom(geom)
        return self.frame.attachNewNode(node)


    def dynamic_minimap(self):
        for planet, button in self.planet_buttons.items():
            for object in self.base.all_objects:
                if planet == object.name:
                    button.setPos(object.node.getPos().x / self.minimap_scale, 0 , object.node.getPos().y / self.minimap_scale)