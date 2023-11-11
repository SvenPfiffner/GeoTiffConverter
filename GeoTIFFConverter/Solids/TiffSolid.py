# Author: Sven Pfiffner
# Created: November 2023

class TiffSolid:

    def __init__(self, tiff):
        self.data = tiff.to_numpy()