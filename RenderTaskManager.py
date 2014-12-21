import os
import glob
import xml.etree.ElementTree as ET
import json
import base64

from Config import Config
from Constants import Constants

# this will manage task manager
# get list file to render
# list task to render
# etc

class RenderTaskManager(Constants):

    # init constructor
    def __init__(self, config):
        self._source_folder = config[RenderTaskManager.C_STR_SOURCE]
        self._blender_location = config[RenderTaskManager.C_STR_BLENDER]
        self._shared_location = config[RenderTaskManager.C_STR_SHARED]
        
    # get render list to render
    def get_render_file_to_render(self, return_type='list'):
        source_file = glob.glob(self._source_folder+'/*')
        
        data_info_file = []
        
        # validate its folder and have info.xml file
        for folder in source_file:
            if os.path.isdir(folder):
                if os.path.isfile(folder + '/' + RenderTaskManager.C_STR_INFO_FILE):
                    info_file = ET.parse(folder + '/' + RenderTaskManager.C_STR_INFO_FILE).getroot()
                    info_file.findall(Constants.C_STR_SCENE)
                    
                    # extract info
                    for info_item in info_file:
                        data_info_item = {}
                        file_id = folder.split('/')[-1]
                        data_info_item[RenderTaskManager.C_STR_ID] = file_id
                        data_info_item[RenderTaskManager.C_STR_SCENE_NAME] = info_item.attrib[RenderTaskManager.C_STR_SCENE_NAME]
                        data_info_item[RenderTaskManager.C_STR_SCENE_FRAME_START] = info_item.attrib[RenderTaskManager.C_STR_SCENE_FRAME_START]
                        data_info_item[RenderTaskManager.C_STR_SCENE_FRAME_END] = info_item.attrib[RenderTaskManager.C_STR_SCENE_FRAME_END]
                        data_info_item[RenderTaskManager.C_STR_SCENE_FRAME_STEP] = info_item.attrib[RenderTaskManager.C_STR_SCENE_FRAME_STEP]
                        
                        data_info_file.append(data_info_item)
                        
        if return_type == 'json':
            return base64.b64encode(json.dumps(data_info_file).encode('UTF-8'))
        else:
            return data_info_file

if __name__ == '__main__':
    print(base64.b64decode(RenderTaskManager(Config().get_config()).get_render_file_to_render(return_type='json')))
