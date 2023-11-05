import numpy as np

class Converter:

    def to_point_cloud(tiff, base_height=0.0):
        # Compute data size
        x_span = abs(tiff.tiff.bounds.right - tiff.tiff.bounds.left)
        y_span = abs(tiff.tiff.bounds.top - tiff.tiff.bounds.bottom)

        # Get elevation data
        data = tiff.to_numpy()[0]

        # Normalize height
        data -= (data.min() - base_height)
        #print(data)

        # Create point cloud
        x = np.linspace(0, ((data.shape[0] - 1) / 2), num = data.shape[0]).reshape((-1, 1))
        x += 0.25
        X = np.matmul(x, np.ones((1, x.shape[0])))
        #print(f"X: {X} Shape: {X.shape}")

        y = np.linspace(0, ((data.shape[1] - 1) / 2), num = data.shape[1]).reshape((1, -1))
        y += 0.25
        Y = np.matmul(np.ones((data.shape[1], 1)), y)

        XYZ = np.dstack((X, Y, data))
        #print(f"XYZ:/n{XYZ}, /nShape: {XYZ.shape}")
       
        return XYZ.reshape((-1, 3))