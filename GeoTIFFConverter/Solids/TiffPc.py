# Author: Sven Pfiffner, Luca Dalbosco
# Created: November 2023

from .TiffSolid import TiffSolid
import numpy as np

class TiffPc(TiffSolid):
    """
    A class representing point clouds of tiff data, implementing the TiffSolid interface.
    """

    def fromTiffFile(tiff) -> 'TiffPc':
        """
        Generates a point cloud representation from a TiffFile object.

        Args:
        tiff (TiffFile): The TiffFile object containing elevation data.

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
       
        return TiffPc(XYZ.reshape((-1, 3)))

    
    def __init__(self) -> None:
        """
        Initializes a TiffPc object.
        """
        pass

    def render(self) -> None:
        """
        Renders the point cloud.
        """
        pass
    
    def save(self, path: str) -> None:
        """
        Saves the point cloud representation to a specified path.

        Args:
        path (str): The path where the point cloud representation will be saved.
        """
        pass
    
    def translate(self, translation_vec: np.ndarray) -> None:
        """
        Translates the point cloud using a translation vector.

        Args:
        translation_vec (np.ndarray): The translation vector to move the point cloud.
        """
        pass
    
    def scale(self, scale_vec: np.ndarray) -> None:
        """
        Scales the point cloud along different axes.

        Args:
        scale_vec (np.ndarray): The scaling factors for each axis.
        """
        pass
    
    def rotate(self, rotation_mat: np.ndarray) -> None:
        """
        Rotates the point cloud based on a rotation matrix.

        Args:
        rotation_mat (np.ndarray): The rotation matrix for transforming the point cloud.
        """
        pass
    
    def transform(self, transf_mat: np.ndarray) -> None:
        """
        Applies a general transformation to the point cloud.

        Args:
        transf_mat (np.ndarray): The transformation matrix.
        """
        pass
    
    def union(self, other: TiffSolid) -> TiffSolid:
        """
        Performs a union operation with another solid.

        Args:
        other (TiffSolid): The other solid to merge with.

        Returns:
        TiffSolid: The result of merging the solids.
        """
        pass