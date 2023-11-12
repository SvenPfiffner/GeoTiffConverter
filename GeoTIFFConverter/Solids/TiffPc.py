# Author: Luca Dalbosco, Sven Pfiffner
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
        # NOTE: The renderer uses OpenGL, which is a right-handed system.
        # thus -> +x-axis (right), +y-axis (up), +z-axis(backwards)

        x = np.linspace(0, ((data.shape[0] - 1) / 2), num = data.shape[0]).reshape((1, -1))

        # Shift 0.25 to the right to account for decentricity of datapoints
        # TODO: Make shift amount dependant on tiff metadata
        x += 0.25
        X = np.matmul(np.ones((x.shape[1], 1)), x)

        z = np.flip(np.linspace(0, ((data.shape[1] - 1) / 2), num = data.shape[1])).reshape((-1, 1))

        # Shift 0.25 down to account for decentricity of datapoints
        # TODO: Make shift amount dependant on tiff metadata
        z += 0.25
        Z = np.matmul(z, np.ones((1, z.shape[0])))

        XYZ = np.dstack((X, data, Z))
       
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
        try:
            pcd.orient_normals_consistent_tangent_plane(100)
        except:
            print("\033[93m[Warning] Normal orientation failed.",
                  "SolidPc can still be used, but might have wrongly aligned point normals!\033[0m")
    
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