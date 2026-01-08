from panda3d.core import Vec3, ClockObject

class Camera_Control:
    def __init__(self, base, target: Vec3):
        self.base = base
        self.camera = base.camera

        # ----- CAMERA TARGET -----
        self.follow_smoothness = 10.0
        self.transition_progress = 0.0 
        self.transition_speed = 3.0  
        self.follow_offset = Vec3(0, 0, 0) 
        self.temp_target = Vec3(0, 0, 0) 
        self.target = target

        # ---- ORBIT STATE ----
        self.yaw = 30  
        self.pitch = 15   
        self.distance = 10

        # ---- SPEEDS ----
        self.rotate_speed = 0.1
        self.zoom_vel = 0.0
        self.zoom_accel_rate = 10000.0
        self.zoom_decel_rate = 10000.0
        self.max_zoom_speed = 20000.0
        self.vel = Vec3(0, 0, 0)
        self.accel_rate = 2000.0
        self.decel_rate = 2000.0
        self.max_speed = 4000.0

        # ---- INPUT FLAGS ----
        self.right_down = False
        self.key_q = False
        self.key_e = False
        self.key_w = False
        self.key_s = False
        self.key_a = False
        self.key_d = False

        base.disableMouse()

        # ---- INPUT BINDINGS ----
        base.accept("mouse3",     self.on_right_down)
        base.accept("mouse3-up",  self.on_right_up)

        base.accept("q",    self.set_key, ["q", True])
        base.accept("q-up", self.set_key, ["q", False])
        base.accept("e",    self.set_key, ["e", True])
        base.accept("e-up", self.set_key, ["e", False])
        base.accept("w",    self.set_key, ["w", True])
        base.accept("w-up", self.set_key, ["w", False])
        base.accept("s",    self.set_key, ["s", True])
        base.accept("s-up", self.set_key, ["s", False])
        base.accept("a",    self.set_key, ["a", True])
        base.accept("a-up", self.set_key, ["a", False])
        base.accept("d",    self.set_key, ["d", True])
        base.accept("d-up", self.set_key, ["d", False])

        # ---- TASK UPDATE ----
        base.taskMgr.add(self.update, "camera-update")

    def set_key(self, key, value): setattr(self, f"key_{key}", value)
    def on_right_down(self): self.right_down = True
    def on_right_up(self): self.right_down = False

    def update(self, task):
        dt = ClockObject.getGlobalClock().getDt()

        # ----- MOUSE ORBIT (yaw / pitch) -----
        if self.base.mouseWatcherNode.hasMouse():
            md = self.base.win.getPointer(0)
            x = md.getX()
            y = md.getY()

            if not hasattr(self, "lx"):
                self.lx, self.ly = x, y

            dx = x - self.lx
            dy = y - self.ly

            if self.right_down:
                self.yaw   -= dx * self.rotate_speed
                self.pitch += dy * self.rotate_speed
                self.pitch = max(-89, min(89, self.pitch))

            self.lx, self.ly = x, y

        # ----- ORBIT BASIS VECTORS -----
        forward = Vec3(
            -self.cosd(self.yaw) * self.cosd(self.pitch),
            -self.sind(self.yaw) * self.cosd(self.pitch),
            -self.sind(self.pitch)
        )
        forward.normalize()

        right = forward.cross(Vec3(0, 0, 1))
        right.normalize()
        up = Vec3(0, 0, 1)
        
        # ----- A D Q E PANNING -----
        if self.base.object_selected == None:
            accel = Vec3(0, 0, 0)
            if self.key_a: accel -= right * self.accel_rate
            if self.key_d: accel += right * self.accel_rate
            if self.key_q: accel += up    * self.accel_rate
            if self.key_e: accel -= up    * self.accel_rate

            self.vel += accel * dt

            if accel.length() == 0:
                self.vel -= self.vel * min(1.0, self.decel_rate * dt)

            if self.vel.length() > self.max_speed:
                self.vel.normalize()
                self.vel *= self.max_speed

            self.target += self.vel * dt

        # -------- TARGET ZOOM W S ----------
        zoom_accel = 0.0
        if self.key_w: zoom_accel -= self.zoom_accel_rate
        if self.key_s: zoom_accel += self.zoom_accel_rate

        self.zoom_vel += zoom_accel * dt

        if zoom_accel == 0:
            self.zoom_vel -= self.zoom_vel * min(1, self.zoom_decel_rate * dt)

        if abs(self.zoom_vel) > self.max_zoom_speed:
            self.zoom_vel = self.max_zoom_speed * (1 if self.zoom_vel > 0 else -1)

        offset = Vec3(
            self.cosd(self.yaw) * self.cosd(self.pitch),
            self.sind(self.yaw) * self.cosd(self.pitch),
            self.sind(self.pitch)
        )

        if self.base.object_selected == None:
            self.target += offset * (self.zoom_vel * dt)
        else:
            if self.distance >= (5 * self.base.object_selected.node.getBounds().getRadius()):
                self.distance += self.zoom_vel * dt
            elif self.zoom_vel > 0:
                self.distance += self.zoom_vel * dt                

        # ------ FOLLOW OBJECT -------
        if self.base.object_selected != None:
            object_pos = self.base.object_selected.node.getPos()
            
            if not hasattr(self, 'following_object') or self.following_object != self.base.object_selected:
                self.following_object = self.base.object_selected
                self.transition_start_pos = self.target 
                self.transition_progress = 0.0
            
            self.transition_progress = min(1.0, self.transition_progress + dt * self.transition_speed)
            
            target_pos = object_pos + self.follow_offset
            
            blend_factor = self.easeInOutCubic(self.transition_progress)
            blended_target = self.transition_start_pos * (1 - blend_factor) + target_pos * blend_factor
            
            error = blended_target - self.temp_target + self.base.object_selected.vel * 1e-3 * (self.base.object_selected.time_scale/ 5e4)
            self.temp_target += error * min(1.0, dt * self.follow_smoothness)
            
            self.target = self.temp_target
        else:
            # When not following, keep temp_target in sync with target
            self.temp_target = self.target
            self.transition_progress = 0.0
            
            if hasattr(self, 'following_object'):
                del self.following_object
            if hasattr(self, 'transition_start_pos'):
                del self.transition_start_pos

        # ----- FINAL CAMERA POSITION FROM ORBIT -----
        cam_x = self.target.x + self.distance * self.cosd(self.yaw) * self.cosd(self.pitch)
        cam_y = self.target.y + self.distance * self.sind(self.yaw) * self.cosd(self.pitch)
        cam_z = self.target.z + self.distance * self.sind(self.pitch)
        self.pos = Vec3(cam_x, cam_y, cam_z)
        
        if self.base.object_selected != None:
            self.pos += self.base.object_selected.vel * 1e-4
        
        self.camera.setPos(self.pos)
        self.camera.lookAt(self.target)
        
        return task.cont
        
    def move_camera_backward(self, distance):
        backward = Vec3(
            self.cosd(self.yaw) * self.cosd(self.pitch),
            self.sind(self.yaw) * self.cosd(self.pitch),
            self.sind(self.pitch)
        )
        backward.normalize()

        cam_pos = self.camera.getPos()
        new_pos = cam_pos + backward * distance
        return Vec3(new_pos)

    def easeInOutCubic(self, t):
        #Smooth easing function for transitions
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - ((-2 * t + 2) ** 3) / 2

    # ------------- trig helpers -------------------

    def sind(self, deg):
        import math
        return math.sin(math.radians(deg))

    def cosd(self, deg):
        import math
        return math.cos(math.radians(deg))

