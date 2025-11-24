from typing import Optional, Dict
from pydantic import BaseModel

class BrandColors(BaseModel):
    primary: str
    secondary: str
    accent: str

class BrandFonts(BaseModel):
    primary: str
    secondary: str

class BrandKitBase(BaseModel):
    name: str
    colors: BrandColors
    fonts: BrandFonts
    logoImageId: Optional[str] = None

class BrandKitCreate(BrandKitBase):
    pass

class BrandKitUpdate(BrandKitBase):
    pass

class BrandKit(BrandKitBase):
    id: str
    ownerId: str

    class Config:
        from_attributes = True
