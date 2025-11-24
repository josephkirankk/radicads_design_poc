from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class DesignBrief(BaseModel):
    """Structured design brief generated from user prompt."""
    
    headline: str = Field(description="Main headline text for the design")
    subheadline: Optional[str] = Field(
        default=None,
        description="Supporting subheadline text, if applicable"
    )
    visual_focus: List[str] = Field(
        description="Key visual elements to emphasize (e.g., product, text, imagery)"
    )
    layout_style: str = Field(
        description="Layout approach (e.g., modern, minimal, bold, elegant, playful)"
    )
    color_scheme: Dict[str, str] = Field(
        description="Color palette with primary, secondary, and accent colors as hex codes"
    )
    format: str = Field(
        default="instagram_post",
        description="Design format (instagram_post, instagram_story, facebook_post, etc.)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "headline": "Summer Sale 50% Off",
                "subheadline": "Limited time offer",
                "visual_focus": ["text", "bold typography"],
                "layout_style": "modern",
                "color_scheme": {
                    "primary": "#FF6B6B",
                    "secondary": "#4ECDC4",
                    "accent": "#FFE66D"
                },
                "format": "instagram_post"
            }
        }


class FabricTextObject(BaseModel):
    """Fabric.js text object schema."""
    
    type: str = "text"
    left: float
    top: float
    width: float
    height: float
    text: str
    fontSize: int
    fontFamily: str = "Arial"
    fontWeight: str = "normal"
    fill: str
    textAlign: str = "left"
    originX: str = "left"
    originY: str = "top"
    angle: float = 0
    opacity: float = 1


class FabricRectObject(BaseModel):
    """Fabric.js rectangle object schema."""
    
    type: str = "rect"
    left: float
    top: float
    width: float
    height: float
    fill: str
    stroke: Optional[str] = None
    strokeWidth: float = 0
    angle: float = 0
    opacity: float = 1
    rx: float = 0  # Border radius x
    ry: float = 0  # Border radius y


class FabricCircleObject(BaseModel):
    """Fabric.js circle object schema."""
    
    type: str = "circle"
    left: float
    top: float
    radius: float
    fill: str
    stroke: Optional[str] = None
    strokeWidth: float = 0
    angle: float = 0
    opacity: float = 1


def get_fabric_canvas_dimensions(format: str) -> Dict[str, int]:
    """
    Get canvas dimensions for different design formats.
    
    Args:
        format: Design format (instagram_post, instagram_story, etc.)
        
    Returns:
        Dict with width and height in pixels
    """
    dimensions = {
        "instagram_post": {"width": 1080, "height": 1080},
        "instagram_story": {"width": 1080, "height": 1920},
        "facebook_post": {"width": 1200, "height": 630},
        "twitter_post": {"width": 1200, "height": 675},
        "linkedin_post": {"width": 1200, "height": 627},
    }
    return dimensions.get(format, {"width": 1080, "height": 1080})


def create_mock_design_brief() -> Dict[str, Any]:
    """Create a mock design brief for fallback purposes."""
    return {
        "headline": "Sample Headline",
        "subheadline": "Sample Subheadline",
        "visual_focus": ["product"],
        "layout_style": "modern",
        "color_scheme": {
            "primary": "#3b82f6",
            "secondary": "#1e293b",
            "accent": "#64748b"
        },
        "format": "instagram_post"
    }


def create_mock_fabric_design(brief: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a mock Fabric.js design for fallback purposes.
    
    Args:
        brief: Design brief to base the mock design on
        
    Returns:
        Fabric.js compatible design JSON
    """
    dimensions = get_fabric_canvas_dimensions(brief.get("format", "instagram_post"))
    color_scheme = brief.get("color_scheme", {})
    primary_color = color_scheme.get("primary", "#3b82f6")
    text_color = color_scheme.get("secondary", "#1e293b")
    accent_color = color_scheme.get("accent", "#64748b")
    
    return {
        "version": "5.3.0",
        "objects": [
            {
                "type": "rect",
                "left": 100,
                "top": 100,
                "width": dimensions["width"] - 200,
                "height": 200,
                "fill": primary_color,
                "stroke": None,
                "strokeWidth": 0,
                "angle": 0,
                "opacity": 1,
                "rx": 10,
                "ry": 10,
            },
            {
                "type": "text",
                "left": dimensions["width"] / 2,
                "top": dimensions["height"] / 2 - 50,
                "width": 400,
                "height": 100,
                "text": brief.get("headline", "Sample Headline"),
                "fontSize": 48,
                "fontFamily": "Arial",
                "fontWeight": "bold",
                "fill": text_color,
                "textAlign": "center",
                "originX": "center",
                "originY": "center",
            },
            {
                "type": "text",
                "left": dimensions["width"] / 2,
                "top": dimensions["height"] / 2 + 50,
                "width": 400,
                "height": 50,
                "text": brief.get("subheadline", "Sample Subheadline"),
                "fontSize": 24,
                "fontFamily": "Arial",
                "fill": accent_color,
                "textAlign": "center",
                "originX": "center",
                "originY": "center",
            }
        ],
        "background": "#ffffff"
    }
