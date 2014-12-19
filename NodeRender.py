import os
import threading
import time
import socket
import psutil
import json
from threading import Thread
import xml.etree.ElementTree as ET
import sys

from Config import Config
from Constants import Constants

# this class handle client script
# check if shared forlder is exist and write able
# if ho access return fail access shared folder to server
class NodeRender(Thread, Constants):
    
    # initialize config file
    def __init__(self):
        # call constructor parent
        Thread.__init__(self)
        
        self.__is_running = 1
        
        # get local ip addr
        ip_addr = socket.gethostbyname(socket.gethostname())
        
        # set filename status node
        self.__node_status_file = NodeRender.C_STR_NODE_STATUS_FOLDER+'node_status.'+ip_addr+'.xml'
        
        # set node status
        self.set_node_status(1)
        
        # thread each user cpu
        # this will automatically alocated
        self.__render_threads = []
        self.__init_render_threads();
        
    # run method thread
    def run(self):
        while self.__is_running:
            try:
            
                # check node status
                # if 0 shutdown node render
                if not self.get_node_status():
                    self.stop_service()
                    
                # get configuration, check if configuration is changed
                config = Config().get_config()
                
                if len(config):
                    print('do: send node info..')
                    self.__send_node_info(config)
                     
                # print error if configuration file not found
                else:
                    print('invalid check: configuration file:config.xml')
            
            except Exception as e:
                print('exception: error while connecting to server')
                print(e)
                
            time.sleep(NodeRender.C_NUM_NODE_RENDER_SLEEP_TIME)
        
    
    # initialize thread processor
    # this will allocate thread for each cpu count
    # max thread instance for render process is equal with cpu count
    def __init_render_threads(self):
        self.__render_threads = []
        
        # init each processor with None value
        # number processor is equals to cpu count
        for index in range(0, psutil.cpu_count()):
            self.__render_threads.append(None)
            
    # check how many render threads are running
    def __get_render_threads_running_count(self):
        count = 0
        for processor in self.__render_threads:
            if processor.__class__.__name__ == 'Thread'\
                and processor.isAlive():
                count += 1
        
        return count
        
    # get available render thread
    # will return in list available thread
    # if all thread is active will return empty list []
    def __get_available_render_threads(self):
        render_threads = []
        
        # collect available render thread
        index = 0
        for processor in self.__render_threads:
            if (processor.__class__.__name__ == 'Thread'\
                and not processor.isAlive()) or processor == None:
                render_threads.append[index]
                
            index += 1
            
        return render_threads
    
    # send message to server
    # report client process to server
    def __send_message(self, ip_addr, port, message):
        data = message

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to server and send data
            sock.connect((ip_addr, port))
            sock.sendall(bytes(data + '\n', 'utf-8'))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), 'utf-8')
            
        finally:
            sock.close()

        print('Sent:     {}'.format(data))
        print('Received: {}'.format(received))
        
    # send node information
    def __send_node_info(self, config):
        self.__send_message(config[NodeRender.C_STR_IP], config[NodeRender.C_STR_PORT], json.dumps(self.__get_node_info(config)))
    
    # get cpu information
    def __get_node_info(self, config):
    
        node_info = {}
    
        # add cpu report type as status cpu infomation
        node_info[NodeRender.C_STR_DATA_TYPE] = NodeRender.C_STR_DATA_CPU
        
        # get cpu count
        node_info[NodeRender.C_STR_CPU_NUM] = psutil.cpu_count()
        
        # get per cpu utilization
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        node_info[NodeRender.C_STR_CPU_USAGE] = cpu_usage
        
        # get average cpu load
        node_info[NodeRender.C_STR_CPU_USAGE_AVR] = sum(cpu_usage)/len(cpu_usage)
        
        # get memory usage
        node_info[NodeRender.C_STR_MEMORY_USED] = psutil.phymem_usage().used
        node_info[NodeRender.C_STR_MEMORY_FREE] = psutil.phymem_usage().free
        
        # get os platform from client
        node_info[NodeRender.C_STR_OS_PLATFORM] = sys.platform
        
        # get os name from client
        node_info[NodeRender.C_STR_OS_HOSTNAME] = socket.gethostname()
        
        # get total thread running from client
        node_info[NodeRender.C_STR_RUNNING_THREAD] = self.__get_render_threads_running_count()
        
        if os.access(config[NodeRender.C_STR_SHARED], os.W_OK):
            # add access shared location info
            node_info[NodeRender.C_STR_SHARED_LOCATION_ACCESS] = NodeRender.C_NUM_SHARED_WRITE_OK
                        
        else:
            # add access shared locaiton info
            node_info[NodeRender.C_STR_SHARED_LOCATION_ACCESS] = NodeRender.C_NUM_SHARED_WRITE_NONE
        
        return node_info
        
    # set node status
    # status should be 0 or 1
    # 0 mean stop
    # 1 mean running
    def set_node_status(self, status):
        if not os.path.isfile(self.__node_status_file):
            
            # create file server info file
            node_status = ET.Element(NodeRender.C_STR_NODE)
            node_status.set(NodeRender.C_STR_STATUS, str(status))
            
            ET.ElementTree(node_status).write(self.__node_status_file, encoding='UTF-8')
            
        else:
            node_status = ET.parse(self.__node_status_file).getroot()
            
            node_status.set(NodeRender.C_STR_STATUS, str(status))
            
            # write to xml
            ET.ElementTree(node_status).write(self.__node_status_file, encoding='UTF-8')
            
    # get status node
    def get_node_status(self):
        node_info = ET.parse(self.__node_status_file).getroot()
        return int(node_info.attrib[NodeRender.C_STR_STATUS])
        
    # start service
    def start_service(self):
        if not self.is_alive():
            self.__is_running = 1
            self.start()
            self.set_node_status(1)
            
    # stop service
    def stop_service(self):
        self.__is_running = 0
        self.set_node_status(0)
        
        # delete server info
        os.remove(self.__node_status_file)
            
# launcher
if __name__ == '__main__':
    NodeRender().start_service()
