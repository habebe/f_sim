import data_simfin
import pandas
import functools
import balance_sheet
import income_statement
import cashflow 

import data_service
import model

class F:
    NoneType = type(None)
    StrType = type("")
    IntType = type(0)

    def __init__(self,config):
        self.__config = config
        self.__simfin = data_service.simfin.DataService(self)
        self.__entities = None

    def config(self):
        return self.__config

    def debug_log(self,content):
        print(content)

    def entities(self, refresh=False):
        if refresh or (type(self.__entities) == self.NoneType):
            self.__entities = self.__storage.entities()
        return self.__entities


    def match_id(self, ticker):
        es = self.entities()
        result = es.loc[es.ticker.str.match(
            ticker.strip(), na=False, case=False)]
        if result.size:
            return result
        return None

    def match_exact_id(self, ticker):
        return self.match_id("^{}$".format(ticker.strip()))

    def get_oid(self, ticker):
        oid = ticker
        if type(ticker) == self.StrType:
            ticker = self.match_exact_id(ticker)
        if type(ticker) == pandas.core.frame.DataFrame:
            oid = int(ticker.index[0])
        if type(oid) == self.IntType:
            return oid
        return None

    def get_company(self, ticker):
        oid = self.get_oid(ticker)
        company = None
        if type(oid) != self.NoneType:
            company = Company(self, ticker, oid)
        return company