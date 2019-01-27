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
    
    def __init__(self,service):
        base_dataservice.BaseDataService.__init__(self,service.config().simfin_storage())
        self.__service = service
        self.__table_name_entities = None
        self.__entities = None
        
        self.__api_key = self.__service.config().simfin_apikey()
        self.add_field(self.table_name_entities(),base_dataservice.FieldDescription("date","DATE"))
        self.add_field(self.table_name_entities(),base_dataservice.FieldDescription("data","LONGBLOB"))
        self.__service.storage().initialize_datasource(self)
        pass

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

    def entities(self,refresh=False):
        if (refresh == True):
            response = self.__request(URL.ALL_ENTITIES)
            data = {"date":datetime.datetime.now(),'data':response}
            self.__service.storage().persist(self,self.table_name_entities(),data)
            self.__entities = json.loads(response)
            self.__entities = pandas.DataFrame(self.__entities)
            #self.__entities.set_index("simId",inplace=True)
        elif(type(self.__entities) == type(None)):
            response = self.__service.storage().query(self.table_name_entities(),select="data",where=None,limit=1)
            if (response != None) and (len(response) > 0):
                self.__entities = json.loads(response[0][0])   
                self.__entities = pandas.DataFrame(self.__entities)
                #self.__entities.set_index("simId",inplace=True)
        return self.__entities