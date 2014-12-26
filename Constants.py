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
    C_STR_LOAD_FACTOR = 'load_factor'
    C_STR_LAST_CONNECTED = 'last_connected'
    C_STR_OS_PLATFORM = 'os_platform'
    C_STR_OS_HOSTNAME = 'os_hostname'
    C_STR_RUNNING_THREAD = 'running_thread'
    
    C_NUM_MAX_FRAME_TO_RENDER_QUEUE = 1000
    
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
    C_STR_OS_PLATFORM = 'os_platform'
    C_STR_OS_FAMILY = 'os_family'
    
    # os family linux or darwin or win
    C_STR_OS_PLATFORM_LINUX = 'linux'
    C_STR_OS_PLATFORM_DARWIN = 'darwin'
    C_STR_OS_PLATFORM_WINDOWS = 'win'
    
    # for define path to shared location unix or windows
    C_STR_OS_FAMILY_UNIX = 'unix'
    C_STR_OS_FAMILY_WINDOWS = 'windows'
    
    C_STR_CONFIG_FILE = 'config.xml'
    
    ######################
    # scene info constants
    ######################
    C_STR_SCENES = 'scenes'
    C_STR_SCENE = 'scene'
    C_STR_NAME = 'name'
    C_STR_FRAME_START = 'frame_start'
    C_STR_FRAME_END = 'frame_end'
    C_STR_FRAME_STEP = 'frame_step'
    C_STR_RENDER_STATUS = 'render_status'
    C_STR_RENDER_PRIORITY = 'render_priority'
    
    C_STR_INFO_FILE = 'info.xml'
    C_STR_FRAME = 'frame'
    C_STR_FORMAT_TYPE = 'format_type'
    C_STR_FRAME_RENDER_STATUS = 'frame_render_status'
    C_STR_ID = 'id'
    C_STR_NODE_HANDLER = 'node_handler'
    C_STR_NEED_TO_RENDER = 'need_to_render'
    
    # status  render of file
    C_NUM_RENDER_START = 1
    C_NUM_RENDER_STOP = 0
    C_STR_RENDER_START = 'render_start'
    C_STR_RENDER_STOP = 'render_stop'
    
    # status render frame
    C_NUM_FRAME_RENDER_COMPLETED = 1
    C_NUM_FRAME_RENDER_UNCOMPLETE = 0
    
    # need to render flag
    C_NUM_NEED_TO_RENDER_TRUE = 1
    C_NUM_NEED_TO_RENDER_FALSE = 0
    
    # render priority
    C_NUM_RENDER_PRIORITY_HIGH = 3
    C_NUM_RENDER_PRIORITY_NORMAL = 2
    C_NUM_RENDER_PRIORITY_LOW = 1
    
    C_STR_RENDER_COMPLETED = 'render_completed'
    C_STR_RENDER_UNCOMPLETED = 'render_uncompleted'
    C_STR_NOT_RENDERED = 'not_rendered'
    
    
