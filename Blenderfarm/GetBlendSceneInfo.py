import bpy
import xml.etree.ElementTree as ET
import time
import os

# this file pass to blender -b
# to generate file info for blender file information in xml format
class GetBlendSceneInfo():

    C_STR_SCENES = 'scenes'
    C_STR_SCENE = 'scene'
    C_STR_NAME = 'name'
    C_STR_FRAME_START = 'frame_start'
    C_STR_FRAME_END = 'frame_end'
    C_STR_FRAME_STEP = 'frame_step'
    C_STR_RENDER_STATUS = 'render_status'
    C_STR_NEED_TO_RENDER = 'need_to_render'
    C_STR_RENDER_PRIORITY = 'render_priority'
    C_STR_RESOLUTION_X = 'resolution_x'
    C_STR_RESOLUTION_Y = 'resolution_y'
    C_NUM_RENDER_SPLIT = 4
    C_NUM_RENDER_SCALE = 1.0
    C_NUM_RENDER_SIZE = C_NUM_RENDER_SCALE / C_NUM_RENDER_SPLIT
    C_STR_STATUS = 'status'
    C_STR_PNG = 'PNG'
    C_STR_BORDER_MIN_X = 'border_min_x'
    C_STR_BORDER_MAX_X = 'border_max_x'
    C_STR_BORDER_MIN_Y = 'border_min_y'
    C_STR_BORDER_MAX_Y = 'border_max_y'
    C_STR_TILE = 'tile'
    C_STR_TILE_POS_X = 'tile_pos_x'
    C_STR_TILE_POS_Y = 'tile_pos_y'
    C_STR_TIMESTAMP = 'timestamp'
    
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
    
        # check modifier for simulation
        # if simulation type generate bake cache
        # generate bake for physic simulation
        bake = False
        ocean_bake = False
        
        for scene in bpy.data.scenes:
            for object in scene.objects:
                for modifier in object.modifiers:
                
                    if modifier.type == 'CLOTH' or modifier.type == 'SOFT_BODY':
                        modifier.point_cache.use_disk_cache = True
                        bake = True
                        
                    if modifier.type == 'SMOKE':
                        modifier.domain_settings.point_cache.use_external = True
                        bake = True
                        
                    if modifier.type == 'DYNAMIC_PAINT':
                        if len(modifier.canvas_settings.canvas_surfaces):
                            bake = True
                            
                    if modifier.type == 'PARTICLE_SYSTEM':
                        modifier.particle_system.point_cache.use_disk_cache = True
                        bake = True
                        
                    if modifier.type == 'OCEAN':
                        modifier.particle_system.point_cache.use_disk_cache = True
                        ocean_bake = True
                        
                    if modifier.type == 'COLLISION'\
                        or modifier.type == 'FLUID_SIMULATION'\
                        or modifier.type == 'COLLISION'\
                        or modifier.type == 'PARTICLE_INSTANCE'\
                        or modifier.type == 'EXPLODE':
                        bake = True
            
        # bake all phy simulation
        bpy.ops.ptcache.free_bake_all()
        if bake:
            bpy.ops.ptcache.bake_all(bake=True)
        if ocean_bake:
            bpy.ops.object.ocean_bake(free=False)
            
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, check_existing=False)
        
        # delete backup saved file
        os.remove(bpy.data.filepath + '1')
        
        scene_info = ET.Element(GetBlendSceneInfo.C_STR_SCENES)
        for scene in bpy.data.scenes:
            scene_item = ET.SubElement(scene_info, GetBlendSceneInfo.C_STR_SCENE)
            scene_item.set(GetBlendSceneInfo.C_STR_NAME, scene.name)
            scene_item.set(GetBlendSceneInfo.C_STR_FRAME_START, str(scene.frame_start))
            scene_item.set(GetBlendSceneInfo.C_STR_FRAME_END, str(scene.frame_end))
            scene_item.set(GetBlendSceneInfo.C_STR_FRAME_STEP, str(scene.frame_step))
            scene_item.set(GetBlendSceneInfo.C_STR_RENDER_STATUS, str(0))
            scene_item.set(GetBlendSceneInfo.C_STR_RESOLUTION_X, str(bpy.context.scene.render.resolution_x))
            scene_item.set(GetBlendSceneInfo.C_STR_RESOLUTION_Y, str(bpy.context.scene.render.resolution_y))
            scene_item.set(GetBlendSceneInfo.C_STR_FORMAT_TYPE, GetBlendSceneInfo.C_STR_PNG)
            scene_item.set(GetBlendSceneInfo.C_STR_TIMESTAMP, str(time.time()))
            
            for index in range(scene.frame_start, (scene.frame_end + 1)):
                scene_frame_item = ET.SubElement(scene_item, GetBlendSceneInfo.C_STR_FRAME)
                scene_frame_item.set(GetBlendSceneInfo.C_STR_FRAME_RENDER_STATUS, str(0))
                scene_frame_item.set(GetBlendSceneInfo.C_STR_ID, str(index))
                scene_frame_item.set(GetBlendSceneInfo.C_STR_NEED_TO_RENDER, str(0))
                
                # define tile position border
                # for distributed partial render
                for index_tile_x in range(0, GetBlendSceneInfo.C_NUM_RENDER_SPLIT):
                    for index_tile_y in range(0, GetBlendSceneInfo.C_NUM_RENDER_SPLIT):
                        scene_frame_tile_item = ET.SubElement(scene_frame_item, GetBlendSceneInfo.C_STR_TILE)
                        border_min_x = float("{0:.8f}".format(index_tile_x * GetBlendSceneInfo.C_NUM_RENDER_SIZE))
                        border_max_x = float("{0:.8f}".format(border_min_x + GetBlendSceneInfo.C_NUM_RENDER_SIZE))
                        border_min_y = float("{0:.8f}".format(index_tile_y * GetBlendSceneInfo.C_NUM_RENDER_SIZE))
                        border_max_y = float("{0:.8f}".format(border_min_y + GetBlendSceneInfo.C_NUM_RENDER_SIZE))
                        
                        scene_frame_tile_item.set(GetBlendSceneInfo.C_STR_STATUS, str(0))
                        scene_frame_tile_item.set(GetBlendSceneInfo.C_STR_BORDER_MIN_X, str(border_min_x))
                        scene_frame_tile_item.set(GetBlendSceneInfo.C_STR_BORDER_MAX_X, str(border_max_x))
                        scene_frame_tile_item.set(GetBlendSceneInfo.C_STR_BORDER_MIN_Y, str(border_min_y))
                        scene_frame_tile_item.set(GetBlendSceneInfo.C_STR_BORDER_MAX_Y, str(border_max_y))
                        scene_frame_tile_item.set(GetBlendSceneInfo.C_STR_TILE_POS_X, str(index_tile_x))
                        scene_frame_tile_item.set(GetBlendSceneInfo.C_STR_TILE_POS_Y, str(index_tile_y))
                    
        ET.ElementTree(scene_info).write(GetBlendSceneInfo.C_STR_INFO_FILE, encoding='UTF-8')
            
GetBlendSceneInfo()
