# Author: Sven Pfiffner
# Created: November 2023

import open3d as o3d
import numpy as np

#Convenience wrapper for commonly used open3d render options for our usecase
class RenderOptions:
    """
    A convenience wrapper providing options for rendering in Open3D.

    This class encapsulates commonly used rendering settings
    to configure how objects are visualized in the rendering process.
    """

    def __init__(self,
                 background_color = np.array([1.0, 1.0, 1.0]),
                 mesh_color = "default",
                 mesh_show_wireframe = False,
                 point_show_normal = False,
                 show_coordinate_frame = False,
                 phong_lighting = True):
        """
        Initializes the RenderOptions object with specified rendering settings.

        Args:
        background_color (np.ndarray, optional): Background color in RGB format. Default is [1.0, 1.0, 1.0].
        mesh_color (str, optional): Color mode for mesh visualization. Default is "default".
        - "default": Default coloring mode.
        - "color": Color-based visualization; the mesh's color information is used for visualization.
        - "x_coordinate": Color visualization based on the X-coordinate information.
        - "y_coordinate": Color visualization based on the Y-coordinate information.
        - "z_coordinate": Color visualization based on the Z-coordinate information.
        - "normal": Visualization based on surface normals.

        mesh_show_wireframe (bool, optional): Whether to show wireframe for mesh visualization. Default is False.
        point_show_normal (bool, optional): Whether to display normals for points. Default is False.
        show_coordinate_frame (bool, optional): Whether to display the coordinate frame. Default is False.
        phong_lighting (bool, optional): Whether to use Phong lighting for rendering. Default is True.
        """

        self.background_color = background_color
        self.mesh_color = mesh_color
        self.mesh_show_wireframe = mesh_show_wireframe
        self.point_show_normal = point_show_normal
        self.show_coordinate_frame = show_coordinate_frame
        self.phong_lighting = phong_lighting

        self._mesh_color_modes = {"default": 0,
                                  "color": 1,
                                  "x_coordinate": 2,
                                  "y_coordinate": 3,
                                  "z_coordinate": 4,
                                  "normal": 9}

    def apply_to_renderer(self, viewer):
        """
        Applies the configured rendering options to an Open3D renderer.

        Args:
        viewer (o3d.visualization.Visualizer): The Open3D renderer to apply the settings to.
        """
        opt = viewer.get_render_option()
        opt.background_color = self.background_color
        # TODO: Add enum
        # opt.mesh_color_option = self._mesh_color_modes[self.mesh_color]
        opt.mesh_show_wireframe = self.mesh_show_wireframe
        opt.point_show_normal = self.point_show_normal
        opt.show_coordinate_frame = self.show_coordinate_frame
        opt.light_on = self.phong_lighting

