# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_dev_tools_int
#
# Script for easy reinstalling single files Blender 3D add-ons from source directory

import bpy
import os
import sys

# --- required custom parameters ------------

filepath = ''   # type here full path to the add-on     Ex: filepath = '/dev/blender/test_addon'
filename = ''   # type here the add-on name             Ex: filename = 'test'

# -------------------------------------------


def install_addon():
    # remove old add-on version
    bpy.ops.preferences.addon_remove(module=filename)
    # remove from memory
    for module in list(sys.modules.keys()):
        if module == filename:
            del sys.modules[filename]
    # install new version
    bpy.ops.preferences.addon_install(filepath=os.path.join(filepath, filename + '.py'), overwrite=True)
    # activate add-on
    bpy.ops.preferences.addon_enable(module=filename)


if __name__ == '__main__':
    print('-'*50)
    install_addon()
    print('-'*50)
