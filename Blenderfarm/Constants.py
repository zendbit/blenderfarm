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
    
    C_NUM_NODE_RENDER_SLEEP_TIME = 0.0001
    
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
    C_STR_THREAD_ACTIVE = 'thread_active'
    
    C_STR_COMPLETED_FRAME = '__completed_frame_info__'
    
    C_STR_TASK_FILE = 'task.json'
    
    C_STR_TASK_FILE_LOCK = 'task.lock'
    
    C_STR_SEND_DATA = 'send_data'
    
    C_NUM_MAX_TILE_QUEUE = 1000
    
    C_STR_STATUS = 'status'
    
    C_STR_NODE_CPUINFO_FILE = 'node_cpuinfo.xml'
    C_STR_SERVER_INFO_FILE = 'server_status.xml'
    
    C_NUM_NODE_MONITOR_SLEEP_TIME = 0.0000005

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
    C_STR_PROTOCOL = 'protocol'
    
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
    C_STR_RESOLUTION_X = 'resolution_x'
    C_STR_RESOLUTION_Y = 'resolution_y'
    
    C_STR_TILE = 'tile'
    C_STR_TILE_POS_X = 'tile_pos_x'
    C_STR_TILE_POS_Y = 'tile_pos_y'
    C_STR_FRAME = 'frame'
    
    C_STR_PNG = 'PNG'
    
    C_STR_BORDER_MIN_X = 'border_min_x'
    C_STR_BORDER_MAX_X = 'border_max_x'
    C_STR_BORDER_MIN_Y = 'border_min_y'
    C_STR_BORDER_MAX_Y = 'border_max_y'
    
    C_NUM_RENDER_SPLIT = 2
    C_NUM_RENDER_SCALE = 1.0

    C_NUM_RENDER_SIZE = C_NUM_RENDER_SCALE / C_NUM_RENDER_SPLIT
    
    C_STR_TIMESTAMP = 'timestamp'
    
    C_STR_INFO_FILE = 'info.xml'
    C_STR_INFO_FILE_LOCK = 'info.lock'
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
    
    C_STR_RENDER_COMPLETED = 'render_completed'
    C_STR_RENDER_UNCOMPLETED = 'render_uncompleted'
    C_STR_NOT_RENDERED = 'not_rendered'
    
    ##################################
    # constants for action parser
    ##################################
    C_STR_ACTION = 'action'
    C_NUM_ACTION_UPDATE_CPUINFO = 1
    C_NUM_ACTION_TASK_REQUEST = 2
    C_NUM_ACTION_RENDER_REPORT = 3
    
    
