# PartSegmentationToolbox

This toolbox provides helper scripts for the application of [MedMeshCNN](https://github.com/LSnyd/MedMeshCNN) and [MeshCNN](https://ranahanocka.github.io/MeshCNN/). 

It includes Blender scripts that 

* prepare Blender for the manual segmentation (prepare_blender.py)
* extract edge labels from the manual segmentation performend in blender (extract_edge_labels.py)
* prints edge labels to objects in blender (print_segmentation.py)

as well as independent python scripts that

* create sseg files (create_sseg.py)
* map segmentation outputs to meshes of different resolution (e.g. to compensate downsampling) (upscale_labels.py)



# Getting Started


### Installation
- Clone this repo:
```bash
git clone https://github.com/LSnyd/PartSegmentationToolbox.git
cd MedMeshCNN
```
- Install dependencies: [Blender](https://www.blender.org/) version 2.82


# Run Blender scripts 

To run the blender scripts, copy and paste the provided script into the Blender Python Console.
Make sure that you update all path according to your own locations. 

### Prepare Blender for manual segmentation
To prepare Blender for the manual segmentation of an object, insert the prepare_blender.py after opening Blender. 
This script creates 4 vertex groups and maps 4 different colors to the group. If you want to create a segmentation with more classes, alter the script accordingly. 

### Perform a manual segmentation
For the manual segmentation please refer to my medium article here. 

### Extract labels from the manual segmentation (.eseg file)
In order to extract the edge labels from the manual segmentation run insert the content of extract_edge_labels.py into the Blender Python Console. 
This script creates an .eseg file of the object, which includes the class labels per edge ordered after their edge ID. 
Afterwards, it is still necessary to create a .seseg file for your object to run MedMeshCNN or MeshCNN. For this you can refer to the Python section of this toolbox. 


### Print segmentation of .eseg file to your object
The print_segmentation.py script lets you print your .eseg files onto the surface of your mesh. 
Make sure that you always keep the vertex order when importing an object. 



# Run Python scripts 


### Create files with soft labels (.seseg file)
To create relevant sseg files for running MedMeshCNN or MeshCNN please run 

```bash
python create_sseg.py /home/user/MedMeshCNN/datasets/human_seg/
```
and include the path to you train, test, seg, sseg folders as an argument. 
Make sure that there is a sseg folder already created in the path. 
This script creates a sseg file for all available eseg files in the eseg folder of the path. 


### Map your segmentation outcome to meshes of varying resolutions
To map your segmentation output to a mesh with a different resolution run 

```bash
python upscale_labels.py /home/user/MedMeshCNN/checkpoints/human_seg/validate/ /home/user/data/high_resolution_meshes/
```
This script maps the segmentation result to the original resolution mesh via a nearest neighbor search within a KD-Tree. 
This is helpful if you had to downsample your meshes to run MeshCNN and want to transfer your results to the original resolution of the mesh. 
Note that this transformation is only possible once. Once you have added labels to your high resolution objects, it is not possible to overwrite them with this script. 


# Questions / Issues
If you have questions or issues running this code, please open an issue.