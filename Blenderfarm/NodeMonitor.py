import os
from threading import Thread
import xml.etree.ElementTree as ET
import time
import copy

# bottle framework
from bottle import Request

from SourceGenerator import SourceGenerator
from Config import Config
from Constants import Constants
from RenderTaskManager import RenderTaskManager

# this class handle server script
# check if shared forlder is exist and write able
# if ho access return fail access shared folder to server
class NodeMonitor(Thread):

    # initialize config file
    def __init__(self, config):
        Thread.__init__(self)
        # init config file
        self._config = config
        
        # thread source generator
        self._sourcegenerator_thread = None
        
        # thread complete frame check
        self._check_complete_frame_thread = None
        
    # copy _s_node_cpuinfo to _node_sort_cpuinfo
    # then sort it by cpu_percent usage average from lowet to highest
    # combine sort by load_factor from lowest to highest
    # need call this before distribute frame to render
    def sort_node_by_cpu_load(self):
        # get cpu info
        node_cpuinfo = self._get_cpu_info()
        
        # copy node_cpuinfo to node_sort_cpuinfo
        node_sort_cpuinfo = copy.deepcopy(node_cpuinfo)
        
        # create key by load factor and cpu usage average
        data_node = node_sort_cpuinfo.findall(Constants.C_STR_NODE)
        
        if data_node != None:
            # save sorted data node
            data_node_sort = []
            
            for elem in data_node:
                data_node_sort.append((float(elem.attrib[Constants.C_STR_CPU_USAGE_AVR]), elem))
                                        
            # sort from lowest to highest
            data_node_sort.sort()
            
            # then re insert sorted cpu info by load factor and cpu usage average
            data_node[:] = [item[-1] for item in data_node_sort]
            
        return node_cpuinfo
    
    # node info manipulator
    def update_node_cpuinfo(self, ip_addr, node_data):
        node_cpuinfo = self._get_cpu_info()
        node_cpuinfo_item = None
            
        # find and ip address in node info file
        # if not exist then register it
        # find all node inside nodes tag
        node_cpuinfo_item = node_cpuinfo.find('.//'+Constants.C_STR_NODE+'/[@'+Constants.C_STR_IP+'=\''+ip_addr+'\']')
        
        # register new node if node not exist
        if node_cpuinfo_item == None:
            node_cpuinfo_item = ET.SubElement(node_cpuinfo, Constants.C_STR_NODE)
            node_cpuinfo_item.set(Constants.C_STR_IP, ip_addr)
            
        node_cpuinfo_item.set(Constants.C_STR_MEMORY_FREE, str(node_data[Constants.C_STR_MEMORY_FREE]))
        node_cpuinfo_item.set(Constants.C_STR_CPU_USAGE, str(node_data[Constants.C_STR_CPU_USAGE]))
        node_cpuinfo_item.set(Constants.C_STR_CPU_USAGE_AVR, str(node_data[Constants.C_STR_CPU_USAGE_AVR]))
        node_cpuinfo_item.set(Constants.C_STR_SHARED_LOCATION_ACCESS, str(node_data[Constants.C_STR_SHARED_LOCATION_ACCESS]))
        node_cpuinfo_item.set(Constants.C_STR_MEMORY_USED, str(node_data[Constants.C_STR_MEMORY_USED]))
        node_cpuinfo_item.set(Constants.C_STR_CPU_NUM, str(node_data[Constants.C_STR_CPU_NUM]))
        node_cpuinfo_item.set(Constants.C_STR_LAST_CONNECTED, str(time.time()))
        node_cpuinfo_item.set(Constants.C_STR_OS_PLATFORM, str(node_data[Constants.C_STR_OS_PLATFORM]))
        node_cpuinfo_item.set(Constants.C_STR_OS_HOSTNAME, str(node_data[Constants.C_STR_OS_HOSTNAME]))
        node_cpuinfo_item.set(Constants.C_STR_THREAD_ACTIVE, str(node_data[Constants.C_STR_THREAD_ACTIVE]))
        
        # write to xml
        # serialize CPU INFO
        print('do: serialize data')
        ET.ElementTree(node_cpuinfo).write(Constants.C_STR_NODE_CPUINFO_FILE, encoding='UTF-8')
        
            
    # get cpu info as tree root object
    def _get_cpu_info(self):
        node_cpuinfo = None
        
        if os.path.isfile(Constants.C_STR_NODE_CPUINFO_FILE):
            node_cpuinfo = ET.parse(Constants.C_STR_NODE_CPUINFO_FILE).getroot()
            
        else:
            node_cpuinfo = ET.Element(Constants.C_STR_NODES)
            
        return node_cpuinfo
    
    # override thread run
    def run(self):
        while True:
            
            # check source generator
            #print('check: source generator')
            if self._sourcegenerator_thread == None or not self._sourcegenerator_thread.is_alive():
                sourcegenerator = SourceGenerator(self._config)
                self._sourcegenerator_thread = Thread(target=sourcegenerator.check_blend_file)
                self._sourcegenerator_thread.start()
                
            # check complete frame
            #if self._check_complete_frame_thread == None or not self._check_complete_frame_thread.is_alive():
            #    check_completed_frame = RenderTaskManager(self._config)
            #    self._check_complete_frame_thread = Thread(target=check_completed_frame.check_rendered_frames)
            #    self._check_complete_frame_thread.start()
            
            RenderTaskManager(self._config).check_rendered_frames()
            
            time.sleep(Constants.C_NUM_NODE_MONITOR_SLEEP_TIME)
