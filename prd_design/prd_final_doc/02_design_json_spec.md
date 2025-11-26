# Radic Pro — Canonical Design JSON Specification

> **Version**: 2.0  
> **Last Updated**: November 2025  
> **Status**: Final

---

## 1. Design Philosophy

### 1.1 Canonical Format Principles

The Design JSON is the **single source of truth** for all design data. It is:

1. **Editor-Agnostic** — Not tied to any specific canvas library (Fabric.js, Konva, Polotno)
2. **Block-Based** — Designs are composed of predefined blocks, not freeform layers
3. **Self-Contained** — All information needed to render the design is in the JSON
4. **Versioned** — Schema version enables forward/backward compatibility
5. **Portable** — Designs can be transferred between systems
6. **Validatable** — Strict schema enables validation and auto-repair

### 1.2 Block System vs Freeform Layers

**Key Insight**: Blocks are a **UI abstraction** over the underlying layer system. In the Design JSON, blocks are represented as layers with specific `blockType` roles.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Creative Concept                             │
│              (Defines which blocks are required)                 │
│                                                                  │
│   "product_highlight" → [background, headline, product, cta]    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Design JSON                               │
│                  (Blocks as typed layers)                        │
│                                                                  │
│   layers: [                                                     │
│     { blockType: "background", type: "image", ... },            │
│     { blockType: "headline", type: "text", ... },               │
│     { blockType: "product_image", type: "image", ... },         │
│     { blockType: "cta", type: "shape", ... }                    │
│   ]                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Editor (Fabric.js)                           │
│               (Renders blocks as objects)                        │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Adapter Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                        Design JSON (Canonical)                   │
│                     Single Source of Truth                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
            ┌───────────┐ ┌───────────┐ ┌───────────┐
            │ Fabric.js │ │  Polotno  │ │   Konva   │
            │  Adapter  │ │  Adapter  │ │  Adapter  │
            └───────────┘ └───────────┘ └───────────┘
                    │           │           │
                    ▼           ▼           ▼
            ┌───────────┐ ┌───────────┐ ┌───────────┐
            │ Fabric    │ │  Polotno  │ │   Konva   │
            │ JSON      │ │  JSON     │ │   JSON    │
            └───────────┘ └───────────┘ └───────────┘
```

**Key Principle**: The Design JSON never changes to accommodate an editor. Adapters handle all translation.

---

## 2. Schema Overview

```
Design JSON v2.0
├── schemaVersion: "2.0"
├── id: string (UUID)
├── meta: MetaObject
│   └── creativeConcept: ConceptType
├── canvas: CanvasObject
├── brand: BrandObject | null
├── blocks: Block[]              // Replaces 'layers' in v2.0
└── smartAssets: Record<string, SmartImageRecipe>
```

### 2.1 Block Types (V1)

| BlockType | Layer Type | Description |
|-----------|------------|-------------|
| `background` | image/color | Canvas background |
| `headline` | text | Main message |
| `subhead` | text | Supporting text |
| `product_image` | image | Hero product shot |
| `cta` | shape+text | Call to action button |
| `logo` | image | Brand logo |
| `offer_tag` | shape+text | Discount badge |
| `price` | text | Product pricing |
| `badge` | shape | Decorative shape |
| `footer` | text | Fine print |

### 2.2 Creative Concepts (V1)

| Concept | Required Blocks |
|---------|-----------------|
| `product_highlight` | background, headline, product_image, cta, logo |
| `offer_focus` | background, headline, offer_tag, cta, badge, logo |
| `problem_solution` | background, headline, subhead, product_image, cta |

---

## 3. Complete Schema Definition

### 3.1 Root Object

```typescript
interface DesignJSON {
  // Schema version for migrations
  schemaVersion: "2.0";
  
  // Unique identifier
  id: string;
  
  // Ownership and metadata
  ownerId: string;
  campaignId?: string;
  
  // Design metadata
  meta: MetaObject;
  
  // Canvas settings
  canvas: CanvasObject;
  
  // Brand settings (embedded for portability)
  brand: BrandObject | null;
  
  // Ordered array of blocks (bottom to top)
  blocks: Block[];
  
  // Smart image recipes for regeneration
  smartAssets: Record<string, SmartImageRecipe>;
}
```

### 3.2 Meta Object

```typescript
interface MetaObject {
  // Human-readable title
  title: string;
  
  // Design format identifier
  format: "instagram_post" | "instagram_story" | "facebook_post" | "twitter_post";
  
  // Creative concept used
  creativeConcept: CreativeConcept;
  
  // Timestamps (ISO 8601)
  createdAt: string;
  updatedAt: string;
  
  // How this design was created
  source: "ai_generated" | "template" | "manual" | "duplicated";
  
  // AI generation tracking (if source = "ai_generated")
  generation?: {
    originalPrompt: string;
    briefHash: string;
    modelVersion: string;  // e.g., "gemini-3-pro"
    imageModel: string;    // e.g., "nano-banana-pro"
    variantIndex: number;
  };
}

type CreativeConcept = 
  | "product_highlight"
  | "offer_focus"
  | "problem_solution"
  // V2 concepts
  | "ingredients"
  | "testimonial"
  | "seasonal"
  | "before_after"
  | "routine";
```

### 3.3 Canvas Object

```typescript
interface CanvasObject {
  // Dimensions
  width: number;   // 1080 for Instagram
  height: number;  // 1080 for square post
  unit: "px";
  
  // Background
  background: BackgroundObject;
}

interface BackgroundObject {
  type: "color" | "gradient" | "image";
  
  // For type = "color"
  color?: string;  // Hex color
  
  // For type = "gradient"
  gradient?: {
    type: "linear" | "radial";
    angle?: number;  // For linear
    stops: Array<{ offset: number; color: string }>;
  };
  
  // For type = "image"
  imageAssetId?: string;
  imageFit?: "cover" | "contain" | "fill";
}
```

### 3.4 Brand Object

```typescript
interface BrandObject {
  // Reference to brand kit (for updates)
  brandKitId: string;
  
  // Embedded brand values (for portability)
  name: string;
  
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    text: string;
    background?: string;
  };
  
  fonts: {
    primary: FontDefinition;
    secondary: FontDefinition;
  };
  
  logoAssetId?: string;
}

interface FontDefinition {
  family: string;
  weights: number[];  // e.g., [400, 700, 800]
  fallback?: string;  // e.g., "sans-serif"
}
```

### 3.5 Layer Types

#### Base Layer Properties

```typescript
interface BaseLayer {
  // Unique identifier within design
  id: string;
  
  // Layer type discriminator
  type: "text" | "image" | "shape";
  
  // Semantic role for AI understanding
  role: LayerRole;
  
  // Position (top-left corner, relative to canvas)
  position: {
    x: number;
    y: number;
  };
  
  // Dimensions
  size: {
    width: number;
    height: number | null;  // null = auto-calculate
  };
  
  // Transform
  rotation: number;  // Degrees, -360 to 360
  opacity: number;   // 0 to 1
  
  // Stacking order (higher = on top)
  zIndex: number;
  
  // Editor state
  locked: boolean;
  visible: boolean;
  
  // Optional name for layer panel
  name?: string;
}

type LayerRole = 
  // Text roles
  | "headline"
  | "subheadline" 
  | "body"
  | "cta"
  | "bullets"
  | "caption"
  // Image roles
  | "product_shot"
  | "background_image"
  | "logo"
  | "decorative_text"
  | "persona"
  | "infographic"
  // Shape roles
  | "badge"
  | "divider"
  | "frame"
  | "background_shape"
  | "decorative";
```

#### Text Layer

```typescript
interface TextLayer extends BaseLayer {
  type: "text";
  role: "headline" | "subheadline" | "body" | "cta" | "bullets" | "caption";
  
  // Text content (plain text, no HTML)
  content: string;
  
  // Typography
  style: TextStyle;
}

interface TextStyle {
  fontFamily: string;
  fontSize: number;        // In pixels
  fontWeight: 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900;
  fontStyle: "normal" | "italic";
  
  lineHeight: number;      // Multiplier (e.g., 1.2)
  letterSpacing: number;   // In pixels
  
  color: string;           // Hex color
  
  textAlign: "left" | "center" | "right";
  verticalAlign: "top" | "middle" | "bottom";
  
  textDecoration: "none" | "underline" | "line-through";
  textTransform: "none" | "uppercase" | "lowercase" | "capitalize";
  
  // Text effects (optional)
  shadow?: TextShadow;
  stroke?: TextStroke;
}

interface TextShadow {
  color: string;
  offsetX: number;
  offsetY: number;
  blur: number;
}

interface TextStroke {
  color: string;
  width: number;
}
```

#### Image Layer

```typescript
interface ImageLayer extends BaseLayer {
  type: "image";
  role: "product_shot" | "background_image" | "logo" | "decorative_text" | "persona" | "infographic";
  
  // Reference to asset in storage
  assetId: string | null;  // null = placeholder
  
  // Display options
  fit: "cover" | "contain" | "fill";
  
  // Image adjustments
  adjustments?: {
    brightness?: number;  // -100 to 100
    contrast?: number;    // -100 to 100
    saturation?: number;  // -100 to 100
  };
  
  // Border radius for rounded images
  borderRadius?: number;
  
  // Smart image metadata (if AI-generated)
  smartImage?: SmartImageReference;
}

interface SmartImageReference {
  // Reference to recipe in smartAssets
  recipeId: string;
  
  // Generation status
  status: "pending" | "generating" | "completed" | "failed";
  
  // Error message if failed
  error?: string;
}
```

#### Shape Layer

```typescript
interface ShapeLayer extends BaseLayer {
  type: "shape";
  role: "badge" | "divider" | "frame" | "background_shape" | "decorative";
  
  // Shape type
  shape: "rectangle" | "circle" | "ellipse" | "line" | "rounded_rect";
  
  // Styling
  style: ShapeStyle;
}

interface ShapeStyle {
  // Fill
  fill: string | null;  // Hex color or null for transparent
  
  // Stroke
  stroke: string | null;
  strokeWidth: number;
  strokeDashArray?: number[];  // For dashed lines
  
  // For rounded_rect
  cornerRadius?: number | {
    topLeft: number;
    topRight: number;
    bottomRight: number;
    bottomLeft: number;
  };
}
```

### 3.6 Smart Image Recipe

```typescript
interface SmartImageRecipe {
  // Unique identifier
  recipeId: string;
  
  // Image type
  type: "product_shot" | "background" | "decorative_text" | "persona" | "infographic";
  
  // The specific image prompt
  prompt: string;
  
  // Holistic context for blending
  holisticContext: HolisticContext;
  
  // AI model to use
  model: "flux-pro" | "gpt-image-1" | "imagen-3" | "sdxl";
  
  // Reference images (for style matching, product shots)
  references: string[];  // Asset IDs
  
  // Generation options
  options: {
    aspectRatio?: "1:1" | "4:3" | "3:4" | "16:9" | "9:16";
    style?: "photo" | "illustration" | "3d" | "flat";
    quality?: "draft" | "standard" | "high";
  };
  
  // Most recent generated asset
  lastGeneratedAssetId: string | null;
  generatedAt: string | null;
}

interface HolisticContext {
  // Overall design purpose
  designPurpose: string;
  
  // Visual theme
  overallTheme: string;
  
  // Target audience
  targetAudience?: string;
  
  // Description of adjacent elements for context
  adjacentElements: string[];
  
  // Brand colors to harmonize with
  brandColors: string[];
  
  // Composition guidance
  compositionHints?: string;
  
  // Style keywords
  styleKeywords: string[];
}
```

---

## 4. Complete Example

```json
{
  "schemaVersion": "1.4",
  "id": "design_550e8400-e29b-41d4-a716-446655440000",
  "ownerId": "user_123",
  "campaignId": "camp_456",
  
  "meta": {
    "title": "Diwali Electronics Sale",
    "format": "instagram_post",
    "createdAt": "2025-11-26T15:30:00Z",
    "updatedAt": "2025-11-26T16:45:00Z",
    "source": "ai_generated",
    "generation": {
      "originalPrompt": "Instagram ad for Diwali electronics sale, 40% OFF, premium dark theme, show headphones",
      "briefHash": "sha256_abc123",
      "modelVersion": "gpt-4.1",
      "variantIndex": 0
    }
  },
  
  "canvas": {
    "width": 1080,
    "height": 1080,
    "unit": "px",
    "background": {
      "type": "color",
      "color": "#050816"
    }
  },
  
  "brand": {
    "brandKitId": "brand_789",
    "name": "VoltSound",
    "colors": {
      "primary": "#FFCC00",
      "secondary": "#050816",
      "accent": "#FF4D00",
      "text": "#FFFFFF"
    },
    "fonts": {
      "primary": {
        "family": "Inter",
        "weights": [400, 700, 800],
        "fallback": "sans-serif"
      },
      "secondary": {
        "family": "DM Sans",
        "weights": [400, 500],
        "fallback": "sans-serif"
      }
    },
    "logoAssetId": "asset_logo_001"
  },
  
  "layers": [
    {
      "id": "layer_headline",
      "type": "text",
      "role": "headline",
      "content": "Diwali Mega Sale",
      "position": { "x": 80, "y": 120 },
      "size": { "width": 920, "height": null },
      "rotation": 0,
      "opacity": 1,
      "zIndex": 100,
      "locked": false,
      "visible": true,
      "name": "Headline",
      "style": {
        "fontFamily": "Inter",
        "fontSize": 72,
        "fontWeight": 800,
        "fontStyle": "normal",
        "lineHeight": 1.1,
        "letterSpacing": -1,
        "color": "#FFFFFF",
        "textAlign": "left",
        "verticalAlign": "top",
        "textDecoration": "none",
        "textTransform": "none"
      }
    },
    {
      "id": "layer_subheadline",
      "type": "text",
      "role": "subheadline",
      "content": "Premium Headphones at Unbeatable Prices",
      "position": { "x": 80, "y": 220 },
      "size": { "width": 600, "height": null },
      "rotation": 0,
      "opacity": 1,
      "zIndex": 90,
      "locked": false,
      "visible": true,
      "name": "Subheadline",
      "style": {
        "fontFamily": "DM Sans",
        "fontSize": 28,
        "fontWeight": 400,
        "fontStyle": "normal",
        "lineHeight": 1.4,
        "letterSpacing": 0,
        "color": "#CCCCCC",
        "textAlign": "left",
        "verticalAlign": "top",
        "textDecoration": "none",
        "textTransform": "none"
      }
    },
    {
      "id": "layer_product",
      "type": "image",
      "role": "product_shot",
      "assetId": "asset_prod_001",
      "position": { "x": 580, "y": 300 },
      "size": { "width": 450, "height": 450 },
      "rotation": 0,
      "opacity": 1,
      "zIndex": 50,
      "locked": false,
      "visible": true,
      "name": "Product Image",
      "fit": "contain",
      "smartImage": {
        "recipeId": "recipe_prod_001",
        "status": "completed"
      }
    },
    {
      "id": "layer_badge",
      "type": "shape",
      "role": "badge",
      "shape": "circle",
      "position": { "x": 80, "y": 400 },
      "size": { "width": 180, "height": 180 },
      "rotation": 0,
      "opacity": 1,
      "zIndex": 80,
      "locked": false,
      "visible": true,
      "name": "Discount Badge",
      "style": {
        "fill": "#FF4D00",
        "stroke": "#FFFFFF",
        "strokeWidth": 4
      }
    },
    {
      "id": "layer_badge_text",
      "type": "text",
      "role": "cta",
      "content": "40%\nOFF",
      "position": { "x": 110, "y": 450 },
      "size": { "width": 120, "height": null },
      "rotation": 0,
      "opacity": 1,
      "zIndex": 85,
      "locked": false,
      "visible": true,
      "name": "Discount Text",
      "style": {
        "fontFamily": "Inter",
        "fontSize": 36,
        "fontWeight": 800,
        "fontStyle": "normal",
        "lineHeight": 1.0,
        "letterSpacing": 0,
        "color": "#FFFFFF",
        "textAlign": "center",
        "verticalAlign": "middle",
        "textDecoration": "none",
        "textTransform": "none"
      }
    },
    {
      "id": "layer_cta",
      "type": "text",
      "role": "cta",
      "content": "Shop Now →",
      "position": { "x": 80, "y": 950 },
      "size": { "width": 200, "height": null },
      "rotation": 0,
      "opacity": 1,
      "zIndex": 70,
      "locked": false,
      "visible": true,
      "name": "CTA",
      "style": {
        "fontFamily": "Inter",
        "fontSize": 24,
        "fontWeight": 700,
        "fontStyle": "normal",
        "lineHeight": 1.2,
        "letterSpacing": 1,
        "color": "#FFCC00",
        "textAlign": "left",
        "verticalAlign": "top",
        "textDecoration": "none",
        "textTransform": "uppercase"
      }
    },
    {
      "id": "layer_logo",
      "type": "image",
      "role": "logo",
      "assetId": "asset_logo_001",
      "position": { "x": 900, "y": 950 },
      "size": { "width": 120, "height": 60 },
      "rotation": 0,
      "opacity": 0.9,
      "zIndex": 60,
      "locked": true,
      "visible": true,
      "name": "Logo",
      "fit": "contain"
    }
  ],
  
  "smartAssets": {
    "recipe_prod_001": {
      "recipeId": "recipe_prod_001",
      "type": "product_shot",
      "prompt": "Professional studio shot of premium wireless headphones, floating at slight angle, dramatic rim lighting from behind",
      "holisticContext": {
        "designPurpose": "Diwali sale advertisement for electronics brand",
        "overallTheme": "Premium, dark, festive with gold accents",
        "targetAudience": "Young urban professionals, tech enthusiasts",
        "adjacentElements": [
          "Golden headline text 'Diwali Mega Sale'",
          "Orange circular discount badge with '40% OFF'",
          "Dark purple background (#050816)"
        ],
        "brandColors": ["#FFCC00", "#050816", "#FF4D00", "#FFFFFF"],
        "compositionHints": "Product should be positioned on the right side, facing left, with warm highlights complementing the gold accent color",
        "styleKeywords": ["premium", "professional", "dramatic lighting", "floating", "clean"]
      },
      "model": "flux-pro",
      "references": ["asset_ref_headphones_001"],
      "options": {
        "aspectRatio": "1:1",
        "style": "photo",
        "quality": "high"
      },
      "lastGeneratedAssetId": "asset_prod_001",
      "generatedAt": "2025-11-26T15:31:00Z"
    }
  }
}
```

---

## 5. Validation Rules

### 5.1 Required Validations

| Rule | Description | Error Level |
|------|-------------|-------------|
| Schema version | Must be "1.4" | Error |
| Design ID | Must be valid UUID format | Error |
| Canvas dimensions | Width/height must be > 0 and ≤ 4096 | Error |
| Layer IDs | Must be unique within design | Error |
| Layer zIndex | Must be integer | Warning (auto-fix) |
| Text content | Must be non-empty for text layers | Error |
| Font size | Must be between 8 and 200 | Warning (clamp) |
| Colors | Must be valid hex format | Error |
| Asset references | Must reference existing assets | Warning |
| Position | x, y must be numbers | Error |
| Opacity | Must be between 0 and 1 | Warning (clamp) |
| Rotation | Must be between -360 and 360 | Warning (normalize) |

### 5.2 Auto-Repair Rules

```python
# validation/auto_repair.py

def repair_design(design: dict) -> tuple[dict, list[str]]:
    """Attempt to repair common issues in design JSON."""
    repairs = []
    
    # Ensure schema version
    if design.get("schemaVersion") != "1.4":
        design["schemaVersion"] = "1.4"
        repairs.append("Updated schema version to 1.4")
    
    # Normalize layer zIndex
    for i, layer in enumerate(design.get("layers", [])):
        if not isinstance(layer.get("zIndex"), int):
            layer["zIndex"] = (i + 1) * 10
            repairs.append(f"Normalized zIndex for layer {layer.get('id')}")
    
    # Clamp font sizes
    for layer in design.get("layers", []):
        if layer.get("type") == "text":
            font_size = layer.get("style", {}).get("fontSize", 24)
            if font_size < 8:
                layer["style"]["fontSize"] = 8
                repairs.append(f"Clamped font size to minimum for {layer.get('id')}")
            elif font_size > 200:
                layer["style"]["fontSize"] = 200
                repairs.append(f"Clamped font size to maximum for {layer.get('id')}")
    
    # Clamp opacity
    for layer in design.get("layers", []):
        opacity = layer.get("opacity", 1)
        if opacity < 0 or opacity > 1:
            layer["opacity"] = max(0, min(1, opacity))
            repairs.append(f"Clamped opacity for {layer.get('id')}")
    
    # Ensure required fields
    for layer in design.get("layers", []):
        if "locked" not in layer:
            layer["locked"] = False
        if "visible" not in layer:
            layer["visible"] = True
    
    return design, repairs
```

---

## 6. Adapter Interface

### 6.1 Abstract Adapter

```typescript
// adapters/base.ts

interface EditorAdapter {
  // Adapter identification
  readonly name: string;
  readonly version: string;
  
  // Convert canonical Design JSON to editor-specific format
  toEditorFormat(design: DesignJSON): EditorFormat;
  
  // Convert editor state back to canonical Design JSON
  fromEditorFormat(editorState: EditorFormat): DesignJSON;
  
  // Partial update: apply patch to editor
  applyPatch(patch: DesignPatch): void;
  
  // Export canvas to image
  exportImage(options: ExportOptions): Promise<Blob>;
}

interface DesignPatch {
  operations: PatchOperation[];
}

type PatchOperation = 
  | { op: "add_layer"; layer: Layer }
  | { op: "remove_layer"; layerId: string }
  | { op: "update_layer"; layerId: string; changes: Partial<Layer> }
  | { op: "update_canvas"; changes: Partial<CanvasObject> }
  | { op: "reorder_layers"; layerIds: string[] };
```

### 6.2 Fabric.js Adapter (Reference Implementation)

```typescript
// adapters/fabric-adapter.ts

import { Canvas, Object as FabricObject, IText, Rect, Circle, Image } from 'fabric';

class FabricAdapter implements EditorAdapter {
  readonly name = "fabric";
  readonly version = "6.0";
  
  private canvas: Canvas;
  
  constructor(canvasElement: HTMLCanvasElement) {
    this.canvas = new Canvas(canvasElement);
  }
  
  toEditorFormat(design: DesignJSON): void {
    // Clear existing
    this.canvas.clear();
    
    // Set canvas size
    this.canvas.setDimensions({
      width: design.canvas.width,
      height: design.canvas.height
    });
    
    // Set background
    this.applyBackground(design.canvas.background);
    
    // Sort layers by zIndex and add
    const sortedLayers = [...design.layers].sort((a, b) => a.zIndex - b.zIndex);
    
    for (const layer of sortedLayers) {
      const fabricObject = this.layerToFabricObject(layer);
      if (fabricObject) {
        // Store canonical layer ID
        fabricObject.set('data', { canonicalId: layer.id, role: layer.role });
        this.canvas.add(fabricObject);
      }
    }
    
    this.canvas.renderAll();
  }
  
  fromEditorFormat(): DesignJSON {
    const objects = this.canvas.getObjects();
    const layers: Layer[] = [];
    
    for (let i = 0; i < objects.length; i++) {
      const obj = objects[i];
      const layer = this.fabricObjectToLayer(obj, i);
      if (layer) {
        layers.push(layer);
      }
    }
    
    return {
      schemaVersion: "1.4",
      // ... other properties from stored design
      layers
    };
  }
  
  private layerToFabricObject(layer: Layer): FabricObject | null {
    switch (layer.type) {
      case "text":
        return this.textLayerToFabric(layer as TextLayer);
      case "image":
        return this.imageLayerToFabric(layer as ImageLayer);
      case "shape":
        return this.shapeLayerToFabric(layer as ShapeLayer);
      default:
        return null;
    }
  }
  
  private textLayerToFabric(layer: TextLayer): IText {
    return new IText(layer.content, {
      left: layer.position.x,
      top: layer.position.y,
      width: layer.size.width,
      angle: layer.rotation,
      opacity: layer.opacity,
      selectable: !layer.locked,
      visible: layer.visible,
      
      // Typography
      fontFamily: layer.style.fontFamily,
      fontSize: layer.style.fontSize,
      fontWeight: layer.style.fontWeight.toString(),
      fontStyle: layer.style.fontStyle,
      lineHeight: layer.style.lineHeight,
      charSpacing: layer.style.letterSpacing * 10, // Fabric uses different scale
      fill: layer.style.color,
      textAlign: layer.style.textAlign,
      
      // Underline/strike
      underline: layer.style.textDecoration === 'underline',
      linethrough: layer.style.textDecoration === 'line-through',
    });
  }
  
  private fabricObjectToLayer(obj: FabricObject, index: number): Layer | null {
    const data = obj.get('data') || {};
    const baseProps = {
      id: data.canonicalId || `layer_${Date.now()}_${index}`,
      position: { x: obj.left || 0, y: obj.top || 0 },
      size: { width: obj.width || 0, height: obj.height || 0 },
      rotation: obj.angle || 0,
      opacity: obj.opacity || 1,
      zIndex: index * 10,
      locked: !obj.selectable,
      visible: obj.visible !== false,
    };
    
    if (obj instanceof IText) {
      return {
        ...baseProps,
        type: "text",
        role: data.role || "body",
        content: obj.text || "",
        style: {
          fontFamily: obj.fontFamily || "Inter",
          fontSize: obj.fontSize || 24,
          fontWeight: parseInt(obj.fontWeight as string) || 400,
          // ... map other properties
        }
      } as TextLayer;
    }
    
    // Handle other types...
    return null;
  }
}
```

---

## 7. Migration Guide

### 7.1 From v1.3 to v1.4

```python
def migrate_v13_to_v14(design: dict) -> dict:
    """Migrate Design JSON from v1.3 to v1.4"""
    
    # Update schema version
    design["schemaVersion"] = "1.4"
    
    # Migrate flat style properties to nested style object
    for layer in design.get("layers", []):
        if layer.get("type") == "text":
            # Move flat properties into style object
            style = layer.get("style", {})
            
            # Migrate if using old flat format
            for prop in ["fontFamily", "fontSize", "fontWeight", "color", "textAlign"]:
                if prop in layer and prop not in style:
                    style[prop] = layer.pop(prop)
            
            # Add new required fields with defaults
            style.setdefault("fontStyle", "normal")
            style.setdefault("lineHeight", 1.2)
            style.setdefault("letterSpacing", 0)
            style.setdefault("verticalAlign", "top")
            style.setdefault("textDecoration", "none")
            style.setdefault("textTransform", "none")
            
            layer["style"] = style
        
        # Add new required layer properties
        layer.setdefault("locked", False)
        layer.setdefault("visible", True)
    
    # Migrate smartImage to smartAssets
    smart_assets = design.get("smartAssets", {})
    for layer in design.get("layers", []):
        if layer.get("type") == "image" and "smartImage" in layer:
            smart = layer["smartImage"]
            recipe_id = smart.get("recipeId")
            if recipe_id and recipe_id not in smart_assets:
                # Move recipe to smartAssets
                smart_assets[recipe_id] = {
                    "recipeId": recipe_id,
                    "type": layer.get("role", "product_shot"),
                    "prompt": smart.get("prompt", ""),
                    "holisticContext": smart.get("holisticContext", {
                        "designPurpose": "",
                        "overallTheme": "",
                        "adjacentElements": [],
                        "brandColors": [],
                        "styleKeywords": []
                    }),
                    "model": smart.get("model", "flux-pro"),
                    "references": smart.get("references", []),
                    "options": smart.get("options", {}),
                    "lastGeneratedAssetId": layer.get("assetId"),
                    "generatedAt": None
                }
            
            # Simplify layer reference
            layer["smartImage"] = {
                "recipeId": recipe_id,
                "status": "completed"
            }
    
    design["smartAssets"] = smart_assets
    
    return design
```

---

## 8. TypeScript Types (Export)

```typescript
// types/design-json.ts
// Auto-generated from schema - do not edit manually

export interface DesignJSON {
  schemaVersion: "1.4";
  id: string;
  ownerId: string;
  campaignId?: string;
  meta: MetaObject;
  canvas: CanvasObject;
  brand: BrandObject | null;
  layers: Layer[];
  smartAssets: Record<string, SmartImageRecipe>;
}

export type Layer = TextLayer | ImageLayer | ShapeLayer;

// ... full type definitions
```
