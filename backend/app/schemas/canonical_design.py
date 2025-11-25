"""
Canonical Design JSON Schema - Editor-Agnostic Format
This is the single source of truth for ad creative designs.
All AI generation, editor operations, and exports operate on this model.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class LayerType(str, Enum):
    """Types of layers in the design."""
    TEXT = "text"
    IMAGE = "image"
    SHAPE = "shape"
    GROUP = "group"


class ImageRole(str, Enum):
    """Semantic role of image layers."""
    PRODUCT = "product"
    PERSON = "person"
    BACKGROUND = "background"
    LOGO = "logo"
    ICON = "icon"
    DECORATION = "decoration"
    COMPLEX_TEXT = "complex_text"  # Text with effects rendered as image


class ShapeType(str, Enum):
    """Types of shape layers."""
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"
    LINE = "line"
    POLYGON = "polygon"


class TextAlign(str, Enum):
    """Text alignment options."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"


class BlendMode(str, Enum):
    """Layer blend modes."""
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    DARKEN = "darken"
    LIGHTEN = "lighten"


class DesignFormat(str, Enum):
    """Supported ad formats."""
    INSTAGRAM_POST = "instagram_post"
    INSTAGRAM_STORY = "instagram_story"
    FACEBOOK_POST = "facebook_post"
    TWITTER_POST = "twitter_post"
    LINKEDIN_POST = "linkedin_post"


# ============================================================================
# POSITION & TRANSFORM
# ============================================================================

class Position(BaseModel):
    """Position and transform properties for layers."""
    x: float = Field(description="X coordinate from left edge (pixels)")
    y: float = Field(description="Y coordinate from top edge (pixels)")
    width: float = Field(description="Width in pixels")
    height: float = Field(description="Height in pixels")
    rotation: float = Field(default=0, description="Rotation in degrees (0-360)")
    z_index: int = Field(description="Stacking order (higher = on top)")
    
    # Alignment helpers
    origin_x: Literal["left", "center", "right"] = Field(
        default="left",
        description="Horizontal origin point for transforms"
    )
    origin_y: Literal["top", "center", "bottom"] = Field(
        default="top",
        description="Vertical origin point for transforms"
    )


# ============================================================================
# EFFECTS & STYLING
# ============================================================================

class Shadow(BaseModel):
    """Drop shadow effect."""
    offset_x: float = Field(description="Horizontal shadow offset (pixels)")
    offset_y: float = Field(description="Vertical shadow offset (pixels)")
    blur: float = Field(description="Blur radius (pixels)")
    color: str = Field(description="Shadow color (hex or rgba)")
    opacity: float = Field(default=1.0, ge=0, le=1, description="Shadow opacity (0-1)")


class Stroke(BaseModel):
    """Stroke/border styling."""
    color: str = Field(description="Stroke color (hex or rgba)")
    width: float = Field(description="Stroke width (pixels)")
    position: Literal["inside", "center", "outside"] = Field(
        default="center",
        description="Stroke position relative to shape edge"
    )


class Effects(BaseModel):
    """Visual effects applied to a layer."""
    opacity: float = Field(default=1.0, ge=0, le=1, description="Layer opacity (0-1)")
    blend_mode: BlendMode = Field(default=BlendMode.NORMAL)
    shadow: Optional[Shadow] = None
    stroke: Optional[Stroke] = None


# ============================================================================
# TEXT LAYER
# ============================================================================

class TextProperties(BaseModel):
    """Typography and text styling properties."""
    content: str = Field(description="The actual text content")
    font_family: str = Field(description="Font family name")
    font_size: float = Field(description="Font size in pixels")
    font_weight: int = Field(default=400, description="Font weight (100-900)")
    line_height: float = Field(default=1.2, description="Line height multiplier")
    letter_spacing: float = Field(default=0, description="Letter spacing in pixels")
    text_align: TextAlign = Field(default=TextAlign.LEFT)
    color: str = Field(description="Text color (hex or rgba)")

    # Advanced text properties
    text_transform: Optional[Literal["none", "uppercase", "lowercase", "capitalize"]] = "none"
    text_decoration: Optional[Literal["none", "underline", "line-through"]] = "none"


# ============================================================================
# IMAGE LAYER
# ============================================================================

class ImageGenerationPrompt(BaseModel):
    """Prompt for AI image generation."""
    prompt: str = Field(
        description="Detailed image generation prompt following best practices"
    )
    negative_prompt: Optional[str] = Field(
        default=None,
        description="Elements to avoid in generation"
    )
    style_modifiers: List[str] = Field(
        default_factory=list,
        description="Style keywords (e.g., 'photorealistic', '3D render', 'minimalist')"
    )
    quality_modifiers: List[str] = Field(
        default_factory=list,
        description="Quality keywords (e.g., 'high detail', '8K', 'professional')"
    )
    aspect_ratio: str = Field(
        description="Aspect ratio for generation (e.g., '1:1', '16:9', '9:16')"
    )
    requires_transparent_bg: bool = Field(
        default=True,
        description="Whether image needs transparent background"
    )


class ImageProperties(BaseModel):
    """Properties for image layers."""
    role: ImageRole = Field(description="Semantic role of the image")

    # Image source (one of these will be populated)
    asset_id: Optional[str] = Field(
        default=None,
        description="Reference to existing uploaded asset"
    )
    generation_prompt: Optional[ImageGenerationPrompt] = Field(
        default=None,
        description="AI generation prompt if image needs to be generated"
    )
    url: Optional[str] = Field(
        default=None,
        description="Direct URL to image (for external images)"
    )

    # Image adjustments
    fit: Literal["fill", "contain", "cover", "scale-down"] = Field(
        default="contain",
        description="How image fits within bounds"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Image filters (brightness, contrast, saturation, etc.)"
    )


# ============================================================================
# SHAPE LAYER
# ============================================================================

class ShapeProperties(BaseModel):
    """Properties for shape layers."""
    shape_type: ShapeType = Field(description="Type of shape")
    fill: Optional[str] = Field(default=None, description="Fill color (hex or rgba)")

    # Shape-specific properties
    border_radius: Optional[float] = Field(
        default=0,
        description="Border radius for rectangles (pixels)"
    )
    corner_style: Optional[Literal["round", "square"]] = Field(
        default="round",
        description="Corner style for shapes"
    )


# ============================================================================
# LAYER DEFINITIONS
# ============================================================================

class TextLayer(BaseModel):
    """Text layer with typography properties."""
    id: str = Field(description="Unique layer identifier")
    type: Literal[LayerType.TEXT] = LayerType.TEXT
    name: str = Field(description="Human-readable layer name")
    position: Position
    text: TextProperties
    effects: Effects = Field(default_factory=Effects)
    locked: bool = Field(default=False, description="Whether layer is locked from editing")
    visible: bool = Field(default=True, description="Whether layer is visible")


class ImageLayer(BaseModel):
    """Image layer for photos, products, logos, etc."""
    id: str = Field(description="Unique layer identifier")
    type: Literal[LayerType.IMAGE] = LayerType.IMAGE
    name: str = Field(description="Human-readable layer name")
    position: Position
    image: ImageProperties
    effects: Effects = Field(default_factory=Effects)
    locked: bool = Field(default=False)
    visible: bool = Field(default=True)


class ShapeLayer(BaseModel):
    """Shape layer for decorative elements."""
    id: str = Field(description="Unique layer identifier")
    type: Literal[LayerType.SHAPE] = LayerType.SHAPE
    name: str = Field(description="Human-readable layer name")
    position: Position
    shape: ShapeProperties
    effects: Effects = Field(default_factory=Effects)
    locked: bool = Field(default=False)
    visible: bool = Field(default=True)


class GroupLayer(BaseModel):
    """Group layer for organizing related layers."""
    id: str = Field(description="Unique layer identifier")
    type: Literal[LayerType.GROUP] = LayerType.GROUP
    name: str = Field(description="Human-readable layer name")
    position: Position
    children: List[str] = Field(
        description="IDs of child layers in this group"
    )
    effects: Effects = Field(default_factory=Effects)
    locked: bool = Field(default=False)
    visible: bool = Field(default=True)


# Union type for all layer types
Layer = Union[TextLayer, ImageLayer, ShapeLayer, GroupLayer]


# ============================================================================
# CANVAS & BACKGROUND
# ============================================================================

class CanvasSize(BaseModel):
    """Canvas dimensions."""
    width: int = Field(description="Canvas width in pixels")
    height: int = Field(description="Canvas height in pixels")
    unit: str = Field(default="px", description="Unit of measurement")


class Background(BaseModel):
    """Canvas background configuration."""
    type: Literal["color", "gradient", "image"] = Field(
        description="Background type"
    )
    color: Optional[str] = Field(
        default=None,
        description="Solid color (hex or rgba)"
    )
    gradient: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Gradient definition (type, colors, angle)"
    )
    image_layer_id: Optional[str] = Field(
        default=None,
        description="Reference to image layer used as background"
    )


# ============================================================================
# BRAND KIT
# ============================================================================

class BrandColors(BaseModel):
    """Brand color palette."""
    primary: str = Field(description="Primary brand color (hex)")
    secondary: str = Field(description="Secondary brand color (hex)")
    accent: str = Field(description="Accent color (hex)")


class BrandFonts(BaseModel):
    """Brand typography."""
    primary: str = Field(description="Primary brand font family")
    secondary: str = Field(description="Secondary brand font family")


class BrandKit(BaseModel):
    """Brand kit information for design consistency."""
    brand_id: Optional[str] = Field(
        default=None,
        description="Reference to brand kit in database"
    )
    name: str = Field(description="Brand name")
    colors: BrandColors
    fonts: BrandFonts
    logo_asset_id: Optional[str] = Field(
        default=None,
        description="Reference to logo asset"
    )


# ============================================================================
# DESIGN METADATA
# ============================================================================

class DesignConstraints(BaseModel):
    """Design constraints and guidelines."""
    safe_zone_margin: float = Field(
        default=0.05,
        description="Safe zone margin as percentage of canvas (0.05 = 5%)"
    )
    min_font_size: float = Field(
        default=12,
        description="Minimum font size in pixels for readability"
    )
    max_layers: int = Field(
        default=20,
        description="Maximum number of layers"
    )
    text_contrast_ratio: float = Field(
        default=4.5,
        description="Minimum contrast ratio for text (WCAG AA = 4.5)"
    )


class DesignMetadata(BaseModel):
    """Design metadata and provenance."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    source: Literal["ai_generated", "template", "manual", "imported"] = Field(
        description="How the design was created"
    )
    ai_prompt: Optional[str] = Field(
        default=None,
        description="Original AI prompt if AI-generated"
    )
    design_style: Optional[str] = Field(
        default=None,
        description="Design style (modern, minimal, bold, elegant, etc.)"
    )
    visual_hierarchy: Optional[List[str]] = Field(
        default=None,
        description="Ordered list of focal points (layer IDs)"
    )


# ============================================================================
# CANONICAL DESIGN JSON
# ============================================================================

class CanonicalDesign(BaseModel):
    """
    Canonical Design JSON - Editor-Agnostic Format

    This is the single source of truth for ad creative designs.
    All AI generation, editor operations, and exports operate on this model.
    """

    # Identity
    id: str = Field(description="Unique design identifier")
    schema_version: str = Field(
        default="2.0",
        description="Schema version for compatibility"
    )
    owner_id: str = Field(description="User ID who owns this design")

    # Basic info
    title: str = Field(description="Design title")
    format: DesignFormat = Field(description="Ad format/platform")

    # Canvas
    canvas: CanvasSize
    background: Background

    # Brand
    brand: Optional[BrandKit] = Field(
        default=None,
        description="Brand kit applied to this design"
    )

    # Layers (ordered by z-index)
    layers: List[Layer] = Field(
        description="All design layers (text, image, shape, group)"
    )

    # Metadata
    metadata: DesignMetadata
    constraints: DesignConstraints = Field(default_factory=DesignConstraints)

    # Campaign association
    campaign_id: Optional[str] = Field(
        default=None,
        description="Associated campaign ID"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "design_abc123",
                "schema_version": "2.0",
                "owner_id": "user_xyz",
                "title": "Summer Sale Instagram Post",
                "format": "instagram_post",
                "canvas": {
                    "width": 1080,
                    "height": 1080,
                    "unit": "px"
                },
                "background": {
                    "type": "color",
                    "color": "#FFFFFF"
                },
                "layers": [],
                "metadata": {
                    "source": "ai_generated",
                    "design_style": "modern"
                }
            }
        }



