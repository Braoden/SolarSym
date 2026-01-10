from panda3d.core import CollisionTraverser, CollisionNode, CollisionRay
from panda3d.core import CollisionHandlerQueue, BitMask32

class Selector:
    def __init__(self, base):
        self.base = base

        # Collision system
        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()

        # The ray from camera to mouse
        self.ray = CollisionRay()
        self.ray_node = CollisionNode("mouseRay")
        self.ray_node.addSolid(self.ray)
        self.ray_node.setFromCollideMask(BitMask32.bit(1))
        self.ray_node.setIntoCollideMask(BitMask32.allOff())

        self.ray_np = base.camera.attachNewNode(self.ray_node)
        self.traverser.addCollider(self.ray_np, self.queue)

    def select(self):
        if not self.base.mouseWatcherNode.hasMouse():
            return None

        # Update ray
        mpos = self.base.mouseWatcherNode.getMouse()
        self.ray.setFromLens(self.base.camNode, mpos.getX(), mpos.getY())

        # Run collision
        self.traverser.traverse(self.base.render)

        if self.queue.getNumEntries() > 0:
            self.queue.sortEntries()
            entry = self.queue.getEntry(0)
            return entry.getIntoNodePath()

        return None
    

