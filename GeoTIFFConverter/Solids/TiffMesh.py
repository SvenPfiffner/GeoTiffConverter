# Author: Sven Pfiffner
# Created: November 2023

import numpy as np
from .TiffSolid import TiffSolid
import open3d as o3d

class TiffMesh(TiffSolid):
    """
    A class representing meshes of tiff data, implementing the TiffSolid interface.
    """

    @staticmethod
    def fromTiffPc(tiff_pc) -> 'TiffMesh':

        # Run Poisson surface reconstruction    
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(tiff_pc.data, depth=9)

        return TiffMesh(mesh, tiff_pc.world_origin,
                      tiff_pc.origin_height)

    def __init__(self, data, world_origin, origin_height) -> None:
        """
        Initializes a TiffMesh object.
        """
        self.data = data
        self.world_origin = world_origin
        self.origin_height = origin_height

    
    def save(self, path: str) -> None:
        """
        Saves the mesh representation to a specified path.

        Args:
        path (str): The path where the mesh representation will be saved.
        """
        o3d.io.write_triangle_mesh(path, self.data)
    
    
    def union(self, other: TiffSolid) -> TiffSolid:
        """
        Performs a union operation with another solid.

        Args:
        other (TiffSolid): The other solid to merge with.

        Returns:
        TiffSolid: The result of merging the solids.
        """
        # TODO: Implement
        pass