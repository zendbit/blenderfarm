from threading import Thread
import json

# this class is node render thread processor
# each time render command assigned from NodeMonitor
# should find available thread before assign render command to this class

class NodeRenderThread(Thread):

    # constructor
    # init NodeObject Reference
    def __init__(self, node_monitor_obj):
        
        self._node_monitor_obj = node_monitor_obj
        self._node_render_data_cmd = ''
        
        
    # set data to render
    # data is send from node monitor
    # will assign here through node render
    # data_cmd is from node render, distribute by node monitor
    def set_render_data_cmd(self, data_cmd):
        self._node_render_data_cmd = data_cmd
    
    # override thread run method
    def run(self):
        pass
