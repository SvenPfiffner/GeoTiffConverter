import numpy as np

class Converter:

    def to_point_cloud(tiff, base_height=0.0):
        # Compute data size
        x_span = abs(tiff.tiff.bounds.right - tiff.tiff.bounds.left)
        y_span = abs(tiff.tiff.bounds.top - tiff.tiff.bounds.bottom)

        # Get elevation data
        data = tiff.to_numpy()[0]
        # Calculate the relative point delta
        dx = x_span / data.shape[0]
        dy = y_span / data.shape[1]

        # Normalize height
        data -= (data.min() - base_height)
        print(data)

        # Create point cloud
        return