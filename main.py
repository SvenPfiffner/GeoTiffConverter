# Sandbox
import GeoTIFFConverter as tiff
import numpy as np
import time

# Load csv resource into TiffFile objects
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
    appendix = tiff.Solids.TiffPc.fromTiffFile(tiff_collection[i], downsample_voxel_size=50)
    pcd.union(appendix)
print("")
pcd.save("davos_pcd.pcd")
pcd.render()