# Author: Sven Pfiffner
# Created: November 2023

import numpy as np

class TiffSolid:
    """
    An interface for tiff solid objects.

    This interface defines methods for common operations on solid representations,
    intended to be implemented by subclasses for different types of solids.
    """

    def render(self) -> None:
        """
        Renders the solid.
        """
        pass

    def save(self, path: str) -> None:
        """
        Saves the representation of the solid to a specified path.

        Args:
        path (str): The path where the solid representation will be saved.
        """
        pass

    def translate(self, translation_vec: np.ndarray) -> None:
        """
        Translates the solid using a translation vector.

        Args:
        translation_vec (np.ndarray): The translation vector to move the solid.

        Note:
        The vector's shape should be compatible with the solid's representation.
        """
        pass
    
    def scale(self, scale_vec: np.ndarray) -> None:
        """
        Scales the solid along different axes.

        Args:
        scale_vec (np.ndarray): The scaling factors for each axis.
        """
        pass

    def rotate(self, rotation_mat: np.ndarray) -> None:
        """
        Rotates the solid based on a rotation matrix.

        Args:
        rotation_mat (np.ndarray): The rotation matrix to apply.
        """
        pass

    def transform(self, transf_mat: np.ndarray) -> None:
        """
        Applies a general transformation to the solid.

        Args:
        transf_mat (np.ndarray): The transformation matrix.
        """
        pass

    def union(self, other: 'TiffSolid') -> 'TiffSolid':
        """
        Performs a union operation with another solid.

        Args:
        other (TiffSolid): The other solid to merge with.

        Returns:
        TiffSolid: The result of merging the solids.
        """
        pass