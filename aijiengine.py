import pymysql

host = "localhost"
port = 3306
user = "root"
passwd = "ary6769339jy"
database = "smart_bid"



class SqlEngine:  # 一个实例，完成一个功能后，完成新的功能需要重新开通实例，因为每个功能最后都close了

    def __init__(self):
        try:
            conn = pymysql.connect(host=host, port=port, user=user, password=passwd, database=database,
                                   connect_timeout=15, charset='utf8')  # 建立数据库链接
            self.conn = conn
            self.coon = True
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f'数据库连接失败：<{e}>')

    def close(self):
        self.cursor.close()
        self.conn.close()

    def insert(self, sql, args):  # 增
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
        except Exception as e:
            print(f'数据插入失败：<{sql}>, {e}')
            self.conn.rollback()
        finally:
            self.close()

    def insertmany(self, sql, args):  # 添加多条记录
        try:
            self.cursor.executemany(sql, args)
            self.conn.commit()
        except Exception as e:
            print(f'数据批量插入失败：<{sql}>, {e}')
            self.conn.rollback()
        finally:
            self.close()

    def update(self, sql):  # 改
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(f'更新数据失败:<{sql}>, {e}')
            self.conn.rollback()
        finally:
            self.close()

    def findone(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print(f'查询一条数据失败：<{sql}>, {e}')
        finally:
            self.close()

    def findall(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print(f'查询所有数据失败：<{sql}>, {e}')
        finally:
            self.close()


class OriginBid:  # t_origin_bid表操作类
    table = 't_origin_bid'

    def insert(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, bid_id, bid_title, bid_type, bid_source, bid_url, create_time, " \
              "create_by) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)".format(self.table)
        engine.insert(sql, args)

    def insertmany(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, bid_id, bid_title, bid_type, bid_source, bid_url, create_time, " \
              "create_by) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)".format(self.table)
        engine.insertmany(sql, args)

    def findall(self, sql):
        engine = SqlEngine()
        data = engine.findall(sql)
        return data

    def update(self, sql):
        engine = SqlEngine()
        engine.update(sql)


class OriginBidInfo:  # t_origin_bid_info表操作类
    table = 't_origin_bid_info'

    def insert(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, bid_id, col_key, col_value, info_addr, is_valid, is_trans, " \
              "create_time, create_by) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(self.table)
        engine.insert(sql, args)

    def insertmany(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, bid_id, col_key, col_value, info_addr, is_valid, is_trans, " \
              "create_time, create_by) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(self.table)
        engine.insertmany(sql, args)

    def findall(self, sql):
        engine = SqlEngine()
        data = engine.findall(sql)
        return data

    def update(self, sql):
        engine = SqlEngine()
        engine.update(sql)


class OriginBidText:  # t_origin_bid_text表操作类
    table = 't_origin_bid_text'

    def insert(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, bid_id, bid_text, is_valid, is_trans, " \
              "create_time, create_by) VALUES(%s, %s, %s, %s, %s, %s, %s)".format(self.table)
        engine.insert(sql, args)

    def insertmany(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, bid_id, bid_text, is_valid, is_trans, " \
              "create_time, create_by) VALUES(%s, %s, %s, %s, %s, %s, %s)".format(self.table)
        engine.insertmany(sql, args)

    def findall(self, sql):
        engine = SqlEngine()
        data = engine.findall(sql)
        return data

    def update(self, sql):
        engine = SqlEngine()
        engine.update(sql)


class TFileAttach:  # t_file_attach表，附件链接
    table = 't_file_attach'

    def insert(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, file_id, bid_id, proj_id, file_name, link, is_valid, create_time, create_by) " \
              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(self.table)
        engine.insert(sql, args)

    def insertmany(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, file_id, bid_id, proj_id, file_name, link, is_valid, create_time, create_by) " \
              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(self.table)
        engine.insertmany(sql, args)

    def findall(self, sql):
        engine = SqlEngine()
        data = engine.findall(sql)
        return data

    def update(self, sql):
        engine = SqlEngine()
        engine.update(sql)


class RProjBid:  # proj_i与bid_id关联表
    table = 'r_proj_bid'


    def insert(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, proj_id, bid_id, is_valid, create_time, create_by) VALUES(%s, %s, %s, %s, %s, " \
              "%s)".format(self.table)
        engine.insert(sql, args)

    def insertmany(self, args):
        engine = SqlEngine()
        sql = "INSERT INTO {}(id, proj_id, bid_id, is_valid, create_time, create_by) VALUES(%s, %s, %s, %s, %s, " \
              "%s)".format(self.table)
        engine.insertmany(sql, args)

    def findall(self, sql):
        engine = SqlEngine()
        data = engine.findall(sql)
        return data

    def update(self, sql):
        engine = SqlEngine()
        engine.update(sql)






