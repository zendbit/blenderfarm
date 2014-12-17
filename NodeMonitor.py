import os
import threading
from threading import Thread
import xml.etree.ElementTree as ET
import time
import socketserver

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
    __S_NODE_CPUINFO = None # cpu node information
    __S_NODE_RENDERINFO = None # render node information
    
    
    # initialize config file
    def __init__(self):
        # call constructor parent
        Thread.__init__(self)
        self.__thread_node_listener = Thread()
        self.__server_monitor = None
        
        # server flags running
        self.__is_running = 1
        
        # set server monitor
        # 1 is running state
        self.set_server_status(1)
        
        
    # run method thread
    def run(self):
        while self.__is_running:
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
            
            
    # node info manipulator
    # update only from this method
    # this is static method
    # call via NodeMonitor.update_node_cpuinfo
    @staticmethod
    def update_node_cpuinfo(ip_addr, node_data):
        # check if __S_NODE_CPUINFO is None
        # if None init with NodeHandler.C_STR_NODE_CPUINFO_FILE
        # if NodeHandler.C_STR_NODE_CPUINFO_FILE Not Exist init with ET.Element(NodeHandler.C_STR_NODES)
        if NodeMonitor.__S_NODE_CPUINFO == None:
            if os.path.isfile(NodeHandler.C_STR_NODE_CPUINFO_FILE):
                NodeMonitor.__S_NODE_CPUINFO = ET.parse(NodeHandler.C_STR_NODE_CPUINFO_FILE).getroot()
            else:
                NodeMonitor.__S_NODE_CPUINFO = ET.Element(NodeHandler.C_STR_NODES)
                
        else:
            # find and ip address in node info file
            # if not exist then register it
            # find all node inside nodes tag
            node_cpuinfo_item = NodeMonitor.__S_NODE_CPUINFO.find('.//'+NodeHandler.C_STR_NODE+'/[@'+NodeHandler.C_STR_IP+'=\''+ip_addr+'\']')
        
            # register new node if node not exist
            if node_cpuinfo_item == None:
                node_cpuinfo_item = ET.SubElement(NodeMonitor.__S_NODE_CPUINFO, NodeHandler.C_STR_NODE)
                node_cpuinfo_item.set(NodeHandler.C_STR_IP, ip_addr)
                
            node_cpuinfo_item.set(NodeHandler.C_STR_MEMORY_FREE, str(node_data[NodeHandler.C_STR_MEMORY_FREE]))
            node_cpuinfo_item.set(NodeHandler.C_STR_CPU_USAGE, str(node_data[NodeHandler.C_STR_CPU_USAGE]))
            node_cpuinfo_item.set(NodeHandler.C_STR_SHARED_LOCATION_ACCESS, str(node_data[NodeHandler.C_STR_SHARED_LOCATION_ACCESS]))
            node_cpuinfo_item.set(NodeHandler.C_STR_MEMORY_USED, str(node_data[NodeHandler.C_STR_MEMORY_USED]))
            node_cpuinfo_item.set(NodeHandler.C_STR_CPU_NUM, str(node_data[NodeHandler.C_STR_CPU_NUM]))
            node_cpuinfo_item.set(NodeHandler.C_STR_LAST_CONNECTED, str(time.time()))
            node_cpuinfo_item.set(NodeHandler.C_STR_OS_PLATFORM, node_data[NodeHandler.C_STR_OS_PLATFORM])
            node_cpuinfo_item.set(NodeHandler.C_STR_OS_HOSTNAME, node_data[NodeHandler.C_STR_OS_HOSTNAME])
                
            # write to xml
            # ET.ElementTree(node_info_root).write(NodeHandler.C_STR_NODE_CPUINFO_FILE, encoding='UTF-8')
                
                
    # serialize data as node_cpuinfo.xml
    def __serialize_data(self):
        # write to xml
        # serialize CPU INFO
        if NodeMonitor.__S_NODE_CPUINFO != None:
            print('do: serialize data')
            ET.ElementTree(NodeMonitor.__S_NODE_CPUINFO).write(NodeHandler.C_STR_NODE_CPUINFO_FILE, encoding='UTF-8')


    # init node monitor server
    def __init_node_server(self, config):
        if not self.__thread_node_listener.is_alive():
        
            # init node monitor instance in node handle
            NodeHandler.set_node_monitor_instance(self)
            
            print('do: starting server...')
            # create socket socketserver TCPServer
            # handle implementation communication between node render and moniotor is in NodeHandler
            self.__server_monitor = socketserver.TCPServer((config[NodeMonitor.C_STR_IP], config[NodeMonitor.C_STR_PORT]), NodeHandler)
            self.__thread_node_listener = Thread(target=self.__server_monitor.serve_forever, daemon=True)
            self.__thread_node_listener.start()
            
            
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
        self.__server_monitor.shutdown()
        self.__is_running = 0
        self.set_server_status(0)
        
        # delete server info
        os.remove(NodeMonitor.C_STR_SERVER_INFO_FILE)
        
        
    # start service
    def start_service(self):
        if not self.is_alive():
            self.__is_running = 1
            self.set_server_status(1)
            self.start()
        
if __name__ == '__main__':
    NodeMonitor().start_service()
