# Blender 3D Development tools Int.
Tools for Blender 3D developement.

**addon_reinst**
---
Script for easy installation / reinstallation developed add-on.

**File versions**

addon_reinst.py - for Blender 2.8 (2019.03.06)

addon_reinst_2_7.py - for Blender 2.7

**Usage:**
- Copy script to the Blender Text Editor
- Specify requred parameters in the special section
    - addon_name - name of the add-on source directory
    - source_path - full path to the add-on source (without directory name)
    - files_mask - add here required to your add-on file masks. All files matches that masks would be included to the add-on installation
    - release_path - path to the directory to copy here zip-archive completed to distribution.
- Press the "Run Script" button
- Now your add-on is installed in Blender
- Make changes to add-on sources
- Just press the "Run Script" button again
- Now your add-on is reinstalled with last changes
