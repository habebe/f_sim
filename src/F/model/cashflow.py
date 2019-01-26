import pandas
import functools
from model import *


class Cashflow(statement.Statement):
    OPERATING_TYPE = 1
    INVESTING_TYPE = 2
    FINANCING_TYPE = 4
    TOTAL_TYPE = 8

    def __init__(self, company, data):
        statement.Statement.__init__(self, company, data)

    def description(self):
        return self.listing

    listing = [
        statement.StatementItem('(Increase) Decrease in Accounts Receivable',
                     OPERATING_TYPE),
        statement.StatementItem('(Increase) Decrease in Inventories', OPERATING_TYPE),
        statement.StatementItem('Acquisition of Fixed Assets & Intangibles',
                     OPERATING_TYPE),
        statement.StatementItem('Acquisition of Intangible Assets', OPERATING_TYPE),
        statement.StatementItem('Cash From (Repayment of) Debt', OPERATING_TYPE),
        statement.StatementItem('Cash From (Repayment of) Long Term Debt, net',
                     OPERATING_TYPE),
        statement.StatementItem('Cash From (Repayment of) Short Term Debt, net',
                     OPERATING_TYPE),
        statement.StatementItem('Cash From (Repurchase of) Equity', OPERATING_TYPE),
        statement.StatementItem('Cash From Long Term Debt', OPERATING_TYPE),
        statement.StatementItem('Cash for Acqusition of Subsidiaries', OPERATING_TYPE),
        statement.StatementItem('Cash for Joint Ventures', OPERATING_TYPE),
        statement.StatementItem('Cash from Financing Activities', OPERATING_TYPE),
        statement.StatementItem('Cash from Investing Activities', OPERATING_TYPE),
        statement.StatementItem('Cash from Operating Activities', OPERATING_TYPE),
        statement.StatementItem('Change in Cash from Disc. Operations and Other',
                     OPERATING_TYPE),
        statement.StatementItem('Change in Fixed Assets & Intangibles', OPERATING_TYPE),
        statement.StatementItem('Change in Working Capital', OPERATING_TYPE),
        statement.StatementItem('Decrease in Capital Stock', OPERATING_TYPE),
        statement.StatementItem('Decrease in Long Term Investment', OPERATING_TYPE),
        statement.StatementItem('Deferred Income Taxes', OPERATING_TYPE),
        statement.StatementItem('Depreciation & Amortization', OPERATING_TYPE),
        statement.StatementItem('Disposition of Fixed Assets', OPERATING_TYPE),
        statement.StatementItem('Disposition of Fixed Assets & Intangibles',
                     OPERATING_TYPE),
        statement.StatementItem('Disposition of Intangible Assets', OPERATING_TYPE),
        statement.StatementItem('Dividends Paid', OPERATING_TYPE),
        statement.StatementItem('Effect of Foreign Exchange Rates', OPERATING_TYPE),
        statement.StatementItem('Increase (Decrease) in Accounts Payable',
                     OPERATING_TYPE),
        statement.StatementItem('Increase (Decrease) in Other', OPERATING_TYPE),
        statement.StatementItem('Increase in Capital Stock', OPERATING_TYPE),
        statement.StatementItem('Increase in Long Term Investment', OPERATING_TYPE),
        statement.StatementItem('Net Cash Before Disc. Operations and FX',
                     OPERATING_TYPE),
        statement.StatementItem('Net Cash Before FX', OPERATING_TYPE),
        statement.StatementItem('Net Cash From Acquisitions & Divestitures',
                     OPERATING_TYPE),
        statement.StatementItem('Net Cash From Discontinued Operations (financing)',
                     OPERATING_TYPE),
        statement.StatementItem('Net Cash From Discontinued Operations (investing)',
                     OPERATING_TYPE),
        statement.StatementItem('Net Cash From Discontinued Operations (operating)',
                     OPERATING_TYPE),
        statement.StatementItem('Net Cash from Divestitures', OPERATING_TYPE),
        statement.StatementItem('Net Cash from Other Acquisitions', OPERATING_TYPE),
        statement.StatementItem('Net Change in Long Term Investment', OPERATING_TYPE),
        statement.StatementItem('Net Changes in Cash', OPERATING_TYPE),
        statement.StatementItem('Net Income', OPERATING_TYPE),
        statement.StatementItem('Net Income From Discontinued Operations',
                     OPERATING_TYPE),
        statement.StatementItem('Net Income/Starting Line', OPERATING_TYPE),
        statement.StatementItem('Non-Cash Items', OPERATING_TYPE),
        statement.StatementItem('Other Adjustments', OPERATING_TYPE),
        statement.StatementItem('Other Change in Fixed Assets & Intangibles',
                     OPERATING_TYPE),
        statement.StatementItem('Other Financing Activities', OPERATING_TYPE),
        statement.StatementItem('Other Investing Activities', OPERATING_TYPE),
        statement.StatementItem('Other Non-Cash Adjustments', OPERATING_TYPE),
        statement.StatementItem('Purchase of Fixed Assets', INVESTING_TYPE),
        statement.StatementItem('Repayments of Long Term Debt', OPERATING_TYPE),
        statement.StatementItem('Stock-Based Compensation', OPERATING_TYPE)
    ]
