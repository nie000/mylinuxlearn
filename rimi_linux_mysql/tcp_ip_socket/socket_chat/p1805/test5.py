# 1. 早上的socket

# 2. 爬取index页面 通过 http://blog.jobbole.com/all-posts/  把1-500页都爬出来
    # 1. 递归方式爬取
    # 2. 生成者消费者模型爬
    # 3. 两个方式的不同

# 3. 通过2把详情页面的a标签爬出来,放到一个任务里面, 另外一个函数取a标签,并且爬取a标签的页面


#1+2+3.....+ 100

# 1. 表达式
# 2. 结束条件

def plus(n):
    # 递归的方式
    if n > 1:
        #plus(99) + 100
        return plus(n-1) + n
    if n == 1:
        return 1

# return 1 1 2 3 5
# 斐波拉契数
def fab(n):
    if n > 2:
        return fab(n-1) + fab(n-2)
    else:
        return 1


print(fab(8))
