import configparser

class Config:
    def __init__(self,filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def __repr__(self):
        buffer = ""
        for i in self.config.sections():
            buffer += " {} (".format(i)
            for j in self.config[i].keys():
                buffer = buffer + " {0}={1}".format(j,self.config[i][j])
            buffer += " )"   
        return buffer

    def __get_value__(self,section_name,key_name):
        if section_name in self.config:
            section = self.config[section_name]
            if key_name in section:
                return section[key_name]
        return None

    def simfin_storage(self):
        return self.__get_value__("simfin","storage")

    def simfin_apikey(self):
        return self.__get_value__("simfin","api-key")

    def misc_storage(self):
        return self.__get_value__("misc","storage")

    def storage_password(self):
        return self.__get_value__("storage","password")
    
    def storage_user(self):
        return self.__get_value__("storage","user")
    
    def storage_host(self):
        return self.__get_value__("storage","host")

