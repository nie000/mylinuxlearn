from celery import  Celery
# 创建应用APP tasks当前文件名相当于当前文件被引入时的__name__
# borker 负责携程队列的中间人 负责协调消费者和生产者 利用redis中的列表类型Lpush, Rpush也能完成 此处使用mq
# backend 记录任务处理结果的数据库或者其他组件
# 如果要指定redis 端口账号密码的方式为密码 地址 端口号 选择数据库号 选择6
# 'redis://:密码@127.0.0.1:6379/6'
app = Celery('tasks', broker='amqp://guest@localhost//', backend='redis://localhost')

@app.task
def add(x, y):
# 一个异步实例，相当于生产者
   return x + y