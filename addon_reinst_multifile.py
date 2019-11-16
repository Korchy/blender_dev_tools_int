# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_dev_tools_int
#
# Script for easy reinstalling multifile Blender 3D add-ons from source directory
#
#   This version is for Blender 2.8
#

import json
import tempfile
import os
import shutil
import glob
import bpy
import sys

# --- required custom parameters ------------

addon_name = 'blender-wire'  # type here add-on name (source directory name)         Ex: addon_name = 'my_addoon'
source_path = 'i:/dev/python/blender'  # type here full path to add-on source directory        Ex: source_path = '/dev/blender/'
files_mask = ['*.py', 'LICENSE', 'README.md', 'cfg.json']  # add required masks for the add-on files
submodule_mask = ['*.py', 'LICENSE', 'README.md']  # add required masks for the files from git submodules
config_file_name = 'cfg.json'  # config file name
release_path = ''  # type here path to copy add-on archive for release     Ex: release_path = '/dev/blender/releases/'

# -------------------------------------------


def install_addon():
    addon_path = os.path.join(source_path, addon_name)

    # files from main add-on source directory
    files = []
    add_path_by_mask(addon_path, files_mask, files)

    # git submodules
    if os.path.exists(os.path.join(source_path, addon_name, '.gitmodules')):
        with open(os.path.join(source_path, addon_name, '.gitmodules'), 'r') as submodules_file:
            for line in submodules_file.readlines():
                if 'path = ' in line:
                    submodule_dir = line.split(' = ')[1].strip()
                    add_path_by_mask(os.path.join(addon_path, submodule_dir), submodule_mask, files)

    # if cfg.json exists and 'dev_mode' parameter exists - switch to release
    dev_mode = None
    cfg_data = {}
    conf_file_path = os.path.abspath(os.path.join(source_path, addon_name, config_file_name))
    if os.path.exists(conf_file_path):
        with open(conf_file_path) as conf_file:
            cfg_data = json.load(conf_file)
            conf_file.close()
    if 'dev_mode' in cfg_data:
        dev_mode = cfg_data['dev_mode']
        cfg_data['dev_mode'] = False  # change to 'release' mode

    # create archive
    with tempfile.TemporaryDirectory() as temp_dir:

        addon_folder_to_files = os.path.join(temp_dir, addon_name, addon_name)
        addon_folder_to_zip = os.path.join(temp_dir, addon_name)

        os.makedirs(addon_folder_to_files)

        # copy files to temp directory
        for file in files:
            current_file_path = os.path.join(addon_folder_to_files, os.path.relpath(file, addon_path))
            if not os.path.exists(os.path.dirname(current_file_path)):
                os.makedirs(os.path.dirname(current_file_path))
            shutil.copy(file, current_file_path)

        # enable 'release' mode in cfg file
        if config_file_name:
            current_config_file_path = os.path.join(addon_folder_to_files, os.path.relpath(conf_file_path, addon_path))
            with open(current_config_file_path, 'w') as conf_file:
                json.dump(cfg_data, conf_file, indent=4)
                conf_file.close()

        # make zip-archieve
        shutil.make_archive(addon_folder_to_zip, 'zip', addon_folder_to_zip)

        addon_zip_path = addon_folder_to_zip + '.zip'

        # copy release archive for custom directory
        if release_path:
            shutil.copy(addon_zip_path, release_path)

        # remove old add-on version
        # bpy.ops.preferences.addon_disable(module=addon_name)
        bpy.ops.preferences.addon_remove(module=addon_name)
        # remove from memory
        for module in list(sys.modules.keys()):
            if hasattr(sys.modules[module], '__package__'):
                if sys.modules[module].__package__ == addon_name:
                    del sys.modules[module]
        # install add-on
        bpy.ops.preferences.addon_install(filepath=addon_zip_path, overwrite=True)
        # activate add-on
        bpy.ops.preferences.addon_enable(module=addon_name)


def add_path_by_mask(root_path, masks_list, file_list):
    for mask in masks_list:
        for file in glob.glob(os.path.join(root_path, mask)):
            file_list.append(file)


if __name__ == '__main__':
    print('-' * 50)
    install_addon()
    print('-' * 50)
