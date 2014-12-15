import socketserver
import json
import os
import xml.etree.ElementTree as ET
import time

from Config import Config
from Constants import Constants

class NodeHandler(socketserver.BaseRequestHandler, Constants):

    # Handle node render request
    # override handle method

    # handle NodeRender request and NodeRender reporting result
    def handle(self):
        try:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            
            # decode json string from node render data
            node_info = json.loads(s=self.data.decode('UTF-8'), encoding='UTF-8')
            
            # check info type of node data
            if node_info[NodeHandler.C_STR_DATA_TYPE] == NodeHandler.C_STR_DATA_CPU:
                self.__register_client(self.client_address[0], node_info)
            
            if node_info[NodeHandler.C_STR_DATA_TYPE] == NodeHandler.C_STR_DATA_RENDER:
                print('render data')
            
            # just send back the same data, but upper-cased
            self.request.sendall(bytes('ok', 'utf-8'))
            
        except Exception as e:
            print('exception: error handle data from node render')
            print(e)


    # handle data type C_STR_DATA_CPU
    # update info_node.xml
    # register new ip connected by client
    # if ip address already registered, don't add
    def __register_client(self, ip_addr, node_data):
        if os.path.isfile(NodeHandler.C_STR_NODE_INFO_FILE):
            node_info = ET.parse(NodeHandler.C_STR_NODE_INFO_FILE)
            node_info_root = node_info.getroot()
            
            # find and ip address in node info file
            # if not exist then register it
            # find all node inside nodes tag
            node_info_item = node_info_root.find('.//'+NodeHandler.C_STR_NODE+'/[@'+NodeHandler.C_STR_IP+'=\''+ip_addr+'\']')
            
            # register new node if node not exist
            if node_info_item == None:
                new_node_info_item = ET.SubElement(node_info_root, NodeHandler.C_STR_NODE)
                new_node_info_item.set(NodeHandler.C_STR_IP, ip_addr)
                new_node_info_item.set(NodeHandler.C_STR_MEMORY_FREE, str(node_data[NodeHandler.C_STR_MEMORY_FREE]))
                new_node_info_item.set(NodeHandler.C_STR_CPU_USAGE, str(node_data[NodeHandler.C_STR_CPU_USAGE]))
                new_node_info_item.set(NodeHandler.C_STR_SHARED_LOCATION_ACCESS, str(node_data[NodeHandler.C_STR_SHARED_LOCATION_ACCESS]))
                new_node_info_item.set(NodeHandler.C_STR_MEMORY_USED, str(node_data[NodeHandler.C_STR_MEMORY_USED]))
                new_node_info_item.set(NodeHandler.C_STR_CPU_NUM, str(node_data[NodeHandler.C_STR_CPU_NUM]))
                new_node_info_item.set(NodeHandler.C_STR_LAST_CONNECTED, str(time.time()))
                new_node_info_item.set(NodeHandler.C_STR_OS_PLATFORM, node_data[NodeHandler.C_STR_OS_PLATFORM])
                
                # write to xml
                ET.ElementTree(node_info_root).write(NodeHandler.C_STR_NODE_INFO_FILE, encoding='UTF-8')
            
            # update information if node exist
            else:
                node_info_item.set(NodeHandler.C_STR_MEMORY_FREE, str(node_data[NodeHandler.C_STR_MEMORY_FREE]))
                node_info_item.set(NodeHandler.C_STR_CPU_USAGE, str(node_data[NodeHandler.C_STR_CPU_USAGE]))
                node_info_item.set(NodeHandler.C_STR_SHARED_LOCATION_ACCESS, str(node_data[NodeHandler.C_STR_SHARED_LOCATION_ACCESS]))
                node_info_item.set(NodeHandler.C_STR_MEMORY_USED, str(node_data[NodeHandler.C_STR_MEMORY_USED]))
                node_info_item.set(NodeHandler.C_STR_CPU_NUM, str(node_data[NodeHandler.C_STR_CPU_NUM]))
                node_info_item.set(NodeHandler.C_STR_LAST_CONNECTED, str(time.time()))
                node_info_item.set(NodeHandler.C_STR_OS_PLATFORM, node_data[NodeHandler.C_STR_OS_PLATFORM])
            
                # write to xml
                ET.ElementTree(node_info_root).write(NodeHandler.C_STR_NODE_INFO_FILE, encoding='UTF-8')
                
        else:
            print('invalid: file not found '+NodeHandler.C_STR_NODE_INFO_FILE)
