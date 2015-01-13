import os
import glob
import xml.etree.ElementTree as ET
import json
import base64
from PIL import Image

from Config import Config
from Constants import Constants

# this will manage task manager
# get list file to render
# list task to render
# etc

class RenderTaskManager():

    # init constructor
    def __init__(self, config):
        # init config
        self._config = config
        
    # get render list to render
    # return type should be
    # 'json' or 'dict'
    # will return dictionary or json string
    # contain group of
    # Constants.C_STR_RENDER_START -> indicate started render of file
    # Constants.C_STR_RENDER_STOP -> indicate paused/not started render of file
    def get_scenes_to_render(self, return_type='dict'):
        source_file = glob.glob(self._config[Constants.C_STR_SOURCE] + os.path.sep + '*')
        
        data_info_file_render_stop = []
        data_info_file_render_start = []
        
        data_info_render = {Constants.C_STR_RENDER_START:[], Constants.C_STR_RENDER_STOP:[]}
        
        # validate its folder and have info.xml file
        for folder in source_file:
            if os.path.isdir(folder):
            
                # if file contain .backup just skip it
                if folder.find('.backup') != -1:
                    continue
                            
                info_file_name = folder + os.path.sep + Constants.C_STR_INFO_FILE
                
                if os.path.isfile(info_file_name):
                    info_file = ET.parse(info_file_name).getroot()
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
                        data_info_item[Constants.C_STR_RESOLUTION_X] = int(info_item.attrib[Constants.C_STR_RESOLUTION_X])
                        data_info_item[Constants.C_STR_RESOLUTION_Y] = int(info_item.attrib[Constants.C_STR_RESOLUTION_Y])
                        data_info_item[Constants.C_STR_FORMAT_TYPE] = info_item.attrib[Constants.C_STR_FORMAT_TYPE]
                        data_info_item[Constants.C_STR_TIMESTAMP] = float(info_item.attrib[Constants.C_STR_TIMESTAMP])
                            
                        # check completed rendered frame
                        completed_rendered_frame = len(info_item.findall(Constants.C_STR_FRAME\
                            + '/[@' + Constants.C_STR_NEED_TO_RENDER + '=\'' + str(Constants.C_NUM_NEED_TO_RENDER_TRUE) + '\']'\
                            + '[@' + Constants.C_STR_FRAME_RENDER_STATUS + '=\'' + str(Constants.C_NUM_FRAME_RENDER_COMPLETED) + '\']'))
                            
                        data_info_item[Constants.C_STR_RENDER_COMPLETED] = int(completed_rendered_frame)
                        
                        # check uncomplete frame need to render
                        uncomplete_render_frame = len(info_item.findall(Constants.C_STR_FRAME\
                            + '/[@' + Constants.C_STR_NEED_TO_RENDER + '=\'' + str(Constants.C_NUM_NEED_TO_RENDER_TRUE) + '\']'\
                            + '[@' + Constants.C_STR_FRAME_RENDER_STATUS + '=\'' + str(Constants.C_NUM_FRAME_RENDER_UNCOMPLETE) + '\']'))
                            
                        data_info_item[Constants.C_STR_RENDER_UNCOMPLETED] = int(uncomplete_render_frame)
                        
                        # check frame not rendered
                        not_rendered_frame = len(info_item.findall(Constants.C_STR_FRAME\
                            + '/[@' + Constants.C_STR_NEED_TO_RENDER + '=\'' + str(Constants.C_NUM_NEED_TO_RENDER_FALSE) + '\']'\
                            + '[@' + Constants.C_STR_FRAME_RENDER_STATUS + '=\'' + str(Constants.C_NUM_FRAME_RENDER_UNCOMPLETE) + '\']'))
                            
                        data_info_item[Constants.C_STR_NOT_RENDERED] = int(not_rendered_frame)
                        
                        # Constants.C_NUM_RENDER_START -> show all started render process
                        # Constants.C_NUM_RENDER_STOP -> show all stoped render process
                        if int(info_item.attrib[Constants.C_STR_RENDER_STATUS]) == Constants.C_NUM_RENDER_START:
                            data_info_file_render_start.append((data_info_item[Constants.C_STR_TIMESTAMP], json.dumps(data_info_item)))
                            
                        elif int(info_item.attrib[Constants.C_STR_RENDER_STATUS]) == Constants.C_NUM_RENDER_STOP:
                            data_info_file_render_stop.append((data_info_item[Constants.C_STR_TIMESTAMP], json.dumps(data_info_item)))
        
        # sort by priority
        data_info_file_render_start.sort()
        data_info_file_render_stop.sort()
        
        # set render info
        # set value as json or as dict
        data_info_render[Constants.C_STR_RENDER_START][:] = [json.loads(item[-1]) for item in data_info_file_render_start]
        data_info_render[Constants.C_STR_RENDER_STOP][:] = [json.loads(item[-1]) for item in data_info_file_render_stop]
        
        if return_type == 'json':
            return base64.b64encode(json.dumps(data_info_render).encode('UTF-8'))
        else:
            return data_info_render
    
    # get scene detail
    # return scene with frame information
    # scene_data should be
    # {Constants.C_STR_ID:folder_id, Constants:C_STR_NAME:scene_name}
    def get_scene_frame_info(self, scene_data):
        file_info_name = self.get_info_file_name(scene_data[Constants.C_STR_ID])
            
        frames_data = []
        
        if os.path.isfile(file_info_name):
            info_file = ET.parse(file_info_name).getroot()
            
            frames = info_file.findall(Constants.C_STR_SCENE\
                + '/' + Constants.C_STR_FRAME)
                
            for frame in frames:
                frame_info = {}
                frame_info[Constants.C_STR_FRAME_RENDER_STATUS] = int(frame.attrib[Constants.C_STR_FRAME_RENDER_STATUS])
                frame_info[Constants.C_STR_ID] = int(frame.attrib[Constants.C_STR_ID])
                frame_info[Constants.C_STR_NEED_TO_RENDER] = int(frame.attrib[Constants.C_STR_NEED_TO_RENDER])
                
                frames_data.append(frame_info)
                
        return frames_data
    
    # check if task.json file locked        
    def is_task_file_locked(self):
        if os.path.isfile(Constants.C_STR_TASK_FILE_LOCK):
            return True
        else:
            return False
            
    # lock task.json
    def lock_task_file(self):
        if not os.path.isfile(Constants.C_STR_TASK_FILE_LOCK):
            lock = open(Constants.C_STR_TASK_FILE_LOCK, 'w')
            lock.write('')
            lock.close()
        
    # unlock task.json
    def unlock_task_file(self):
        if os.path.isfile(Constants.C_STR_TASK_FILE_LOCK):
            os.remove(Constants.C_STR_TASK_FILE_LOCK)
    
    # check if info file is exist or not
    # if not indicate file or folder render properties
    # already deleted
    def is_info_file_exist(self, folder_id):
        info_file = self._config[Constants.C_STR_SOURCE]\
            + os.path.sep\
            + folder_id\
            + os.path.sep\
            + Constants.C_STR_INFO_FILE
        
        return os.path.isfile(info_file)
        
    # check if task.json file locked        
    def is_info_file_locked(self):
        info_file_lock = self._config[Constants.C_STR_SOURCE]\
            + os.path.sep\
            + folder_id\
            + os.path.sep\
            + Constants.C_STR_INFO_FILE_LOCK
            
        if os.path.isfile(info_file_lock):
            return True
        else:
            return False
            
    # lock task.json
    def lock_info_file(self, folder_id):
        info_file_lock = self._config[Constants.C_STR_SOURCE]\
            + os.path.sep\
            + folder_id\
            + os.path.sep\
            + Constants.C_STR_INFO_FILE_LOCK
            
        if not os.path.isfile(info_file_lock):
            lock = open(info_file_lock, 'w')
            lock.write('')
            lock.close()
        
    # unlock task.json
    def unlock_info_file(self, folder_id):
        info_file_lock = self._config[Constants.C_STR_SOURCE]\
            + os.path.sep\
            + folder_id\
            + os.path.sep\
            + Constants.C_STR_INFO_FILE_LOCK
            
        if os.path.isfile(info_file_lock):
            os.remove(info_file_lock)
        
    # reset scene to process
    def reset_scene_to_process(self):
        self.lock_task_file()
        os.remove(Constants.C_STR_TASK_FILE)
        self.get_scene_to_process()
        self.unlock_task_file()
        
    # get scene to proceess
    # save scene info and all tiles to precess
    # refresh will renew cached to render list
    # return as list of dictionary
    def get_scene_to_process(self):
        
        task_list = []
        
        if not os.path.isfile(Constants.C_STR_TASK_FILE):
            # check lenght if 0 then save file
            f_task = open(Constants.C_STR_TASK_FILE, 'w')
            f_task.write(json.dumps(task_list))
            f_task.close()
            
        else:
            f_task = open(Constants.C_STR_TASK_FILE, 'r')
            task_data = f_task.readlines()
            
            if len(task_data):
                f_task_list = json.loads(task_data[0])
                f_task.close()
                if len(f_task_list):
                    return f_task_list
        
        #get scene to process
        scene_to_process = self.get_scenes_to_render()[Constants.C_STR_RENDER_START]
        
        for scene in scene_to_process:
            # get scene info
            info_file = ET.parse(self._config[Constants.C_STR_SOURCE]\
                + os.path.sep\
                + scene[Constants.C_STR_ID]\
                + os.path.sep\
                + Constants.C_STR_INFO_FILE).getroot()
            
            # get frame to render
            # uncompleted status
            frames_to_process = info_file.findall(Constants.C_STR_SCENE\
                + '/' + Constants.C_STR_FRAME\
                + '/[@' + Constants.C_STR_NEED_TO_RENDER + '=\'' + str(Constants.C_NUM_NEED_TO_RENDER_TRUE) + '\']'\
                + '[@' + Constants.C_STR_FRAME_RENDER_STATUS + '=\'' + str(Constants.C_NUM_FRAME_RENDER_UNCOMPLETE) + '\']')
                
            for frame in frames_to_process:
                tiles_to_process = frame.findall(Constants.C_STR_TILE\
                    + '/[@' + Constants.C_STR_STATUS + '=\'' + str(Constants.C_NUM_FRAME_RENDER_UNCOMPLETE) + '\']')
                
                for tile in tiles_to_process:
                    data_to_process = {}
                    data_to_process[Constants.C_STR_ID] = scene[Constants.C_STR_ID] # folder name
                    data_to_process[Constants.C_STR_NAME] = scene[Constants.C_STR_NAME] # scene name
                    data_to_process[Constants.C_STR_FRAME] = frame.attrib[Constants.C_STR_ID] # frame number
                    data_to_process[Constants.C_STR_BORDER_MIN_X] = tile.attrib[Constants.C_STR_BORDER_MIN_X] # render tile border
                    data_to_process[Constants.C_STR_BORDER_MAX_X] = tile.attrib[Constants.C_STR_BORDER_MAX_X] # render tile border
                    data_to_process[Constants.C_STR_BORDER_MIN_Y] = tile.attrib[Constants.C_STR_BORDER_MIN_Y] # render tile border
                    data_to_process[Constants.C_STR_BORDER_MAX_Y] = tile.attrib[Constants.C_STR_BORDER_MAX_Y] # render tile border
                    data_to_process[Constants.C_STR_TILE_POS_X] = tile.attrib[Constants.C_STR_TILE_POS_X] # render tile pos x
                    data_to_process[Constants.C_STR_TILE_POS_Y] = tile.attrib[Constants.C_STR_TILE_POS_Y] # render tile pos y
                    data_to_process[Constants.C_STR_RESOLUTION_X] = scene[Constants.C_STR_RESOLUTION_X] # resolution x
                    data_to_process[Constants.C_STR_RESOLUTION_Y] = scene[Constants.C_STR_RESOLUTION_Y] # resolution y
            
                    task_list.append(data_to_process)
                    
        # if queue must not more than C_NUM_MAX_TILE_QUEUE
        #if len(self._scene_to_process) >= Constants.C_NUM_MAX_TILE_QUEUE:
        #    return self._scene_to_process
        f_task = open(Constants.C_STR_TASK_FILE, 'w')
        f_task_list = json.dumps(task_list)
        f_task.write(f_task_list)
        f_task.close()
        return task_list
                        
                        
        # return scene to process
        #return self._scene_to_process
        
    # get render task from queue
    # get from _scene_to_process
    def pop_render_task(self):
    
        # get first task render
        task_list = self.get_scene_to_process()
        if len(task_list):
            task = task_list.pop(0)
            
            # check folder id to render is exist
            # check if folder id exist in source folder
            folder_id = self._config[Constants.C_STR_SOURCE]\
                + os.path.sep\
                + task[Constants.C_STR_ID]
            
            if not os.path.isdir(folder_id):
                # remove task.json
                # then call self.get_scene_to_render again
                os.remove(Constants.C_STR_TASK_FILE)
                task_list = self.get_scene_to_process()
                
                
            f_task = open(Constants.C_STR_TASK_FILE, 'w')
            f_task_list = json.dumps(task_list)
            f_task.write(f_task_list)
            f_task.close()
            return task
            
        else:
            return []
    
    # status will applied to all scene
    def pause_all_scenes(self, pause=True):
        source_file = glob.glob(self._config[Constants.C_STR_SOURCE] + os.path.sep + '*')
        
        # validate its folder and have info.xml file
        for folder in source_file:
            if os.path.isdir(folder):
            
                info_file_name = folder + os.path.sep + Constants.C_STR_INFO_FILE
                
                if os.path.isfile(info_file_name):
                    
                    render_status = Constants.C_NUM_RENDER_START
                    
                    if pause:
                        render_status = Constants.C_NUM_RENDER_STOP
                        
                    # get folder id
                    folder_id = folder.split(os.path.sep)[-1]
                    
                    # get rendered status and set to stop
                    info_file = ET.parse(info_file_name).getroot()
                    scenes = info_file.findall(Constants.C_STR_SCENE)
                    
                    for scene in scenes:
                        scene.set(Constants.C_STR_RENDER_STATUS, str(render_status))
                        
                    # serialize data
                    ET.ElementTree(info_file).write(info_file_name, encoding='UTF-8')
    
    # get total frame rendered
    def get_total_frame_rendered(self, folder_id, scene_name):
        info_file = self._config[Constants.C_STR_SOURCE] + os.path.sep + folder_id + os.path.sep + Constants.C_STR_INFO_FILE
        print(info_file)
        
        if os.path.isfile(info_file):
            info_file = ET.parse(info_file).getroot()
            completed_rendered_frame = len(info_file.findall(Constants.C_STR_SCENE\
                + '/' + Constants.C_STR_FRAME\
                + '/[@' + Constants.C_STR_FRAME_RENDER_STATUS + '=\'' + str(Constants.C_NUM_FRAME_RENDER_COMPLETED) + '\']'))
                
            return completed_rendered_frame
        else:
            return -1
    
    # check if frame completed render
    # if completed change status in info.xml
    # frame_render_status to 1
    def check_rendered_frames(self):
        # check if folder Constants.C_STR_COMPLETED_FRAME exists
        complete_frame_folder = self._config[Constants.C_STR_SOURCE] + os.path.sep + Constants.C_STR_COMPLETED_FRAME
        
        if os.path.isdir(complete_frame_folder):
            complete_frames = complete_frame_folder + os.path.sep +'*.ok'
            
            for complete_frame in glob.glob(complete_frames):
    
                # parse data frame information
                file_name = complete_frame.split(os.path.sep)[-1]
                frame_info = file_name.split('_')
                frame = int(frame_info[-1].replace('.ok', ''))
                scene_name = frame_info[-2]
                folder_id = file_name.replace(('_' + frame_info[-2] + '_' + frame_info[-1]), '')
                
                # set frame render to complete
                self.set_frame_render_completed({Constants.C_STR_ID:folder_id,\
                    Constants.C_STR_NAME:scene_name,\
                    Constants.C_STR_FRAME:frame})
                
                # remove temporary tile image
                tile_frame_prefix = self._config[Constants.C_STR_SOURCE]\
                    + os.path.sep + folder_id\
                    + os.path.sep + Constants.C_STR_TILE\
                    + os.path.sep + folder_id + '_' + scene_name + '_' + str(frame) + '*'
                    
                for frame_tile in glob.glob(tile_frame_prefix):
                    if os.path.isfile(frame_tile):
                        os.remove(frame_tile)
                
                # remove frame log
                os.remove(complete_frame)
                
    # get info file name
    def get_info_file_name(self, folder_id):
        return self._config[Constants.C_STR_SOURCE]\
            + os.path.sep + folder_id\
            + os.path.sep + Constants.C_STR_INFO_FILE
        
    # check if all frame rendered
    def set_scene_render_completed(self):
        scene_data = self.get_scenes_to_render()
        
        scenes = scene_data[Constants.C_STR_RENDER_START]
        
        for scene in scenes:
            info_file_name = self.get_info_file_name(scene[Constants.C_STR_ID])
            
            if os.path.isfile(info_file_name):
                info_file = ET.parse(info_file_name).getroot()
                
                # check completed rendered frame
                completed_rendered_frame = len(info_file.findall(Constants.C_STR_SCENE\
                    + '/[@' + Constants.C_STR_NAME + '=\'' + scene[Constants.C_STR_NAME] + '\']'
                    + '/' + Constants.C_STR_FRAME\
                    + '/[@' + Constants.C_STR_NEED_TO_RENDER + '=\'' + str(Constants.C_NUM_NEED_TO_RENDER_TRUE) + '\']'\
                    + '[@' + Constants.C_STR_FRAME_RENDER_STATUS + '=\'' + str(Constants.C_NUM_FRAME_RENDER_COMPLETED) + '\']'))
                
                # check uncomplete frame need to render
                uncomplete_render_frame = len(info_file.findall(Constants.C_STR_SCENE\
                    + '/[@' + Constants.C_STR_NAME + '=\'' + scene[Constants.C_STR_NAME] + '\']'
                    + '/' + Constants.C_STR_FRAME\
                    + '/[@' + Constants.C_STR_NEED_TO_RENDER + '=\'' + str(Constants.C_NUM_NEED_TO_RENDER_TRUE) + '\']'\
                    + '[@' + Constants.C_STR_FRAME_RENDER_STATUS + '=\'' + str(Constants.C_NUM_FRAME_RENDER_UNCOMPLETE) + '\']'))
                
                # set scene to complete rendered
                if completed_rendered_frame and not uncomplete_render_frame:
                    scene_obj = info_file.find(Constants.C_STR_SCENE\
                        + '/[@' + Constants.C_STR_NAME + '=\'' + scene[Constants.C_STR_NAME] + '\']')
                        
                    scene_obj.set(Constants.C_STR_RENDER_STATUS, str(Constants.C_NUM_RENDER_STOP))
                    
                    # serialize data
                    ET.ElementTree(info_file).write(info_file_name, encoding='UTF-8')
                
    # set rendered frame flag to complete
    # {Constant.C_STR_ID:folder_name, Constants.C_STR_NAME:scene name, Constants.C_STR_FRAME:frame id}
    def set_frame_render_completed(self, scene_data):
        info_file_name = self.get_info_file_name(scene_data[Constants.C_STR_ID])
        
        if os.path.isfile(info_file_name):
            info_file = ET.parse(info_file_name).getroot()
            
            # get frame object
            frame_to_process = info_file.find(Constants.C_STR_SCENE\
                + '/[@' + Constants.C_STR_NAME + '=\'' + scene_data[Constants.C_STR_NAME] + '\']'\
                + '/' + Constants.C_STR_FRAME + '/[@' + Constants.C_STR_ID + '=\'' + str(scene_data[Constants.C_STR_FRAME]) + '\']')
                
            frame_to_process.set(Constants.C_STR_FRAME_RENDER_STATUS, str(Constants.C_NUM_FRAME_RENDER_COMPLETED))
            
            # serialize data
            ET.ElementTree(info_file).write(info_file_name, encoding='UTF-8')
    
    # set frame to render
    # parameter in json data
    # all parameter can't be empty'
    # {Constants.C_STR_ID: folder_name, Constants.C_STR_NAME: scene_name, Constants.C_STR_FRAME: 'frame, frame, frame', Constants.C_STR_RENDER_STATUS, Constant.C_STR_NEED_TO_RENDER, Constants.C_STR_RENDER_PAUSE: pause flag}
    # if frame = '' indicate to render all
    # if frame = '-1' indicate don't render anithing'
    def set_scene_to_render(self, scene_data):
        info_file_name = self.get_info_file_name(scene_data[Constants.C_STR_ID])
        
        if os.path.isfile(info_file_name):
            
            need_to_render = scene_data[Constants.C_STR_NEED_TO_RENDER]
            
            info_file = ET.parse(info_file_name).getroot()
            
            # validate frames
            # if Constants.C_STR_FRAME = ''
            # indicate render all frames
            frames = scene_data[Constants.C_STR_FRAME].split(',')
            
            # get scene to process by scene name
            scene_to_process = info_file.find(Constants.C_STR_SCENE\
                + '/[@' + Constants.C_STR_NAME + '=\'' + scene_data[Constants.C_STR_NAME] + '\']')
                    
            # set scene render status
            scene_to_process.set(Constants.C_STR_RENDER_STATUS, str(scene_data[Constants.C_STR_RENDER_STATUS]))
            
            # if scene frame == '' set render all        
            if scene_data[Constants.C_STR_FRAME] == '':
                # get all frames count
                frames = range(1, int(scene_to_process.attrib[Constants.C_STR_FRAME_END]) + 1)
            
            # set frame to render
            for frame in frames:
                set_frame = str(frame).strip()
                
                frame_to_process = info_file.find(Constants.C_STR_SCENE\
                    + '/[@' + Constants.C_STR_NAME + '=\'' + scene_data[Constants.C_STR_NAME] + '\']'
                    + '/' + Constants.C_STR_FRAME + '/[@' + Constants.C_STR_ID + '=\'' + set_frame + '\']')
                
                if scene_data.get(Constants.C_STR_RENDER_PAUSE) == Constants.C_NUM_RENDER_RESTART:
                    # set frame to render status
                    frame_to_process.set(Constants.C_STR_NEED_TO_RENDER, str(need_to_render))
                
                    # set flag to uncomplete
                    # if not pause state set to uncomplete
                    if need_to_render:
                        frame_to_process.set(Constants.C_STR_FRAME_RENDER_STATUS, str(Constants.C_NUM_FRAME_RENDER_UNCOMPLETE))
                
                    # delete frame if file rendered file exist
                    output_frame_file_name = self._get_frame_output_file_name({Constants.C_STR_FRAME : set_frame,\
                        Constants.C_STR_NAME : scene_data[Constants.C_STR_NAME],\
                        Constants.C_STR_ID : scene_data[Constants.C_STR_ID]})
                
                    if os.path.isfile(output_frame_file_name):
                        os.remove(output_frame_file_name)
                
            # serialize data
            ET.ElementTree(info_file).write(info_file_name, encoding='UTF-8')
            
    # check if render process tiles of frame is complete
    def is_frame_render_complete(self, render_data):
        # if tiles of frame render complete then merge tile into frame
        # merge file will named as format folder_id_scene_name_frame
        tiles_frame = self._get_tile_output_folder(render_data)\
            + os.path.sep + render_data[Constants.C_STR_ID]\
            + '_' + render_data[Constants.C_STR_NAME]\
            + '_' + render_data[Constants.C_STR_FRAME] + '_*'
            
        # if render complete
        # num tiles each frame must equals with square root of Constants.C_NUM_RENDER_SPLIT
        if os.path.isfile(self._get_frame_output_file_name(render_data)):
            return True
            
        elif os.path.isfile(self._get_frame_output_completed_file_name(render_data)):
            return True
            
        elif len(glob.glob(tiles_frame)) == (Constants.C_NUM_RENDER_SPLIT * Constants.C_NUM_RENDER_SPLIT):
            # merge image if render completed
            self._merge_image(render_data)
            
            # create completed frame flag
            if not os.path.isfile(self._get_frame_output_completed_file_name(render_data)):
                frame_ok = open(self._get_frame_output_completed_file_name(render_data), 'w')
                frame_ok.write('')
                frame_ok.close()
            
            return True
            
        else:
            return False
    
    # get tile name
    def _get_tile_output_folder(self, render_data):
        output_folder = self._config[Constants.C_STR_SOURCE]\
            + os.path.sep + render_data[Constants.C_STR_ID]\
            + os.path.sep + Constants.C_STR_TILE
            
        return output_folder
        
    # get frame output folder
    def _get_frame_output_folder_name(self, render_data):
        output_folder = self._config[Constants.C_STR_SOURCE]\
            + os.path.sep + render_data[Constants.C_STR_ID]\
            + os.path.sep + Constants.C_STR_FRAME
            
        return output_folder
        
    # get output frame name
    def _get_frame_output_file_name(self, render_data):
        zero_prefix = 10 - len(render_data[Constants.C_STR_FRAME])
        zero_prefix = '0' * zero_prefix
        
        frame_output_name = self._get_frame_output_folder_name(render_data)\
            + os.path.sep + render_data[Constants.C_STR_NAME]\
            + '_' + zero_prefix + render_data[Constants.C_STR_FRAME] + '.png'
            
        return frame_output_name
        
    def _get_frame_output_completed_file_name(self, render_data):
        zero_prefix = 10 - len(render_data[Constants.C_STR_FRAME])
        zero_prefix = '0' * zero_prefix
         
        completed_frame_folder = self._config[Constants.C_STR_SOURCE] + os.path.sep + Constants.C_STR_COMPLETED_FRAME
        
        frame_output_completed_frame = completed_frame_folder\
            + os.path.sep + render_data[Constants.C_STR_ID]\
            + '_' + render_data[Constants.C_STR_NAME]\
            + '_' + zero_prefix + render_data[Constants.C_STR_FRAME] + '.ok'
            
        # check if output frame folder not exist
        # create it
        if not os.path.isdir(completed_frame_folder):
            os.mkdir(completed_frame_folder, 0o777)
            os.chmod(completed_frame_folder, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)
            
        return frame_output_completed_frame
    
    # merge render data
    def _merge_image(self, render_data):
        tile_data_prefix = self._get_tile_output_folder(render_data)\
            + os.path.sep\
            + render_data[Constants.C_STR_ID]\
            + '_' + render_data[Constants.C_STR_NAME]\
            + '_' + render_data[Constants.C_STR_FRAME]
            
        resolution_x = int(render_data[Constants.C_STR_RESOLUTION_X])
        resolution_y = int(render_data[Constants.C_STR_RESOLUTION_Y])
           
        x_increment = resolution_x/Constants.C_NUM_RENDER_SPLIT
        y_increment = resolution_y/Constants.C_NUM_RENDER_SPLIT
        
        new_im = Image.new('RGBA', (int(resolution_x), int(resolution_y)))
        x_position = 0
        y_position = 0
        
        for x in range(0, Constants.C_NUM_RENDER_SPLIT):
            # reset y postition
            y_position = 0
            
            for y in range(Constants.C_NUM_RENDER_SPLIT - 1, -1, -1): # reverse y axis blender is from bottom left, pil is from top left
                tile_image = Image.open(tile_data_prefix + '_' + str(x) + '_' + str(y) + '.png')
                tile_width, tile_height = tile_image.size
                
                new_im.paste(tile_image, (x_position, y_position))
                
                y_position += tile_height
                
                if not y:
                    x_position += tile_width
        
        if not os.path.isfile(self._get_frame_output_file_name(render_data)):
            new_im.save(self._get_frame_output_file_name(render_data), 'png')
