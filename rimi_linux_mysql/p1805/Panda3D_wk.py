
#引入一个showbase实例
from direct.showbase.ShowBase import ShowBase

#引入，Actor类，包含用于创建、操作的方法，以及在角色上播放动画
from direct.actor.Actor import Actor

#引入Sequence--用来管理幕（动画）
from direct.interval.IntervalGlobal import Sequence

#从Panda3D内核引入Point3，控制动画角色的位置，方向等动作；
from panda3d.core import Point3


#我们使主类继承自ShowBase。ShowBase类加载大多数其他Panda3D模块，并提供3D窗口出现。
class Panda_wk(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # 禁用鼠标
        self.disableMouse()

        # 用库自带的-loader加载器-下的-加载模型函数-来载入环境模型，参数是模型的路径；
        self.environ = self.loader.loadModel("models/environment")

        # -self.render-创建渲染场景图，用于渲染3d几何图形的主要场景图。
        # reparenttTo把环境模型放入场景,这个方法相当于指向一个路径，引入render，render的意思是底板；
        self.environ.reparentTo(self.render)
        # 对环境模型进行比例-scale-(x, z, y)
        self.environ.setScale(1, 1, 1)
        #对环境模型进行位置调整（x,z,y,三轴）
        self.environ.setPos(-20, 35, 0)

        # 添加镜头；
        self.Camera()

        # 载入熊猫角色,参数是-熊猫的模型-和-熊猫走路的动作模型-
        self.pandaActor = Actor("models/panda-model",
                                     {"walk": "models/panda-walk4"})
        # 熊猫走路动作的动画循环
        self.pandaActor.loop("walk")
        #设置熊猫模型的比例-scale-（x, z, y）；
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        # 把熊猫模型放入场景
        self.pandaActor.reparentTo(self.render)


        # 创建四幕，位移动作（动画），PosInterval管理位置参数，HprInterval管理方向参数；
        P1 = self.pandaActor.posInterval(3,                                #动作时间
                                        Point3(0, -5, 0),                 #参数指向值（x,z,y)
                                        startPos=Point3(0, 5, 0))         #初始位置
        P2 = self.pandaActor.posInterval(3,
                                        Point3(0, 5, 0),
                                        startPos=Point3(0, -5, 0))
        H1 = self.pandaActor.hprInterval(1,
                                        Point3(180, 0, 0),               #参数指向值（z,y,x)
                                        startHpr=Point3(0, 0, 0))          #初始值
        H2 = self.pandaActor.hprInterval(1,
                                        Point3(0, 0, 0),
                                        startHpr=Point3(180, 0, 0))
        # 创建情节并运行四幕位移动画
        self.pandaMove = Sequence(P1,
                                  H1,
                                  P2,
                                  H2,
                                  name="pandaMove")
        # 让位移动画循环起来
        self.pandaMove.loop()

        # 定义镜头
    def Camera(self):
        #镜头的位置(x,z,y)和方向（x,z,y）
        self.camera.setPos(0, -13, 0)
        self.camera.setHpr(0, 0, 0)
          
app = Panda_wk()
app.run()