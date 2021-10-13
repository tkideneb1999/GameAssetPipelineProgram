from enum import Enum

class Asset_Type(Enum):
    ASSET3D = 0
    TEXTURE = 1
    SCENEFILE = 2


class Asset:
    def __init__(self, name, location, asset_type):
        self.name = name
        self.location = location
        self.asset_type = asset_type


class Asset3D(Asset):
    def __init__(self, name, location):
        super.__init__(name, location, Asset_Type.ASSET3D)


class AssetTexture(Asset):
    def __init__(self, name, location):
        super.__init__(name, location, Asset_Type.TEXTURE)
