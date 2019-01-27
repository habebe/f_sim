import pandas
import functools
import model.statement

ASSETS = lambda x:  ((x.type & BalanceSheet.ASSET_TYPE) and not (x.type & BalanceSheet.TOTAL_TYPE))
CURRENT_ASSETS = lambda x: ((x.type & BalanceSheet.CURRENT_TYPE) and (x.type & BalanceSheet.ASSET_TYPE) and not (x.type & BalanceSheet.TOTAL_TYPE))
NON_CURRENT_ASSETS = lambda x: ((x.type & BalanceSheet.NON_CURRENT_TYPE) and (x.type & BalanceSheet.ASSET_TYPE))
TOTAL_ASSETS = lambda x: ((x.type & BalanceSheet.TOTAL_TYPE) and (x.type & BalanceSheet.ASSET_TYPE))

TOTAL_LIABILITIES = lambda x: ((x.type & BalanceSheet.TOTAL_TYPE) and (x.type & BalanceSheet.LIABILITY_TYPE))
TOTAL_EQUITIES = lambda x: ((x.type & BalanceSheet.TOTAL_TYPE) and (x.type & BalanceSheet.EQUITY_TYPE))

class BalanceSheet(model.statement.Statement):
    ASSET_TYPE = 1
    LIABILITY_TYPE = 2
    EQUITY_TYPE = 4
    TOTAL_TYPE = 8
    CURRENT_TYPE = 16
    NON_CURRENT_TYPE = 32

    def __init__(self, company, data):
        model.statement.Statement.__init__(self,company,data)
     
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
        model.statement.StatementItem('Accounts & Notes Receivable', ASSET_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Accounts Payable', LIABILITY_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Accounts Receivable, Net', ASSET_TYPE),
        model.statement.StatementItem('Accrued Liabilities', LIABILITY_TYPE),
        model.statement.StatementItem('Accrued Taxes', LIABILITY_TYPE),
        model.statement.StatementItem('Accumulated Depreciation', ASSET_TYPE),
        model.statement.StatementItem('Additional Paid in Capital', ASSET_TYPE),
        model.statement.StatementItem('Assets Held-for-Sale', ASSET_TYPE),
        model.statement.StatementItem('Cash & Cash Equivalents', ASSET_TYPE ),
        model.statement.StatementItem('Cash, Cash Equivalents & Short Term Investments',ASSET_TYPE| CURRENT_TYPE),
        model.statement.StatementItem('Common Stock', ASSET_TYPE),
        model.statement.StatementItem('Current Portion of Long Term Debt', ASSET_TYPE),
        model.statement.StatementItem('Deferred Compensation', LIABILITY_TYPE),
        model.statement.StatementItem('Deferred Revenue', ASSET_TYPE),
        model.statement.StatementItem('Deferred Tax Assets', ASSET_TYPE),
        model.statement.StatementItem('Deferred Tax Liabilities', LIABILITY_TYPE),
        model.statement.StatementItem('Derivative & Hedging Assets', ASSET_TYPE),
        model.statement.StatementItem('Derivatives & Hedging', ASSET_TYPE),
        model.statement.StatementItem('Discontinued Operations', LIABILITY_TYPE),
        model.statement.StatementItem('Equity Before Minority Interest', EQUITY_TYPE),
        model.statement.StatementItem('Finished Goods', ASSET_TYPE),
        model.statement.StatementItem('Goodwill', ASSET_TYPE),
        model.statement.StatementItem('Income Taxes Receivable', ASSET_TYPE),
        model.statement.StatementItem('Intangible Assets', ASSET_TYPE),
        model.statement.StatementItem('Interest & Dividends Payable', LIABILITY_TYPE),
        model.statement.StatementItem('Inventories', ASSET_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Investments in Affiliates', ASSET_TYPE),
        model.statement.StatementItem('Long Term Borrowings', LIABILITY_TYPE),
        model.statement.StatementItem('Long Term Capital Leases', LIABILITY_TYPE),
        model.statement.StatementItem('Long Term Debt', LIABILITY_TYPE),
        model.statement.StatementItem('Long Term Investments', ASSET_TYPE),
        model.statement.StatementItem('Long Term Investments & Receivables', ASSET_TYPE),
        model.statement.StatementItem('Long Term Marketable Securities', ASSET_TYPE),
        model.statement.StatementItem('Long Term Receivables', ASSET_TYPE),
        model.statement.StatementItem('Minority Interest', ASSET_TYPE),
        model.statement.StatementItem('Miscellaneous Long Term Assets', ASSET_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Miscellaneous Long Term Liabilities', ASSET_TYPE),
        model.statement.StatementItem('Miscellaneous Short Term Assets', ASSET_TYPE ),
        model.statement.StatementItem('Miscellaneous Short Term Liabilities', LIABILITY_TYPE),
        model.statement.StatementItem('Notes Receivable, Net', ASSET_TYPE),
        model.statement.StatementItem('Other Equity', ASSET_TYPE),
        model.statement.StatementItem('Other Intangible Assets', ASSET_TYPE),
        model.statement.StatementItem('Other Inventory', LIABILITY_TYPE),
        model.statement.StatementItem('Other Long Term Assets', ASSET_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Other Long Term Liabilities', LIABILITY_TYPE),
        model.statement.StatementItem('Other Payables & Accruals', LIABILITY_TYPE),
        model.statement.StatementItem('Other Post-Retirement Benefits', LIABILITY_TYPE),
        model.statement.StatementItem('Other Share Capital', ASSET_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Other Short Term Assets', ASSET_TYPE ),
        model.statement.StatementItem('Other Short Term Liabilities', LIABILITY_TYPE),
        model.statement.StatementItem('Payables & Accruals', ASSET_TYPE),
        model.statement.StatementItem('Pension Liabilities', LIABILITY_TYPE),
        model.statement.StatementItem('Pensions', LIABILITY_TYPE),
        model.statement.StatementItem('Preferred Equity', EQUITY_TYPE),
        model.statement.StatementItem('Prepaid Expense', LIABILITY_TYPE),
        model.statement.StatementItem('Prepaid Expenses', LIABILITY_TYPE),
        model.statement.StatementItem('Prepaid Pension Costs', LIABILITY_TYPE),
        model.statement.StatementItem('Property, Plant & Equipment', ASSET_TYPE | NON_CURRENT_TYPE),
        model.statement.StatementItem('Property, Plant & Equipment, Net', ASSET_TYPE | NON_CURRENT_TYPE),
        model.statement.StatementItem('Raw Materials', ASSET_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Retained Earnings', EQUITY_TYPE),
        model.statement.StatementItem('Share Capital & Additional Paid-In Capital',ASSET_TYPE),
        model.statement.StatementItem('Short Term Borrowings', LIABILITY_TYPE),
        model.statement.StatementItem('Short Term Capital Leases', LIABILITY_TYPE),
        model.statement.StatementItem('Short Term Debt', LIABILITY_TYPE),
        model.statement.StatementItem('Short Term Investments', ASSET_TYPE),
        model.statement.StatementItem('Total Assets', ASSET_TYPE | TOTAL_TYPE),
        model.statement.StatementItem('Total Current Assets',  ASSET_TYPE | TOTAL_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Total Current Liabilities', LIABILITY_TYPE | TOTAL_TYPE | CURRENT_TYPE),
        model.statement.StatementItem('Total Equity', TOTAL_TYPE | EQUITY_TYPE),
        model.statement.StatementItem('Total Liabilities', LIABILITY_TYPE | TOTAL_TYPE),
        model.statement.StatementItem('Total Liabilities & Equity', TOTAL_TYPE ),
        model.statement.StatementItem('Total Noncurrent Assets', ASSET_TYPE | TOTAL_TYPE | NON_CURRENT_TYPE),
        model.statement.StatementItem('Total Noncurrent Liabilities', LIABILITY_TYPE | TOTAL_TYPE | NON_CURRENT_TYPE),
        model.statement.StatementItem('Treasury Stock', ASSET_TYPE),
        model.statement.StatementItem('Unbilled Revenues', ASSET_TYPE),
        model.statement.StatementItem('Work In Process', ASSET_TYPE)
    ]
