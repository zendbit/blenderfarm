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
        
        self.__config_tree = ET.parse(Config.CONFIG_FILE)
        self.__config_root = self.__config_tree.getroot()
        
        # call config parse config.xml
        self.__parse_config()
        
    # parse xml configuration
    def __parse_config(self):
        for child in self.__config_root:
            if child.tag == Config.SERVER_TAG:
                self.__server_ip = child.attrib[Config.IP_ATTR]
                self.__server_port = child.attrib[Config.PORT_ATTR]
            
            if child.tag == Config.SHARED_TAG:
                self.__shared_location = child.attrib[Config.LOCATION_ATTR]
                
            if child.tag == Config.BLENDER_TAG:
                self.__blender_location = child.attrib[Config.LOCATION_ATTR]
                
            if child.tag == Config.SOURCE_TAG:
                self.__source_folder = child.attrib[Config.FOLDER_ATTR]
                
            if child.tag == Config.OUTPUT_TAG:
                self.__output_folder = child.attrib[Config.FOLDER_ATTR]
                
    # return configuration
    def get_config(self):
        config = {}
        
        config['server_ip'] = self.__server_ip
        config['server_port'] = int(self.__server_port)
        config['shared_location'] = self.__shared_location
        config['blender_location'] = self.__blender_location
        config['source_folder'] = self.__shared_location + self.__source_folder
        config['output_folder'] = self.__shared_location + self.__output_folder
        
        return config
        
