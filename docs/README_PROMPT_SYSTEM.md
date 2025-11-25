# 🎨 AI Ad Creative Prompt Engineering System

> **A production-ready, research-backed system for generating professional ad creatives using AI**

Built with 2025 best practices in prompt engineering, structured output, and image generation.

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Quick Start](#quick-start)
5. [Documentation](#documentation)
6. [Examples](#examples)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

---

## 🎯 Overview

This system enables you to generate professional ad creatives by simply describing what you want in natural language. The AI:

1. **Understands your requirements** (product, message, audience, style)
2. **Applies design best practices** (visual hierarchy, composition, typography)
3. **Generates structured layouts** (canonical JSON format)
4. **Creates optimized image prompts** (for transparent background generation)
5. **Ensures brand consistency** (colors, fonts, logo placement)

### What You Get

```
"Create a summer sale ad for wireless headphones"
                    ↓
    Professional Instagram post with:
    • Optimized layout and composition
    • Brand-consistent colors and fonts
    • High-quality product image (AI-generated)
    • Conversion-focused copy
    • Ready to edit in canvas editor
```

---

## ✨ Key Features

### 🎨 Design Excellence
- ✅ **Visual Hierarchy:** Clear focal points and eye flow
- ✅ **Professional Composition:** Rule of thirds, safe zones, balance
- ✅ **Typography Best Practices:** Readability, contrast, hierarchy
- ✅ **Color Theory:** 60-30-10 rule, brand consistency
- ✅ **Platform Optimization:** Instagram, Facebook, LinkedIn, Twitter

### 🤖 AI-Powered
- ✅ **Structured Output:** Guaranteed valid JSON with Pydantic
- ✅ **Chain-of-Thought:** AI reasons through design decisions
- ✅ **Brand Integration:** Automatic color/font application
- ✅ **Smart Defaults:** Fallbacks and error handling

### 🖼️ Image Generation
- ✅ **Role-Specific Templates:** Product, person, background, icon
- ✅ **Transparent Backgrounds:** All images PNG with alpha channel
- ✅ **Model Optimization:** DALL-E, Midjourney, Stable Diffusion, Flux
- ✅ **Quality Prompts:** Detailed, optimized for best results

### 🔧 Developer-Friendly
- ✅ **Editor-Agnostic:** Canonical format converts to any editor
- ✅ **Fully Typed:** Pydantic schemas for validation
- ✅ **Modular:** Easy to extend and customize
- ✅ **Well-Documented:** Comprehensive guides and examples

---

## 🏗️ Architecture

### Three-Layer System

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT LAYER                     │
│  Natural language + Brand kit + References + Prefs      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  AI GENERATION LAYER                    │
│  • System Prompt (expert role + principles)             │
│  • Canonical JSON Generation                            │
│  • Image Prompt Generation                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  CONVERSION LAYER                       │
│  • Image Generation (transparent backgrounds)           │
│  • Canonical → Editor Format (Fabric.js)                │
│  • Canvas Rendering                                     │
└─────────────────────────────────────────────────────────┘
```

### Core Components

| Component | File | Purpose |
|-----------|------|---------|
| **Canonical Schema** | `canonical_design.py` | Editor-agnostic design format |
| **System Prompt** | `ad_creative_system_prompt.py` | AI layout generation prompt |
| **Image Prompts** | `image_generation_prompts.py` | Image generation templates |
| **Layout Generator** | `canonical_layout_generator.py` | Service for generating layouts |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
uv pip install pydantic google-generativeai
```

### 2. Configure API Keys

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL_NAME=gemini-2.0-flash-exp
```

### 3. Generate Your First Design

```python
from app.services.canonical_layout_generator import canonical_layout_generator

# Define your inputs
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
    }
}

# Generate layout
canonical_design = await canonical_layout_generator.generate_layout(
    user_prompt=user_prompt,
    brand_kit=brand_kit,
    preferences={"style": "modern", "tone": "energetic"}
)

# canonical_design is now a validated CanonicalDesign object
print(f"Generated {len(canonical_design.layers)} layers")
print(f"Format: {canonical_design.format}")
print(f"Canvas: {canonical_design.canvas.width}x{canonical_design.canvas.height}")
```

### 4. Generate Images

```python
from app.prompts.image_generation_prompts import optimize_prompt_for_model

# Extract image layers
image_layers = [
    layer for layer in canonical_design.layers
    if layer.type == "image" and layer.image.generation_prompt
]

# Generate each image
for layer in image_layers:
    prompt = optimize_prompt_for_model(
        base_prompt={
            "prompt": layer.image.generation_prompt.prompt,
            "negative_prompt": layer.image.generation_prompt.negative_prompt
        },
        model="dall-e-3",
        aspect_ratio=layer.image.generation_prompt.aspect_ratio
    )
    
    # Call your image generation API
    image_url = await generate_image(prompt)
    layer.image.url = image_url
```

### 5. Convert to Editor Format

```python
# Convert to Fabric.js (you'll need to implement this converter)
from app.converters.canonical_to_fabric import convert_to_fabric

fabric_json = convert_to_fabric(canonical_design)

# Return to frontend
return {
    "design_id": canonical_design.id,
    "fabric": fabric_json
}
```

---

## 📚 Documentation

### Complete Guides

| Document | Description | Link |
|----------|-------------|------|
| **System Overview** | Complete architecture and design | [AI_CREATIVE_PROMPT_SYSTEM.md](./AI_CREATIVE_PROMPT_SYSTEM.md) |
| **Quick Start** | Get started in 5 minutes | [QUICK_START_GUIDE.md](./QUICK_START_GUIDE.md) |
| **Example** | Real-world e-commerce ad | [OPTIMIZED_PROMPT_EXAMPLE.md](./OPTIMIZED_PROMPT_EXAMPLE.md) |
| **Summary** | Executive summary | [PROMPT_SYSTEM_SUMMARY.md](./PROMPT_SYSTEM_SUMMARY.md) |

### Code Reference

| File | Purpose |
|------|---------|
| `canonical_design.py` | Pydantic schemas for canonical JSON |
| `ad_creative_system_prompt.py` | System prompt builder |
| `image_generation_prompts.py` | Image prompt templates |
| `canonical_layout_generator.py` | Layout generation service |

---

## 💡 Examples

### Example 1: E-commerce Product Ad

```python
result = await canonical_layout_generator.generate_layout(
    user_prompt="Create an Instagram post for wireless headphones, 50% off Black Friday sale",
    brand_kit=audiotech_brand,
    preferences={"style": "modern", "emphasis": "discount"}
)
```

**Output:** Professional Instagram post (1080x1080) with:
- Bold "50% OFF" headline
- Product image with transparent background
- Brand colors and fonts
- Call-to-action text
- Logo placement

### Example 2: Lifestyle Brand Ad

```python
result = await canonical_layout_generator.generate_layout(
    user_prompt="Create a peaceful yoga studio ad with zen atmosphere",
    brand_kit=zenflow_brand,
    preferences={"style": "minimalist", "tone": "calming"}
)
```

**Output:** Serene design with:
- Soft color palette
- Person in yoga pose
- Elegant typography
- Minimalist composition

### Example 3: Tech Product Launch

```python
result = await canonical_layout_generator.generate_layout(
    user_prompt="Announce our new AI-powered smartwatch with health tracking",
    brand_kit=techco_brand,
    preferences={"style": "futuristic", "tone": "innovative"}
)
```

**Output:** Modern tech ad with:
- Sleek product visualization
- Feature highlights
- Bold, tech-forward design
- Premium feel

---

## ✅ Best Practices

### For Prompts
1. **Be Specific:** Include product, message, audience, and style
2. **Provide Context:** Mention campaign goals and constraints
3. **Use Brand Kits:** Always provide colors, fonts, and logo
4. **Set Preferences:** Specify style, tone, and emphasis

### For Images
1. **Always Request Transparent Backgrounds:** Essential for layering
2. **Use Role-Specific Templates:** Better results than generic prompts
3. **Optimize for Model:** Different models need different formats
4. **Include Quality Modifiers:** "high resolution", "professional quality"

### For Validation
1. **Always Validate:** Use Pydantic schemas
2. **Check Constraints:** Bounds, font sizes, contrast ratios
3. **Handle Errors:** Implement retry logic with backoff
4. **Log Everything:** Track generation success/failure rates

---

## ❓ FAQ

### Q: What AI models are supported?
**A:** The system works with any model that supports structured JSON output (Gemini, GPT-4, Claude). Image generation supports DALL-E, Midjourney, Stable Diffusion, Flux, and custom models.

### Q: Can I use my own brand kit?
**A:** Yes! Just provide colors, fonts, and optionally a logo asset ID.

### Q: How do I customize the design principles?
**A:** Edit `ad_creative_system_prompt.py` to modify the design principles section.

### Q: What if the AI generates invalid coordinates?
**A:** The system includes automatic validation and clamping to ensure all coordinates are within canvas bounds.

### Q: Can I generate multiple variations?
**A:** Yes! Call the generator multiple times with different preferences or add variation numbers to the prompt.

### Q: How do I convert to my editor format?
**A:** Implement a converter from canonical JSON to your editor's format (see Fabric.js example in docs).

### Q: What about accessibility?
**A:** The system enforces WCAG AA contrast ratios (≥4.5:1) and minimum font sizes.

### Q: Can I refine generated designs?
**A:** Yes! You can pass the canonical JSON back with refinement instructions to iterate.

---

## 🎯 Next Steps

1. **Read the full documentation:** Start with [AI_CREATIVE_PROMPT_SYSTEM.md](./AI_CREATIVE_PROMPT_SYSTEM.md)
2. **Try the examples:** Follow [QUICK_START_GUIDE.md](./QUICK_START_GUIDE.md)
3. **Implement converters:** Create canonical → your editor format
4. **Integrate image generation:** Connect your preferred image API
5. **Test thoroughly:** Generate designs for your use cases
6. **Customize:** Adapt prompts and schemas to your needs

---

## 📞 Support

- **Documentation:** See `docs/` folder
- **Issues:** Open a GitHub issue
- **Questions:** Check FAQ above

---

**Built with ❤️ using 2025 AI best practices**
