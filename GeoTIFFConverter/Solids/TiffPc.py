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
    def fromTiffFile(tiff, normal_plane_orient = False, downsample_voxel_size = 0) -> 'TiffPc':
        """
        Generates a point cloud representation from a TiffFile object.

        Args:
        tiff (TiffFile): The TiffFile object containing elevation data.
        normal_plane_orient (bool, optional): Wether the point normals should be
        oriented using consistent tangent plane. Otherwise trivial orientation is used.
        Defaults to False
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
        origin_height = data.min()
        data -= origin_height

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

        # Retrieve the x,z coordinate of the tiff
        origin_coord = tiff.get_bounding_coordinates()[0]

       
        return TiffPc(XYZ.reshape((-1, 3)), origin_coord,
                      origin_height, normal_plane_orient=normal_plane_orient,
                      downsample_voxel_size = downsample_voxel_size)

    
    def __init__(self, point_coords, world_origin, origin_height, normal_plane_orient = False, downsample_voxel_size = 0) -> None:
        """
        Initializes a TiffPc object.

        Args:
        point_coords (np.ndarray): The coordinates of the points.
        world_origin (Coordinate): The real-world 2d coordinate of the
        origin point.
        origin_height (float): The real-world height of the origin point
        normal_plane_orient (bool, optional): Wether the point normals should be
        oriented using consistent tangent plane. Otherwise trivial orientation is used.
        Defaults to False
        downsample_voxel_size (int, optional): Strength of the voxel downsampling
        for the points. Defaults to 0
        """
        # Pass the point_coords to Open3D.o3d.geometry.PointCloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_coords)

        # Downsample if needed
        if downsample_voxel_size > 0:
            pcd = pcd.voxel_down_sample(voxel_size=downsample_voxel_size)
            

        # TODO: Evaluate wether the trivial approach is sufficient for mesh creation
        pcd.estimate_normals()
        if normal_plane_orient:
            try:
                pcd.orient_normals_consistent_tangent_plane(100)
            except:
                print("\033[93m[Warning] Normal orientation failed.",
                    "SolidPc can still be used, but might have wrongly aligned point normals!\033[0m")
        else:
            pcd.orient_normals_to_align_with_direction((0,1,0))

        
    
        self.data = pcd
        self.world_origin = world_origin
        self.origin_height = origin_height
    
    def save(self, path: str) -> None:
        """
        Saves the point cloud representation to a specified path.

        Args:
        path (str): The path where the point cloud representation will be saved.
        """
        o3d.io.write_point_cloud(path, self.data)
    
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