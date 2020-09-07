import numpy as np

V = np.array

def get_edges(faces):
    """
    gemm_edges: array (#E x 4) of the 4 one-ring neighbors for each edge
    sides: array (#E x 4) indices (values of: 0,1,2,3) indicating where an edge is in the gemm_edge entry of the 4 neighboring edges
    for example edge i -> gemm_edges[gemm_edges[i], sides[i]] == [i, i, i, i]
    """
    edge2key = dict()
    edges = []
    edges_count = 0
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
    return edges


def segments(vs, edges):
    all_edge_verts = {}
    for edge_c, edge_group in enumerate(edges):
        edge_verts = np.array([])
        for edge_idx in edge_group:
            edge = vs[edge_idx]
            try:
                edge_verts = np.concatenate((edge_verts, edge))
            except:
                edge_verts = edge
        all_edge_verts[edge_c] = edge_verts
    return all_edge_verts


def parse_obje(obj_file, scale_by):
    vs = []
    faces = []
    edges = []

    def add_to_edges():
        if edge_c >= len(edges):
            for _ in range(len(edges), edge_c + 1):
                edges.append([])
        edges[edge_c].append(edge_v)

    with open(obj_file) as f:
        for line in f:
            line = line.strip()
            splitted_line = line.split()
            if not splitted_line:
                continue
            elif splitted_line[0] == 'v':
                vs.append([float(v) for v in splitted_line[1:]])

            elif splitted_line[0] == 'f':
                try:
                    faces.append([int(c) - 1 for c in splitted_line[1:]])
                except ValueError:
                    faces.append([int(c.split('/')[0]) for c in splitted_line[1:]])
            elif splitted_line[0] == 'e':
                if len(splitted_line) >= 4:
                    edge_v = [int(c) - 1 for c in splitted_line[1:-1]]
                    edge_c = int(splitted_line[-1])
                    add_to_edges()

    vs = V(vs)
    faces = V(faces, dtype=int)
    edges = [V(c, dtype=int) for c in edges]
    if len(edges) == 0:
        edges = get_edges(faces)
        export(obj_file, vs, edges, faces)
    return vs, faces, edges



def export(file, vs, edges, faces ,  vcolor=None):
        with open(file, 'w+') as f:
            for vi, v in enumerate(vs):
                vcol = ' %f %f %f' % (vcolor[vi, 0], vcolor[vi, 1], vcolor[vi, 2]) if vcolor is not None else ''
                f.write("v %f %f %f%s\n" % (v[0], v[1], v[2], vcol))
            for face_id in range(len(faces) - 1):
                f.write("f %d %d %d\n" % (faces[face_id][0] , faces[face_id][1], faces[face_id][2] ))
            for edge in edges:
                f.write("\ne %d %d" % (edge[0] , edge[1]))