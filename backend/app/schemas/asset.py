from datetime import datetime
from pydantic import BaseModel

class AssetBase(BaseModel):
    type: str # logo, product_image, background
    url: str

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: str
    ownerId: str
    createdAt: datetime

    class Config:
        from_attributes = True
