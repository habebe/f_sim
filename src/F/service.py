import pandas
import functools
import data_service.simfin
import data_service.misc
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
        self.__misc = data_service.misc.DataService(self)
        self.__entities = None

    def config(self):
        return self.__config

    def simfin(self):
        return self.__simfin

    def misc(self):
        return self.__misc

    def storage(self):
        return self.__storage

    def debug_log(self,content):
        print(content)

    def earning_report_dates(self,refresh=False,release_date=None,append_simid=True):
        result = self.__misc.earning_report_dates(refresh)
        if release_date != None:
            result = result.loc[result.release_date == release_date]
        if append_simid == True:
            simids = []
            for row in result.iterrows():
                ticker = row[1].loc['ticker']
                simids.append(self.get_oid(ticker))
            result.insert(0,"simid",simids)
            result = result.loc[result.simid > 0]
        return result


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
            oid = ticker["simId"]
            oid = oid[oid.index[0]]
            return oid
        if type(oid) == int:
            return oid
        if type(oid) == float:
            return int(oid)
        return None

    def get_company(self, ticker):
        oid = self.get_oid(ticker)
        company = None
        if type(oid) != self.NoneType:
            company = model.company.Company(self, ticker, oid)
        return company