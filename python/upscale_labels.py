import numpy as np
import glob
import os
from scipy import spatial
from helpers import parse_obje, segments, export
from tempfile import mkstemp
from shutil import move
import sys




def map_labels(file_low, file_high):
    # parse objects
    vs_low, faces_low, edges_low = parse_obje(file_low, 0)
    vs_high, faces_high, edges_high = parse_obje(file_high, 0)

    # get labels
    labels = segments(vs_low, edges_low)

    # Reverse key, value in dict
    new_labels_dict = {}
    for k, v in labels.items():
        for i in v:
            new_labels_dict[str(i)] = k

    #build kdtree
    labelled = np.vstack([item[1] for item in labels.items()])
    tree = spatial.KDTree(labelled)

    # Get nn
    nn = [np.asarray(labelled[tree.query(coords)[1]]) for coords in vs_high]
    uplabels_verts = [new_labels_dict.get(str(coords)) for coords in nn ]

    #for edges_high1 in edges_high:
    edges_higher = [ [int(c) - 1 for c in edges_high1] for edges_high1 in edges_high ]


    uplabel_edges = [ uplabels_verts[edge[0]] for edge in edges_higher]

    return uplabel_edges



def export_segments(file, segments):
            cur_segments = segments
            fh, abs_path = mkstemp()
            edge_key = 0
            with os.fdopen(fh, 'w') as new_file:
                with open(file) as old_file:
                    for line in old_file:
                        if line[0] == 'e':
                            new_file.write('%s %d' % (line.strip(),  cur_segments[edge_key]))
                            if edge_key < len(cur_segments):
                                edge_key += 1
                                new_file.write('\n')
                        else:
                            new_file.write(line)
            os.remove(file)
            move(abs_path, file)

def mapping(path_segmentation, path_target):
    for file_low in glob.glob(os.path.join(path_segmentation, '*.obj')):
        basename = os.path.splitext(os.path.basename(file_low))[0] + '.obj'
        basename = basename.replace("_0", "")
        file_high = path_target + basename

        if os.path.isfile(file_high):
            uplabels = map_labels(file_low, file_high)
            export_segments(file_high, uplabels)


if __name__ == '__main__':
    mapping(sys.argv[1], sys.argv[2])
