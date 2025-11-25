# Quick Start Guide: AI Ad Creative Generation

## 🚀 Getting Started in 5 Minutes

This guide will help you quickly integrate the AI ad creative generation system into your application.

---

## Step 1: Understanding the Flow

```
User Input → AI Layout Generation → Image Generation → Editor Rendering
```

1. **User provides:** Natural language prompt + brand kit
2. **AI generates:** Canonical Design JSON with layout and image prompts
3. **System generates:** All required images with transparent backgrounds
4. **System converts:** Canonical JSON → Fabric.js JSON
5. **Frontend renders:** Design in canvas editor

---

## Step 2: Basic Usage

### Generate a Design

```python
from app.prompts.ad_creative_system_prompt import build_generation_prompt
from app.schemas.canonical_design import CanonicalDesign
from google import genai

# 1. Prepare your inputs
user_prompt = "Create a summer sale ad for wireless headphones with 50% off"

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
    "logo_asset_id": "asset_123"  # Optional
}

preferences = {
    "style": "modern",
    "tone": "energetic",
    "target_audience": "young professionals"
}

# 2. Build the prompt
prompt = build_generation_prompt(
    user_prompt=user_prompt,
    brand_kit=brand_kit,
    preferences=preferences
)

# 3. Call AI model
client = genai.Client(api_key="your_api_key")
response = await client.aio.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": CanonicalDesign.model_json_schema()
    }
)

# 4. Parse and validate
canonical_json = CanonicalDesign.model_validate_json(response.text)
```

### Generate Images

```python
from app.prompts.image_generation_prompts import optimize_prompt_for_model, ImageGenerationModel

# Extract image layers that need generation
image_layers = [
    layer for layer in canonical_json.layers
    if layer.type == "image" and layer.image.generation_prompt
]

generated_images = {}

for layer in image_layers:
    gen_prompt = layer.image.generation_prompt
    
    # Optimize for your image generation model
    optimized = optimize_prompt_for_model(
        base_prompt={
            "prompt": gen_prompt.prompt,
            "negative_prompt": gen_prompt.negative_prompt or ""
        },
        model=ImageGenerationModel.NANO_BANANA,  # or DALLE_3, FLUX, etc.
        aspect_ratio=gen_prompt.aspect_ratio
    )
    
    # Call your image generation service
    image_url = await your_image_service.generate(
        prompt=optimized["prompt"],
        **optimized  # Pass model-specific parameters
    )
    
    generated_images[layer.id] = image_url

# Inject generated images back into canonical JSON
for layer in canonical_json.layers:
    if layer.id in generated_images:
        layer.image.url = generated_images[layer.id]
        layer.image.generation_prompt = None  # Clear after generation
```

### Convert to Editor Format

```python
from app.converters.canonical_to_fabric import convert_to_fabric

# Convert canonical JSON to Fabric.js format
fabric_json = convert_to_fabric(canonical_json)

# Return to frontend
return {
    "design_id": canonical_json.id,
    "canonical": canonical_json.model_dump(),
    "fabric": fabric_json,
    "generated_images": generated_images
}
```

---

## Step 3: Using Image Generation Templates

### Product Image

```python
from app.prompts.image_generation_prompts import ProductImagePrompts

prompt = ProductImagePrompts.ecommerce_product(
    product_name="wireless headphones",
    product_category="electronics",
    style="photorealistic"
)

# Returns:
# {
#   "prompt": "wireless headphones, electronics product, professional product photography...",
#   "negative_prompt": "blurry, low quality, distorted..."
# }
```

### Person/Model Image

```python
from app.prompts.image_generation_prompts import PersonImagePrompts

prompt = PersonImagePrompts.model_portrait(
    demographics="young professional woman, 25-35 years old",
    expression="confident smile",
    style="professional"
)
```

### Background Image

```python
from app.prompts.image_generation_prompts import BackgroundImagePrompts

prompt = BackgroundImagePrompts.abstract_background(
    color_scheme=["#FF6B6B", "#4ECDC4"],
    mood="energetic",
    complexity="medium"
)
```

### Icon/Graphic

```python
from app.prompts.image_generation_prompts import IconGraphicPrompts

prompt = IconGraphicPrompts.icon(
    icon_subject="shopping cart",
    style="modern",
    color_scheme="monochrome"
)
```

---

## Step 4: Error Handling

```python
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

try:
    # Validate canonical JSON
    canonical_json = CanonicalDesign.model_validate_json(response.text)
    
    # Validate constraints
    if len(canonical_json.layers) > canonical_json.constraints.max_layers:
        raise ValueError(f"Too many layers: {len(canonical_json.layers)}")
    
    # Validate coordinates are within bounds
    for layer in canonical_json.layers:
        if layer.position.x < 0 or layer.position.x > canonical_json.canvas.width:
            raise ValueError(f"Layer {layer.id} x position out of bounds")
        if layer.position.y < 0 or layer.position.y > canonical_json.canvas.height:
            raise ValueError(f"Layer {layer.id} y position out of bounds")
    
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    # Fall back to template or retry generation
    canonical_json = get_fallback_template(user_prompt, brand_kit)

except Exception as e:
    logger.error(f"Generation failed: {e}")
    # Retry with exponential backoff
    await retry_with_backoff(generate_design, max_retries=3)
```

---

## Step 5: Testing

### Test the Complete Flow

```python
import pytest
from app.prompts.ad_creative_system_prompt import build_generation_prompt
from app.schemas.canonical_design import CanonicalDesign

@pytest.mark.asyncio
async def test_design_generation():
    """Test complete design generation flow."""
    
    # Arrange
    user_prompt = "Create a summer sale ad"
    brand_kit = {
        "name": "Test Brand",
        "colors": {"primary": "#FF0000", "secondary": "#00FF00", "accent": "#0000FF"},
        "fonts": {"primary": "Arial", "secondary": "Helvetica"}
    }
    
    # Act
    prompt = build_generation_prompt(user_prompt, brand_kit)
    # ... call AI service ...
    
    # Assert
    assert canonical_json.format in ["instagram_post", "instagram_story", "facebook_post"]
    assert len(canonical_json.layers) > 0
    assert canonical_json.canvas.width > 0
    assert canonical_json.canvas.height > 0
```

---

## Common Patterns

### Pattern 1: Batch Generation

```python
async def generate_campaign_designs(campaign_brief: str, brand_kit: dict, count: int = 5):
    """Generate multiple design variations for A/B testing."""
    designs = []
    
    for i in range(count):
        prompt = build_generation_prompt(
            user_prompt=f"{campaign_brief} (Variation {i+1})",
            brand_kit=brand_kit,
            preferences={"variation": i+1}
        )
        
        design = await generate_design(prompt)
        designs.append(design)
    
    return designs
```

### Pattern 2: Iterative Refinement

```python
async def refine_design(canonical_json: CanonicalDesign, feedback: str):
    """Refine an existing design based on user feedback."""
    
    refinement_prompt = f"""
    Refine this design based on the following feedback:
    {feedback}
    
    Current design:
    {canonical_json.model_dump_json()}
    
    Make targeted improvements while maintaining the overall structure.
    """
    
    # Generate refined version
    refined = await generate_design(refinement_prompt)
    return refined
```

### Pattern 3: Template-Based Generation

```python
async def generate_from_template(template_id: str, customizations: dict):
    """Generate design from a template with customizations."""
    
    template = await get_template(template_id)
    
    prompt = f"""
    Use this template as a base:
    {template.model_dump_json()}
    
    Apply these customizations:
    {customizations}
    
    Maintain the template's structure but update colors, text, and images.
    """
    
    return await generate_design(prompt)
```

---

## Next Steps

1. **Read the full documentation:** `docs/AI_CREATIVE_PROMPT_SYSTEM.md`
2. **Explore the schemas:** `backend/app/schemas/canonical_design.py`
3. **Review prompt templates:** `backend/app/prompts/`
4. **Implement converters:** Create `canonical_to_fabric.py` converter
5. **Set up image generation:** Integrate with your preferred image gen API
6. **Test thoroughly:** Write comprehensive tests for all components

---

## Troubleshooting

### Issue: AI generates invalid JSON

**Solution:** Ensure you're using structured output with JSON schema validation:
```python
config={
    "response_mime_type": "application/json",
    "response_json_schema": CanonicalDesign.model_json_schema()
}
```

### Issue: Coordinates out of bounds

**Solution:** Add post-processing validation and clamping:
```python
def clamp_coordinates(layer, canvas_width, canvas_height):
    layer.position.x = max(0, min(layer.position.x, canvas_width))
    layer.position.y = max(0, min(layer.position.y, canvas_height))
```

### Issue: Generated images don't have transparent backgrounds

**Solution:** Ensure every image prompt includes:
```python
"transparent background, PNG with alpha channel, isolated on white"
```

### Issue: Text is unreadable

**Solution:** Validate contrast ratios and font sizes:
```python
def validate_text_readability(text_layer, background_color):
    contrast = calculate_contrast_ratio(text_layer.text.color, background_color)
    if contrast < 4.5:
        raise ValueError(f"Insufficient contrast: {contrast}")
```

---

**Need Help?** Check the full documentation or open an issue on GitHub.
