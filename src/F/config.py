import configparser

class Config:
    def __init__(self,filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def __get_value__(self,section_name,key_name):
        if section_name in self.config:
            section = self.config[section_name]
            if key_name in section:
                return section[key_name]
        return None

    def simfin_apikey(self):
        return self.__get_value__("simfin","api-key")

    def storage_password(self):
        return self.__get_value__("storage","password")
    
    def storage_user(self):
        return self.__get_value__("storage","user")
    
    def storage_host(self):
        return self.__get_value__("storage","host")

