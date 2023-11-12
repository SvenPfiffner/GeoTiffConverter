# Author: Sven Pfiffner
# Created: November 2023

import numpy as np
import open3d as o3d
from abc import ABC, abstractmethod

class TiffSolid(ABC):
    """
    An abstract class for tiff solid objects.

    This abstract class defines solid representations of tiff data,
    intended to be implemented by subclasses for different types of solids.
    """

    data = None # Contains the solid specific data

    def render(self, render_options=None) -> None:
        """
        Renders the solid.

        Args:
        render_options (RenderOptions, optional): Options to apply to the renderer
        """

        viewer = o3d.visualization.Visualizer()
        viewer.create_window()
        viewer.add_geometry(self.data)

        # Apply render options
        if render_options is not None:
            render_options.apply_to_renderer(viewer)
        
        viewer.run()
        viewer.destroy_window()

    def translate(self, translation_vec: np.ndarray) -> None:
        """
        Translates the solid using a translation vector.

        Args:
        translation_vec (np.ndarray): The translation vector to move the solid.
        """
        self.data.translate(translation_vec)
    
    def scale(self, scale_factor: float) -> None:
        """
        Scales the solid by a given factor

        Args:
        scale_vec (float): The scaling factor

        Note: This scale is origin-preserving and might change the
        center of mass
        """
        self.data.scale(scale_factor, center=(0, 0, 0))

    def rotate(self, rotation_vec: np.ndarray) -> None:
        """
        Rotates the solid based on a rotation vector.

        Args:
        rotation_vec (np.ndarray): A 3d vector that encodes rotation in the x,y,z axes.
        """
        R = self.data.get_rotation_matrix_from_xyz(rotation_vec)
        self.data.rotate(R)

    def transform(self, transf_mat: np.ndarray) -> None:
        """
        Applies a general transformation to the solid.

        Args:
        transf_mat (np.ndarray): A 4x4 homogeneous transformation matrix.
        """
        self.data.transform(transf_mat)

    @abstractmethod
    def union(self, other: 'TiffSolid') -> 'TiffSolid':
        """
        Performs a union operation with another solid.

        Args:
        other (TiffSolid): The other solid to merge with.

        Returns:
        TiffSolid: The result of merging the solids.
        """
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """
        Saves the representation of the solid to a specified path.

        Args:
        path (str): The path where the solid representation will be saved.
        """
        pass