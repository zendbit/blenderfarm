import os
import threading
import time
import psutil
import socket
import json
from threading import Thread
import xml.etree.ElementTree as ET
import sys
import base64
from urllib import request
import subprocess
import glob
import stat

from Config import Config
from Constants import Constants
from RenderTaskManager import RenderTaskManager

# this class handle client script
# check if shared forlder is exist and write able
# if ho access return fail access shared folder to server
class NodeRender(Thread):
    
    # initialize config file
    def __init__(self):
        # call constructor parent
        Thread.__init__(self)
        
        # thread runner
        self._thread_runner = None
        
        # config value
        self._config = Config().get_config()
        
        # init render task manager
        self._task_manager = RenderTaskManager(self._config)
        self._task_manager.get_scene_to_process()
        
    # run method thread
    def run(self):
        while True:
            try:
               
                # get configuration, check if configuration is changed
                self._config = Config().get_config()
                
                if len(self._config):
                    # get render from queue
                    try:
                        if not self._task_manager.is_task_file_locked():
                            self._task_manager.lock_task_file()
                            render_data = self._task_manager.pop_render_task()
                            self._task_manager.unlock_task_file()
                            
                            if len(render_data):
                                self._do_render(render_data)
                                
                    except Exception as e:
                        print(e)
                        if self._task_manager.is_task_file_locked():
                            self._task_manager.unlock_task_file()
                        
                    #print('do: send node info..')
                    #self._send_node_cpuinfo(config)
                     
                # print error if configuration file not found
                else:
                    print('invalid check: configuration file:config.xml')
            
            except Exception as e:
                print(e)
                
            time.sleep(Constants.C_NUM_NODE_RENDER_SLEEP_TIME)
    
    # encode data from node
    def _encode_data(self, data):
        return base64.b64encode(data.encode('UTF-8')).decode('UTF-8')
        
    # decode data from node
    def _decode_data(self, data):
        return base64.b64decode(data).decode('UTF-8')
        
    # send message to server
    # report client process to server
    # message should be in string
    def _send_message(self, message):
        data = self._encode_data(message)
        
        # send data to server
        return request.urlopen(self._config[Constants.C_STR_PROTOCOL]\
            + self._config[Constants.C_STR_IP]\
            + ':' + str(self._config[Constants.C_STR_PORT])\
            + '/?send_data=' + data).readall()
    
    # send node render information
    def _send_node_renderinfo(self):
        self._send_message(json.dumps(self._get_node_info(config)))
    
    # send request to get task from server
    def _send_request_task(self):
        if (self._thread_runner == None) or (not self._thread_runner.is_alive()):
            node_request = {}
            
            # action type
            node_request[Constants.C_STR_ACTION] = Constants.C_NUM_ACTION_TASK_REQUEST
            
            result = self._decode_data(self._send_message(json.dumps(node_request)))
            
            if result != '0':
                render_data = json.loads(result)
                # init thread runner
                self._thread_runner = threading.Thread(target=self._do_render, args=(render_data))
                self._thread_runner.start()
                
    # send node information
    def _send_node_cpuinfo(self):
        self._send_message(json.dumps(self._get_node_info(config)))
                
    # get do render
    def _do_render(self, render_data):
    
        if not self._task_manager.is_frame_render_complete(render_data):
            # check if blender file is exist
            blend_file = self._config[Constants.C_STR_SOURCE]\
                + os.path.sep\
                + render_data[Constants.C_STR_ID]\
                + os.path.sep\
                + render_data[Constants.C_STR_ID] + '.blend'
                
            if os.path.isfile(blend_file):
                # generate RenderTile script parameter
                py_param = self._config[Constants.C_STR_SOURCE] + os.path.sep + render_data[Constants.C_STR_ID] + os.path.sep + Constants.C_STR_TILE\
                    + ' ' + render_data[Constants.C_STR_ID]\
                    + ' ' + render_data[Constants.C_STR_NAME]\
                    + ' ' + render_data[Constants.C_STR_FRAME]\
                    + ' ' + render_data[Constants.C_STR_BORDER_MIN_X]\
                    + ' ' + render_data[Constants.C_STR_BORDER_MAX_X]\
                    + ' ' + render_data[Constants.C_STR_BORDER_MIN_Y]\
                    + ' ' + render_data[Constants.C_STR_BORDER_MAX_Y]\
                    + ' ' + render_data[Constants.C_STR_TILE_POS_X]\
                    + ' ' + render_data[Constants.C_STR_TILE_POS_Y]\
                    
                render_cmd = self._config[Constants.C_STR_BLENDER]\
                    + ' -b ' + blend_file\
                    + ' -S ' + render_data[Constants.C_STR_NAME]\
                    + ' -P RenderTile.py -- ' + py_param
                    
                # call render command as tiled
                subprocess.call(render_cmd, shell=True)
                
                # call check render complete
                self._task_manager.is_frame_render_complete(render_data)
    
    # get cpu information
    def _get_node_info(self):
    
        node_info = {}
    
        # action type
        node_info[Constants.C_STR_ACTION] = Constants.C_NUM_ACTION_UPDATE_CPUINFO
        
        # add cpu report type as status cpu infomation
        node_info[Constants.C_STR_DATA_TYPE] = Constants.C_STR_DATA_CPU
        
        # get cpu count
        node_info[Constants.C_STR_CPU_NUM] = psutil.cpu_count()
        
        # get per cpu utilization
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        node_info[Constants.C_STR_CPU_USAGE] = cpu_usage
        
        # get average cpu load
        node_info[Constants.C_STR_CPU_USAGE_AVR] = sum(cpu_usage)/float(len(cpu_usage))
        
        # get memory usage
        node_info[Constants.C_STR_MEMORY_USED] = psutil.phymem_usage().used
        node_info[Constants.C_STR_MEMORY_FREE] = psutil.phymem_usage().free
        
        # get os platform from client
        node_info[Constants.C_STR_OS_PLATFORM] = sys.platform
        
        # get os name from client
        node_info[Constants.C_STR_OS_HOSTNAME] = socket.gethostname()
        
        # check if thread render is active
        thread_active = 0
        if self._thread_runner != None and self._thread_runner.is_alive():
            thread_active = 1
            
        node_info[Constants.C_STR_THREAD_ACTIVE] = thread_active
        
        if os.access(self._config[Constants.C_STR_SHARED], os.W_OK):
            # add access shared location info
            node_info[Constants.C_STR_SHARED_LOCATION_ACCESS] = Constants.C_NUM_SHARED_WRITE_OK
                        
        else:
            # add access shared locaiton info
            node_info[Constants.C_STR_SHARED_LOCATION_ACCESS] = Constants.C_NUM_SHARED_WRITE_NONE
        
        return node_info
            
# launcher
if __name__ == '__main__':
    NodeRender().start()
