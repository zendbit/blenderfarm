import glob
import os
import datetime
import stat
import shutil
import subprocess
from Config import Config

from Constants import Constants

# this file generate .blend into source to be processed
# this will generate folder name, named as file name

class SourceGenerator():

    def __init__(self, config):
        self._config = config
        
    def check_blend_file(self):
        self._get_blend_file()
        
    # get all .blend file
    def _get_blend_file(self):
    
        blend_files = glob.glob(self._config[Constants.C_STR_SOURCE] + os.path.sep + '*.blend')
        
        # check folder is exist or not, if exist rename folder into new backup folder
        # then create new folder with configuration file
        os.umask(0000)
        
        # get current datetime as string
        c_datetime = str(datetime.datetime.today()).replace(' ', '_').replace('.', '_').replace(':', '-')
            
        for blend_file in blend_files:
            
            print('do: generate source ' + blend_file)
            
            # get .blend position from right
            # define dir_name
            # define frames_dir_name
            # define tiles_dir_name
            dir_name = blend_file.replace('.blend', '')
            frames_dir_name = dir_name + os.path.sep + Constants.C_STR_FRAME
            tiles_dir_name = dir_name + os.path.sep + Constants.C_STR_TILE
            
            # get blend file name
            file_name = blend_file.replace(self._config[Constants.C_STR_SOURCE], dir_name)
            
            if os.path.isdir(dir_name):
                # rename old directory into .back.backup_time
                os.rename(dir_name, dir_name+'_'+c_datetime+'.backup')
                os.mkdir(dir_name, 0o777)
                os.chmod(dir_name, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)
                shutil.move(blend_file, dir_name)
            else:
                # create directory if not exist
                os.mkdir(dir_name, 0o777)
                os.chmod(dir_name, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)
                shutil.move(blend_file, dir_name)
                
            # create frames directory
            if not os.path.isdir(frames_dir_name):
                os.mkdir(frames_dir_name, 0o777)
                os.chmod(frames_dir_name, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)
                
            # create tiles directory
            if not os.path.isdir(tiles_dir_name):
                os.mkdir(tiles_dir_name, 0o777)
                os.chmod(tiles_dir_name, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)
            
            # create tiles directory
                
            # run blender in background to get information
            subprocess.call(self._config[Constants.C_STR_BLENDER] + ' -b ' + file_name + ' -P GetBlendSceneInfo.py' + ' -t 32 ', shell=True)
            
            print('do: generate info.xml for ' + blend_file)
            # move info.xml into dir_name
            shutil.move(os.getcwd() + os.path.sep + Constants.C_STR_INFO_FILE, dir_name)
            
            print('confirm: generate source success')
