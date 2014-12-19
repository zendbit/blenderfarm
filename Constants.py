# constant class
# hold all constants value

class Constants():
    
    #######################
    # node render constants
    #######################
    # send data report type to server monitor
    C_STR_DATA_CPU = 'node_cpu_info'
    C_STR_DATA_RENDER = 'node_render_info'
    
    # write access to shared flag
    C_NUM_SHARED_WRITE_OK = 1
    C_NUM_SHARED_WRITE_NONE = 0
    
    C_NUM_NODE_RENDER_SLEEP_TIME = 2
    
    C_STR_NODE_STATUS_FOLDER = 'node_status/'
    
    ########################
    # node monitor constants
    ########################
    C_STR_NODES = 'nodes'
    C_STR_NODE = 'node'
    C_STR_MEMORY_FREE = 'memory_free'
    C_STR_CPU_USAGE = 'cpu_usage'
    C_STR_CPU_USAGE_AVR = 'cpu_usage_avr'
    C_STR_SHARED_LOCATION_ACCESS = 'shared_location_access'
    C_STR_DATA_TYPE = 'data_type'
    C_STR_MEMORY_USED = 'memory_used'
    C_STR_CPU_NUM = 'cpu_num'
    C_STR_LAST_CONNECTED = 'last_connected'
    C_STR_OS_PLATFORM = 'os_platform'
    C_STR_OS_HOSTNAME = 'os_hostname'
    C_STR_RUNNING_THREAD = 'running_thread'
    
    C_STR_STATUS = 'status'
    
    C_STR_NODE_CPUINFO_FILE = 'node_cpuinfo.xml'
    C_STR_SERVER_INFO_FILE = 'server_status.xml'
    
    C_NUM_NODE_MONITOR_SLEEP_TIME = 1

    ##################
    # config constants
    ##################
    C_STR_SERVER = 'server'
    C_STR_IP = 'ip'
    C_STR_PORT = 'port'
    C_STR_SHARED = 'shared'
    C_STR_LOCATION = 'location'
    C_STR_BLENDER = 'blender'
    C_STR_SOURCE = 'source'
    C_STR_FOLDER = 'folder'
    C_STR_OUTPUT = 'output'
    
    C_STR_CONFIG_FILE = 'config.xml'
    
    ######################
    # scene info constants
    ######################
    C_STR_SCENES = 'scenes'
    C_STR_SCENE = 'scene'
    C_STR_SCENE_NAME = 'name'
    C_STR_SCENE_FRAME_START = 'frame_start'
    C_STR_SCENE_FRAME_END = 'frame_end'
    C_STR_SCENE_FRAME_STEP = 'frame_step'
    
    
