class FieldDescription:
    def __init__(self,name,data_type):
        self.name = name
        self.data_type = data_type
        pass

class BaseDataService:
    def __init__(self,storage_name):
        self.__storage_name = storage_name
        self.fields = {}
        pass

    def add_field(self,name,field):
        if name in self.fields:
            self.fields[name].append(field) 
        else:
            self.fields[name] = [field]
            pass
        pass

    def storage_name(self):
        return self.__storage_name

    def object_descriptions(self):
        return self.fields