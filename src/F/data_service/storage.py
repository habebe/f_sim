import mysql.connector

class Storage:
    def __init__(self,service):
        self.__service = service
        self.__connection = None
        self.__initialize()
        pass

    def __initialize(self):
        self.__connection = mysql.connector.connect(host=self.__service.config().storage_host(),
                                                    user=self.__service.config().storage_user(),
                                                    password=self.__service.config().storage_password(),
                                                    use_pure=True)

    def initialize_datasource(self,data_source):
        cursor = self.__connection.cursor(buffered=True)
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(data_source.storage_name()))
        tables_descriptions = data_source.object_descriptions()
        for table_name in tables_descriptions:
            column_descriptions = tables_descriptions[table_name]
            size = len(column_descriptions)
            columns = ""
            for i in range(size):
                column_description = column_descriptions[i] 
                columns = columns + " {0} {1} ".format(column_description.name,column_description.data_type)
                if i < (size-1):
                    columns = columns + ","
                    pass
                pass
            statement = '''CREATE TABLE IF NOT EXISTS {0} ( {1} ) '''.format(table_name,columns)
            cursor.execute(statement)
        cursor.close()
        self.__connection.commit()

    def persist(self,data_source,table_name,data):
        tables_descriptions = data_source.object_descriptions()
        column_descriptions = tables_descriptions[table_name]
        size = len(column_descriptions)
        column_names = ""
        column_values = ""
        update_values = ""
        for i in range(size):
            column_description = column_descriptions[i]
            column_names  += " {0} ".format(column_description.name)
            column_values += " %({0})s ".format(column_description.name)
            update_values += " {0} = %({0})s ".format(column_description.name)
            if i < (size - 1):
                column_names += ","
                column_values += ","
                update_values += ","
        statement = '''INSERT INTO {0}({1}) VALUES({2}) ON DUPLICATE KEY UPDATE {3}'''.format(table_name,column_names,column_values,update_values)
        cursor = self.__connection.cursor(buffered=True)
        cursor.execute(statement,data)
        self.__connection.commit()
        cursor.close()
        pass

    def query(self,table_name,select,where=None,limit=None):
        statement = '''SELECT {0} from {1} '''.format(select,table_name)
        if where != None:
            statement += 'where {0} '.format(where)
        if limit != None:
            statement += 'limit {0}'.format(limit)
        cursor = self.__connection.cursor(buffered=True)
        cursor.execute(statement)
        result = cursor.fetchall()
        return result

  


