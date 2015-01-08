# render tile
# part of frame will render as tile
import bpy
import os
import sys

class RenderTile():
    
    # init parameter
    def __init__(self, output_folder_path, folder_id, scene_name, frame_to_render, border_min_x, border_max_x, border_min_y, border_max_y, tile_pos_x, tile_pos_y):
    
        self._output_folder_path = output_folder_path
        self._folder_id = folder_id
        self._border_min_x = border_min_x
        self._border_max_x = border_max_x
        self._border_min_y = border_min_y
        self._border_max_y = border_max_y
        self._tile_pos_x = tile_pos_x
        self._tile_pos_y = tile_pos_y
        self._frame_to_render = frame_to_render 
        self._scene_name = scene_name
        
    def render_tile(self):
        # use border and crop
        bpy.context.scene.render.use_border = True
        bpy.context.scene.render.use_crop_to_border = True
        
        bpy.context.scene.render.resolution_percentage = 100

        # set context for current frame
        bpy.context.scene.frame_set(self._frame_to_render)
        
        # set border for this tile
        bpy.context.scene.render.border_min_x = self._border_min_x
        bpy.context.scene.render.border_max_x = self._border_max_x
        bpy.context.scene.render.border_min_y = self._border_min_y
        bpy.context.scene.render.border_max_y = self._border_max_y
        
        bpy.ops.render.render()
        RR = "Render Result"
        bpy.data.images[RR].save_render(self._output_folder_path\
            + os.path.sep\
            + self._folder_id\
            + '_'\
            + self._scene_name\
            + '_'\
            + str(self._frame_to_render)\
            + '_'\
            + str(self._tile_pos_x)\
            + '_'\
            + str(self._tile_pos_y)\
            + '.png')

# get python argument

param = sys.argv

try:
    '''
        paramter
        output_folder_path
        folder_id
        frame_to_render
        border_min_x
        border_max_x
        border_min_y
        border_max_y
        tile_pos_x
        tile_pos_y
    '''
    # python parameter
    param_index = param.index('--')
    
    R = RenderTile(param[param_index + 1],\
        param[param_index + 2],\
        param[param_index + 3],\
        int(param[param_index + 4]),\
        float(param[param_index + 5]),\
        float(param[param_index + 6]),\
        float(param[param_index + 7]),\
        float(param[param_index + 8]),\
        int(param[param_index + 9]),\
        int(param[param_index + 10]))
    
    R.render_tile()
    
except Exception as e:
    print('exception: tile render failed')
    print(e)
    
