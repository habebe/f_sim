import requests
import pandas
from importlib import reload
import mysql.connector
import datetime
import json
import pickle

class URL:
    ALL_ENTITIES = "https://simfin.com/api/v1/info/all-entities"
    GENERAL = "https://simfin.com/api/v1/companies/id/{0}"
    STATEMENT_LIST = "https://simfin.com/api/v1/companies/id/{0}/statements/list"
    STATEMENT_STD = "https://simfin.com/api/v1/companies/id/{0}/statements/standardised"
    STATEMENT_ORG = "https://simfin.com/api/v1/companies/id/{0}/statements/original"
    TTM_RATIO = "https://simfin.com/api/v1/companies/id/{0}/ratios"
    AGGREGATED_SHARES = "https://simfin.com/api/v1/companies/id/{0}/shares/aggregated"

class DataService:
    def __init__(self,service):
        self.service = service
        self.api_key = self.service.config().simfin_apikey()
        pass

    def request(self,request_type,params = None):
        if params == None:
            params = {}
        params["api-key"] = self.api_key
        self.service.debug_log("simfin request:{}".format(request_type))
        response = requests.get(request_type,params=params)
        json_data = response.json()
        if 'error' in json_data:
            raise Exception("simfin exception {} ".format(json_data['error']))
        return json_data

    def all_entities(self):
        return self.request(URL.ALL_ENTITIES)

    def company_info(self,sim_id):
        return self.request(URL.GENERAL.format(sim_id))

    def statement_list(self,sim_id):
        print("Fetch statement list {}".format(sim_id))
        return self.request(URL.STATEMENT_LIST.format(sim_id))

    def ttm_ratio(self,sim_id):
        return self.request(URL.TTM_RATIO.format(sim_id))

    def statement_std_pl(self,sim_id,fyear,ptype="TTM"):
        return self.generic_statement(
            sim_id,
            URL.STATEMENT_STD,
            'pl',
            fyear,
            ptype
        )

    def statement_org_pl(self,sim_id,fyear,ptype="TTM"):
        return self.generic_statement(
            sim_id,
            URL.STATEMENT_ORG,
            'pl',
            fyear,
            ptype
        )

    def statement_std_bs(self,sim_id,fyear,ptype="TTM"):
        return self.generic_statement(
            sim_id,
            URL.STATEMENT_STD,
            'bs',
            fyear,
            ptype
        )

    def statement_org_bs(self,sim_id,fyear,ptype="TTM"):
        return self.generic_statement(
            sim_id,
            URL.STATEMENT_ORG,
            'bs',
            fyear,
            ptype
        )

    def statement_org_cf(self,sim_id,fyear,ptype="TTM"):
        return self.generic_statement(
            sim_id,
            URL.STATEMENT_ORG,
            'cf',
            fyear,
            ptype
        )

    def statement_std_cf(self,sim_id,fyear,ptype="TTM"):
        return self.generic_statement(
            sim_id,
            URL.STATEMENT_STD,
            'cf',
            fyear,
            ptype
        )

    def generic_statement(self,sim_id,request_type,stype,fyear,ptype):
        request_type = request_type.format(sim_id)
        params = {
            'stype':stype,
            'ptype':ptype,
            'fyear':fyear
        }
        return self.request(request_type,params)

    def aggregated_shares(self,oid):
        return self.request(URL.AGGREGATED_SHARES.format(oid))

