import pandas
import functools
import model.balance_sheet
import model.income_statement
import model.cashflow 

class Company:
    def __init__(self, service, ticker, oid):
        self.ticker = ticker
        self.oid = oid
        self.service = service
        self.balance_sheet = None
        self.income_statement = None
        self.cashflow = None

    def cf(self):
        if self.cashflow == None:
            data = self.service.get_statement(self.ticker, "cf",1e-6,quarter=-1,fy=True,prefix=False)
            self.cashflow = cashflow.Cashflow(self,data)
        return self.cashflow

    def bs(self):
        if self.balance_sheet == None:
            data = self.service.get_statement(self.ticker, "bs",1e-6,quarter=4,fy=False,prefix=False)
            self.balance_sheet = balance_sheet.BalanceSheet(self,data)
        return self.balance_sheet


    def pl(self):
        if self.income_statement == None:
            data = self.service.get_statement(self.ticker, "pl",1e-6,quarter=-1,fy=True,prefix=False)
            self.income_statement = income_statement.IncomeStatement(self,data)
        return self.income_statement

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
