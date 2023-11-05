import GeoTIFFConverter as tiff
import numpy as np

x, o = np.linspace(1, 16, 4).reshape((-1, 4)), np.ones((4, 1))
X = np.matmul(o, x)
Y = X.copy().transpose()
coord = np.dstack([X,Y]).reshape((-1, 2))

print(X)
print(Y)
print(coord)
#tiff.MeshUtil.test()

print(tiff.Converter.to_point_cloud(file1)[0])
