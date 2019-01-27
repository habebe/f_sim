import pandas
import functools
import data_service.simfin
import data_service.storage
import model.company

class Service:
    NoneType = type(None)
    StrType = type("")
    IntType = type(0)

    def __init__(self,config):
        self.__config = config
        self.__storage = data_service.storage.Storage(self)
        self.__simfin = data_service.simfin.DataService(self)
        self.__entities = None

    def config(self):
        return self.__config

    def storage(self):
        return self.__storage

    def debug_log(self,content):
        print(content)

    def entities(self, refresh=False):
        return self.__simfin.entities(refresh)

    def match_id(self, ticker):
        es = self.__simfin.entities(False)
        result = es.loc[es.ticker.str.match(
            ticker.strip(), na=False, case=False)]
        if result.size:
            return result
        return None

    def match_exact_id(self, ticker):
        return self.match_id("^{}$".format(ticker.strip()))

    def get_oid(self, ticker):
        oid = ticker
        if type(ticker) == str:
            ticker = self.match_exact_id(ticker)
        if type(ticker) == pandas.core.frame.DataFrame:
            oid = int(ticker.index[0])
        if type(oid) == int:
            return oid
        return None

    def get_company(self, ticker):
        oid = self.get_oid(ticker)
        company = None
        if type(oid) != self.NoneType:
            company = model.company.Company(self, ticker, oid)
        return company