import socketserver
import json
import os
import xml.etree.ElementTree as ET
import time
import threading
import base64

from Config import Config
from Constants import Constants

class NodeHandler(socketserver.BaseRequestHandler, Constants):

    # Handle node render request
    # override handle method

    # NodeMonitor instance
    _NODE_MONITOR_INSTANCE = None

    # handle NodeRender request and NodeRender reporting result
    def handle(self):
        try:
            # self.request is the TCP socket connected to the client
            self.data = base64.b64decode(self.request.recv(1024).strip())
            
            # decode json string from node render data
            node_info = json.loads(s=self.data.decode('UTF-8'), encoding='UTF-8')
            
            # check info type of node data
            # handle with multithread
            if node_info[NodeHandler.C_STR_DATA_TYPE] == NodeHandler.C_STR_DATA_CPU:
                threading.Thread(target=NodeHandler._NODE_MONITOR_INSTANCE.update_node_cpuinfo, args=(self.client_address[0], node_info)).start()
            
            if node_info[NodeHandler.C_STR_DATA_TYPE] == NodeHandler.C_STR_DATA_RENDER:
                print('render data')
            
            # self.request.sendall(bytes('ok', 'UTF-8'))
            self.request.sendall(base64.b64encode('ok'.encode('UTF-8')))
            
        except Exception as e:
            print('exception: error handle data from node render')
            print(e)
            
    @staticmethod
    def set_node_monitor_instance(node_monitor_obj):
        NodeHandler._NODE_MONITOR_INSTANCE = node_monitor_obj
