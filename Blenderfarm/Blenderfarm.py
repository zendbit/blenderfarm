import base64
import json

# bottle framework
from bottle import Bottle
from bottle import Request
from bottle import request

from Config import Config
from Constants import Constants
from NodeMonitor import NodeMonitor
from RenderTaskManager import RenderTaskManager

'''
    this class handle all entity of renderfarm
    using bottle framework
'''

class Blenderfarm(Bottle):

    def __init__(self):
        Bottle.__init__(self)
        
        # initialize config
        self._config = Config().get_config()
        
        # register routes
        self._register_routes()
        
        # init node monitor
        self._node_monitor = NodeMonitor(self._config)
        
        # init render task manager
        self._task_manager = RenderTaskManager(self._config)
        
        # build cache task render
        self._task_manager.get_scene_to_process()
        
        # start node monitor
        self._node_monitor.start()
        
    # register routes
    # handle routes
    def _register_routes(self):
        self.route(path='/parse', method='GET', callback=self._parse_action)
        self.route(path='/', method='GET', callback=self._parse_action)
    
    # parse action
    # handler request from client
    def _parse_action(self):
        send_data = self._decode_data(self._request().GET.get(Constants.C_STR_SEND_DATA))
        
        if send_data != None:
            # get json object
            send_data = json.loads(send_data)
            
            # update cpu info
            if int(send_data[Constants.C_STR_ACTION]) == Constants.C_NUM_ACTION_UPDATE_CPUINFO:
                self._node_monitor.update_node_cpuinfo(self._request().remote_addr, send_data)
            
            # response request task from node
            if int(send_data[Constants.C_STR_ACTION]) == Constants.C_NUM_ACTION_TASK_REQUEST:
                render_task = self._task_manager.get_render_task()
                
                if render_task:
                    return self._encode_data(render_task)
                else:
                    return self._encode_data('0')
                
            return 1
            
        else:
            return 0
        
    # encode data from node
    def _encode_data(self, data):
        return base64.b64encode(data.encode('UTF-8')).decode('UTF-8')
        
    # decode data from node
    def _decode_data(self, data):
        return base64.b64decode(data).decode('UTF-8')
        
    
    # request helper
    # just call this function to get request environment from client
    def _request(self):
        return Request(request.environ)
    
    # start renderfarm service
    def start_renderfarm(self):
        self.run(host=self._config[Constants.C_STR_IP], port=self._config[Constants.C_STR_PORT])
        
        
if __name__ == '__main__':
    Blenderfarm().start_renderfarm()
    
