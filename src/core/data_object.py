class KeyValue:
    def __init__(self,_id,_value,_type):
        self.id = _id
        self.value = _value
        self.type = _type
        pass
    
    def __repr__(self):
        return "KeyValue({0})={1}".format(self.id,self.value)

class Data:
    type_economy = "economy"
    type_stock = "stock"
    econ_description = {
            "FRED/NROUST":"Natural Rate of Unemployment (Short-Term)",
            "FRED/GDPPOT":"Real Potential Gross Domestic Product",
            "FRED/NGDPPOT":"Nominal Potential Gross Domestic Product",
            "FRED/NROU":"Natural Rate of Unemployment (Long-Term)",
            "FRED/UNRATEMD":"FOMC Summary of Economic Projections for the Civilian Unemployment Rate, Median",
            "FRED/GDPC1MD":"FOMC Summary of Economic Projections for the Growth Rate of Real Gross Domestic Product, Median",
            "FRED/PCECTPIMD":"FOMC Summary of Economic Projections for the Personal Consumption Expenditures Inflation Rate, Median",
            "FRED/JCXFEMD":"FOMC Summary of Economic Projections for the Personal Consumption Expenditures less Food and Energy Inflation Rate, Median",
            "FRED/FEDTARRL":"FOMC Summary of Economic Projections for the Fed Funds Rate, Range, Low",
            "FRED/FEDTARRM":"FOMC Summary of Economic Projections for the Fed Funds Rate, Range, Midpoint"
        }
        
    def __init__(self,_id,_source,_type,_sector,_industry,_category,_start,_end,_description,_data):
        self.id = _id
        self.source = _source
        self.type = _type
        self.sector = _sector
        self.industry = _industry
        self.category = _category
        self.start = _start
        self.end = _end
        self.description = _description
        self.data_frame = _data
        pass

    def is_stock(self):
        return self.type.value == Data.type_stock

    def __repr__(self):
        return "id:{0}\nsource:{1}\ntype:{2}\nsector:{3}\nindustry:{8}\nstart:{4}\nend:{5}\ndescription:{6}\ndata:{7}".format(
            self.id,
            self.source,
            self.type,
            self.sector,
            self.start,
            self.end,
            self.description,
            self.data_frame.describe(),
            self.industry
        )
    pass


class Company:
    def __init__(self,_id,_name,_lastsale,_marketCap,_ipoyear,_sector,_industry,_exchange,_summary,_date):
        self.id = _id
        self.name = _name
        self.lastsale = _lastsale
        self.marketcap = _marketCap
        self.ipoyear = _ipoyear
        self.sector = _sector
        self.industry = _industry
        self.exchange = _exchange
        self.summary = _summary
        self.date = _date
        pass
    
    def __repr__(self):
        return "id:{0}\nname:{1}\nlastSale:{2}\nMarketCap:{3}\nIPO-year:{4}\nsector:{5}\nindustry:{6}\nexchange:{7}\ndate:{8}".format(
            self.id,
            self.name,
            self.lastsale,
            self.marketcap,
            self.ipoyear,
            self.sector,
            self.industry,
            self.exchange,
            self.date
        )
    pass