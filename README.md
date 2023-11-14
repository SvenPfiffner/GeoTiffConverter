# GeoTiffConverter
![python_v3.8.18](https://img.shields.io/badge/Python-3.8.18-green)
![unit_tests](https://github.com/SvenPfiffner/GeoTiffConverter/actions/workflows/python-app.yml/badge.svg?branch=main)
![Banner](https://github.com/SvenPfiffner/GeoTiffConverter/blob/main/geotiff.png?raw=true)

## Installation
Run ```pip install -r requirements.txt``` in the root directory

## Usage
The repository can be used in two different ways. Either via installation as a python module or a limited UI.
### Python module
Add the ```GeoTIFFConverter``` directory to your python project and import the module via
```python
  import GeoTIFFConverter
```
**Load a TIFF File**
To load a TIFF file, the TiffFile class from the GeoTIFFConverter module is utilized. This class takes the path to a TIFF file as a parameter and allows you to access the data and metadata of the TIFF file.
```python
file1 = tiff.TiffFile("data/input/1.tif")
```

**Create Point Cloud from TIFF File**
The ```TiffPc.fromTiffFile``` method is used to create a point cloud from a loaded TIFF files elevation data.
```python
pcd = tiff.Solids.TiffPc.fromTiffFile(file1)
```

**Combine Point Clouds**
To combine multiple point clouds into a single point cloud, the union method is used. It takes the coordinate-metadata of the underlying TIFFs into account to combine the point clouds at correct relative positions
```python
pcd = tiff.Solids.TiffPc.fromTiffFile(file1)
pcd.union(tiff.Solids.TiffPc.fromTiffFile(file2))
```

**Create a Mesh from a Point Cloud**
To create a mesh from a point cloud, the ```TiffMesh.fromTiffPc``` method is employed.
```python
mesh = tiff.Solids.TiffMesh.fromTiffPc(pcd)
```

**Rendering a Point Cloud or Mesh**
The render method of the ```TiffPc``` and ```TiffMesh``` objects can be called to render the respective geometry data using default rendering options
```python
pcd.render()
mesh.render()
```
Custom rendering options can be added to change the visualization. A custom rendering option is created with the ```RenderOptions``` class. This custom option is then passed to the render method. The following example visualizes a mesh with coloring based on elevation
```python
options = tiff.Solids.RenderOptions(mesh_color="y_coordinate")
mesh.render(render_options=options)
```

### UI
A limited scope of functionality is provided by a voluntary gradio ui. It does not cover all functionality but should be enough to visualize and convert tiff height data. To start the UI,
- Run ```python gui.py``` in the root directory to start the WebUI. It will be accessible under **http://127.0.0.1:7860/**

### Supported systems
The converter is based on the implementation of [pyproj](https://pypi.org/project/pyproj/). A list of supported map projections for the TIFF files is given [here](https://proj.org/en/9.3/operations/projections/index.html)