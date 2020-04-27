import pymysql
from apiauto.conf import config
from apiauto.common import log

logger = log.log()

#获取db配置
dbconfig = config.getconfig()
user = dbconfig['test_mysql']['user']
pwd = dbconfig['test_mysql']['pwd']
ip = dbconfig['test_mysql']['ip']
database = dbconfig['test_mysql']['database']
port = int(dbconfig['test_mysql']['port'])

class Mydb:
    def __init__(self):
        try:
            logger.info('*****数据库连接中*****')
            self.db = pymysql.connect(host=ip,user=user,password=pwd,database=database,port=port)
            self.cursor = self.db.cursor()
            logger.info('*****数据库连接成功*****')
        except Exception as e:
            logger.info('*****数据库连接失败*****')
            logger.info(e)

    
    def select(self,sql):
        logger.info('*****查询数据库*****')
        logger.info(sql)
        try:
            self.cursor.execute(sql)
            logger.info('*****查询成功*****')
        except Exception as e:
            logger.info('*****查询失败*****')
        #获取查询结果
        result = self.cursor.fetchall()
        return result

    
    def update(self,sql):
        logger.info('*****修改数据库*****')
        logger.info(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info('*****修改成功*****')
        except Exception as e:
            logger.info('*****修改失败*****')
            self.db.rollback()


    def insert(self,sql):
        logger.info('*****插入数据*****')
        logger.info(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info('*****插入成功*****')
        except Exception as e:
            logger.info('*****插入失败*****')
            self.db.rollback()


    def delete(self,sql):
        logger.info('*****删除数据*****')
        logger.info(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info('*****删除成功*****')
        except Exception as e:
            logger.info('*****删除失败*****')
            self.db.rollback()
        
    
    def closedb(self):
        try:
            logger.info('*****关闭数据库连接*****')
            self.db.close()
            logger.info('*****关闭成功*****')
        except Exception as e:
            logger.info('*****关闭成功*****')
            logger.info(e)


