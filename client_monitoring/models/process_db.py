# encoding:utf-8

"""
功能：获取首页展示所需数据
作者：程亚楠
更新时间：2016.1.12
优化代码
"""
from base_db import BaseDb
import torndb


class ProcessDb (BaseDb):
    def __init__(self):
        BaseDb.__init__ (self)  # 执行父类

    def fetch_user_process(self,user_id):
        """获取指定用户关注的进程最新状态信息,首页数据"""
        sql = """
        
                SELECT a.process_id,pid, process_name, host_ip, mem, cpu, vsz, rss, process_info.create_time, a.create_time as detect_time, a.`status`,a.log_size
             FROM  process_status AS a,
                (
                    SELECT
                        process_id,
                        MAX(create_time) AS `date`
                    FROM
                        process_status
                    GROUP BY
                        process_id
                ) AS b,
              process_info,
              host_info
            WHERE
                a.process_id = b.process_id
            AND a.create_time = b.date
            AND process_info.process_id = a.process_id
            AND host_info.host_id = process_info.host_id
            AND process_info.user_id = '%s'
            AND process_info.save = '1'
        
        """
        result = self.db.query(sql % user_id)

        return result

    def fetch_process(self,user_id,process_id):
        """获取进程所有信息"""
        sql = """
        SELECT
            process_status.process_id,
            `status`,
            error_info,
            process_name,
            log_route,
            code_route,
            log_name,
            cmd,
            shell,
            process_info.create_time,
            process_status.create_time AS detect_time,
            host_ip,
            pid,
            cpu,
            mem,
            process_info.comment,
            vsz,
            rss,
            log_size,
            interval_time
        FROM
            `process_status`,
            process_info,
            host_info
        WHERE
            process_info.user_id = '%s'
        AND process_status.process_id = '%s'
        AND process_status.process_id = process_info.process_id
        AND host_info.host_id = process_info.host_id
        ORDER BY detect_time DESC 
        """
        result =self.db.query(sql % (user_id,process_id))
        return result

    def save_process_status(self, process_id,cpu, mem, vsz, rss, log_size, status, error_info):
        """插入主机信息"""
        sql = 'INSERT INTO process_status (process_id, cpu, mem, vsz, rss, log_size, status, error_info) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s")'
        try:
            self.db.insert(sql % (process_id, cpu, mem, vsz, rss, log_size, status, error_info))  # process_info 元组
            # self.db.close()
            return "执行成功"
        except:  # 已存在该结果
            # self.db.close()
            return "执行失败"

    def no_focus_process(self, process_id):
        """取消关注进程"""
        import random
        save = random.randrange(2, 100000000000000)   # 随机数，很重要
        sql = 'update process_info set save = "%s" WHERE process_id = "%s"'
        try:
            self.db.execute(sql % (save, process_id))
            return "执行成功"
        except:  # 已存在该结果
            return "执行失败"


    def update_process(self, process_id,log_route,code_route,log_name,code_name,shell,cmd,interval_time,comment):
        """取消关注进程"""
        sql = 'update process_info set log_route = "%s",code_route="%s",log_name="%s",process_name = "%s",shell = "%s",cmd="%s",interval_time="%s",comment="%s" WHERE process_id = "%s"'
        try:
            self.db.execute(sql % (log_route,code_route,log_name,code_name,shell,cmd,interval_time,comment,process_id))
            return "执行成功"
        except:  # 已存在该结果
            return "执行失败"

    def save_process_info(self, process_info):
        """插入修改后的进程信息"""
        sql = 'INSERT INTO process_info (process_id, user_id,host_id,process_name,pid,create_time,log_route,code_route,interval_time,save,comment,cmd,shell,log_name) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
        try:
            self.db.insert(sql % process_info )  # process_info 元组
            # self.db.close()
            return "保存成功"
        except torndb.IntegrityError:  # 已存在该结果
            # self.db.close()
            return "保存失败，数据库已有该进程信息"

    def save_execute_process_info(self, process_info):
        """修改重新执行的进程信息"""
        sql = 'update process_info set pid= "%s",log_route = "%s",code_route="%s",log_name="%s",process_name="%s",shell="%s",cmd="%s",interval_time="%s",comment="%s" WHERE process_id = "%s"'
        try:
            self.db.execute(sql % process_info)  # process_info 元组
            # self.db.close()
            return "更新成功"
        except torndb.IntegrityError:  # 已存在该结果
            # self.db.close()
            return "更新失败"

