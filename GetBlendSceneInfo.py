import bpy
import xml.etree.ElementTree as ET

# this file pass to blender -b
# to generate file info for blender file information in xml format
class GetBlendSceneInfo():

    C_STR_SCENES = 'scenes'
    C_STR_SCENE = 'scene'
    C_STR_SCENE_NAME = 'name'
    C_STR_SCENE_FRAME_START = 'frame_start'
    C_STR_SCENE_FRAME_END = 'frame_end'
    C_STR_SCENE_FRAME_STEP = 'frame_step'
    C_STR_INFO_FILE = 'info.xml'
    C_STR_FRAME = 'frame'
    C_STR_FORMAT_TYPE = 'format_type'
    C_STR_FRAME_RENDER_STATUS = 'frame_render_status'
    C_STR_ID = 'id'
    C_STR_NODE_HANDLER = 'node_handler'
    
    
    def __init__(self):
        self.__get_scene_info()
        
    # get scene information
    # get scene name
    # get scene frame_start
    # get scene frame_end
    # get scene frame_step
    def __get_scene_info(self):
        scene_info = ET.Element(GetBlendSceneInfo.C_STR_SCENES)
        for scene in bpy.data.scenes:
            scene_item = ET.SubElement(scene_info, GetBlendSceneInfo.C_STR_SCENE)
            scene_item.set(GetBlendSceneInfo.C_STR_SCENE_NAME, scene.name)
            scene_item.set(GetBlendSceneInfo.C_STR_SCENE_FRAME_START, str(scene.frame_start))
            scene_item.set(GetBlendSceneInfo.C_STR_SCENE_FRAME_END, str(scene.frame_end))
            scene_item.set(GetBlendSceneInfo.C_STR_SCENE_FRAME_STEP, str(scene.frame_step))
            
            for index in range(scene.frame_start, (scene.frame_end + 1)):
                scene_frame_item = ET.SubElement(scene_item, GetBlendSceneInfo.C_STR_FRAME)
                scene_frame_item.set(GetBlendSceneInfo.C_STR_FORMAT_TYPE, '')
                scene_frame_item.set(GetBlendSceneInfo.C_STR_FRAME_RENDER_STATUS, str(0))
                scene_frame_item.set(GetBlendSceneInfo.C_STR_ID, str(index))
                scene_frame_item.set(GetBlendSceneInfo.C_STR_NODE_HANDLER, str(0))
            
        ET.ElementTree(scene_info).write(GetBlendSceneInfo.C_STR_INFO_FILE, encoding='UTF-8')
            
GetBlendSceneInfo()
