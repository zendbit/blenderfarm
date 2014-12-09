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
            if node_info[NodeHandler.DATA_TYPE_ATTR] == NodeHandler.DATA_CPU:
                self.__register_client(self.client_address[0], node_info)
            
            if node_info[NodeHandler.DATA_TYPE_ATTR] == NodeHandler.DATA_RENDER:
                print('render data')
            
            # just send back the same data, but upper-cased
            self.request.sendall(bytes('ok', 'utf-8'))
            
        except Exception as e:
            print('exception: error handle data from node render')
            print(e)


    # handle data type DATA_CPU
    # update info_node.xml
    # register new ip connected by client
    # if ip address already registered, don't add
    def __register_client(self, ip_addr, node_data):
        if os.path.isfile(NodeHandler.NODE_INFO_FILE):
            node_info = ET.parse(NodeHandler.NODE_INFO_FILE)
            node_info_root = node_info.getroot()
            
            # find and ip address in node info file
            # if not exist then register it
            # find all node inside nodes tag
            node_info_item = node_info_root.find('.//'+NodeHandler.NODE_TAG+'/[@'+NodeHandler.IP_ATTR+'=\''+ip_addr+'\']')
            
            # register new node if node not exist
            if node_info_item == None:
                new_node_info_item = ET.SubElement(node_info_root, NodeHandler.NODE_TAG)
                new_node_info_item.set(NodeHandler.IP_ATTR, ip_addr)
                new_node_info_item.set(NodeHandler.MEMORY_FREE_ATTR, str(node_data[NodeHandler.MEMORY_FREE_ATTR]))
                new_node_info_item.set(NodeHandler.CPU_USAGE_ATTR, str(node_data[NodeHandler.CPU_USAGE_ATTR]))
                new_node_info_item.set(NodeHandler.SHARED_LOCATION_ACCESS_ATTR, str(node_data[NodeHandler.SHARED_LOCATION_ACCESS_ATTR]))
                new_node_info_item.set(NodeHandler.MEMORY_USED_ATTR, str(node_data[NodeHandler.MEMORY_USED_ATTR]))
                new_node_info_item.set(NodeHandler.CPU_NUM_ATTR, str(node_data[NodeHandler.CPU_NUM_ATTR]))
                new_node_info_item.set(NodeHandler.LAST_CONNECTED_ATTR, str(time.time()))
                
                # write to xml
                ET.ElementTree(node_info_root).write(NodeHandler.NODE_INFO_FILE, encoding='UTF-8')
            
            # update information if node exist
            else:
                node_info_item.set(NodeHandler.MEMORY_FREE_ATTR, str(node_data[NodeHandler.MEMORY_FREE_ATTR]))
                node_info_item.set(NodeHandler.CPU_USAGE_ATTR, str(node_data[NodeHandler.CPU_USAGE_ATTR]))
                node_info_item.set(NodeHandler.SHARED_LOCATION_ACCESS_ATTR, str(node_data[NodeHandler.SHARED_LOCATION_ACCESS_ATTR]))
                node_info_item.set(NodeHandler.MEMORY_USED_ATTR, str(node_data[NodeHandler.MEMORY_USED_ATTR]))
                node_info_item.set(NodeHandler.CPU_NUM_ATTR, str(node_data[NodeHandler.CPU_NUM_ATTR]))
                node_info_item.set(NodeHandler.LAST_CONNECTED_ATTR, str(time.time()))
            
                # write to xml
                ET.ElementTree(node_info_root).write(NodeHandler.NODE_INFO_FILE, encoding='UTF-8')
                
        else:
            print('invalid: file not found '+NodeHandler.NODE_INFO_FILE)
