# encoding:utf-8

import time
import MySQLdb
from mysql_config import SOURCE_CONFIG


class MySQL(object):
    """对MySQLdb常用函数进行封装的类"""
    
    error_code = ''  # MySQL错误号码

    _instance = None  # 本类的实例
    _conn = None  # 数据库conn
    _cur = None  # 游标

    _TIMEOUT = 30  # 默认超时30秒
    _timecount = 0
        
    def __init__(self, dbconfig=SOURCE_CONFIG):
        """构造器：根据数据库连接参数，创建MySQL连接"""
        try:
            self._conn = MySQLdb.connect(host=dbconfig['host'],
                                         port=dbconfig['port'], 
                                         user=dbconfig['user'],
                                         passwd=dbconfig['passwd'],
                                         db=dbconfig['db'],
                                         charset=dbconfig['charset'])
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error! ', e.args[0], e.args[1]
            print error_msg
            
            # 如果没有超过预设超时时间，则再次尝试连接，
            if self._timecount < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                return self.__init__(dbconfig)
            else:
                raise Exception(error_msg)
        
        self._cur = self._conn.cursor()
        self._instance = MySQLdb

    def query(self,sql):
        """执行 SELECT 语句"""
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result

    def update(self,sql):
        """执行 UPDATE 及 DELETE 语句"""
        try:
            self._cur.execute("SET NAMES utf8") 
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result

    def update_no_commit(self,sql):
        """执行 UPDATE 及 DELETE 语句"""
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
            # self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result

    def update_many(self,sql,args):
        """执行 UPDATE 及 DELETE 语句"""
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.executemany(sql, args)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result
        
    def insert(self,sql):
        """执行 INSERT 语句。如主键为自增长int，则返回新生成的ID"""
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return self._conn.insert_id()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print e
            return False

    def insert_no_commit(self,sql):
        """执行 INSERT 语句。如主键为自增长int，则返回新生成的ID"""
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            # self._conn.commit()
            return self._conn.insert_id()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print e
            return False

    def truncate(self, sql):
        """
        删除数据库表
        :param sql: 删除语句
        :return: 删除结果
        """
        try:
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            result = False
        return result

    def fetch_all_rows(self):
        """获取结果行
        :rtype:
        :return: 结果
        """
        return self._cur.fetchall()
 
    def get_row_count(self):
        """获取结果行数"""
        return self._cur.rowcount
                          
    def commit(self):
        """数据库commit操作"""
        self._conn.commit()
                        
    def rollback(self):
        """数据库回滚操作"""
        self._conn.rollback()
           
    def __del__(self): 
        """释放资源（系统GC自动调用）"""
        try:
            self._cur.close() 
            self._conn.close() 
        except:
            pass
        
    def close(self):
        """关闭数据库连接"""
        self.__del__()
