'''
Prints segmentation to object in Blender
Requires Blender 2.8
Author: Lisa Schneider

@input:
    Object and labels per edge for 4 classes

@output:
    Object colored segmentation with 4 different classes
'''


import numpy as np

labels_path = '/home/user/MedMeshCNN/seg/{}.eseg'

group = bpy.context.object.vertex_groups.new(name="1")
group = bpy.context.object.vertex_groups.new(name="2")
group = bpy.context.object.vertex_groups.new(name="3")
group = bpy.context.object.vertex_groups.new(name="4")

#Assign material to vertex group
red = bpy.data.materials.new(name='red')
bpy.context.object.data.materials.append(red)
yellow = bpy.data.materials.new(name='yellow')
bpy.context.object.data.materials.append(yellow)
blue = bpy.data.materials.new(name='blue')
bpy.context.object.data.materials.append(blue)
green = bpy.data.materials.new(name='green')
bpy.context.object.data.materials.append(green)



obdata = bpy.context.object.data
active_object = bpy.context.active_object
vertex_groups = active_object.vertex_groups[:]

input = labels_path.format(bpy.context.active_object.data.name)
seg_labels = np.loadtxt(open(input, 'r'), dtype='int')
faces_edges = []
edges = []
edge2key = {}
edge_nb = []
edges_count = 0
nb_count = []


dict = {"1": [],
"2": [],
"3": [],
"4": [],
 }

for face in obdata.polygons: 
     vert = [face.vertices[0],face.vertices[1],face.vertices[2]]
     for i in range(3):
            cur_edge = (vert[i], vert[(i + 1) % 3])
            faces_edges.append(cur_edge)

for idx, edge in enumerate(faces_edges):
     edge = tuple(sorted(list(edge)))
     faces_edges[idx] = edge
     if edge not in edge2key:
            edge2key[edge] = edges_count
            edges.append(list(edge))

#edge labels
for idx, edge in enumerate(edges):
 group = str(seg_labels[idx]) 
 print(idx,group, edge, idx)
 dict[group].append(edge[0])
 dict[group].append(edge[1])


bpy.ops.object.mode_set(mode='OBJECT')

for vertex_group in vertex_groups:
 indices = vertex_group.name
 result = dict[indices]
 vertex_group.add(result, 1.0, 'ADD')


bpy.data.materials['red'].diffuse_color = (0.938686, 0.0069953, 0.0122865, 1)
bpy.data.materials['yellow'].diffuse_color = (1, 0.346704, 0.0116123, 1)
bpy.data.materials['blue'].diffuse_color = (0.0116122, 0.0742136, 0.799103, 1)
bpy.data.materials['green'].diffuse_color = (0.0684782, 0.439657, 0.0129831, 1)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.object.vertex_group_deselect()

for i in range(1,5):
 bpy.ops.object.vertex_group_set_active(group=str(i))
 bpy.ops.object.vertex_group_select()
 bpy.context.object.active_material_index = i
 bpy.ops.object.material_slot_assign()
 bpy.ops.object.vertex_group_deselect()
