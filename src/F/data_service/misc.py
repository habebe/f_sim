
import requests
import pandas
from importlib import reload
import mysql.connector
import datetime
import json
import pickle
import data_service.base_dataservice as base_dataservice
import datetime
import bs4 as bs

class URL:
    SEEKING_ALPHA = "https://seekingalpha.com/earnings/earnings-calendar"
 
class DataService(base_dataservice.BaseDataService):
    TABLE_EARNINGS_REPORT = "{0}.earning_reports"
    KEY_EARNINGS_REPORT = 0

    def __init__(self,service):
        base_dataservice.BaseDataService.__init__(self,service.config().misc_storage())
        self.__service = service
        self.__table_name_earnings_report = None
        self.__earning_report_dates = None
        
        self.__api_key = self.__service.config().simfin_apikey()
        self.add_field(self.table_name_earnings_report(),base_dataservice.FieldDescription("id","INTEGER PRIMARY KEY"))
        self.add_field(self.table_name_earnings_report(),base_dataservice.FieldDescription("date","DATE"))
        self.add_field(self.table_name_earnings_report(),base_dataservice.FieldDescription("data","LONGBLOB"))
        self.__service.storage().initialize_datasource(self)
        pass

    def table_name_earnings_report(self):
        if self.__table_name_earnings_report == None:
            self.__table_name_earnings_report =  self.TABLE_EARNINGS_REPORT.format(self.__service.config().misc_storage())
        return self.__table_name_earnings_report


    def __request_earnings_report_dates(self):
        self.__service.debug_log("Fetching Earning Report Dates")
        response = requests.get(URL.SEEKING_ALPHA)
        soup = bs.BeautifulSoup(response.text,"lxml")
        table = soup.find('table',{'class':'earningsTable'})
        trs = table.findAll('tr')
        result = []
        for tr in trs[1:]:
            result.append({
                "ticker":tr.get_attribute_list('data-ticker')[0],
                "name":tr.find('span',{'class':'ticker-name'}).text,
                "release_time":tr.find('span',{'class':'release-time'}).text,
                "release_date":tr.find('span',{'class':'release-date'}).text
            })
        return json.dumps(result)

    def earning_report_dates(self,refresh=False):
        if (refresh == True):
            response = self.__request_earnings_report_dates()
            data = {"date":datetime.datetime.now(),'data':response,'id':self.KEY_EARNINGS_REPORT}
            self.__service.storage().persist(self,self.table_name_earnings_report(),data)
            self.__earning_report_dates = json.loads(response)
            self.__earning_report_dates = pandas.DataFrame(self.__earning_report_dates)
            self.__earning_report_dates['release_date'] = pandas.to_datetime(self.__earning_report_dates['release_date'])
        elif(type(self.__earning_report_dates) == type(None)):
            response = self.__service.storage().query(self.table_name_earnings_report(),select="data",where="id = {}".format(self.KEY_EARNINGS_REPORT),limit=1)
            if (response != None) and (len(response) > 0):
                self.__earning_report_dates = json.loads(response[0][0])   
                self.__earning_report_dates = pandas.DataFrame(self.__earning_report_dates)
                self.__earning_report_dates['release_date'] = pandas.to_datetime(self.__earning_report_dates["release_date"])
            else:
                response = self.__request_earnings_report_dates()
                data = {"date":datetime.datetime.now(),'data':response,'id':self.KEY_EARNINGS_REPORT}
                self.__service.storage().persist(self,self.table_name_earnings_report(),data)
                self.__earning_report_dates = json.loads(response)
                self.__earning_report_dates = pandas.DataFrame(self.__earning_report_dates)
                self.__earning_report_dates['release_date'] = pandas.to_datetime(self.__earning_report_dates['release_date'])
        return self.__earning_report_dates