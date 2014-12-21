import xml.etree.ElementTree as ET

from Constants import Constants

class Config(Constants):
    
    # initial file, to read config.xml
    def __init__(self):
        self._server_ip = None
        self._server_port = None
        self._shared_location = None
        self._blender_location = None
        self._source_folder = None
        self._output_folder = None
        
        self._config_tree = ET.parse(Config.C_STR_CONFIG_FILE)
        self._config_root = self._config_tree.getroot()
        
        # call config parse config.xml
        self.__parse_config()
        
    # parse xml configuration
    def __parse_config(self):
        for child in self._config_root:
            if child.tag == Config.C_STR_SERVER:
                self._server_ip = child.attrib[Config.C_STR_IP]
                self._server_port = child.attrib[Config.C_STR_PORT]
            
            if child.tag == Config.C_STR_SHARED:
                self._shared_location = child.attrib[Config.C_STR_LOCATION]
                
            if child.tag == Config.C_STR_BLENDER:
                self._blender_location = child.attrib[Config.C_STR_LOCATION]
                
            if child.tag == Config.C_STR_SOURCE:
                self._source_folder = child.attrib[Config.C_STR_FOLDER]
                
            if child.tag == Config.C_STR_OUTPUT:
                self._output_folder = child.attrib[Config.C_STR_FOLDER]
                
    # return configuration
    def get_config(self):
        config = {}
        
        config[Config.C_STR_IP] = self._server_ip
        config[Config.C_STR_PORT] = int(self._server_port)
        config[Config.C_STR_SHARED] = self._shared_location
        config[Config.C_STR_BLENDER] = self._blender_location
        config[Config.C_STR_SOURCE] = self._shared_location + self._source_folder
        config[Config.C_STR_OUTPUT] = self._shared_location + self._output_folder
        
        return config
        
