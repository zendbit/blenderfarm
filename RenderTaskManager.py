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

class RenderTaskManager():

    # init constructor
    def __init__(self, config):
        self._source_folder = config[Constants.C_STR_SOURCE]
        self._blender_location = config[Constants.C_STR_BLENDER]
        self._shared_location = config[Constants.C_STR_SHARED]
        
    # get render list to render
    # return type should be
    # 'json' or 'dict'
    # will return dictionary or json string
    # contain group of
    # Constants.C_STR_RENDER_START -> indicate started render of file
    # Constants.C_STR_RENDER_STOP -> indicate paused/not started render of file
    def get_file_to_render(self, return_type='dict'):
        source_file = glob.glob(self._source_folder + os.path.sep + '*')
        
        data_info_file_render_stop = []
        data_info_file_render_start = []
        
        data_info_render = {Constants.C_STR_RENDER_START:[], Constants.C_STR_RENDER_STOP:[]}
        
        # validate its folder and have info.xml file
        for folder in source_file:
            if os.path.isdir(folder):
                if os.path.isfile(folder + os.path.sep + Constants.C_STR_INFO_FILE):
                    info_file = ET.parse(folder + os.path.sep + Constants.C_STR_INFO_FILE).getroot()
                    info_file.findall(Constants.C_STR_SCENE)
                    
                    # extract info
                    for info_item in info_file:
                        
                        data_info_item = {}
                        file_id = folder.split(os.path.sep)[-1]
                        data_info_item[Constants.C_STR_ID] = file_id
                        data_info_item[Constants.C_STR_NAME] = info_item.attrib[Constants.C_STR_NAME]
                        data_info_item[Constants.C_STR_FRAME_START] = int(info_item.attrib[Constants.C_STR_FRAME_START])
                        data_info_item[Constants.C_STR_FRAME_END] = int(info_item.attrib[Constants.C_STR_FRAME_END])
                        data_info_item[Constants.C_STR_FRAME_STEP] = int(info_item.attrib[Constants.C_STR_FRAME_STEP])
                        data_info_item[Constants.C_STR_RENDER_STATUS] = int(info_item.attrib[Constants.C_STR_RENDER_STATUS])
                        data_info_item[Constants.C_STR_RENDER_PRIORITY] = int(info_item.attrib[Constants.C_STR_RENDER_PRIORITY])
                            
                        # check completed rendered frame
                        completed_rendered_frame = len(info_item.findall(Constants.C_STR_FRAME\
                            + '/[@need_to_render=\''\
                            + str(Constants.C_NUM_NEED_TO_RENDER_TRUE)\
                            + '\'][@frame_render_status=\''\
                            + str(Constants.C_NUM_FRAME_RENDER_COMPLETED)\
                            + '\']'))
                            
                        data_info_item[Constants.C_STR_RENDER_COMPLETED] = int(completed_rendered_frame)
                        
                        # check uncomplete frame need to render
                        uncomplete_render_frame = len(info_item.findall(Constants.C_STR_FRAME\
                            + '/[@need_to_render=\''\
                            + str(Constants.C_NUM_NEED_TO_RENDER_TRUE)\
                            + '\'][@frame_render_status=\''\
                            + str(Constants.C_NUM_FRAME_RENDER_UNCOMPLETE)\
                            + '\']'))
                            
                        data_info_item[Constants.C_STR_RENDER_UNCOMPLETED] = int(uncomplete_render_frame)
                        
                        # check frame not rendered
                        not_rendered_frame = len(info_item.findall(Constants.C_STR_FRAME\
                            + '/[@need_to_render=\''\
                            + str(Constants.C_NUM_NEED_TO_RENDER_FALSE)\
                            + '\'][@frame_render_status=\''\
                            + str(Constants.C_NUM_FRAME_RENDER_UNCOMPLETE)\
                            + '\']'))
                            
                        data_info_item[Constants.C_STR_NOT_RENDERED] = int(not_rendered_frame)
                        
                        # Constants.C_NUM_RENDER_START -> show all started render process
                        # Constants.C_NUM_RENDER_STOP -> show all stoped render process
                        if int(info_item.attrib[Constants.C_STR_RENDER_STATUS]) == Constants.C_NUM_RENDER_START:
                            data_info_file_render_start.append((data_info_item[Constants.C_STR_RENDER_PRIORITY], json.dumps(data_info_item)))
                            
                        elif int(info_item.attrib[Constants.C_STR_RENDER_STATUS]) == Constants.C_NUM_RENDER_STOP:
                            data_info_file_render_stop.append((data_info_item[Constants.C_STR_RENDER_PRIORITY], json.dumps(data_info_item)))
        
        # sort by priority
        data_info_file_render_start.sort(reverse=True)
        data_info_file_render_stop.sort(reverse=True)
        
        # set render info
        # set value as json or as dict
        data_info_render[Constants.C_STR_RENDER_START][:] = [json.loads(item[-1]) for item in data_info_file_render_start]
        data_info_render[Constants.C_STR_RENDER_STOP][:] = [json.loads(item[-1]) for item in data_info_file_render_stop]
        
        if return_type == 'json':
            return base64.b64encode(json.dumps(data_info_render).encode('UTF-8'))
        else:
            return data_info_render

if __name__ == '__main__':
    print(base64.b64decode(RenderTaskManager(Config().get_config()).get_file_to_render(return_type='json')))
    #RenderTaskManager(Config().get_config()).get_file_to_render(return_type='json')
