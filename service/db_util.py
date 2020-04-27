# 导入:
from sqlalchemy import Column, String, create_engine, Integer, Text, DateTime, func, Boolean, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建对象的基类:
Base = declarative_base()


class DBManager:
    def __init__(self):
        # engine = create_engine('mysql+pymysql://root:root@localhost:3306/cloud_reader', echo=True)
        self.engine = create_engine('mysql+pymysql://root:root@localhost:3306/spiderflow')
        Base.metadata.create_all(self.engine)

        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=self.engine)

    def add(self, entity):
        session = self.DBSession()

        session.add(entity)

        session.commit()
        session.refresh(entity)
        session.expunge(entity)

        session.close()

    def delete(self, entity, *args):

        session = self.DBSession()
        q = session.query(entity)
        for arg in args:
            q = q.filter(arg)
        q.delete()
        session.commit()
        session.close()

    def query_one_or_none(self, entity, *args):
        session = self.DBSession()
        q = session.query(entity)
        for arg in args:
            q = q.filter(arg)
        result = q.one_or_none()
        session.close()
        return result

    def query_order_by_field(self, entity, order_by, args=[], offset=0, limit=10, ):
        session = self.DBSession()
        q = session.query(entity)
        for arg in args:
            q = q.filter(arg)
        q = q.order_by(order_by)
        q = q.limit(limit)
        q = q.offset(offset)
        result = q.all()
        session.close()
        return result

    def query_sql(self, sql):
        """
        execute sql
        :param sql:
        :return: result
        """
        session = self.DBSession()

        cursor = session.execute(sql)
        result = cursor.fetchall()
        session.close()
        return result

    def list_table(self):
        result = self.query_sql("show table status;")
        tables = [v[0] for v in result]
        return tables

    def show_table_columns(self, table_name):
        result = self.query_sql(f"desc {table_name};")
        return result


if __name__ == '__main__':
    db = DBManager()
    # print(db.list_table())
    print(db.show_table_columns('data_wanqu'))
#     # a = Article(title='你好111222', title_en='hello111222', link='http://ssssss')
#     # db.add(a)
#     result = db.query_sql(
#         "SELECT s.`subject`,r.book_id from bk_subject s, bk_relationship r WHERE s.id = r.subject_id and s.id =1306")
#     print(result)
