import sqlite3
import os
from EZVIZ_CAM.ezviz import EZVIZ_Status, EZVIZ
from EZVIZ_CAM.ftp_manager import FTP_Manager

from dao.ProcessingObject import ProcessingObject,p_type
import time

class SQL_manager:
    def __init__(self, ip, full_name=""):
        self.sql_create_FILE_TABLE = '''CREATE TABLE "FILE_TABLE" (
                                        "ID"	INTEGER NOT NULL UNIQUE,
                                        "FILE_NAME"	VARCHAR(255) NOT NULL,
                                        "MODIFY_TIME"	DATETIME NOT NULL,
                                        "STATUS"	INT NOT NULL,
                                        "FILE_PATH"	VARCHAR(255) NOT NULL,
                                        "SERVER_PATH"	VARCHAR(255) NOT NULL,
                                        "FULL_NAME"	INTEGER NOT NULL,
                                        FOREIGN KEY("STATUS") REFERENCES "STATUS"("ID"),
                                        PRIMARY KEY("ID" AUTOINCREMENT)
                                    )'''    
        self.sql_create_STATUS = '''CREATE TABLE "STATUS" (
                                    "ID"	INTEGER NOT NULL UNIQUE,
                                    "TYPE"	VARCHAR(255) NOT NULL,
                                    PRIMARY KEY("ID" AUTOINCREMENT)
                                )'''
        self.sql_create_RECORD = '''CREATE TABLE "RECORD" (
                                    "ID"	INTEGER NOT NULL UNIQUE,
                                    "FLAG"	INTEGER NOT NULL,
                                    PRIMARY KEY("ID" AUTOINCREMENT)
                                )'''
        self.sql_create_NV_CARD = '''CREATE TABLE "NV_CARD" (
                                    "ID"	INTEGER NOT NULL UNIQUE,
                                    "STATUS"	INTEGER NOT NULL,
                                    PRIMARY KEY("ID" AUTOINCREMENT)
                                )'''
        self.sql_create_PROGRESS = '''CREATE TABLE "PROGRESS" (
                                    "ID"	INTEGER NOT NULL UNIQUE,
                                    "PATH"	VARCHAR(255) NOT NULL,
                                    "START" VARCHAR(255) NOT NULL,
                                    "END" VARCHAR(255) NOT NULL,
                                    PRIMARY KEY("ID" AUTOINCREMENT)
                                )'''
        # self.sql_create_PROCESS_FILE_TABLE = ''''CREATE TABLE "PROCESS_FILE_TABLE" (
        #                                 "ID"	INTEGER NOT NULL UNIQUE,
        #                                 "FILE_NAME"	VARCHAR(255) NOT NULL,
        #                                 "MODIFY_TIME"	DATETIME NOT NULL,
        #                                 "STATUS"	INT NOT NULL,
        #                                 "FILE_PATH"	VARCHAR(255) NOT NULL,
        #                                 "SERVER_PATH"	VARCHAR(255) NOT NULL,
        #                                 "FULL_NAME"	INTEGER NOT NULL,
        #                                 FOREIGN KEY("STATUS") REFERENCES "STATUS"("ID"),
        #                                 PRIMARY KEY("ID" AUTOINCREMENT)
        #                             )'''    
        self.connection_name = ip + '.db'
        self.ip = ip
        self.full_name = full_name

        if not os.path.exists(self.connection_name):
            self.create_database()
            self.init_status()

        if full_name != "":
            self.check_init()
            self.init_record()
            self.init_nv_card()
            # self.init_progress()
        else:
            pass            
            
    def init_status(self):
        sqls = ['''INSERT INTO "main"."STATUS" ("TYPE") VALUES ('UNFETECH')''',
        '''INSERT INTO "main"."STATUS" ("TYPE") VALUES ('WAITINGFORDOWNLOADING')''',
        '''INSERT INTO "main"."STATUS" ("TYPE") VALUES ('DOWNLOADING')''',
        '''INSERT INTO "main"."STATUS" ("TYPE") VALUES ('WAITINGFORRUNNING')''',
        '''INSERT INTO "main"."STATUS" ("TYPE") VALUES ('RUNNING')''',
        '''INSERT INTO "main"."STATUS" ("TYPE") VALUES ('FINISHED')''']
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        # 编写sql语句
        for item in sqls:
            cour.execute(item)
        cour.close()
        conn.commit()
        conn.close()

    def init_record(self):
        sql = '''INSERT OR REPLACE INTO "main"."RECORD" ("ID", "FLAG") VALUES (1, 0)'''
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        # 编写sql语句
        cour.execute(sql)
        cour.close()
        conn.commit()
        conn.close()

    def init_nv_card(self):
        sql = '''INSERT OR REPLACE INTO "main"."NV_CARD" ("ID", "STATUS") VALUES (1, 0)'''
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        # 编写sql语句
        cour.execute(sql)
        cour.close()
        conn.commit()
        conn.close()

    def create_database(self):
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        # 编写sql语句
        cour.execute(self.sql_create_FILE_TABLE)
        cour.execute(self.sql_create_STATUS)
        cour.execute(self.sql_create_RECORD)
        cour.execute(self.sql_create_NV_CARD)
        cour.execute(self.sql_create_PROGRESS)
        # cour.execute(self.sql_create_PROCESS_FILE_TABLE)
        cour.close()
        conn.commit()
        conn.close()

    def check_init(self):
        conn = sqlite3.connect(self.connection_name)
        cour = conn.cursor()
        sql = 'select * from FILE_TABLE'
        cour.execute(sql)
        for item in cour.fetchall():
            self.update_status(item[0], EZVIZ_Status.UNFETCHING.value)
        cour.close()
        
        mgr = FTP_Manager(self.ip, self.full_name)
        ezviz_list = mgr.openFTPFile()
        for item in ezviz_list:
            # 创建游标
            cour = conn.cursor()
            # 编写sql语句
            sql = "INSERT INTO FILE_TABLE (FILE_NAME, MODIFY_TIME, STATUS, FILE_PATH, SERVER_PATH, FULL_NAME) SELECT ?, ?, ?, ?, ?, ? WHERE not exists (select * from FILE_TABLE where MODIFY_TIME=? AND SERVER_PATH=?)"
            # 执行sql语句
            cour.execute(sql, (item.file_name, str(item.modify_time), int(EZVIZ_Status.UNFETCHING.value), item.file_path, item.server_path, self.full_name, str(item.modify_time), item.server_path))
            # 关闭游标
            conn.commit()
            cour.close()
            # 关闭连接
        conn.close()

    # def check_process_init(self):
    #     conn = sqlite3.connect(self.connection_name)
    #     cour = conn.cursor()
    #     sql = 'select * from PROCESS_FILE_TABLE'
    #     cour.execute(sql)
    #     for item in cour.fetchall():
    #         self.update_status(item[0], EZVIZ_Status.UNFETCHING.value)
    #     cour.close()
        
    #     mgr = FTP_Manager(self.ip, self.full_name)
    #     ezviz_list = mgr.openFTPFile()
    #     for item in ezviz_list:
    #         # 创建游标
    #         cour = conn.cursor()
    #         # 编写sql语句
    #         sql = "INSERT INTO PROCESS_FILE_TABLE (FILE_NAME, MODIFY_TIME, STATUS, FILE_PATH, SERVER_PATH, FULL_NAME) SELECT ?, ?, ?, ?, ?, ? WHERE not exists (select * from PROCESS_FILE_TABLE WHERE MODIFY_TIME=? AND SERVER_PATH=?)"
    #         # 执行sql语句
    #         cour.execute(sql, (item.file_name, str(item.modify_time), int(EZVIZ_Status.UNFETCHING.value), item.file_path, item.server_path, self.full_name, str(item.modify_time), item.server_path))
    #         # 关闭游标
    #         conn.commit()
    #         cour.close()
    #         # 关闭连接
    #     conn.close()

    # def update_process_status(self, id, status):
    #     conn = sqlite3.connect(self.connection_name)
    #     # 创建游标
    #     cour = conn.cursor()
    #     # 编写sql语句
    #     sql = 'UPDATE PROCESS_FILE_TABLE SET STATUS=? WHERE ID=?'
    #     # 执行sql语句
    #     cour.execute(sql,(int(status), int(id)))
    #     # 关闭游标
    #     cour.close()
    #     # 关闭连接
    #     conn.commit()
    #     conn.close()

    def update_status(self, id, status):
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        # 编写sql语句
        sql = 'UPDATE FILE_TABLE SET STATUS=? WHERE ID=?'
        # 执行sql语句
        cour.execute(sql,(int(status), int(id)))
        # 关闭游标
        cour.close()
        # 关闭连接
        conn.commit()
        conn.close()
        
    def get_file_table(self, record_flag):
        mgr = FTP_Manager(self.ip, self.full_name)
        ezviz_list = mgr.openFTPFile()
        if record_flag:
            ezviz_list = ezviz_list[:-1]
        conn = sqlite3.connect(self.connection_name)
        for item in ezviz_list:
            # 创建游标
            cour = conn.cursor()
            # 编写sql语句
            sql = "INSERT INTO FILE_TABLE (FILE_NAME, MODIFY_TIME, STATUS, FILE_PATH, SERVER_PATH, FULL_NAME) SELECT ?, ?, ?, ?, ?, ? WHERE not exists (select * from FILE_TABLE where MODIFY_TIME=? AND SERVER_PATH=?)"
            # 执行sql语句
            cour.execute(sql, (item.file_name, str(item.modify_time), int(EZVIZ_Status.WAITINGFORDOWNLOADING.value), item.file_path, item.server_path, self.full_name, str(item.modify_time), item.server_path))
            # 关闭游标
            conn.commit()
            cour.close()
            # 关闭连接
        cour = conn.cursor()
        sql = 'select * from FILE_TABLE WHERE STATUS = 2'
        cour.execute(sql)
        res = []
        for item in cour.fetchall():
            temp = EZVIZ(item[4],item[5],item[1],item[2])
            temp.id = item[0]
            temp.status = item[3]
            temp.full_name = self.full_name
            res.append(temp)
        conn.commit()
        cour.close()
        conn.close()
        return res

    def get_downloaded_file_table(self):
        conn = sqlite3.connect(self.connection_name)
        cour = conn.cursor()
        sql = 'select * from FILE_TABLE WHERE STATUS = 4'
        cour.execute(sql)
        res = []
        for item in cour.fetchall():
            temp = EZVIZ(item[4],item[5],item[1],item[2])
            temp.id = item[0]
            temp.status = item[3]
            temp.full_name = self.full_name
            res.append(temp)
        conn.commit()
        cour.close()
        conn.close()
        return res
    
    def check_status(self, id):
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        # 编写sql语句
        sql = 'select STATUS from FILE_TABLE WHERE ID = ?'
        # 执行sql语句
        cour.execute(sql,(int(id),))
        # 打印查询结果
        res = cour.fetchall()
        # 关闭游标
        cour.close()
        # 关闭连接
        conn.close()
        return res[0][0]
    
    def update_record_status(self, flag):
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        # 编写sql语句
        sql = 'UPDATE RECORD SET FLAG=? WHERE ID=1'
        # 执行sql语句
        cour.execute(sql,(flag,))
        # 关闭游标
        cour.close()
        # 关闭连接
        conn.commit()
        conn.close()
    
    def check_record_status(self):
        conn = sqlite3.connect(self.connection_name)
        cour = conn.cursor()
        sql = 'select * from RECORD WHERE FLAG = 1'
        cour.execute(sql)
        flag = False
        if len(cour.fetchall()) > 0:
            flag = True
        cour.close()
        conn.close()
        return flag

    def check_running_status(self, full_name):
        conn = sqlite3.connect(self.connection_name)
        cour = conn.cursor()
        sql = 'select * from FILE_TABLE WHERE FULL_NAME=? AND (STATUS=4 OR STATUS=5)'
        cour.execute(sql,(full_name,))
        flag = False
        if len(cour.fetchall()) > 0:
            flag = True
        cour.close()
        conn.close()
        return flag

    def check_downloading_status(self, full_name):
        conn = sqlite3.connect(self.connection_name)
        cour = conn.cursor()
        sql = 'select * from FILE_TABLE WHERE FULL_NAME=? AND (STATUS=2 OR STATUS=3)'
        cour.execute(sql,(full_name,))
        flag = False
        if len(cour.fetchall()) > 0:
            flag = True
        cour.close()
        conn.close()
        return flag

    def check_nv_status(self, w):
        conn = sqlite3.connect(self.connection_name)
        cour = conn.cursor()
        sql = 'select STATUS from NV_CARD WHERE STATUS = 0'
        cour.execute(sql)
        flag = True
        cur = int(cour.fetchall()[0][0])
        if cur + w > 9:
            flag = False
        cour.close()
        conn.close()
        return flag
    
    def update_nv_status(self, cost):
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        sql = 'select STATUS from NV_CARD'
        cour.execute(sql)
        ori = cour.fetchall()[0]
        cost += int(ori[0])
        sql = 'UPDATE NV_CARD SET STATUS=?'
        # 执行sql语句
        cour.execute(sql,(cost,))
        # 关闭游标
        cour.close()
        # 关闭连接
        conn.commit()
        conn.close()

    def init_progress(self):
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        sql = 'truncate table PROGRESS'
        cour.execute(sql)
        # 关闭游标
        cour.close()
        # 关闭连接
        conn.commit()
        conn.close()

    def get_progress(self, path, cur):
        conn = sqlite3.connect(self.connection_name)
        # 创建游标
        cour = conn.cursor()
        sql = 'select * from PROGRESS'
        cour.execute(sql)
        progress = 0
        for item in cour.fetchall():
            path = item[1]
            start = item[2]
            end = item[3]
            progress = ((cur - start) / (end - start)) * 100
            if progress >= 100:
                sql = 'select COUNT(*) from FILE_TABLE WHERE FULL_NAME=?'
                cour.execute(sql, (path,))
                count_total = int(cour.fetchall()[0])
                sql = 'select COUNT(*) from FILE_TABLE WHERE FULL_NAME=? AND STATUS=6'
                cour.execute(sql, (path,))
                complete_total = int(cour.fetchall()[0])
                if count_total != complete_total:
                    progress = 99

        # 关闭游标
        cour.close()
        # 关闭连接
        conn.close()
        return progress

    def get_waitingruning(self):
        conn = sqlite3.connect(self.connection_name)
        res = []
        # 创建游标
        cour = conn.cursor()
        sql = 'select * from FILE_TABLE WHERE STATUS=4'
        cour.execute(sql)

        for item in cour.fetchall():
            temp = EZVIZ(item[4],item[5],item[1],item[2])
            temp.id = item[0]
            temp.status = item[3]
            temp.full_name = self.full_name
            res.append(temp)
        conn.commit()
        cour.close()
        conn.close()
        return res
