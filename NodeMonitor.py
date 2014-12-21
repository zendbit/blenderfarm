import os
import threading
from threading import Thread
import xml.etree.ElementTree as ET
import time
import socketserver
import copy

from SourceGenerator import SourceGenerator
from Config import Config
from NodeHandler import NodeHandler
from Constants import Constants

# this class handle server script
# check if shared forlder is exist and write able
# if ho access return fail access shared folder to server
class NodeMonitor(Thread, Constants):
    
    # hold node info data before save to node_info.xml
    # this will hold xml etree getroot object
    _s_node_cpuinfo = None # cpu node information
    _s_node_renderinfo = None # render node information
    
    
    # initialize config file
    def __init__(self):
        # call constructor parent
        Thread.__init__(self)
        self._thread_node_listener = Thread()
        self._server_monitor = None
        
        # server flags running
        self._is_running = 1
        
        # set server monitor
        # 1 is running state
        self.set_server_status(1)
        
        # hold temporary data
        # this will do sort by cpu average, running thread
        # sort by cpu running thread asc, from min running thread to max running thread
        _node_sort_cpuinfo = None
        
        # list available frame to render
        # this is depend on queue and priority
        _frame_to_render = []
        
    # run method thread
    def run(self):
        while self._is_running:
            try:
                # get configuration, check if configuration is changed
                config = Config().get_config()
                
                if len(config):
                    # check node information file
                    self.__check_node_info_file()
                    
                    if os.access(config[NodeMonitor.C_STR_SHARED], os.W_OK):
                        
                        print("check: shared location access ok")
                        
                        # check server status
                        # if status equals to 1 server monitor is running
                        # else shutdown server and quit thread
                        if not self.get_server_status():
                            self.stop_service()
                            
                        
                        # check blend file in source folder
                        # then create source project
                        SourceGenerator(config)
                        
                        # listen request from node render client
                        # check if thread node listener is alive or not
                        self.__init_node_server(config)
                        
                        # serialize data into xml file
                        self.__serialize_data()
                        
                    else:
                        print('invalid check: can\'t access shared location')
            
            except Exception as e:
                print('exception: error while initialize server')
                print(e)
                
            time.sleep(NodeMonitor.C_NUM_NODE_MONITOR_SLEEP_TIME)
            
    # copy _s_node_cpuinfo to _node_sort_cpuinfo
    # then sort it by cpu_percent usage average from lowet to highest
    # combine sort by load_factor from lowest to highest
    # need call this before distribute frame to render
    def _sort_node_by_cpu_load(self):
        # copy _s_node_cpuinfo to _node_sort_cpuinfo
        if self._s_node_cpuinfo != None:
            self._node_sort_cpuinfo = copy.deepcopy(self._s_node_cpuinfo)
            
            # create key by load factor and cpu usage average
            data_node = self._node_sort_cpuinfo.findall(NodeMonitor.C_STR_NODE)
            
            # save sorted data node
            data_node_sort = []
            
            for elem in data_node:
                data_node_sort.append((float(elem.attrib[NodeMonitor.C_STR_LOAD_FACTOR]),
                                        float(elem.attrib[NodeMonitor.C_STR_CPU_USAGE_AVR]),
                                        elem))
                                        
            # sort from lowest to highest
            data_node_sort.sort()
            
            # then re insert sorted cpu info by load factor and cpu usage average
            data_node[:] = [item[-1] for item in data_node_sort]
    
    # node info manipulator
    # update only from this method
    # this is static method
    # call via NodeMonitor.update_node_cpuinfo
    @staticmethod
    def update_node_cpuinfo(ip_addr, node_data):
        # check if _s_node_cpuinfo is None
        # if None init with NodeHandler.C_STR_NODE_CPUINFO_FILE
        # if NodeHandler.C_STR_NODE_CPUINFO_FILE Not Exist init with ET.Element(NodeHandler.C_STR_NODES)
        if NodeMonitor._s_node_cpuinfo == None:
            if os.path.isfile(NodeHandler.C_STR_NODE_CPUINFO_FILE):
                NodeMonitor._s_node_cpuinfo = ET.parse(NodeHandler.C_STR_NODE_CPUINFO_FILE).getroot()
            else:
                NodeMonitor._s_node_cpuinfo = ET.Element(NodeHandler.C_STR_NODES)
                
        else:
            # find and ip address in node info file
            # if not exist then register it
            # find all node inside nodes tag
            node_cpuinfo_item = NodeMonitor._s_node_cpuinfo.find('.//'+NodeHandler.C_STR_NODE+'/[@'+NodeHandler.C_STR_IP+'=\''+ip_addr+'\']')
        
            # register new node if node not exist
            if node_cpuinfo_item == None:
                node_cpuinfo_item = ET.SubElement(NodeMonitor._s_node_cpuinfo, NodeHandler.C_STR_NODE)
                node_cpuinfo_item.set(NodeHandler.C_STR_IP, ip_addr)
                
            node_cpuinfo_item.set(NodeHandler.C_STR_MEMORY_FREE, str(node_data[NodeHandler.C_STR_MEMORY_FREE]))
            node_cpuinfo_item.set(NodeHandler.C_STR_CPU_USAGE, str(node_data[NodeHandler.C_STR_CPU_USAGE]))
            node_cpuinfo_item.set(NodeHandler.C_STR_CPU_USAGE_AVR, str(node_data[NodeHandler.C_STR_CPU_USAGE_AVR]))
            node_cpuinfo_item.set(NodeHandler.C_STR_SHARED_LOCATION_ACCESS, str(node_data[NodeHandler.C_STR_SHARED_LOCATION_ACCESS]))
            node_cpuinfo_item.set(NodeHandler.C_STR_MEMORY_USED, str(node_data[NodeHandler.C_STR_MEMORY_USED]))
            node_cpuinfo_item.set(NodeHandler.C_STR_CPU_NUM, str(node_data[NodeHandler.C_STR_CPU_NUM]))
            node_cpuinfo_item.set(NodeHandler.C_STR_LOAD_FACTOR, str(node_data[NodeHandler.C_STR_LOAD_FACTOR]))
            node_cpuinfo_item.set(NodeHandler.C_STR_LAST_CONNECTED, str(time.time()))
            node_cpuinfo_item.set(NodeHandler.C_STR_OS_PLATFORM, str(node_data[NodeHandler.C_STR_OS_PLATFORM]))
            node_cpuinfo_item.set(NodeHandler.C_STR_OS_HOSTNAME, str(node_data[NodeHandler.C_STR_OS_HOSTNAME]))
            node_cpuinfo_item.set(NodeHandler.C_STR_RUNNING_THREAD, str(node_data[NodeHandler.C_STR_RUNNING_THREAD]))
                
            # write to xml
            # ET.ElementTree(node_info_root).write(NodeHandler.C_STR_NODE_CPUINFO_FILE, encoding='UTF-8')
                
                
    # serialize data as node_cpuinfo.xml
    def __serialize_data(self):
        # write to xml
        # serialize CPU INFO
        if NodeMonitor._s_node_cpuinfo != None:
            print('do: serialize data')
            ET.ElementTree(NodeMonitor._s_node_cpuinfo).write(NodeHandler.C_STR_NODE_CPUINFO_FILE, encoding='UTF-8')


    # init node monitor server
    def __init_node_server(self, config):
        if not self._thread_node_listener.is_alive():
        
            # init node monitor instance in node handle
            NodeHandler.set_node_monitor_instance(self)
            
            print('do: starting server...')
            # create socket socketserver TCPServer
            # handle implementation communication between node render and moniotor is in NodeHandler
            self._server_monitor = socketserver.TCPServer((config[NodeMonitor.C_STR_IP], config[NodeMonitor.C_STR_PORT]), NodeHandler)
            self._thread_node_listener = Thread(target=self._server_monitor.serve_forever, daemon=True)
            self._thread_node_listener.start()
            
            
    # get check if file node node_info.xml exist
    # if not exist create it
    def __check_node_info_file(self):
        if not os.path.isfile(NodeMonitor.C_STR_NODE_CPUINFO_FILE):
            
            # create xml parent structure
            node_info = ET.Element(NodeMonitor.C_STR_NODES)
            ET.ElementTree(node_info).write(NodeMonitor.C_STR_NODE_CPUINFO_FILE, encoding='UTF-8')
            
            
    # set server status
    # status should be 0 or 1
    # 0 mean stop
    # 1 mean running
    def set_server_status(self, status):
        if not os.path.isfile(NodeMonitor.C_STR_SERVER_INFO_FILE):
            
            # create file server info file
            server_info = ET.Element(NodeMonitor.C_STR_SERVER)
            server_info.set(NodeMonitor.C_STR_STATUS, str(status))
            
            ET.ElementTree(server_info).write(NodeMonitor.C_STR_SERVER_INFO_FILE, encoding='UTF-8')
            
        else:
            server_info = ET.parse(NodeHandler.C_STR_SERVER_INFO_FILE).getroot()
            
            server_info.set(NodeMonitor.C_STR_STATUS, str(status))
            
            # write to xml
            ET.ElementTree(server_info).write(NodeHandler.C_STR_SERVER_INFO_FILE, encoding='UTF-8')
            
            
    # get status server
    def get_server_status(self):
        server_info = ET.parse(NodeHandler.C_STR_SERVER_INFO_FILE).getroot()
        return int(server_info.attrib[NodeMonitor.C_STR_STATUS])
        
        
    # shutdown server
    def stop_service(self):
        self._server_monitor.shutdown()
        self._is_running = 0
        self.set_server_status(0)
        
        # delete server info
        os.remove(NodeMonitor.C_STR_SERVER_INFO_FILE)
        
        
    # start service
    def start_service(self):
        if not self.is_alive():
            self._is_running = 1
            self.set_server_status(1)
            self.start()
        
if __name__ == '__main__':
    NodeMonitor().start_service()
