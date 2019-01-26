import data_simfin
import pandas
import functools
import statement

ASSETS = lambda x:  ((x.type & BalanceSheet.ASSET_TYPE) and not (x.type & BalanceSheet.TOTAL_TYPE))
CURRENT_ASSETS = lambda x: ((x.type & BalanceSheet.CURRENT_TYPE) and (x.type & BalanceSheet.ASSET_TYPE) and not (x.type & BalanceSheet.TOTAL_TYPE))
NON_CURRENT_ASSETS = lambda x: ((x.type & BalanceSheet.NON_CURRENT_TYPE) and (x.type & BalanceSheet.ASSET_TYPE))
TOTAL_ASSETS = lambda x: ((x.type & BalanceSheet.TOTAL_TYPE) and (x.type & BalanceSheet.ASSET_TYPE))

TOTAL_LIABILITIES = lambda x: ((x.type & BalanceSheet.TOTAL_TYPE) and (x.type & BalanceSheet.LIABILITY_TYPE))
TOTAL_EQUITIES = lambda x: ((x.type & BalanceSheet.TOTAL_TYPE) and (x.type & BalanceSheet.EQUITY_TYPE))

class BalanceSheet(statement.Statement):
    ASSET_TYPE = 1
    LIABILITY_TYPE = 2
    EQUITY_TYPE = 4
    TOTAL_TYPE = 8
    CURRENT_TYPE = 16
    NON_CURRENT_TYPE = 32

    def __init__(self, company, data):
        statement.Statement.__init__(self,company,data)
     
    def description(self):
        return self.listing


    def assets(self,year=None):
        return self.apply(ASSETS,year)

    def current_assets(self,year=None):
        return self.apply(CURRENT_ASSETS,year)

    def non_current_assets(self,year=None):
        return self.apply(NON_CURRENT_ASSETS,year)

    def total_assets(self,year=None):
        return self.apply(TOTAL_ASSETS,year)

    def total_liabilities(self,year=None):
        return self.apply(TOTAL_LIABILITIES,year)

    def total_equity(self,year=None):
        return self.apply(TOTAL_EQUITIES,year)

    listing = [
        statement.StatementItem('Accounts & Notes Receivable', ASSET_TYPE | CURRENT_TYPE),
        statement.StatementItem('Accounts Payable', LIABILITY_TYPE | CURRENT_TYPE),
        statement.StatementItem('Accounts Receivable, Net', ASSET_TYPE),
        statement.StatementItem('Accrued Liabilities', LIABILITY_TYPE),
        statement.StatementItem('Accrued Taxes', LIABILITY_TYPE),
        statement.StatementItem('Accumulated Depreciation', ASSET_TYPE),
        statement.StatementItem('Additional Paid in Capital', ASSET_TYPE),
        statement.StatementItem('Assets Held-for-Sale', ASSET_TYPE),
        statement.StatementItem('Cash & Cash Equivalents', ASSET_TYPE ),
        statement.StatementItem('Cash, Cash Equivalents & Short Term Investments',ASSET_TYPE| CURRENT_TYPE),
        statement.StatementItem('Common Stock', ASSET_TYPE),
        statement.StatementItem('Current Portion of Long Term Debt', ASSET_TYPE),
        statement.StatementItem('Deferred Compensation', LIABILITY_TYPE),
        statement.StatementItem('Deferred Revenue', ASSET_TYPE),
        statement.StatementItem('Deferred Tax Assets', ASSET_TYPE),
        statement.StatementItem('Deferred Tax Liabilities', LIABILITY_TYPE),
        statement.StatementItem('Derivative & Hedging Assets', ASSET_TYPE),
        statement.StatementItem('Derivatives & Hedging', ASSET_TYPE),
        statement.StatementItem('Discontinued Operations', LIABILITY_TYPE),
        statement.StatementItem('Equity Before Minority Interest', EQUITY_TYPE),
        statement.StatementItem('Finished Goods', ASSET_TYPE),
        statement.StatementItem('Goodwill', ASSET_TYPE),
        statement.StatementItem('Income Taxes Receivable', ASSET_TYPE),
        statement.StatementItem('Intangible Assets', ASSET_TYPE),
        statement.StatementItem('Interest & Dividends Payable', LIABILITY_TYPE),
        statement.StatementItem('Inventories', ASSET_TYPE | CURRENT_TYPE),
        statement.StatementItem('Investments in Affiliates', ASSET_TYPE),
        statement.StatementItem('Long Term Borrowings', LIABILITY_TYPE),
        statement.StatementItem('Long Term Capital Leases', LIABILITY_TYPE),
        statement.StatementItem('Long Term Debt', LIABILITY_TYPE),
        statement.StatementItem('Long Term Investments', ASSET_TYPE),
        statement.StatementItem('Long Term Investments & Receivables', ASSET_TYPE),
        statement.StatementItem('Long Term Marketable Securities', ASSET_TYPE),
        statement.StatementItem('Long Term Receivables', ASSET_TYPE),
        statement.StatementItem('Minority Interest', ASSET_TYPE),
        statement.StatementItem('Miscellaneous Long Term Assets', ASSET_TYPE | CURRENT_TYPE),
        statement.StatementItem('Miscellaneous Long Term Liabilities', ASSET_TYPE),
        statement.StatementItem('Miscellaneous Short Term Assets', ASSET_TYPE ),
        statement.StatementItem('Miscellaneous Short Term Liabilities', LIABILITY_TYPE),
        statement.StatementItem('Notes Receivable, Net', ASSET_TYPE),
        statement.StatementItem('Other Equity', ASSET_TYPE),
        statement.StatementItem('Other Intangible Assets', ASSET_TYPE),
        statement.StatementItem('Other Inventory', LIABILITY_TYPE),
        statement.StatementItem('Other Long Term Assets', ASSET_TYPE | CURRENT_TYPE),
        statement.StatementItem('Other Long Term Liabilities', LIABILITY_TYPE),
        statement.StatementItem('Other Payables & Accruals', LIABILITY_TYPE),
        statement.StatementItem('Other Post-Retirement Benefits', LIABILITY_TYPE),
        statement.StatementItem('Other Share Capital', ASSET_TYPE | CURRENT_TYPE),
        statement.StatementItem('Other Short Term Assets', ASSET_TYPE ),
        statement.StatementItem('Other Short Term Liabilities', LIABILITY_TYPE),
        statement.StatementItem('Payables & Accruals', ASSET_TYPE),
        statement.StatementItem('Pension Liabilities', LIABILITY_TYPE),
        statement.StatementItem('Pensions', LIABILITY_TYPE),
        statement.StatementItem('Preferred Equity', EQUITY_TYPE),
        statement.StatementItem('Prepaid Expense', LIABILITY_TYPE),
        statement.StatementItem('Prepaid Expenses', LIABILITY_TYPE),
        statement.StatementItem('Prepaid Pension Costs', LIABILITY_TYPE),
        statement.StatementItem('Property, Plant & Equipment', ASSET_TYPE | NON_CURRENT_TYPE),
        statement.StatementItem('Property, Plant & Equipment, Net', ASSET_TYPE | NON_CURRENT_TYPE),
        statement.StatementItem('Raw Materials', ASSET_TYPE | CURRENT_TYPE),
        statement.StatementItem('Retained Earnings', EQUITY_TYPE),
        statement.StatementItem('Share Capital & Additional Paid-In Capital',ASSET_TYPE),
        statement.StatementItem('Short Term Borrowings', LIABILITY_TYPE),
        statement.StatementItem('Short Term Capital Leases', LIABILITY_TYPE),
        statement.StatementItem('Short Term Debt', LIABILITY_TYPE),
        statement.StatementItem('Short Term Investments', ASSET_TYPE),
        statement.StatementItem('Total Assets', ASSET_TYPE | TOTAL_TYPE),
        statement.StatementItem('Total Current Assets',  ASSET_TYPE | TOTAL_TYPE | CURRENT_TYPE),
        statement.StatementItem('Total Current Liabilities', LIABILITY_TYPE | TOTAL_TYPE | CURRENT_TYPE),
        statement.StatementItem('Total Equity', TOTAL_TYPE | EQUITY_TYPE),
        statement.StatementItem('Total Liabilities', LIABILITY_TYPE | TOTAL_TYPE),
        statement.StatementItem('Total Liabilities & Equity', TOTAL_TYPE ),
        statement.StatementItem('Total Noncurrent Assets', ASSET_TYPE | TOTAL_TYPE | NON_CURRENT_TYPE),
        statement.StatementItem('Total Noncurrent Liabilities', LIABILITY_TYPE | TOTAL_TYPE | NON_CURRENT_TYPE),
        statement.StatementItem('Treasury Stock', ASSET_TYPE),
        statement.StatementItem('Unbilled Revenues', ASSET_TYPE),
        statement.StatementItem('Work In Process', ASSET_TYPE)
    ]
