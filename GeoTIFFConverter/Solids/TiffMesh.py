# Author: Sven Pfiffner
# Created: November 2023

import numpy as np
from .TiffSolid import TiffSolid
from .TiffPc import TiffPc
import open3d as o3d

class TiffMesh(TiffSolid):
    """
    A class representing meshes of tiff data, implementing the TiffSolid interface.
    """

    @staticmethod
    def fromTiffFile(tiff) -> 'TiffMesh':

        # Load as TiffPc
        tiff_pc = TiffPc.fromTiffFile(tiff)

        # Run Poisson surface reconstruction    
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(tiff_pc.data, depth=9)

        return TiffMesh(mesh, tiff_pc.world_origin,
                      tiff_pc.origin_height)

    @staticmethod
    def fromTiffPc(tiff_pc) -> 'TiffMesh':

        # Run Poisson surface reconstruction    
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
        # Assert matching origin coordinate projection
        same_proj = self.world_origin.proj_string == other.world_origin.proj_string
        assert same_proj, "TiffSolids from different coordinate systems can't be combined"

        # Get offset of TiffSolids
        offset = other.world_origin.to_numpy() - self.world_origin.to_numpy()
        offset_height = other.origin_height - self.origin_height

        # Apply offset to other tile
        other.translate((offset[0, 0], offset_height ,offset[1, 0]))

        # Merge geometries
        self.data += other.data