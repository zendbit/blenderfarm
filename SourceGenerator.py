import glob
import os
import datetime
import stat
import shutil
import subprocess
from Config import Config


# this file generate .blend into source to be processed
# this will generate folder name, named as file name

class SourceGenerator():

    def __init__(self, config):
        self.__source_folder = config["source_folder"]
        self.__blender_location = config["blender_location"]
        self.__shared_location = config["shared_location"]
        
        self.__get_blend_file()
        
    # get all .blend file
    def __get_blend_file(self):
    
        blend_files = glob.glob(self.__source_folder+'/*.blend')
        
        # check folder is exist or not, if exist rename folder into new backup folder
        # then create new folder with configuration file
        os.umask(0000)
        
        # get current datetime as string
        c_datetime = str(datetime.datetime.today()).replace(' ', '_').replace('.', '_').replace(':', '-')
            
        for blend_file in blend_files:
            
            print('do: generate source ' + blend_file)
            
            # get .blend position from right
            dir_name = blend_file.replace('.blend', '')
            
            # get blend file name
            file_name = blend_file.replace(self.__source_folder, dir_name)
            
            if os.path.isdir(dir_name):
                # rename old directory into .back.backup_time
                os.rename(dir_name, dir_name+'_'+c_datetime+'_back')
                os.mkdir(dir_name, 0o777)
                os.chmod(dir_name, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)  
                shutil.move(blend_file, dir_name)
            else:
                # create directory if not exist
                os.mkdir(dir_name, 0o777)
                os.chmod(dir_name, stat.S_IRWXO|stat.S_IRWXU|stat.S_IRWXG)
                shutil.move(blend_file, dir_name)
                
            # run blender in background to get information
            os.system(self.__blender_location + ' -b ' + file_name + ' -P GetBlendSceneInfo.py')
            
            print('do: generate info.xml for ' + blend_file)
            # move info.xml into dir_name
            shutil.move(os.getcwd() + '/info.xml', dir_name)
            
            print('confirm: generate source success')
