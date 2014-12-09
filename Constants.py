# constant class
# hold all constants value

class Constants():
    
    #######################
    # node render constants
    #######################
    # send data report type to server monitor
    DATA_CPU = 'node_cpu_info'
    DATA_RENDER = 'node_render_info'
    
    # write access to shared flag
    SHARED_WRITE_OK = 1
    SHARED_WRITE_NONE = 0
    
    NODE_RENDER_SLEEP_TIME = 0.5
    
    NODE_STATUS_FOLDER = 'node_status/'
    
    ########################
    # node monitor constants
    ########################
    NODES_TAG = 'nodes'
    NODE_TAG = 'node'
    MEMORY_FREE_ATTR = 'memory_free'
    CPU_USAGE_ATTR = 'cpu_usage'
    SHARED_LOCATION_ACCESS_ATTR = 'shared_location_access'
    DATA_TYPE_ATTR = 'data_type'
    MEMORY_USED_ATTR = 'memory_used'
    CPU_NUM_ATTR = 'cpu_num'
    LAST_CONNECTED_ATTR = 'last_connected'
    
    STATUS_ATTR = 'status'
    
    NODE_INFO_FILE = 'node_info.xml'
    SERVER_INFO_FILE = 'server_status.xml'
    
    NODE_MONITOR_SLEEP_TIME = 0.05

    ##################
    # config constants
    ##################
    SERVER_TAG = 'server'
    IP_ATTR = 'ip'
    PORT_ATTR = 'port'
    SHARED_TAG = 'shared'
    LOCATION_ATTR = 'location'
    BLENDER_TAG = 'blender'
    SOURCE_TAG = 'source'
    FOLDER_ATTR = 'folder'
    OUTPUT_TAG = 'output'
    
    CONFIG_FILE = 'config.xml'
    
    ######################
    # scene info constants
    ######################
    SCENES_TAG = 'scenes'
    SCENE_TAG = 'scene'
    SCENE_NAME_ATTR = 'name'
    SCENE_FRAME_START_ATTR = 'frame_start'
    SCENE_FRAME_END_ATTR = 'frame_end'
    SCENE_FRAME_STEP_ATTR = 'frame_step'
    
    
