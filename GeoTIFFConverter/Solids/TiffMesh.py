# Author: Sven Pfiffner
# Created: November 2023

from .TiffSolid import TiffSolid

class TiffMesh(TiffSolid):
    
    def __init__(self, tiff):
        super().__init__(tiff)