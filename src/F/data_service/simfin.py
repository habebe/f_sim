import requests
import pandas
from importlib import reload
import mysql.connector
import datetime
import json
import pickle
import data_service.base_dataservice as base_dataservice
import datetime
class URL:
    ALL_ENTITIES = "https://simfin.com/api/v1/info/all-entities"
    GENERAL = "https://simfin.com/api/v1/companies/id/{0}"
    STATEMENT_LIST = "https://simfin.com/api/v1/companies/id/{0}/statements/list"
    STATEMENT_STD = "https://simfin.com/api/v1/companies/id/{0}/statements/standardised"
    STATEMENT_ORG = "https://simfin.com/api/v1/companies/id/{0}/statements/original"
    TTM_RATIO = "https://simfin.com/api/v1/companies/id/{0}/ratios"
    AGGREGATED_SHARES = "https://simfin.com/api/v1/companies/id/{0}/shares/aggregated"

class DataService(base_dataservice.BaseDataService):
    TABLE_ENTITIES = "{0}.entities"
    TABLE_COMPANY_DATA = "{0}.company_data"
    TABLE_TTM_RATIO = "{0}.ttm_ratio"
    TABLE_STATEMENT_LIST = "{0}.statement_list"

    def __init__(self,service):
        base_dataservice.BaseDataService.__init__(self,service.config().simfin_storage())
        self.__service = service
        self.__table_name_entities = None
        self.__table_name_company_data = None
        self.__table_ttm_ratio = None
        self.__statement_list = None

        self.__entities = None

        self.__api_key = self.__service.config().simfin_apikey()
        self.add_field(self.table_name_entities(),base_dataservice.FieldDescription("date","DATE"))
        self.add_field(self.table_name_entities(),base_dataservice.FieldDescription("data","LONGBLOB"))

        self.add_field(self.table_name_company_data(),base_dataservice.FieldDescription("simId","INTEGER PRIMARY KEY"))
        self.add_field(self.table_name_company_data(),base_dataservice.FieldDescription("date","DATE"))
        self.add_field(self.table_name_company_data(),base_dataservice.FieldDescription("data","LONGBLOB"))

        self.add_field(self.table_name_ttm_ratio(),base_dataservice.FieldDescription("simId","INTEGER PRIMARY KEY"))
        self.add_field(self.table_name_ttm_ratio(),base_dataservice.FieldDescription("date","DATE"))
        self.add_field(self.table_name_ttm_ratio(),base_dataservice.FieldDescription("data","LONGBLOB"))

        
        self.add_field(self.table_name_statement_list(),base_dataservice.FieldDescription("simId","INTEGER PRIMARY KEY"))
        self.add_field(self.table_name_statement_list(),base_dataservice.FieldDescription("date","DATE"))
        self.add_field(self.table_name_statement_list(),base_dataservice.FieldDescription("data","LONGBLOB"))
        self.__service.storage().initialize_datasource(self)
        pass

    def table_name_statement_list(self):
        if self.__statement_list == None:
            self.__statement_list =  self.TABLE_STATEMENT_LIST.format(self.__service.config().simfin_storage())
        return self.__statement_list

    def table_name_ttm_ratio(self):
        if self.__table_ttm_ratio == None:
            self.__table_ttm_ratio =  self.TABLE_TTM_RATIO.format(self.__service.config().simfin_storage())
        return self.__table_ttm_ratio

    def table_name_company_data(self):
        if self.__table_name_company_data == None:
            self.__table_name_company_data =  self.TABLE_COMPANY_DATA.format(self.__service.config().simfin_storage())
        return self.__table_name_company_data

    def table_name_entities(self):
        if self.__table_name_entities == None:
            self.__table_name_entities =  self.TABLE_ENTITIES.format(self.__service.config().simfin_storage())
        return self.__table_name_entities

    def __request(self,request_type,params = None):
        if params == None:
            params = {}
        params["api-key"] = self.__api_key
        self.__service.debug_log("simfin request:{}".format(request_type))
        response = requests.get(request_type,params=params)
        json_data = response.json()
        if 'error' in json_data:
            raise Exception("simfin exception {} ".format(json_data['error']))
        return response.text

    def company_data(self,simId,refresh=False):
        __company_data = None
        if (refresh == True):
            response = self.__request(URL.GENERAL.format(simId))
            data = {"date":datetime.datetime.now(),'data':response,"simId":simId}
            self.__service.storage().persist(self,self.table_name_company_data(),data)
            data = json.loads(response)
            __company_data = pandas.DataFrame(columns=data.keys()).transpose()
            __company_data[0] = data.values()
        else:
            response = self.__service.storage().query(self.table_name_company_data(),select="data",where="simId = {}".format(simId),limit=1)
            if (response != None) and (len(response) > 0):
                data = json.loads(response[0][0])   
                __company_data = pandas.DataFrame(columns=data.keys()).transpose()
                __company_data[0] = data.values()
            else:
                response = self.__request(URL.GENERAL.format(simId))
                data = {"date":datetime.datetime.now(),'data':response,"simId":simId}
                self.__service.storage().persist(self,self.table_name_company_data(),data)
                data = json.loads(response)
                __company_data = pandas.DataFrame(columns=data.keys()).transpose()
                __company_data[0] = data.values()
        return __company_data

    def ratios(self,simId,refresh=False):
        result = None
        if (refresh == True):
            response = self.__request(URL.TTM_RATIO.format(simId))
            data = {"date":datetime.datetime.now(),'data':response,"simId":simId}
            self.__service.storage().persist(self,self.table_name_ttm_ratio(),data)
            result = json.loads(response)
            result = pandas.DataFrame(result)
        elif(type(result) == type(None)):
            response = self.__service.storage().query(self.table_name_ttm_ratio(),select="data",where=None,limit=1)
            if (response != None) and (len(response) > 0):
                result = json.loads(response[0][0])   
                result = pandas.DataFrame(result)
            else:
                response = self.__request(URL.TTM_RATIO.format(simId))
                data = {"date":datetime.datetime.now(),'data':response,"simId":simId}
                self.__service.storage().persist(self,self.table_name_ttm_ratio(),data)
                result = json.loads(response)
                result = pandas.DataFrame(result)
        return result
  
    def statement_list(self,simId,stmt_type,refresh=False):
        result = None
        if (refresh == True):
            response = self.__request(URL.STATEMENT_LIST.format(simId))
            data = {"date":datetime.datetime.now(),'data':response,"simId":simId}
            self.__service.storage().persist(self,self.table_name_statement_list(),data)
            result = json.loads(response)
            result = pandas.DataFrame(result[stmt_type])
        elif(type(result) == type(None)):
            response = self.__service.storage().query(self.table_name_statement_list(),select="data",where=None,limit=1)
            if (response != None) and (len(response) > 0):
                result = json.loads(response[0][0])   
                result = pandas.DataFrame(result[stmt_type])
            else:
                response = self.__request(URL.STATEMENT_LIST.format(simId))
                data = {"date":datetime.datetime.now(),'data':response,"simId":simId}
                self.__service.storage().persist(self,self.table_name_statement_list(),data)
                result = json.loads(response)
                result = pandas.DataFrame(result[stmt_type])
        return result

    def entities(self,refresh=False):
        if (refresh == True):
            response = self.__request(URL.ALL_ENTITIES)
            data = {"date":datetime.datetime.now(),'data':response}
            self.__service.storage().persist(self,self.table_name_entities(),data)
            self.__entities = json.loads(response)
            self.__entities = pandas.DataFrame(self.__entities)
        elif(type(self.__entities) == type(None)):
            response = self.__service.storage().query(self.table_name_entities(),select="data",where=None,limit=1)
            if (response != None) and (len(response) > 0):
                self.__entities = json.loads(response[0][0])   
                self.__entities = pandas.DataFrame(self.__entities)
            else:
                response = self.__request(URL.ALL_ENTITIES)
                data = {"date":datetime.datetime.now(),'data':response}
                self.__service.storage().persist(self,self.table_name_entities(),data)
                self.__entities = json.loads(response)
                self.__entities = pandas.DataFrame(self.__entities)
        return self.__entities