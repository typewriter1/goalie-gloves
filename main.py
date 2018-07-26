from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import random, sys



class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_confined)
        base.win.requestProperties(props)

        self.setupCollision()

        self.pitch = loader.loadModel("models/pitch.egg")
        self.pitch.find("**/GoalLineCollision").setTag("name", "goal")
        self.pitch.reparentTo(render)

        self.hands = loader.loadModel("models/hands.egg")
        self.hands.setTag("name", "hands")
        self.hands.reparentTo(render)
        self.hands.setPos(0, -26.2, 0.8)
        self.hands.setScale(0.5)
        self.hands.lookAt(base.camera)

        self.ball = Ball()

        self.accept("escape", sys.exit)
        self.accept("1", base.oobe)

        

        base.camera.setPos(0, -31, 1)
        base.disableMouse()

        base.taskMgr.add(self.handsMoveTask, "move hands")
        

        

        self.al = AmbientLight("al")
        self.al.setColor((0.6, 0.6, 0.6, 1))
        self.alnp = render.attachNewNode(self.al)
        render.setLight(self.alnp)

        self.dl = DirectionalLight("dl")
        self.dl.setShadowCaster(True, 4096, 4096)
        self.dlnp = render.attachNewNode(self.dl)
        self.dlnp.lookAt(0, 0.2, -1)
        render.setLight(self.dlnp)        
        base.setBackgroundColor(0.2, 0.3, 0.5)


        self.mx, self.my = 0, 0

        self.accept("ball-into-goal", self.handleGoal)
        self.accept("ball-into-hands", self.handleSave)

        

        self.elapsedFrames = 0
        self.saved = False
        self.score  = 0
        self.totalShots = 0.00000000000001

        

    def handsMoveTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            self.mx = base.mouseWatcherNode.getMouseX()
            self.my = base.mouseWatcherNode.getMouseY()

        posX = self.mx
        self.hands.setX(posX)

        posZ = self.my
        #if posZ > 0:
        self.hands.setZ(posZ)

        self.hands.setR(self.hands.getX() * 20)
        return task.cont

    def setupCollision(self):
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerEvent()
        base.pusher.addInPattern('%(name)ft-into-%(name)it')

        
    def handleSave(self, e):
        self.ball.saved = True
        self.ball.reverse()
        taskMgr.doMethodLater(0.3, self.ball.reset, 'Reset Ball')
        print("Saved!!")
        self.score += 1
        print(self.score / self.totalShots)
        self.totalShots += 1

    def handleGoal(self, e):
        taskMgr.doMethodLater(0.3, self.ball.reset, 'Reset Ball')
        print("Goal!!")
        self.score -= 1
        print(self.score / self.totalShots)
        self.totalShots += 1


class Ball(object):
    def __init__(self):
        self.ball = loader.loadModel("models/ball.egg")
        self.ball.reparentTo(render)
        self.reset()
        base.taskMgr.add(self.ballMoveTask, "move ball")
        self.setupCollision()
        
    def reset(self, task = None):
        self.ball.setPos(0, -20, 0.2)
        self.dx, self.dy, self.dz = random.uniform(-1.1, 1.1), -10, random.uniform(0.05, 1)

    
    def ballMoveTask(self, task):
        dt = globalClock.getDt()
        self.ball.setPos(self.ball, self.dx * dt, self.dy * dt, self.dz* dt)
        return task.cont

    
    def reverse(self, event = None):
        self.dx = -self.dx
        self.dy = -self.dy
        self.saved = True
        
    def setupCollision(self):
        cs = CollisionSphere(0, 0, 0, 0.1)
        cnodePath = self.ball.attachNewNode(CollisionNode('cnode'))
        cnodePath.setTag("name", "ball")
        cnodePath.show()
        cnodePath.node().addSolid(cs)
        base.cTrav.addCollider(cnodePath, base.pusher)
        #base.pusher.addCollider(cnodePath, self.ball)


        

g = Game()
g.run()
