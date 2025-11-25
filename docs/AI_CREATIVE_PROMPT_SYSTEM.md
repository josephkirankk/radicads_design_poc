# AI Ad Creative Generation System

## 🎯 Overview

This document describes the comprehensive prompt engineering system for generating professional ad creatives using AI. The system follows 2025 best practices for structured output, chain-of-thought reasoning, and high-quality image generation.

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Canonical JSON Schema](#canonical-json-schema)
3. [Prompt Engineering Strategy](#prompt-engineering-strategy)
4. [Image Generation Prompts](#image-generation-prompts)
5. [Workflow](#workflow)
6. [Best Practices](#best-practices)
7. [Examples](#examples)

---

## 🏗️ System Architecture

### Three-Stage Pipeline

```
┌─────────────────┐
│  User Input     │
│  + Brand Kit    │
│  + References   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Stage 1: AI Layout Gen     │
│  ─────────────────────────  │
│  • Analyze requirements     │
│  • Plan design strategy     │
│  • Generate Canonical JSON  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Stage 2: Image Generation  │
│  ─────────────────────────  │
│  • Extract image layers     │
│  • Generate prompts         │
│  • Create images (PNG+α)    │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Stage 3: Editor Conversion │
│  ─────────────────────────  │
│  • Convert to Fabric.js     │
│  • Inject generated images  │
│  • Render in canvas         │
└─────────────────────────────┘
```

### Key Components

1. **Canonical Design JSON** (`canonical_design.py`)
   - Editor-agnostic format
   - Single source of truth
   - Fully typed with Pydantic

2. **System Prompt** (`ad_creative_system_prompt.py`)
   - Expert role definition
   - Design principles
   - Technical constraints
   - Output specification

3. **Image Prompts** (`image_generation_prompts.py`)
   - Template-based generation
   - Model-specific optimization
   - Role-specific prompts (product, person, background, etc.)

---

## 📐 Canonical JSON Schema

### Design Philosophy

The Canonical Design JSON is:
- **Editor-agnostic**: Not tied to Fabric.js or any specific editor
- **Semantic**: Describes intent, not just rendering
- **Extensible**: Easy to add new layer types and properties
- **Validatable**: Strict types with Pydantic schemas

### Core Structure

```json
{
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
  
  "brand": {
    "brand_id": "brand_123",
    "name": "Acme Corp",
    "colors": {
      "primary": "#FF6B6B",
      "secondary": "#4ECDC4",
      "accent": "#FFE66D"
    },
    "fonts": {
      "primary": "Inter",
      "secondary": "DM Sans"
    },
    "logo_asset_id": "asset_logo_1"
  },
  
  "layers": [
    {
      "id": "layer_1",
      "type": "text",
      "name": "Headline",
      "position": {
        "x": 540,
        "y": 400,
        "width": 800,
        "height": 100,
        "rotation": 0,
        "z_index": 10,
        "origin_x": "center",
        "origin_y": "center"
      },
      "text": {
        "content": "50% OFF SALE",
        "font_family": "Inter",
        "font_size": 72,
        "font_weight": 700,
        "line_height": 1.2,
        "letter_spacing": 0,
        "text_align": "center",
        "color": "#FF6B6B"
      },
      "effects": {
        "opacity": 1.0,
        "blend_mode": "normal",
        "shadow": {
          "offset_x": 0,
          "offset_y": 4,
          "blur": 8,
          "color": "rgba(0,0,0,0.3)",
          "opacity": 1.0
        }
      }
    },
    {
      "id": "layer_2",
      "type": "image",
      "name": "Product Image",
      "position": {
        "x": 540,
        "y": 700,
        "width": 400,
        "height": 400,
        "rotation": 0,
        "z_index": 5,
        "origin_x": "center",
        "origin_y": "center"
      },
      "image": {
        "role": "product",
        "generation_prompt": {
          "prompt": "wireless headphones, modern design, professional product photography...",
          "negative_prompt": "blurry, low quality, distorted...",
          "style_modifiers": ["photorealistic", "studio lighting"],
          "quality_modifiers": ["high resolution", "8K detail"],
          "aspect_ratio": "1:1",
          "requires_transparent_bg": true
        }
      },
      "effects": {
        "opacity": 1.0
      }
    }
  ],
  
  "metadata": {
    "created_at": "2025-11-25T10:00:00Z",
    "updated_at": "2025-11-25T10:00:00Z",
    "source": "ai_generated",
    "ai_prompt": "Create a summer sale ad for wireless headphones",
    "design_style": "modern",
    "visual_hierarchy": ["layer_1", "layer_2"]
  },
  
  "constraints": {
    "safe_zone_margin": 0.05,
    "min_font_size": 14,
    "max_layers": 20,
    "text_contrast_ratio": 4.5
  }
}
```

### Layer Types

#### 1. Text Layer
```python
{
  "type": "text",
  "text": {
    "content": "Your text here",
    "font_family": "Inter",
    "font_size": 48,
    "font_weight": 700,
    "color": "#000000"
  }
}
```

#### 2. Image Layer
```python
{
  "type": "image",
  "image": {
    "role": "product" | "person" | "background" | "logo" | "icon",
    "generation_prompt": {...},  # For AI-generated images
    "asset_id": "...",           # For uploaded images
    "url": "..."                 # For external images
  }
}
```

#### 3. Shape Layer
```python
{
  "type": "shape",
  "shape": {
    "shape_type": "rectangle" | "circle" | "ellipse",
    "fill": "#FF0000",
    "border_radius": 10
  }
}
```

#### 4. Group Layer
```python
{
  "type": "group",
  "children": ["layer_id_1", "layer_id_2"]
}
```

---

## 🎨 Prompt Engineering Strategy

### 1. System Role (Expert Persona)

```
You are an expert ad creative designer with 15+ years of experience...
```

**Why this works:**
- Establishes authority and expertise
- Primes the model for high-quality output
- Sets expectations for professional results

### 2. Design Principles (Knowledge Base)

Includes comprehensive guidelines on:
- Visual hierarchy
- Composition & layout
- Typography
- Color theory
- Platform optimization
- Conversion best practices

**Why this works:**
- Provides context for decision-making
- Ensures consistency across generations
- Embeds best practices into every output

### 3. Technical Constraints (Boundaries)

Specifies:
- Canvas dimensions for each platform
- Layer limits
- Safe zones
- Text readability requirements
- Image generation requirements

**Why this works:**
- Prevents invalid outputs
- Ensures technical feasibility
- Maintains performance standards

### 4. Chain-of-Thought (Reasoning Process)

```
STEP 1: ANALYZE & PLAN
STEP 2: DESIGN DECISIONS  
STEP 3: GENERATE CANONICAL JSON
```

**Why this works:**
- Improves output quality through structured thinking
- Makes AI reasoning transparent
- Reduces errors and hallucinations

### 5. Structured Output (JSON Schema)

Uses Pydantic schemas for validation:
```python
response = await client.generate_content(
    prompt=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": CanonicalDesign.model_json_schema()
    }
)
```

**Why this works:**
- Guarantees valid JSON output
- Enforces type safety
- Enables automatic validation

---

## 🖼️ Image Generation Prompts

### Prompt Structure

All image generation prompts follow this structure:

```
[Subject] + [Style] + [Composition] + [Lighting] + [Quality Modifiers]
```

**Example:**
```
wireless headphones product, professional product photography,
centered composition isolated product, studio lighting soft shadows,
high resolution sharp focus professional quality 8K detail,
transparent background PNG with alpha channel
```

### Role-Specific Templates

#### Product Images

```python
from app.prompts.image_generation_prompts import ProductImagePrompts

prompt = ProductImagePrompts.ecommerce_product(
    product_name="wireless headphones",
    product_category="electronics",
    style="photorealistic",
    background="transparent"
)
```

**Output:**
```json
{
  "prompt": "wireless headphones, electronics product, professional product photography, photorealistic, centered composition, isolated product, front-facing view, studio lighting, soft shadows, even illumination, high resolution, sharp focus, professional quality, commercial photography, 8K detail, transparent background, PNG with alpha channel, isolated on white",
  "negative_prompt": "blurry, low quality, distorted, watermark, text, background clutter"
}
```

#### Person/Model Images

```python
prompt = PersonImagePrompts.model_portrait(
    demographics="young professional woman, 25-35 years old",
    expression="confident smile",
    style="professional"
)
```

#### Background Images

```python
prompt = BackgroundImagePrompts.abstract_background(
    color_scheme=["#FF6B6B", "#4ECDC4"],
    mood="energetic",
    complexity="medium"
)
```

#### Icons & Graphics

```python
prompt = IconGraphicPrompts.icon(
    icon_subject="shopping cart",
    style="modern",
    color_scheme="monochrome"
)
```

#### Complex Text Effects

```python
prompt = ComplexTextPrompts.text_with_effects(
    text_content="50% OFF",
    effect_type="gradient",
    color_scheme=["#FF6B6B", "#FFE66D"]
)
```

### Model-Specific Optimization

Different image generation models require different prompt formats:

```python
from app.prompts.image_generation_prompts import optimize_prompt_for_model

# For DALL-E 3
dalle_prompt = optimize_prompt_for_model(
    base_prompt=prompt,
    model=ImageGenerationModel.DALLE_3,
    aspect_ratio="1:1"
)

# For Midjourney
mj_prompt = optimize_prompt_for_model(
    base_prompt=prompt,
    model=ImageGenerationModel.MIDJOURNEY,
    aspect_ratio="16:9"
)

# For Stable Diffusion
sd_prompt = optimize_prompt_for_model(
    base_prompt=prompt,
    model=ImageGenerationModel.STABLE_DIFFUSION,
    aspect_ratio="1:1"
)
```

### Transparent Background Requirements

**Critical:** All generated images for ad creatives MUST have transparent backgrounds.

Every prompt includes:
```
transparent background, PNG with alpha channel, isolated on white
```

This ensures images can be:
- Layered properly in the editor
- Positioned anywhere on the canvas
- Composited with other elements
- Exported cleanly

---

## 🔄 Workflow

### Complete Generation Flow

```python
from app.services.ai_layout import layout_ai
from app.prompts.ad_creative_system_prompt import build_generation_prompt
from app.prompts.image_generation_prompts import optimize_prompt_for_model

# Step 1: Prepare input
user_prompt = "Create a summer sale ad for wireless headphones"
brand_kit = {
    "name": "AudioTech",
    "colors": {
        "primary": "#FF6B6B",
        "secondary": "#4ECDC4",
        "accent": "#FFE66D"
    },
    "fonts": {
        "primary": "Inter",
        "secondary": "DM Sans"
    },
    "logo_asset_id": "asset_logo_1"
}

# Step 2: Generate canonical JSON
prompt = build_generation_prompt(
    user_prompt=user_prompt,
    brand_kit=brand_kit,
    preferences={"style": "modern", "tone": "energetic"}
)

canonical_json = await layout_ai.generate_canonical_design(prompt)

# Step 3: Extract and generate images
image_layers = [
    layer for layer in canonical_json["layers"]
    if layer["type"] == "image" and layer["image"].get("generation_prompt")
]

generated_images = {}
for layer in image_layers:
    gen_prompt = layer["image"]["generation_prompt"]

    # Optimize for specific model
    optimized = optimize_prompt_for_model(
        base_prompt={
            "prompt": gen_prompt["prompt"],
            "negative_prompt": gen_prompt.get("negative_prompt", "")
        },
        model=ImageGenerationModel.NANO_BANANA,
        aspect_ratio=gen_prompt["aspect_ratio"]
    )

    # Generate image
    image_url = await image_generator.generate(optimized)
    generated_images[layer["id"]] = image_url

# Step 4: Inject generated images into canonical JSON
for layer in canonical_json["layers"]:
    if layer["id"] in generated_images:
        layer["image"]["url"] = generated_images[layer["id"]]
        # Remove generation_prompt after generation
        del layer["image"]["generation_prompt"]

# Step 5: Convert to editor format (Fabric.js)
fabric_json = convert_canonical_to_fabric(canonical_json)

# Step 6: Return to frontend for rendering
return fabric_json
```

### Error Handling & Validation

```python
from pydantic import ValidationError

try:
    # Validate canonical JSON
    validated = CanonicalDesign.model_validate(canonical_json)

    # Check constraints
    if len(validated.layers) > validated.constraints.max_layers:
        raise ValueError(f"Too many layers: {len(validated.layers)}")

    # Validate coordinates
    for layer in validated.layers:
        if layer.position.x < 0 or layer.position.x > validated.canvas.width:
            raise ValueError(f"Layer {layer.id} x position out of bounds")
        if layer.position.y < 0 or layer.position.y > validated.canvas.height:
            raise ValueError(f"Layer {layer.id} y position out of bounds")

except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    # Fall back to template or retry generation
```

---

## ✅ Best Practices

### 1. Prompt Engineering

**DO:**
- ✅ Use clear, specific language
- ✅ Provide examples (few-shot learning)
- ✅ Include constraints and boundaries
- ✅ Use chain-of-thought reasoning
- ✅ Validate output with schemas

**DON'T:**
- ❌ Use vague or ambiguous terms
- ❌ Omit technical constraints
- ❌ Skip validation steps
- ❌ Ignore model-specific requirements

### 2. Image Generation

**DO:**
- ✅ Always request transparent backgrounds
- ✅ Use role-specific templates
- ✅ Include quality modifiers
- ✅ Specify aspect ratios
- ✅ Use negative prompts

**DON'T:**
- ❌ Generate images without context
- ❌ Forget to specify PNG format
- ❌ Use generic prompts
- ❌ Ignore model limitations

### 3. Design Quality

**DO:**
- ✅ Follow visual hierarchy principles
- ✅ Maintain safe zones (5-10% margin)
- ✅ Ensure text readability (contrast ≥ 4.5:1)
- ✅ Use brand colors consistently
- ✅ Limit layers to 5-10 for performance

**DON'T:**
- ❌ Overcrowd the canvas
- ❌ Use too many fonts (max 2-3)
- ❌ Place text on busy backgrounds
- ❌ Ignore platform specifications

### 4. Performance

**DO:**
- ✅ Cache generated images
- ✅ Optimize image sizes
- ✅ Use lazy loading
- ✅ Implement retry logic
- ✅ Monitor generation times

**DON'T:**
- ❌ Generate unnecessarily large images
- ❌ Skip caching
- ❌ Ignore timeouts
- ❌ Generate images synchronously

---

## 📚 Examples

### Example 1: E-commerce Product Ad

**Input:**
```python
user_prompt = "Create an Instagram post for our new wireless headphones. Emphasize the 50% off sale."
brand_kit = {
    "name": "AudioTech",
    "colors": {"primary": "#FF6B6B", "secondary": "#1A1A1A", "accent": "#FFE66D"},
    "fonts": {"primary": "Inter", "secondary": "DM Sans"}
}
```

**Generated Canonical JSON:**
```json
{
  "format": "instagram_post",
  "canvas": {"width": 1080, "height": 1080},
  "background": {"type": "color", "color": "#1A1A1A"},
  "layers": [
    {
      "type": "text",
      "name": "Headline",
      "text": {
        "content": "50% OFF",
        "font_family": "Inter",
        "font_size": 96,
        "font_weight": 800,
        "color": "#FF6B6B"
      },
      "position": {"x": 540, "y": 200, "z_index": 10}
    },
    {
      "type": "image",
      "name": "Product",
      "image": {
        "role": "product",
        "generation_prompt": {
          "prompt": "wireless headphones, modern design, professional product photography...",
          "aspect_ratio": "1:1",
          "requires_transparent_bg": true
        }
      },
      "position": {"x": 540, "y": 600, "width": 500, "height": 500, "z_index": 5}
    }
  ]
}
```

### Example 2: Lifestyle Brand Ad

**Input:**
```python
user_prompt = "Create a lifestyle ad for our yoga studio. Show a peaceful, zen atmosphere."
brand_kit = {
    "name": "ZenFlow Yoga",
    "colors": {"primary": "#8BC34A", "secondary": "#F5F5F5", "accent": "#FF9800"},
    "fonts": {"primary": "Playfair Display", "secondary": "Lato"}
}
```

**Key Features:**
- Soft, calming colors
- Person in yoga pose (generated image)
- Elegant typography
- Minimalist composition

---

## 🔧 Implementation Checklist

- [x] Canonical JSON schema defined
- [x] System prompt created
- [x] Image generation templates built
- [ ] Integration with AI service (Gemini/GPT-4)
- [ ] Image generation service integration
- [ ] Canonical → Fabric.js converter
- [ ] Validation and error handling
- [ ] Caching layer
- [ ] Performance monitoring
- [ ] User testing and iteration

---

## 📖 References

### Research & Best Practices
- Google's 68-page Prompt Engineering Guide (2025)
- OpenAI Structured Outputs Documentation
- WCAG 2.1 Accessibility Guidelines
- Design Principles from Nielsen Norman Group

### Tools & Libraries
- Pydantic for schema validation
- Google Gemini for structured output
- Image generation APIs (DALL-E, Midjourney, Stable Diffusion)
- Fabric.js for canvas rendering

---

**Last Updated:** 2025-11-25
**Version:** 2.0
**Author:** Radic AI Team
