import os
import threading
import time
import socket
import psutil
import json
from threading import Thread
import xml.etree.ElementTree as ET

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
        self.__node_status_file = NodeRender.NODE_STATUS_FOLDER+'node_status.'+ip_addr+'.xml'
        
        # set node status
        self.set_node_status(1)
        
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
                
            time.sleep(NodeRender.NODE_RENDER_SLEEP_TIME)
        
    
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
        self.__send_message(config['server_ip'], config['server_port'], json.dumps(self.__get_node_info(config)))
    
    # get cpu information
    def __get_node_info(self, config):
    
        node_info = {}
        
        # add cpu report type as status cpu infomation
        node_info['data_type'] = NodeRender.DATA_CPU
        
        # get cpu count
        node_info['cpu_num'] = psutil.cpu_count()
        
        # get per cpu utilization
        node_info['cpu_usage'] = psutil.cpu_percent(interval=1, percpu=True)
        
        # get memory usage
        node_info['memory_used'] = psutil.phymem_usage().used
        node_info['memory_free'] = psutil.phymem_usage().free
        
        if os.access(config['shared_location'], os.W_OK):
            # add access shared location info
            node_info['shared_location_access'] = NodeRender.SHARED_WRITE_OK
                        
        else:
            # add access shared locaiton info
            node_info['shared_location_access'] = NodeRender.SHARED_WRITE_NONE
        
        return node_info
        
    # set node status
    # status should be 0 or 1
    # 0 mean stop
    # 1 mean running
    def set_node_status(self, status):
        if not os.path.isfile(self.__node_status_file):
            
            # create file server info file
            node_status = ET.Element(NodeRender.NODE_TAG)
            node_status.set(NodeRender.STATUS_ATTR, str(status))
            
            ET.ElementTree(node_status).write(self.__node_status_file, encoding='UTF-8')
            
        else:
            node_status = ET.parse(self.__node_status_file).getroot()
            
            node_status.set(NodeRender.STATUS_ATTR, str(status))
            
            # write to xml
            ET.ElementTree(node_status).write(self.__node_status_file, encoding='UTF-8')
            
    # get status node
    def get_node_status(self):
        node_info = ET.parse(self.__node_status_file).getroot()
        return int(node_info.attrib[NodeRender.STATUS_ATTR])
        
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
