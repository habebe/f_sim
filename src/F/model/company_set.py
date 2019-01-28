import model.company
import pandas

class CompanySet:
    def __init__(self,service,earning_report):
        self.__service = service
        self.__earning_report = earning_report
        self.__companies = None
        self.__ratios = None
        pass

    def earning_report(self):
        return self.__earning_report

    def companies(self):
        if type(self.__companies) == type(None):
            self.__companies = []
            for row in self.__earning_report.iterrows():
                company = self.__service.get_company(row[1].loc['simid'])
                self.__companies.append(company)
        return self.__companies

    def ratios(self,brief=True):
        if type(self.__ratios) == type(None):
            for company in self.companies():
                r = company.ratios().transpose()
                d = r.iloc[0].tolist()
                if type(self.__ratios) == type(None):
                    self.__ratios = pandas.DataFrame(columns=r.columns)
                    self.__ratios.index.names = ["ticker"]
                self.__ratios.loc[company.ticker()] = d
            if brief:
                self.__ratios = self.__ratios[[
                    'Market Capitalisation','Net Income (common shareholders)','Total Debt', 'Free Cash Flow',
                    'Return on Equity', 'Return on Assets', 'Free Cash Flow to Net Income',
                    'Current Ratio', 'Liabilities to Equity Ratio', 'Debt to Assets Ratio',
                    'Earnings per Share, Basic', 'Earnings per Share, Diluted',
                    'Sales per Share', 'Book Value per Share', 'Free Cash Flow per Share',
                    'Dividends per Share', 'Price to Earnings Ratio',
                    'Price to Sales Ratio', 'Price to Book Value',
                    'Price to Free Cash Flow',
                    'EV/EBITDA', 'EV/Sales', 'EV/FCF', 'Book to Market Value',
                    'Operating Income/EV', 'Pietroski F-Score']]
        return self.__ratios


