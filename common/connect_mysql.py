import pymysql


dbinfo = {
    "host":"120.79.243.237",
    "user":"root",
    "password":"OorwdAS6",
    "port":4306,
}

class DbConnect():
    def __init__(self,db_cof,database="spman_center"):
    #实例化
        self.db_conf = db_cof
        #打开数据库连接
        self.db = pymysql.connect(database=database,
                                  cursorclass = pymysql.cursors.DictCursor,
                                  **db_cof)
        #使用cursors方法获取操作游标
        self.cursors = self.db.cursor()

    def select(self, sql):
        # 执行sql语句
        self.cursors.execute(sql)
        #返回多个元组
        result = self.cursors.fetchall()
        return result

    def close(self):
        self.db.close()

    def excute(self, sql):
        try:
            #执行sql语句
            self.cursors.execute(sql)
            #提交修改
            self.db.commit()
        except:
            #发生错误时回滚
            self.db.rollback()


def select_sql(sel_sql):
    db =  DbConnect(dbinfo,database="spman_center")
    result = db.select(sel_sql)
    db.close()
    return result

def excute_sql(del_sql):
    #连接数据库
    db =  DbConnect(dbinfo,database="spman_center")
    #插入sql语句
    result = db.excute(del_sql)
    db.close()
    return result

def select1_sql(sel1_sql):
    db =  DbConnect(dbinfo,database="inside_user_center")
    result = db.select(sel1_sql)
    db.close()
    return result

def excute1_sql(del1_sql):
    #连接数据库
    db =  DbConnect(dbinfo,database="inside_user_center")
    #插入sql语句
    result = db.excute(del1_sql)
    db.close()
    return result


if __name__ == '__main__':
    # sel_sql = 'SELECT * FROM spman_center.merchant where short_name = "小可爱";'
    # sel1_sql = 'SELECT * FROM inside_user_center.user where user_name = "小可爱";'
    # del_sql = 'DELETE  FROM spman_center.merchant where short_name = "小可爱";'
    # del1_sql = 'DELETE from inside_user_center.user where user_name = "小可爱";'
    del_sql = 'DELETE  from spman_center.merchant_relation  WHERE uid = 2454 and puid = 2137;'

    # result = select_sql(sel_sql)
    # result1 = select1_sql(sel1_sql)
    excute_sql(del_sql)
    # excute1_sql(del1_sql)







