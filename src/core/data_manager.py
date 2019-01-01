import datetime
import requests_cache
import pickle
import os
import requests
import bs4 as bs
import data_object
import csv
import pandas_datareader
import time
import data_storage

class DataManager:
    def __init__(self,storage):
        self.storage = storage
        self.expire_after = datetime.timedelta(days=3)
        self.session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=self.expire_after)
        self.setup()
        pass

    @classmethod
    def setup(cls):
        os.environ['QUANDL_API_KEY'] = 'rWiPz485Q_iPZSujz8om'
        pass
    pass

    def fetch_SP500_tickers(self):
        response = None
        _id = self.storage.META_DATA_SP500_TICKERS
        if _id in self.storage.meta_data:
            response = self.storage.meta_data[_id]
        else:
            response = self.storage.fetch_meta_data(_id)
            if response != None:
                print(response)
                self.storage.meta_data[_id] = response
                response = response
        if response == None:
            response = self.request_SP500_tickers()
            self.storage.meta_data[_id] = response
            self.storage.insert_meta_data(_id,response)
        return response

    def parse_currency(self,value):
        return float(value.replace("$","").replace("M","e6").replace("B","e9"))
   
    def parse_int(self,value,default_value):
        result = default_value
        try:
            result = int(value)
        except:
            pass
        return result
 
    def request_company(self):
        exchanges = ["nasdaq","nyse","amex"]
        params = {
            "letter":0,
            "render":"download"
        }
        current_date = datetime.datetime.today()
        for exchange in exchanges:
            params["exchange"] = exchange
            response = requests.get("https://www.nasdaq.com/screening/companies-by-name.aspx",params=params)
            data = response.text.split("\n")
            rows = csv.reader(data)
            exchangeId = self.storage.get_map_using_value(self.storage.EXCHANGE,exchange)
            next(rows)
            for row in rows:
                if len(row) >= 7:
                    sectorId = self.storage.get_map_using_value(self.storage.SECTOR,row[5])
                    industryId = self.storage.get_map_using_value(self.storage.INDUSTRY,row[6])
                    company = None
                    try:
                        company = data_object.Company(
                            row[0],
                            row[1],
                            float(row[2]),
                            self.parse_currency(row[3]),
                            self.parse_int(row[4],0),
                            sectorId,
                            industryId,
                            exchangeId,
                            row[7],
                            current_date
                        )
                    except:
                        pass
                    if company:
                        self.storage.insert_company(company)
  
            
            #print (data)
    
    def request_SP500_tickers(self):
        response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        soup = bs.BeautifulSoup(response.text,"lxml")
        table = soup.find('table',{'class':'wikitable sortable'})
        row = table.findAll('tr')
        tickers = {}
        for row in table.findAll('tr')[1:]:
            tds = row.findAll('td')
            tickers[tds[0].text] = {"description":tds[1].text,"sector":tds[3].text,"industry":tds[4].text}
        return tickers

    def fetch_data(self,_id):
        return self.storage.fetch(_id)

    def stock_data(self,_id,start=None,end=None):
        result = None
        if end == None:
            end = datetime.datetime.today()
            pass
        if start == None:
            start = datetime.datetime.today() - datetime.timedelta(days=20*365)
            pass
        result = self.storage.fetch(_id)
        if result == None:
            _source = self.storage.get_map_using_value(self.storage.SOURCE,"yahoo")
            _type = self.storage.get_map_using_value(self.storage.TYPE,data_object.Data.type_stock)
            _description = _id
            _sector = None
            _industry = None
            tickers = self.fetch_SP500_tickers()
            _category = None
            if _id in tickers:
                ticker = tickers[_id]
                _sector = self.storage.get_map_using_value(self.storage.SECTOR,ticker["sector"])
                _industry = self.storage.get_map_using_value(self.storage.INDUSTRY,ticker["industry"])
                _description = ticker["description"]
                _category = self.storage.get_map_using_value(self.storage.CATEGORY,"SP-500")
            dataframe = pandas_datareader.data.DataReader(_id,_source.value,start=start,end=end) 
            result = data_object.Data(_id,_source,_type,_sector,_industry,_category,start,end,_description,dataframe)
            self.storage.insert(result)
            print("Sleeping for 10")
            time.sleep(10)
        return result

    def economy_data(self,_id,start=None,end=None):
        result = None
        if end == None:
            end = datetime.datetime.today()
            pass
        if start == None:
            start = datetime.datetime.today() - datetime.timedelta(days=20*365)
            pass
        result = self.storage.fetch(_id)
        if result == None:
            _source = self.storage.get_map_using_value(self.storage.SOURCE,"quandl")
            _type = self.storage.get_map_using_value(self.storage.TYPE,data_object.Data.type_economy)
            _sector = self.storage.get_map_using_value(self.storage.SECTOR,"{}".format(data_object.Data.type_economy))
            _industry = self.storage.get_map_using_value(self.storage.INDUSTRY,"{}".format(data_object.Data.type_economy))
            _description = None
            if _id in data_object.Data.econ_description:
                _description = data_object.Data.econ_description[_id]
            else:
                _description = "{0}".format(_type)
                pass
            dataframe = pandas_datareader.data.DataReader(_id,_source.value,start=start,end=end,session=self.session) 
            result = data_object.Data(_id,_source,_type,_sector,_industry,None,start,end,_description,dataframe)
            self.storage.insert(result)
        return result



