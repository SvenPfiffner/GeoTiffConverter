import open3d as o3d
import numpy as np

class MeshUtil:
    
    def point_cloud_to_mesh(xyz, path, downsample_voxel_size=0):
        
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

        # Save
        R = mesh.get_rotation_matrix_from_xyz((-np.pi / 2, 0, 0))
        mesh.rotate(R, center=(0, 0, 0))
        o3d.io.write_triangle_mesh(path, mesh)