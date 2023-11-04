import open3d as o3d
import numpy as np

class MeshUtil:
    
    def point_cloud_to_mesh(xyz, path):
        x = np.linspace(-3, 3, 401)
        mesh_x, mesh_y = np.meshgrid(x, x)
        z = np.sinc((np.power(mesh_x, 2) + np.power(mesh_y, 2)))
        z_norm = (z - z.min()) / (z.max() - z.min())
        xyz = np.zeros((np.size(mesh_x), 3))
        xyz[:, 0] = np.reshape(mesh_x, -1)
        xyz[:, 1] = np.reshape(mesh_y, -1)
        xyz[:, 2] = np.reshape(z_norm, -1)

        # Pass xyz to Open3D.o3d.geometry.PointCloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)

        # Estimate normals
        pcd.estimate_normals()
        pcd.orient_normals_consistent_tangent_plane(100)

        # Run Poisson surface reconstruction    
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

        # Visualize
        mesh.paint_uniform_color([0.165, 0.969, 0.965])
        mesh.compute_vertex_normals()
        o3d.visualization.draw_geometries([mesh])

        # Save
        o3d.io.write_triangle_mesh(path, mesh)