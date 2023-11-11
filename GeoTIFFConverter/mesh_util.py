import open3d as o3d
import numpy as np

class MeshUtil:
    """
    A utility class for handling mesh operations using Open3D.
    """

    def add_base_to_mesh(mesh):
        """
        Add a baseplate to the provided mesh.

        Args:
        mesh (o3d.geometry.TriangleMesh): The mesh to which the baseplate will be added.

        Returns:
        o3d.geometry.TriangleMesh: The updated mesh with the baseplate.
        """

        # TODO: Add a baseplate to the mesh
        return mesh

    def point_cloud_to_mesh(xyz, path, downsample_voxel_size=0, add_base=False):
        """
        Convert a point cloud to a mesh and save it to a file.

        Args:
        xyz (np.array): Input point cloud as a NumPy array.
        path (str): File path to save the resulting mesh.
        downsample_voxel_size (float, optional): Voxel size for downsampling. Defaults to 0.
        add_base (bool, optional): Flag to add a baseplate to the mesh. Defaults to False.
        """
        
        # Pass xyz to Open3D.o3d.geometry.PointCloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)

        if downsample_voxel_size > 0:
            print("Point-cloud downsampled")
            pcd = pcd.voxel_down_sample(voxel_size=downsample_voxel_size)

        # Estimate normals
        pcd.estimate_normals()
        pcd.orient_normals_consistent_tangent_plane(100)

        # Run Poisson surface reconstruction    
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

        if add_base:
            mesh = MeshUtil.add_base_to_mesh(mesh)

        # Save
        R = mesh.get_rotation_matrix_from_xyz((-np.pi / 2, 0, 0))
        mesh.rotate(R, center=(0, 0, 0))
        o3d.io.write_triangle_mesh(path, mesh)