import numpy as np
from .TiffFile import TiffFile

class Converter:

    #Generate the point-cloud for a single tiff
    def tile_to_point_cloud(tiff: TiffFile, base_height: float = 0.0) -> list:
        # Get elevation data
        data = tiff.to_numpy()[0]

        # Normalize height
        data -= (data.min() - base_height)
        #print(data)

        # Create point cloud
        x = np.linspace(0, ((data.shape[0] - 1) / 2), num = data.shape[0]).reshape((-1, 1))

        #Shift 0.25 to the right to account for decentricity of datapoints
        #Shift further to account for the position on a global coordinate system
        x += (0.25 + tiff.tiff.bounds.left)
        X = np.matmul(x, np.ones((1, x.shape[0])))


        y = np.linspace(0, ((data.shape[1] - 1) / 2), num = data.shape[1]).reshape((1, -1))

        #Shift 0.25 down to account for decentricity of datapoints
        #Shift further to account for the position on a global coordinate system
        y += (0.25 + tiff.tiff.bounds.top)
        Y = np.matmul(np.ones((data.shape[1], 1)), y)

        XYZ = np.dstack((X, Y, data))
       
        return XYZ.reshape((-1, 3))
    

    #Generate a point-clouds for multiple tiffs and merge them
    def to_point_cloud(all_tiffs: list, base_height: float = 0.0) -> list:

        first_tile = True

        x_minima = []
        y_minima = []

        for tiff in all_tiffs:
            tile_cloud = Converter.tile_to_point_cloud(tiff, base_height)

            x_minima.append(tile_cloud[0][0])
            y_minima.append(tile_cloud[0][1])

            #Copy first tile-cloud, afterwards merge (stack horizontally) total point-cloud with new tile-cloud
            if first_tile:
                first_tile = False
                point_cloud = tile_cloud.copy()
            else:
                point_cloud = np.hstack((point_cloud, tile_cloud))
            
        
        #Find smallest used values for the x-/y-coordinates
        min_x = min(x_minima)
        min_y = min(y_minima)

        #Shift the point-cloud to the local origin (top left)
        point_cloud = list(map(lambda coord: [coord[0] - (min_x - 0.25), coord[1] - (min_y - 0.25), coord[2]], point_cloud))

        return point_cloud