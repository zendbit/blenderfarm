import xml.etree.ElementTree as ET

from Constants import Constants

class Config(Constants):
    
    # initial file, to read config.xml
    def __init__(self):
        self.__server_ip = None
        self.__server_port = None
        self.__shared_location = None
        self.__blender_location = None
        self.__source_folder = None
        self.__output_folder = None
        
        self.__config_tree = ET.parse(Config.C_STR_CONFIG_FILE)
        self.__config_root = self.__config_tree.getroot()
        
        # call config parse config.xml
        self.__parse_config()
        
    # parse xml configuration
    def __parse_config(self):
        for child in self.__config_root:
            if child.tag == Config.C_STR_SERVER:
                self.__server_ip = child.attrib[Config.C_STR_IP]
                self.__server_port = child.attrib[Config.C_STR_PORT]
            
            if child.tag == Config.C_STR_SHARED:
                self.__shared_location = child.attrib[Config.C_STR_LOCATION]
                
            if child.tag == Config.C_STR_BLENDER:
                self.__blender_location = child.attrib[Config.C_STR_LOCATION]
                
            if child.tag == Config.C_STR_SOURCE:
                self.__source_folder = child.attrib[Config.C_STR_FOLDER]
                
            if child.tag == Config.C_STR_OUTPUT:
                self.__output_folder = child.attrib[Config.C_STR_FOLDER]
                
    # return configuration
    def get_config(self):
        config = {}
        
        config[Config.C_STR_IP] = self.__server_ip
        config[Config.C_STR_PORT] = int(self.__server_port)
        config[Config.C_STR_SHARED] = self.__shared_location
        config[Config.C_STR_BLENDER] = self.__blender_location
        config[Config.C_STR_SOURCE] = self.__shared_location + self.__source_folder
        config[Config.C_STR_OUTPUT] = self.__shared_location + self.__output_folder
        
        return config
        
