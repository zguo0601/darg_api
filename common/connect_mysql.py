import os
from common.common_func_read_yaml import readyaml
import pymysql


dbinfo = {
    "host":"120.79.243.237",
    "user":"root",
    "password":"OorwdAS6",
    "port":4306,
}




class DbConnect():

    def __init__(self,db_conf,database="spman_center"):
        #实例化
        self.db_conf = db_conf
        #打开数据库连接
        self.db = pymysql.connect(database=database,
                                  cursorclass = pymysql.cursors.DictCursor,
                                  **db_conf)
        #使用cursors方法获取操作游标
        self.cursors = self.db.cursor()
    #数据库查询方法
    def select(self, sql):
        # 执行sql语句
        self.cursors.execute(sql)
        #返回多个元组
        result = self.cursors.fetchall()
        return result
    #关闭数据库连接
    def close(self):
        self.db.close()

    #修改数据库方法
    def excute(self, sql):
        try:
            #执行sql语句
            self.cursors.execute(sql)
            #提交修改
            self.db.commit()
        except:
            #发生错误时回滚
            self.db.rollback()


# #从yaml读取数据库配置信息
# curpath = os.path.dirname(os.path.realpath(__file__))
# # yaml文件的路径
# yamlpath = os.path.join('data.yaml')
# dbinfo = readyaml(yamlpath)['dbinfo'][0]


def select_sql_spman_center(sel_sql):
    db =  DbConnect(dbinfo,database="spman_center")
    result = db.select(sel_sql)
    db.close()
    return result

def excute_sql_spman_center(del_sql):
    #连接数据库
    db =  DbConnect(dbinfo,database="spman_center")
    #插入sql语句
    result = db.excute(del_sql)
    db.close()
    return result

def select1_sql_inside_user_center(sel1_sql):
    db =  DbConnect(dbinfo,database="inside_user_center")
    result = db.select(sel1_sql)
    db.close()
    return result

def excute1_sql_inside_user_center(del1_sql):
    #连接数据库
    db =  DbConnect(dbinfo,database="inside_user_center")
    #插入sql语句
    result = db.excute(del1_sql)
    db.close()
    return result

def select_taskid_number(sel_sql):
    db = DbConnect(dbinfo, database="spman_center")
    result = db.select(sel_sql)
    db.close()
    return result




if __name__ == '__main__':
    #curpath = os.path.dirname(os.path.realpath(__file__))
    # yaml文件的路径
    # yamlpath = os.path.join('test_data.yaml')
    # task_data = readyaml(yamlpath)['dbinfo'][0]
    # task_data1 = readyaml(yamlpath)['task_sex_data']
    # print(task_data)
    # print(task_data1)
    sql1 = 'select * FROM spman_center.task where  merchant_name = "极限传媒" and status = 1 order by id desc limit 1;'
    # sql2 = 'select *  FROM spman_center.task where  title = "哈哈哈哈1";'
    r = select_taskid_number(sql1)
    id = r[0]["id"]
    print(r)
    print(id)
    # print(r2)










