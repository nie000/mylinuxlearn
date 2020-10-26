import MySQLdb
from MySQLdb.cursors import DictCursor

class MysqlDB:
    def __init__(self,host='127.0.0.1',user='root',db='zk_db',password='root123'):
        self.host=host
        self.user=user
        self.db=db
        self.password=password
    def open(self):
        con=MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.db,port=3306,charset='utf8')
        return con
    def __enter__(self):
        self.con=self.open()
        self.cur=self.con.cursor(cursor=DictCursor)
        return self.cur
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_tb is not None:
                self.con.rollback()
                return False
            else:
                self.con.commit()
                return True
        finally:
            self.cur.close()
            self.con.close()
if __name__ == '__main__':
    with MysqlDB() as cur:
        cur.execute('select * from tbl_user limit 10')
        data=cur.fetchall()
        print(data)