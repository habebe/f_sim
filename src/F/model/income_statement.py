import pandas
import functools
from model import *

REVENUE = lambda x:  (x.type & IncomeStatement.REVENUE_TYPE)
INCOME = lambda x:  (x.type & IncomeStatement.INCOME_TYPE)
class IncomeStatement(statement.Statement):
    MISC_TYPE = 1
    REVENUE_TYPE = 2
    OPERATING_EXPENSES_TYPE = 4
    INCOME_TYPE = 8

    def __init__(self, company, data):
        statement.Statement.__init__(self,company,data)
     
    def description(self):
        return self.listing

    def revenue(self,year=None):
        result = self.apply(REVENUE,year)
        gross_profit = result[["Gross Profit"]].rename(columns={"Gross Profit":"Gross Margin(%)"})
        revenue = result[["Revenue"]].rename(columns={"Revenue":"Gross Margin(%)"})
        revenue = 100*gross_profit/revenue
        result = result.join(revenue)
        return result

    def income(self,year=None):
        result = self.apply(INCOME,year)
        return result

    listing = [
        statement.StatementItem('Abnormal Derivatives', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Abnormal Gains (Losses)', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Acquired In-Process R&D', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Asset Write-Down', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Cost of Financing Revenue', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Cost of Goods & Services', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Cost of Other Revenue', MISC_TYPE),
        statement.StatementItem('Cost of revenue', REVENUE_TYPE),
        statement.StatementItem('Current Income Tax', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Deferred Income Tax', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Depreciation & Amortization', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Discontinued Operations', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Disposal of Assets', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Early extinguishment of Debt', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Financing Revenue', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Foreign Exchange Gain (Loss)', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('General & Administrative', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Gross Profit', REVENUE_TYPE),
        statement.StatementItem('Impairment of Goodwill & Intangibles',
                           OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Income (Loss) Including Minority Interest',
                           OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Income (Loss) from Affiliates', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Income (Loss) from Affiliates, net of taxes',
                           OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Income (Loss) from Continuing Operations',
                           OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Income Tax (Expense) Benefit, net', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Insurance Settlement', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Interest Expense', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Interest Expense, net', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Interest Income', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Legal Settlement', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Merger / Acquisition Expense', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Minority Interest', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Net Extraordinary Gains (Losses)', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Net Income', INCOME_TYPE),
        statement.StatementItem('Net Income Available to Common Shareholders',
                           INCOME_TYPE),
        statement.StatementItem('Non-Operating Income (Loss)', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Operating Expenses', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Operating Income (Loss)', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Other Abnormal Items', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Other Adjustments', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Other Investment Income (Loss)', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Other Non-Operating Income (Loss)', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Other Operating Expense', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Other Operating Income', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Other Revenue', MISC_TYPE),
        statement.StatementItem('Preferred Dividends', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Pretax Income (Loss)', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Pretax Income (Loss), Adjusted', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Provision For Doubtful Accounts', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Research & Development', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Restructuring Charges', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Revenue', REVENUE_TYPE),
        statement.StatementItem('Sale of Business', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Sale of and Unrealized Investments', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Sales & Services Revenue', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Selling & Marketing', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Selling, General & Administrative', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('Tax Allowance/Credit', OPERATING_EXPENSES_TYPE),
        statement.StatementItem('XO & Accounting Charges & Other', OPERATING_EXPENSES_TYPE)
    ]
