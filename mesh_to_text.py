import bpy
import json
import os

save_to = 'd:'

active_object = bpy.context.object

file_name = active_object.name
save_to_file = os.path.join(save_to, file_name + '.json')

mesh_data = {
    'vertices': [],
    'faces': [],
    'vert_groups': {}
}

mesh_data['vertices'] = [(vert.co.x, vert.co.y, vert.co.z) for vert in active_object.data.vertices]
mesh_data['faces'] = [[vert for vert in polygon.vertices] for polygon in active_object.data.polygons]

for group in bpy.context.object.vertex_groups:
    mesh_data['vert_groups'].update({group.name: [vert.index for vert in bpy.context.object.data.vertices if group.index in [i.group for i in vert.groups]]})

with open(save_to_file, 'w') as file:
    json.dump(mesh_data, file, indent=4)
