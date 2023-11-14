# Sandbox
import GeoTIFFConverter as tiff
import numpy as np

from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r] took: %2.4f sec' % \
          (f.__name__, kw, te-ts))
        return result
    return wrap


@timing
def files_to_mesh():
    file1 = tiff.TiffFile("data/input/1.tif")
    file2 = tiff.TiffFile("data/input/2.tif")
    file3 = tiff.TiffFile("data/input/3.tif")
    file4 = tiff.TiffFile("data/input/4.tif")

    pcd = tiff.Solids.TiffPc.fromTiffFile(file1)
    pcd.union(tiff.Solids.TiffPc.fromTiffFile(file2))
    pcd.union(tiff.Solids.TiffPc.fromTiffFile(file3))
    pcd.union(tiff.Solids.TiffPc.fromTiffFile(file4))

    mesh = tiff.Solids.TiffMesh.fromTiffPc(pcd)
    return mesh

mesh = files_to_mesh()

options = tiff.Solids.RenderOptions(mesh_color="y_coordinate")
mesh.render(render_options=options)



# Load csv resource into TiffFile objects
"""
with open("data/tiffdata.csv") as file:
    paths = [line.rstrip() for line in file]
tiff_collection = tiff.TiffFile.fromCollection(paths)

# Merge to pointcloud
start = time.time()
pcd = tiff.Solids.TiffPc.fromTiffFile(tiff_collection[0], downsample_voxel_size=50)
end = time.time()
print(f"\033[94mMerge will take approximately {len(tiff_collection) * int(end - start)}s\033[0m")
for i in range(1, len(tiff_collection)):
    print(f"\033[94mMerging {i+1}/{len(tiff_collection)}\033[0m", end='\r')
    appendix = tiff.Solids.TiffPc.fromTiffFile(tiff_collection[i], downsample_voxel_size=50 )
    pcd.union(appendix)
print("")
pcd.save("davos_pcd.pcd")
pcd.render()
"""

