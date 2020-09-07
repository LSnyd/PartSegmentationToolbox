import numpy as np
import os
import glob
import filecmp
import sys


'''
Creates esseg files for accuracy with smooth transitions between classes 
Requires Objects and corresponding labels per edge
Author: Rana Hanocka / Lisa Schneider

@input: 
    <input_path> path where seg, sseg, train, test folders are placed 

@output:
    esseg files for all objects
    to run it from cmd line:
    python create_sseg.py /home/user/MedMeshCNN/datasets/human_seg/
'''

def get_gemm_edges(faces, export_name_edges):
    """
    gemm_edges: array (#E x 4) of the 4 one-ring neighbors for each edge
    sides: array (#E x 4) indices (values of: 0,1,2,3) indicating where an edge is in the gemm_edge entry of the 4 neighboring edges
    for example edge i -> gemm_edges[gemm_edges[i], sides[i]] == [i, i, i, i]
    """
    edge_nb = []
    edge2key = dict()
    edges = []
    edges_count = 0
    nb_count = []
    for face_id, face in enumerate(faces):
        faces_edges = []
        for i in range(3):
            cur_edge = (face[i], face[(i + 1) % 3])
            faces_edges.append(cur_edge)
        for idx, edge in enumerate(faces_edges):
            edge = tuple(sorted(list(edge)))
            faces_edges[idx] = edge
            if edge not in edge2key:
                edge2key[edge] = edges_count
                edges.append(list(edge))
                edge_nb.append([-1, -1, -1, -1])
                nb_count.append(0)
                edges_count += 1
        for idx, edge in enumerate(faces_edges):
            edge_key = edge2key[edge]
            edge_nb[edge_key][nb_count[edge_key]] = edge2key[faces_edges[(idx + 1) % 3]]
            edge_nb[edge_key][nb_count[edge_key] + 1] = edge2key[faces_edges[(idx + 2) % 3]]
            nb_count[edge_key] += 2
    np.savetxt(export_name_edges, edges, fmt='%i')
    return edge_nb, edges


def load_faces(path):
    with open(path, 'r') as f:
        for line in f:
            inner_list = [vertices.strip() for vertices in line.split(',')]
            gemm_edges.append(inner_list)
    return gemm_edges


def load_labels(path):
    with open(path, 'r') as f:
        content = f.read().splitlines()
        return content

def create_sseg_file(gemms, labels, export_name_seseg):
    gemmlabels = {}
    classes = len(np.unique(labels))
    totaledges = len(gemms)
    sseg = np.zeros([ totaledges, classes])
    for i, edges in enumerate(gemms):
        alllabels = []
        for edge in range(len(edges)):
            lookupEdge = edges[edge]
            label = labels[lookupEdge]
            alllabels.append(label)
        gemmlabels[i] = alllabels

    for i, edges in enumerate(gemms):
            gemmlab = gemmlabels[i]
            uniqueValues, counts = np.unique(gemmlab, return_counts=True)
            for j, label in enumerate(uniqueValues):
                weight = 0.125*counts[j]
                sseg[i][int(label) - 1] = weight
    np.savetxt(export_name_seseg, sseg,  fmt='%1.6f')

def get_obj(file):
    vs, faces = [], []
    f = open(file)
    for line in f:
        line = line.strip()
        splitted_line = line.split()
        if not splitted_line:
            continue

        elif splitted_line[0] == 'v':
            vs.append([float(v) for v in splitted_line[1:4]])
        elif splitted_line[0] == 'f':
            face_vertex_ids = [int(c.split('/')[0]) for c in splitted_line[1:]]

            #Checking if all 3 values available
            assert len(face_vertex_ids) == 3
            #calculate -1 to make sure first index is 0 not 1 (as in obj. file)
            face_vertex_ids = [(ind - 1) if (ind >= 0) else (len(vs) + ind)
                              for ind in face_vertex_ids]
            faces.append(face_vertex_ids)
    f.close()
    faces = np.asarray(faces, dtype=int)
    assert np.logical_and(faces >= 0, faces < len(vs)).all()
    return faces



def create_files(path):
    print("path", glob.glob(os.path.join(path, 'train/*.obj')))
    for filename in glob.glob(os.path.join(path, 'train/*.obj')):
        print(filename)
        basename = os.path.splitext(os.path.basename(filename))[0]
        print(basename)
        label_name = os.path.join(os.path.join(path, 'seg'), basename + '.eseg')
        export_name_seseg = os.path.join(os.path.join(path, 'sseg'), basename + '.seseg')
        export_name_edges = os.path.join(os.path.join(path, 'edges'), basename + '.edges')

        faces = get_obj(filename)
        gemms, edges = get_gemm_edges(faces, export_name_edges)

        if os.path.isfile(label_name):
            labels = load_labels(label_name)
            print(len(labels))
            create_sseg_file(gemms, labels, export_name_seseg)
        else:
            print(label_name, "is no directory")


if __name__ == '__main__':
    create_files(sys.argv[1])