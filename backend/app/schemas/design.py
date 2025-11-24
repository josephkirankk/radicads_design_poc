from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class SmartImageRecipe(BaseModel):
    recipeId: str
    source: str
    role: str

class Layer(BaseModel):
    id: str
    type: str
    content: Optional[str] = None
    fontFamily: Optional[str] = None
    fontSize: Optional[int] = None
    fontWeight: Optional[int] = None
    lineHeight: Optional[float] = None
    color: Optional[str] = None
    textAlign: Optional[str] = None
    x: float
    y: float
    width: float
    height: Optional[float] = None
    rotation: float = 0
    zIndex: int
    imageId: Optional[str] = None
    shape: Optional[str] = None
    fill: Optional[str] = None
    stroke: Optional[str] = None
    strokeWidth: Optional[int] = None
    radius: Optional[int] = None
    smartImage: Optional[SmartImageRecipe] = None

class Background(BaseModel):
    type: str
    color: Optional[str] = None
    imageId: Optional[str] = None

class DesignBrand(BaseModel):
    brandId: str
    primaryColor: str
    secondaryColor: str
    accentColor: str
    fontPrimary: str
    fontSecondary: str
    logoImageId: Optional[str] = None

class DesignSize(BaseModel):
    width: int
    height: int
    unit: str = "px"

class DesignMeta(BaseModel):
    source: str
    createdAt: datetime
    updatedAt: datetime

class DesignJSON(BaseModel):
    id: str
    schemaVersion: str = "1.1"
    ownerId: str
    campaignId: Optional[str] = None
    title: str
    format: str
    size: DesignSize
    background: Background
    brand: Optional[DesignBrand] = None
    layers: List[Layer]
    meta: DesignMeta

class DesignCreate(BaseModel):
    title: str
    format: str
    brandId: Optional[str] = None

class DesignUpdate(BaseModel):
    title: Optional[str] = None
    designJson: Optional[Dict[str, Any]] = None
