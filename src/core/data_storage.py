import os
import datetime
import pickle
import requests_cache
import pandas_datareader
import requests
import bs4 as bs
import time
import sys
import mysql.connector
import pandas 
import data_object

class DataStorage:
    database_name = "stock_sim"
    table_company = "company"
    table_raw_data = "raw_data"
    table_meta_data = "meta_data"
    TYPE = "RAW_DATA_TYPE"
    SOURCE = "RAW_DATA_SOURCE"
    SECTOR = "RAW_DATA_SECTOR"
    INDUSTRY = "RAW_DATA_INDUSTRY"
    CATEGORY = "RAW_DATA_CATEGORY"
    EXCHANGE = "RAW_DATA_EXCHANGE"
    table_attributes = [TYPE,SOURCE,SECTOR,INDUSTRY,CATEGORY,EXCHANGE]

    META_DATA_SP500_TICKERS = "SP500-Tickers"

    def __init__(self,password,host="localhost",user="stock"):
        self.connection = None
        self.value_maps = {}
        self.id_maps = {}

        self.host = host
        self.user = user
        self.password = password
        for i in self.table_attributes:
            self.value_maps[i] = {}
            self.id_maps[i] = {}
            pass

        self.meta_data = {}

        self.dataset = {}
        self.companies = {}
        self.__initialize__()
        pass

    def __del__(self):
        self.close()
        pass

    def close(self):
        if self.connection:
            #self.connection.close()
            self.connection = None
        pass

    def __initialize__(self):
        self.connection = mysql.connector.connect(host=self.host,user=self.user,password=self.password,use_pure=True)
        cursor = self.connection.cursor(buffered=True)
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.database_name))
        cursor.execute("USE {}".format(self.database_name))
        cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                id VARCHAR(8) PRIMARY KEY,
                source INTEGER,
                type INTEGER,
                sector INTEGER,
                industry INTEGER,
                category INTEGER,
                start DATETIME,
                end DATETIME,
                description TEXT,
                data LONGBLOB 
            )'''.format(self.table_raw_data))
        cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                id VARCHAR(8) PRIMARY KEY,
                name TEXT,
                lastsale DOUBLE,
                marketcap DOUBLE,
                ipoyear INTEGER,
                sector INTEGER,
                industry INTEGER,
                exchange INTEGER,
                summary TEXT,
                date DATETIME
            )'''.format(self.table_company))
        cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                id VARCHAR(256) PRIMARY KEY,
                value BLOB
                )'''.format(self.table_meta_data))
        for i in self.table_attributes:
            cursor.execute('''CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                value TEXT
                )'''.format(i))
        cursor.close()
        self.connection.commit()

    def insert_meta_data(self,_id,_value):
        statement = '''INSERT INTO {0}(id,value) VALUES(%s,%s)
        ON DUPLICATE KEY UPDATE
        value = %s
        '''.format(self.table_meta_data)
        cursor = self.connection.cursor()
        _value = pickle.dumps(_value)
        cursor.execute(statement,[_id,_value,_value])
        self.connection.commit()
        cursor.close()

    def update_meta_data(self,_id,_value):
        statement = '''UPDATE {} SET value=%s WHERE id=%s'''.format(self.table_meta_data)
        cursor = self.connection.cursor()
        _value = pickle.dumps(_value)
        cursor.execute(statement,[_value,_id])
        self.connection.commit()
        cursor.close()
    
    def fetch_meta_data(self,_id):
        statement = '''SELECT value FROM {} where id=%s'''.format(self.table_meta_data)
        cursor = self.connection.cursor()
        cursor.execute(statement,[_id])
        result = cursor.fetchone()
        cursor.close()
        if result != None:
            result = pickle.loads(result[0])
        return result

    def drop_meta_data(self,_id):
        statement = '''DELETE FROM {} where id=%s'''.format(self.table_meta_data)
        cursor = self.connection.cursor()
        cursor.execute(statement,[_id])
        cursor.close()
        self.connection.commit()

    def insert_map(self,map_name,value):
        statement = '''INSERT INTO {0}(value) VALUES(%s)'''.format(map_name)
        cursor = self.connection.cursor()
        cursor.execute(statement,[value])
        self.connection.commit()
        cursor.close()

    def fetch_map_using_value(self,map_name,value):
        statement = '''SELECT id,value FROM {} where value=%s'''.format(map_name)
        cursor = self.connection.cursor()
        cursor.execute(statement,[value])
        result = cursor.fetchone()
        return result

    def fetch_map_using_id(self,map_name,_id):
        statement = '''SELECT id,value FROM {} where id=%s'''.format(map_name)
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(statement,[_id])
        result = cursor.fetchone()
        cursor.close()
        return result

    def persist_into_map(self,map_name,value):
        data = self.fetch_map_using_value(map_name,value)
        if data == None:
            self.insert_map(map_name,value)
            data = self.fetch_map_using_value(map_name,value)
        return data

    def get_map_using_value(self,_type,value):
        if value in self.value_maps[_type]:
            return self.value_maps[_type][value]
        result = self.persist_into_map(_type,value)
        if result != None:
            source = data_object.KeyValue(result[0],result[1],_type)
            self.value_maps[_type][value] = source
            self.id_maps[_type][source.id] = source
            return source
        return None

    def get_map_using_id(self,_type,_id):
        if _id == None:
            return None
        if _id in self.id_maps[_type]:
            return self.id_maps[_type][_id]
        result = self.fetch_map_using_id(_type,_id)
        if result != None:
            source = data_object.KeyValue(result[0],result[1],_type)
            self.value_maps[_type][_id] = source
            self.id_maps[_type][source.id] = source
            return source
        return None

    def insert(self,data):
        statement = '''
        INSERT INTO {}(id,source,type,sector,industry,category,start,end,description,data)
        VALUES(%(id)s,%(source)s,%(type)s,%(sector)s,%(industry)s,%(category)s,%(start)s,%(end)s,%(description)s,%(data)s)
        ON DUPLICATE KEY UPDATE
        source = %(source)s,
        type = %(type)s,
        sector =%(sector)s,
        industry = %(industry)s,
        category = %(category)s,
        start = %(start)s,
        end = %(end)s,
        description = %(description)s,
        data = %(data)s
        '''.format(self.table_raw_data)
        _sector = data.sector
        if _sector:
            _sector = data.sector.id
        _industry = data.industry
        if _industry:
            _industry = data.industry.id
        _type = data.type
        if _type:
            _type = data.type.id
        _category = data.category
        if _category:
            _category = data.category.id
        _source = data.source
        if _source:
            _source = data.source.id
        _data = pickle.dumps(data.data_frame)
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(statement,
        {
            'id':data.id,
            "source":_source,
            "type":_type,
            "sector":_sector,
            "industry":_industry,
            "category":_category,
            "start":data.start,
            "end":data.end,
            "description":data.description,
            "data":_data
        }
        )
        self.connection.commit()
        cursor.close()

    def insert_company(self,data):
        statement = '''
        INSERT INTO {}(id,name,lastsale,marketcap,ipoyear,sector,industry,exchange,summary,date)
        VALUES(%(id)s,%(name)s,%(lastsale)s,%(marketcap)s,%(ipoyear)s,%(sector)s,%(industry)s,%(exchange)s,%(summary)s,%(date)s)
        ON DUPLICATE KEY UPDATE
        name = %(name)s,
        lastsale = %(lastsale)s,
        marketcap =%(marketcap)s,
        ipoyear = %(ipoyear)s,
        sector = %(sector)s,
        industry = %(industry)s,
        exchange = %(exchange)s,
        summary = %(summary)s,
        date = %(date)s
        '''.format(self.table_company)
        _sector = data.sector
        if _sector:
            _sector = data.sector.id
        _industry = data.industry
        if _industry:
            _industry = data.industry.id
        _exchange = data.exchange
        if _exchange:
            _exchange = data.exchange.id
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(statement,
        {
            'id':data.id,
            "name":data.name,
            "lastsale":data.lastsale,
            "marketcap":data.marketcap,
            "ipoyear":data.ipoyear,
            "sector":_sector,
            "industry":_industry,
            "exchange":_exchange,
            "summary":data.summary,
            "date":data.date
        }
        )
        self.connection.commit()
        cursor.close()

    def fetch_company(self,_id):
        if _id in self.dataset:
            return self.dataset[_id]
        statement = '''SELECT id,name,lastsale,marketcap,ipoyear,sector,industry,exchange,summary,date FROM {} where id=%s'''.format(self.table_company)
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(statement,[_id])
        result = cursor.fetchone()
        if result != None:
            _sector = self.get_map_using_id(self.SECTOR,result[5])
            _industry = self.get_map_using_id(self.INDUSTRY,result[6])
            _exchange = self.get_map_using_id(self.EXCHANGE,result[7])
            result = data_object.Company(
                _id,
                result[1],
                result[2],
                result[3],
                result[4],
                _sector,
                _industry,
                _exchange,
                result[8],
                result[9]
            )
            self.dataset[_id] = result
        return result

    def fetch(self,_id):
        if _id in self.companies:
            return self.companies[_id]
        statement = '''SELECT id,source,type,sector,industry,category,start,end,description,data FROM {} where id=%s'''.format(self.table_raw_data)
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(statement,[_id])
        result = cursor.fetchone()
        if result != None:
            _source = self.get_map_using_id(self.SOURCE,result[1])
            _type = self.get_map_using_id(self.TYPE,result[2])
            _sector = self.get_map_using_id(self.SECTOR,result[3])
            _industry = self.get_map_using_id(self.INDUSTRY,result[4])
            _category = self.get_map_using_id(self.CATEGORY,result[5])
            result = data_object.Data(
                _id,
                _source,
                _type,
                _sector,
                 _industry,
                 _category,
                result[6],
                result[7],
                result[8],
                pickle.loads(result[9])
            )
            self.dataset[_id] = result
        return result

    def drop(self,_id):
        statement = '''DELETE FROM {} where id=%s'''.format(self.table_raw_data)
        cursor = self.connection.cursor()
        cursor.execute(statement,[_id])
        cursor.close()
        self.connection.commit()
        if _id in self.dataset:
            del self.dataset[_id]

if __name__ == "__main__":
    storage = DataStorage("3599")
    storage.insert_meta_data("hello2",[325,6,7,8])
    data = storage.fetch_meta_data("hello2")
    print(data)
    storage.drop_meta_data("hello2")
    data = storage.fetch_meta_data("hello2")
    print(data)


    result = storage.get_map_using_value(DataStorage.SECTOR,"Fake Data")

   # def __init__(self,_id,_source,_type,_sector,_industry,_category,_start,_end,_description,_data):

    data = data_object.Data("HELLO",None,None,None,None,None,datetime.datetime.today(),datetime.datetime.today(),"Some description",pandas.DataFrame({"A":[1,2,3,4]}))
    storage.insert(data)

    data = storage.fetch("HELLO")
    print(data)

    storage.drop("HELLO")
    data = storage.fetch("HELLO")
    print("NEW DATA" + str(data))

