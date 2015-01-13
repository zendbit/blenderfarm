import xml.etree.ElementTree as ET
import sys
import os

from Constants import Constants

class Config():
    
    # initial file, to read config.xml
    def __init__(self):
        self._server_ip = None
        self._server_port = None
        self._shared_location = None
        self._blender_location = None
        self._source_folder = None
        self._protocol = None
        
        self._config_tree = ET.parse(Constants.C_STR_CONFIG_FILE)
        self._config_root = self._config_tree.getroot()
        
        # call config parse config.xml
        self.__parse_config()
        
    # parse xml configuration
    def __parse_config(self):
        # get properties config file
        self._server_ip = self._config_root.find('./' + Constants.C_STR_SERVER).attrib[Constants.C_STR_IP]
        self._server_port = self._config_root.find('./' + Constants.C_STR_SERVER).attrib[Constants.C_STR_PORT]
        self._protocol = self._config_root.find('./' + Constants.C_STR_SERVER).attrib[Constants.C_STR_PROTOCOL]
        
        # check os type
        # linux, or windows or darwin
        if sys.platform.find(Constants.C_STR_OS_PLATFORM_LINUX) > -1\
            or sys.platform.find(Constants.C_STR_OS_PLATFORM_DARWIN) > -1:
            # get shared location if os family is unix
            self._shared_location = self._config_root.find('./'\
                                    + Constants.C_STR_SHARED\
                                    + '/'\
                                    + '[@'\
                                    + Constants.C_STR_OS_FAMILY\
                                    + '=\'' + Constants.C_STR_OS_FAMILY_UNIX\
                                    + '\']').attrib[Constants.C_STR_LOCATION]
            
            # get blender location if os platform is linux
            self._blender_location = self._config_root.find('./'\
                                    + Constants.C_STR_BLENDER\
                                    + '/'\
                                    + '[@'\
                                    + Constants.C_STR_OS_PLATFORM\
                                    + '=\''\
                                    + Constants.C_STR_OS_PLATFORM_LINUX\
                                    + '\']').attrib[Constants.C_STR_LOCATION]
            
            # override blender location if os plaform is darwin or osx
            if sys.platform.find(Constants.C_STR_OS_PLATFORM_DARWIN):
                self._blender_location = self._config_root.find('./'\
                                    + Constants.C_STR_BLENDER\
                                    + '/' + '[@' + Constants.C_STR_OS_PLATFORM + '=\'' + Constants.C_STR_OS_PLATFORM_DARWIN + '\']').attrib[Constants.C_STR_LOCATION]
            
        if sys.platform.find(Constants.C_STR_OS_PLATFORM_WINDOWS) > -1:
            # get shared location for windows family
            self._shared_location = self._config_root.find('./'\
                                    + Constants.C_STR_SHARED\
                                    + '/'\
                                    + '[@'\
                                    + Constants.C_STR_OS_FAMILY\
                                    + '=\''\
                                    + Constants.C_STR_OS_FAMILY_WINDOWS\
                                    + '\']').attrib[Constants.C_STR_LOCATION]
                                    
            # get blender location if os platform is windows
            self._blender_location = self._config_root.find('./'\
                                    + Constants.C_STR_BLENDER\
                                    + '/'\
                                    + '[@'\
                                    + Constants.C_STR_OS_PLATFORM\
                                    + '=\''\
                                    + Constants.C_STR_OS_PLATFORM_WINDOWS\
                                    + '\']').attrib[Constants.C_STR_LOCATION]
            
        self._source_folder = self._shared_location\
                            + os.path.sep\
                            + self._config_root.find('./' + Constants.C_STR_SOURCE).attrib[Constants.C_STR_FOLDER]
             
    # return configuration
    def get_config(self):
        config = {}
        
        config[Constants.C_STR_IP] = self._server_ip
        config[Constants.C_STR_PORT] = int(self._server_port)
        config[Constants.C_STR_SHARED] = self._shared_location
        config[Constants.C_STR_BLENDER] = self._blender_location
        config[Constants.C_STR_SOURCE] = self._source_folder
        config[Constants.C_STR_PROTOCOL] = self._protocol
        
        return config
