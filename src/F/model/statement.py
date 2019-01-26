class StatementItem:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Statement:
    def __init__(self,company,data):
        self.company = company
        self.data = data

    def description(self):
        assert("description listing is not provided.")

    def all(self,year=None,tolerance=0):
        data = None
        if year != None:
            data = self.data.loc[self.data.index >= year]
        else:
            data = self.data
        sum = data.sum().abs()
        sum = sum.loc[sum > tolerance].sort_values(ascending = False)
        index = sum.index
        data = data[index]
        return data


    def apply(self, condition,year=None):
        listing = list(filter(condition, self.description()))
        listing = map(lambda x: x.name, listing)
        statements = self.data[list(listing)]
        if year != None:
            statements = statements.loc[statements.index >= year]
        return statements