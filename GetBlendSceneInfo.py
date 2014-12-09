import bpy
import xml.etree.ElementTree as ET

# this file pass to blender -b
# to generate file info for blender file information in xml format
class GetBlendSceneInfo():

    SCENES_TAG = 'scenes'
    SCENE_TAG = 'scene'
    SCENE_NAME_ATTR = 'name'
    SCENE_FRAME_START_ATTR = 'frame_start'
    SCENE_FRAME_END_ATTR = 'frame_end'
    SCENE_FRAME_STEP_ATTR = 'frame_step'
    
    
    def __init__(self):
        self.__get_scene_info()
        self.__info_scene_file = 'info.xml'
        
    # get scene information
    # get scene name
    # get scene frame_start
    # get scene frame_end
    # get scene frame_step
    def __get_scene_info(self):
        scene_info = ET.Element(GetBlendSceneInfo.SCENES_TAG)
        for scene in bpy.data.scenes:
            scene_item = ET.SubElement(scene_info, GetBlendSceneInfo.SCENE_TAG)
            scene_item.set(GetBlendSceneInfo.SCENE_NAME_ATTR, scene.name)
            scene_item.set(GetBlendSceneInfo.SCENE_FRAME_START_ATTR, str(scene.frame_start))
            scene_item.set(GetBlendSceneInfo.SCENE_FRAME_END_ATTR, str(scene.frame_end))
            scene_item.set(GetBlendSceneInfo.SCENE_FRAME_STEP_ATTR, str(scene.frame_step))
            
        ET.ElementTree(scene_info).write(self.__info_scene_file, encoding='UTF-8')
            
GetBlendSceneInfo()
