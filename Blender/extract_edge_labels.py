
import bpy
import numpy as np

'''
Extracts edge labels from segmentation via Blender 
Requires Blender 2.8
Author: Lisa Schneider

@input: 
    Segmented object in Blender

@output:
    .txt file with labels per edge
    to run it insert into Blender console after segmenting the object
'''

verticeGroups = {}
edgeLabels = []
faceLabels = []
edges = []
faces_edges = []
edge_nb = []
edge2key = {}
edges_count = 0
nb_count = []
edge_path = '/home/user/MedMeshCNN/human_seg/edges/{}.edges'
eseg_path = '/home/user/MedMeshCNN/human_seg/seg/{}.eseg'

ob = bpy.context.object
obdata = bpy.context.object.data

vgroup_names = {vgroup.index: vgroup.name for vgroup in ob.vertex_groups}
vgroups = {v.index: [vgroup_names[g.group] for g in v.groups] for v in obdata.vertices}

#get group for vertices; save in dict
for idx in range(len(obdata.vertices)):
    group = vgroups[idx]
    verticeGroups[idx] = group

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

np.savetxt(edge_path.format(bpy.context.active_object.name), edges, delimiter=',',fmt='%s')



#each edge made of two vertices; get group of first vertice
for idx, edge in enumerate(edges):
      vertix = edge[1]
      groups = verticeGroups[vertix]
      if len(groups) == 2:
         edgeLabels.append(groups[1])
      else:
         edgeLabels.append(groups[0])

np.savetxt(eseg_path.format(bpy.context.active_object.name), edgeLabels, delimiter=',',fmt='%s')


