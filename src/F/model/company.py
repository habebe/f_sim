import pandas
import functools
import model.balance_sheet
import model.income_statement
import model.cashflow 

class Company:
    def __init__(self, service, ticker, oid):
        self.__ticker = ticker
        self.__oid = oid
        self.__service = service
        self.__balance_sheet = None
        self.__income_statement = None
        self.__cashflow = None
        self.__info = None
        self.__ratios = None

    def info(self):
        if type(self.__info) == type(None):
            self.__info = self.__service.simfin().company_data(self.__oid)
        return self.__info

    def ratios(self):
        if type(self.__ratios) == type(None):
            self.__ratios = self.__service.simfin().ratios(self.__oid)[["indicatorName","value"]]
            self.__ratios.set_index("indicatorName",inplace=True)
        return self.__ratios

    def statement_list(self,stmt_type,not_calculated_only=True,fy=True,quarter=-1):
        listing = self.__service.simfin().statement_list(self.__oid,stmt_type)
        if type(listing) != type(None):
            if not_calculated_only == True:
                listing = listing.loc[listing.calculated == False]
            if fy == True:
                listing = listing.loc[listing.period.str.match("FY", na=False)]
            elif quarter == 0:
                quarter = "^Q"
                listing = listing.loc[listing.period.str.match(quarter, na=False)]
            elif quarter != -1:
                quarter = "Q{}".format(quarter)
                listing = listing.loc[listing.period.str.match(quarter, na=False)]
        return listing

    def __statment(self,stmt_lists,stype,factor,prefix):
        stmt_lists = stmt_lists[::-1]
        data_frame = None
        for stmt_list in stmt_lists.iterrows():
            fyear = stmt_list[1].fyear
            ptype = stmt_list[1].period
            values = self.__service.simfin().statement(self.__oid,stype,ptype,fyear,refresh=False,raw=True)
            m = {}
            values = values["values"]
            for i in values:
                _n = i["standardisedName"]
                _v = i["valueChosen"]
                if _v == None:
                    _v = 0
                else:
                    _v = float(_v)*factor
                m[_n] = _v
            results = None
            if prefix:
                results = {"{0}.{1}".format(ptype,fyear):m}    
            else:
                results = {int(fyear):m}  
            df = pandas.DataFrame(results)
            if type(data_frame) == type(None):
                data_frame = df
            else:
                data_frame = data_frame.join(df)
        data_frame = data_frame.transpose()
        return data_frame

    def pl(self):
        if self.__income_statement == None:
            stmt_lists = self.statement_list("pl",True,True,-1)
            data = self.__statment(stmt_lists,"pl",1e-6,False)
            self.__income_statement = model.income_statement.IncomeStatement(self,data)
        return self.__income_statement


    def cf(self):
        if self.__cashflow == None:
            stmt_lists = self.statement_list("cf",True,True,-1)
            data = self.__statment(stmt_lists,"cf",1e-6,False)
            self.__cashflow = model.cashflow.Cashflow(self,data)
        return self.__cashflow

    def bs(self):
        if self.__balance_sheet == None:
            stmt_lists = self.statement_list("bs",True,False,4)
            data = self.__statment(stmt_lists,"bs",1e-6,False)
            self.__balance_sheet = model.cashflow.Cashflow(self,data)
        return self.__balance_sheet

    def averaged(self,data,name):
        previous = None
        data_frame = pandas.DataFrame(columns=[name])
        for i in data.iterrows():
            value = i[1][0]
            if previous == None:
                current = value
            else:
                current = (value+previous)/2
            previous = value
            data_frame.loc[i[0]] = [current]
        return data_frame

    def fcf(self,year=None):
        cf = self.cf().all(year)
        return cf[["Cash from Operating Activities"]].rename(columns={"Cash from Operating Activities":"FCF"}) + cf[["Purchase of Fixed Assets"]].rename(columns={"Purchase of Fixed Assets":"FCF"})

    def moat(self,year=None):
        fcf = self.fcf(year)
        pl = self.pl().all(year)
        bs = self.bs().all(year)
        revenue = pl[["Revenue"]]
        averaged = self.averaged(bs[["Total Assets"]],"Total Assets")
        
        ratio = 100 * fcf.rename(columns={"FCF":"FCF/Revenue"}) / revenue.rename(columns={"Revenue":"FCF/Revenue"})
        roe = 100 * pl[["Net Income"]].rename(columns={"Net Income":"ROE"}) / bs[["Total Equity"]].rename(columns={"Total Equity":"ROE"}) 
        roa = 100 * pl[["Net Income"]].rename(columns={"Net Income":"ROA"}) / averaged.rename(columns={"Total Assets":"ROA"}) 
        return revenue.join(fcf).join(ratio).join(roe).join(roa)


    def metrics(self,year=None):
        pl = self.pl().all(year)
        bs = self.bs().all(year)
        averaged = self.averaged(bs[["Total Assets"]],"Total Assets")
        averaged_inventory = self.averaged(bs[["Inventories"]],"Inventories")
        roe = 100 * pl[["Net Income"]].rename(columns={"Net Income":"ROE"}) / bs[["Total Equity"]].rename(columns={"Total Equity":"ROE"}) 
        roa = 100 * pl[["Net Income"]].rename(columns={"Net Income":"ROA"}) / averaged.rename(columns={"Total Assets":"ROA"}) 
        margin = 100 * pl[["Net Income"]].rename(columns={"Net Income":"Net Margin"}) / pl[["Revenue"]].rename(columns={"Revenue":"Net Margin"}) 
        asset_turn_over = 100 * pl[["Revenue"]].rename(columns={"Revenue":"Asset Turnover"}) / averaged.rename(columns={"Total Assets":"Asset Turnover"}) 
        
        cog = pl[["Cost of revenue"]].abs()
        inventory_turn_over = cog.rename(columns={"Cost of revenue":"Inventory Turnover"}) / averaged_inventory.rename(columns={"Inventories":"Inventory Turnover"}) 

        delta_R = pandas.DataFrame(pl["Revenue"].diff()).rename(columns={"Revenue":"Diff(Revenue)"})
        delta_AR = pandas.DataFrame(bs["Accounts Receivable, Net"].diff()).rename(columns={"Accounts Receivable, Net":"Diff(Receivable)"})
        return roe.join(roa).join(margin).join(asset_turn_over).join(inventory_turn_over).join(delta_R).join(delta_AR)


    def ratio(self,data,revenue,new_name=None,reference_name="Revenue"):
        name = data.columns[0]
        if new_name == None:
            new_name = "{}".format(name)
        return 100 * data.rename(columns={name:new_name}) .abs()/revenue.rename(columns={reference_name:new_name}) 
      

    def pl_ratio(self,year=None,tolerance=0,reference="Revenue"):
        pl = self.pl().all(year)
        reference_value = pl[[reference]]
        result_set = None
        result_map = {}
        for column in pl.columns:
            result = self.ratio(pl[[column]],reference_value,reference_name=reference)
            sum = result.sum()[0]
            if sum > tolerance:
                if sum in result_map:
                    result_map[sum].append(result)
                else:
                    result_map[sum] = [result]
                    pass
                pass
            pass
        keys = list(result_map.keys())
        keys.sort(reverse=True)
        for i in keys:
            l = result_map[i]
            for j in l:
                if type(result_set) == type(None):
                    result_set = j
                else:
                    result_set = result_set.join(j)
        return result_set

    def pl_ratio_avg(self,year=None,tolerance=0,reference="Revenue"):
        result = self.pl_ratio(year,tolerance,reference)
        size = result.shape[0]
        return result.sum()/size



    def income_metrics(self,year=None):
        pl = self.pl().all(year)
        revenue = pl[["Revenue"]]
        
        r = self.ratio(pl[["Revenue"]],revenue)
        cor = self.ratio(pl[["Cost of revenue"]],revenue)
        gross_profit = self.ratio(pl[["Gross Profit"]],revenue)
        rnd = self.ratio(pl[["Research & Development"]],revenue,"RnD")
        sga = self.ratio(pl[["Selling, General & Administrative"]],revenue,"SGA")
        net_income = self.ratio(pl[["Net Income"]],revenue)

        opi = self.ratio(pl[["Operating Income (Loss)"]],revenue,"Operating Income")
        ope = self.ratio(pl[['Operating Expenses']],revenue,"Operating Expenses")
        tax = self.ratio(pl[['Income Tax (Expense) Benefit, net']],revenue)
        
        return r.join(cor).join(gross_profit).join(rnd).join(sga).join(ope).join(opi).join(tax).join(net_income)

    def apply_growth(self,data):
        previous = None
        new_data = pandas.DataFrame(columns=["Growth({0})".format(data.columns[0])])
        for i in data.iterrows():
            if previous == None:
                previous = i[1][0]
            else:
                current = i[1][0]
                result = (100.0*(current - previous )) / previous
                new_data.loc[i[0]] = [result]
                previous = current
        return new_data

    def divide(self,top,bottom,name,factor=1):
        return factor*top.rename(columns={top.columns[0]:name}) / bottom.rename(columns={bottom.columns[0]:name})

    def multiply(self,top,bottom,name,factor=1):
        return factor*top.rename(columns={top.columns[0]:name}) * bottom.rename(columns={bottom.columns[0]:name})

    def add(self,top,bottom,name):
        return top.rename(columns={top.columns[0]:name}) + bottom.rename(columns={bottom.columns[0]:name})

    def subtract(self,top,bottom,name):
        return top.rename(columns={top.columns[0]:name}) - bottom.rename(columns={bottom.columns[0]:name})

    def growth(self,year=None):
        pl = self.pl().all(year)
        revenue = 100*pl[["Revenue"]].diff() / pl[["Revenue"]]
        revenue = revenue.rename(columns={"Revenue":"Diff(Revenue)"})
        net_income = pl[["Net Income"]].diff() / pl[["Net Income"]]
        net_income = 100*net_income.rename(columns={"Net Income":"Diff(Net Income)"})
        return self.apply_growth(pl[["Revenue"]]).join(self.apply_growth(pl[["Net Income"]]))

    def profit(self,year=None):
        pl = self.pl().all(year)
        bs = self.bs().all(year)
        averaged = self.averaged(bs[["Total Assets"]],"Total Assets")
        net_margin = self.divide(pl[["Net Income"]],pl[["Revenue"]],"Net Margin",1)
        asset_turn_over = self.divide(pl[["Revenue"]],averaged,"Asset Turnover",1)
        roa = self.multiply(net_margin,asset_turn_over,"ROA",factor=1/(1))
        leverage = self.divide(bs[["Total Assets"]],bs[["Total Equity"]],"Financial Leverage",1)
        roe = self.multiply(leverage,roa,"ROE",factor=1/(1))
        fcf = self.fcf(year)
        return net_margin.join(asset_turn_over).join(roa).join(leverage).join(roe).join(fcf)
        
    def operating_assets(self,year=None):
        bs = self.bs().all(year)
        ar = bs[['Accounts Receivable, Net']]
        inv = bs[['Inventories']]
        rec = bs[['Property, Plant & Equipment, Net']]
        return self.add(self.add(ar,inv,"operating assets"),rec,"operating assets")
