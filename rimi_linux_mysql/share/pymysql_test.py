import pymysql
conn = pymysql.connect(host="127.0.0.1",user="root",passwd=""
                                                           "",db="pymysql_test")
cursor = conn.cursor()

#游标
# sql = """CREATE TABLE pymysql_test (
# FIRST_NAME CHAR(20) NOT NULL,
# LAST_NAME CHAR(20),
# AGE INT,
# SEX CHAR(1),
# INCOME FLOAT )"""
#
# cursor.execute(sql)

# row_affected = cursor.execute("create table t1(id INT ,name VARCHAR(20))")

# row_affected=cursor.execute("INSERT INTO t1(id,name) values (1,'alvin'),(2,'xialv')")

# cursor.execute("update t1 set name = 'silv2' where id=2")


# 查询数据
row_affected = cursor.execute("select * from t1")
one = cursor.fetchone()

# many=cursor.fetchmany(2)
# all=cursor.fetchall()


# scroll
# cursor.scroll(-1,mode='relative') # 相对当前位置移动

# cursor.scroll(2,mode='absolute') # 相对绝对位置移动


# 更改获取数据结果的数据类型,默认是元组,可以改为字典等:conn.cursor(cursor=pymysql.cursors.DictCursor)


conn.commit()
cursor.close()
conn.close()