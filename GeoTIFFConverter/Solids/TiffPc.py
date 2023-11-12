# Author: Sven Pfiffner, Luca Dalbosco
# Created: November 2023

from .TiffSolid import TiffSolid
import open3d as o3d
import numpy as np

class TiffPc(TiffSolid):
    """
    A class representing point clouds of tiff data, implementing the TiffSolid interface.
    """

    @staticmethod
    def fromTiffFile(tiff, downsample_voxel_size = 0) -> 'TiffPc':
        """
        Generates a point cloud representation from a TiffFile object.

        Args:
        tiff (TiffFile): The TiffFile object containing elevation data.
        downsample_voxel_size (int): Strength of the voxel downsampling
        for the points. Defaults to 0

        Returns:
        TiffPc: A point cloud representation generated from the provided TiffFile.

        Note:
        This function extracts elevation data from the TiffFile and generates a point cloud
        by considering the data structure and geospatial information from the TiffFile's metadata.
        """

        # We assume that the elevation is encoded in the first band
        data = tiff.to_numpy()[0]

        # Normalize height
        data -= (data.min())

        # Create point cloud
        x = np.linspace(0, ((data.shape[0] - 1) / 2), num = data.shape[0]).reshape((-1, 1))

        # Shift 0.25 to the right to account for decentricity of datapoints
        # TODO: Make shift amount dependant on tiff metadata
        # Shift further to account for the position on a global coordinate system
        x += (0.25 + tiff.tiff.bounds.left)
        X = np.matmul(x, np.ones((1, x.shape[0])))


        y = np.linspace(0, ((data.shape[1] - 1) / 2), num = data.shape[1]).reshape((1, -1))

        # Shift 0.25 down to account for decentricity of datapoints
        # TODO: Make shift amount dependant on tiff metadata
        # Shift further to account for the position on a global coordinate system
        y += (0.25 + tiff.tiff.bounds.top)
        Y = np.matmul(np.ones((data.shape[1], 1)), y)

        XYZ = np.dstack((X, Y, data))
       
        return TiffPc(XYZ.reshape((-1, 3)), downsample_voxel_size = downsample_voxel_size)

    
    def __init__(self, point_coords, downsample_voxel_size = 0) -> None:
        """
        Initializes a TiffPc object.

        Args:
        point_coords (np.ndarray): The coordinates of the points.
        downsample_voxel_size (int): Strength of the voxel downsampling
        for the points. Defaults to 0
        """

        # Pass the point_coords to Open3D.o3d.geometry.PointCloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_coords)

        # Downsample if needed
        if downsample_voxel_size > 0:
            pcd = pcd.voxel_down_sample(voxel_size=downsample_voxel_size)

        # Estimate normals
        pcd.estimate_normals()
        pcd.orient_normals_consistent_tangent_plane(100)
    
        self.data = pcd
    
    def save(self, path: str) -> None:
        """
        Saves the point cloud representation to a specified path.

        Args:
        path (str): The path where the point cloud representation will be saved.
        """
        o3d.io.write_point_cloud(path, self.pcd)
    
    def union(self, other: TiffSolid) -> TiffSolid:
        """
        Performs a union operation with another solid.

        Args:
        other (TiffSolid): The other solid to merge with.

        Returns:
        TiffSolid: The result of merging the solids.
        """
        pass