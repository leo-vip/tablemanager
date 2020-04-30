from core.globals import db_manager


class TableService:
    def list_tables(self):
        return db_manager.list_table()

    def show_table_column(self, table_name):
        return db_manager.show_table_columns(table_name)

    def sql_page(self, table_name, page, limit, where):
        start = (page - 1) * limit
        if where is not None and len(where.strip()) != 0:
            where = f"where {where}"

        sql = f"select * from {table_name} {where} limit {start},{limit}"
        return db_manager.query_sql(sql)

    def count(self, table_name):
        sql = f"select count(*) from {table_name}"
        return db_manager.query_sql(sql)[0][0]

    def getPK(self, table_name):
        return db_manager.getPK(table_name)

    def query_data_by_id(self, column, value, table_name):

        return db_manager.query_sql(f"select * from {table_name} where {column} = {value}")

    def update_column(self, name, value, table_name, columns:dict):
        def get_format_value(value):
            if value.isdigit():
                return f"{value}"
            else:
                return f"'{value}'"
        _cols = []
        for column in columns.keys():
            _cols.append(f"{column}={get_format_value(columns[column])}")
        _cols_str = ",".join(_cols)

        sql = f"update {table_name} set {_cols_str} where {name} = {get_format_value(value)}"
        db_manager.execute_sql(sql)
        pass


if __name__ == '__main__':
    service = TableService()
    # result = service.sql_page('data_wanqu_detail', 1, 20)
    #
    # for result_ in result:
    #     print(result_)
    print(service.count('data_wanqu_detail'))
