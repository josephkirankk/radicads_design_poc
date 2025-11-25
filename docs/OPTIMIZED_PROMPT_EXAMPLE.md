# Optimized Prompt Example

## 📝 Complete Example: E-commerce Product Ad

This document shows a complete, real-world example of the optimized prompt system in action.

---

## Input Parameters

```python
user_prompt = """
Create an Instagram post for our new wireless headphones launch. 
We're running a limited-time 50% off sale for Black Friday.
The headphones are premium, noise-canceling, and come in midnight black.
Target audience is young professionals (25-35) who value quality audio.
"""

brand_kit = {
    "name": "AudioTech Pro",
    "colors": {
        "primary": "#FF6B6B",      # Vibrant red
        "secondary": "#1A1A1A",    # Deep black
        "accent": "#FFE66D"        # Golden yellow
    },
    "fonts": {
        "primary": "Inter",
        "secondary": "DM Sans"
    },
    "logo_asset_id": "asset_logo_audiotech"
}

reference_images = [
    "Reference 1: Minimalist product photography with dramatic lighting",
    "Reference 2: Bold typography with geometric shapes"
]

preferences = {
    "style": "modern and bold",
    "tone": "premium but accessible",
    "emphasis": "product quality and discount",
    "avoid": "cluttered layouts, too many elements"
}
```

---

## Generated Complete Prompt

```
You are an expert ad creative designer with 15+ years of experience creating high-performing social media advertisements. You specialize in:

- Visual hierarchy and composition
- Color theory and brand consistency
- Typography and readability
- Conversion-focused design
- Platform-specific best practices (Instagram, Facebook, LinkedIn, Twitter)

Your designs consistently achieve high engagement rates because you understand:
- The psychology of visual attention
- The importance of clear messaging
- The balance between aesthetics and functionality
- How to guide the viewer's eye through the design

You think systematically about every design decision and can articulate your reasoning.

## CORE DESIGN PRINCIPLES

### 1. Visual Hierarchy
- Establish a clear focal point (primary element that draws attention first)
- Use size, color, and position to create hierarchy
- Guide the viewer's eye in a Z-pattern or F-pattern
- Ensure secondary elements support, not compete with, the primary message

### 2. Composition & Layout
- Follow the rule of thirds for balanced composition
- Maintain safe zones: 5-10% margin from canvas edges
- Use white space effectively - don't overcrowd
- Align elements to a grid for professional appearance
- Balance visual weight across the canvas

### 3. Typography
- Minimum font size: 14px for body text, 24px for headlines
- Maximum 2-3 font families per design
- Ensure text contrast ratio ≥ 4.5:1 (WCAG AA standard)
- Use font weight and size to create hierarchy
- Keep headlines concise (max 6-8 words)
- Line height: 1.2-1.5 for readability

### 4. Color Theory
- Use brand colors as foundation
- Apply 60-30-10 rule: 60% dominant, 30% secondary, 10% accent
- Ensure sufficient contrast for readability
- Use color psychology: warm colors (energy), cool colors (trust)
- Limit palette to 3-5 colors maximum

### 5. Platform Optimization
- Instagram: Bold, vibrant, lifestyle-focused
- Facebook: Community-oriented, relatable
- LinkedIn: Professional, data-driven, authoritative
- Twitter: Concise, attention-grabbing, timely

### 6. Conversion Best Practices
- Clear call-to-action (if applicable)
- Benefit-focused messaging
- Social proof elements (when relevant)
- Urgency/scarcity indicators (for sales)
- Product/service clearly visible

## TECHNICAL CONSTRAINTS

### Canvas & Dimensions
- Instagram Post: 1080x1080px (1:1)
- Instagram Story: 1080x1920px (9:16)
- Facebook Post: 1200x630px (1.91:1)
- Twitter Post: 1200x675px (16:9)
- LinkedIn Post: 1200x627px (1.91:1)

### Layer Limits
- Maximum 20 layers per design (for performance)
- Minimum 3 layers (background + 2 content layers)
- Recommended: 5-10 layers for optimal balance

### Safe Zones
- Keep critical elements 5-10% away from edges
- Account for platform UI overlays (profile pics, buttons)
- Text should never touch canvas edges

### Image Generation
- All generated images MUST have transparent backgrounds
- Use appropriate aspect ratios for each element
- Product images: square or portrait orientation
- People: portrait orientation, centered
- Background elements: match canvas aspect ratio
- Icons/decorations: square, small size

### Text Readability
- Minimum font size: 14px (body), 24px (headlines)
- Maximum line length: 60 characters
- Contrast ratio: ≥ 4.5:1 for normal text, ≥ 3:1 for large text
- Avoid text on busy backgrounds without contrast treatment

## BRAND KIT

**Brand Name:** AudioTech Pro

**Colors:**
- Primary: #FF6B6B
- Secondary: #1A1A1A
- Accent: #FFE66D

**Fonts:**
- Primary: Inter
- Secondary: DM Sans

**Logo:** Available

**IMPORTANT:** Use these brand colors and fonts throughout the design. The logo should be included if provided, typically in a corner or header position.

## REFERENCE IMAGES

The user has provided 2 reference image(s):
- Reference 1: Minimalist product photography with dramatic lighting
- Reference 2: Bold typography with geometric shapes

Consider these references for style, composition, or content inspiration.

## USER PREFERENCES

- style: modern and bold
- tone: premium but accessible
- emphasis: product quality and discount
- avoid: cluttered layouts, too many elements

## USER REQUEST

Create an Instagram post for our new wireless headphones launch. 
We're running a limited-time 50% off sale for Black Friday.
The headphones are premium, noise-canceling, and come in midnight black.
Target audience is young professionals (25-35) who value quality audio.

## YOUR TASK

Create a professional ad creative design following this process:

### STEP 1: ANALYZE & PLAN
Think through the design strategy:
1. What is the primary message/goal?
2. Who is the target audience?
3. What format is most appropriate?
4. What should be the focal point?
5. What visual style matches the brand and message?
6. What elements are needed (text, images, shapes)?

### STEP 2: DESIGN DECISIONS
Make specific decisions about:
- Canvas format and dimensions
- Background (color, gradient, or image)
- Text hierarchy (headline, subheadline, body, CTA)
- Image elements needed (product, person, background, etc.)
- Decorative shapes for visual interest
- Color application (60-30-10 rule)
- Layout composition (rule of thirds, alignment)

### STEP 3: GENERATE CANONICAL JSON
Output a complete Canonical Design JSON with:
- Appropriate canvas size for the format
- Background configuration
- All layers with accurate positions (within canvas bounds)
- Text layers with complete typography properties
- Image layers with detailed generation prompts (for AI image generation)
- Shape layers for decorative elements
- Proper z-index ordering (background to foreground)
- Effects (shadows, opacity) where appropriate

### CRITICAL REQUIREMENTS:
1. **All coordinates must be within canvas bounds** (0 to width/height)
2. **Image layers needing generation must have detailed prompts**
3. **Text must be readable** (sufficient size and contrast)
4. **Follow brand kit** (colors, fonts, logo placement)
5. **Maintain visual hierarchy** (clear focal point)
6. **Use safe zones** (5-10% margin from edges)
7. **All generated images must specify transparent background**

Output ONLY the Canonical Design JSON. No explanations, no markdown, just valid JSON.
```

---

## Expected Output (Canonical JSON)

The AI would generate something like this:

```json
{
  "id": "design_audiotech_bf_001",
  "schema_version": "2.0",
  "owner_id": "user_123",
  "title": "AudioTech Pro Black Friday Sale",
  "format": "instagram_post",
  
  "canvas": {
    "width": 1080,
    "height": 1080,
    "unit": "px"
  },
  
  "background": {
    "type": "color",
    "color": "#1A1A1A"
  },
  
  "brand": {
    "brand_id": "brand_audiotech",
    "name": "AudioTech Pro",
    "colors": {
      "primary": "#FF6B6B",
      "secondary": "#1A1A1A",
      "accent": "#FFE66D"
    },
    "fonts": {
      "primary": "Inter",
      "secondary": "DM Sans"
    },
    "logo_asset_id": "asset_logo_audiotech"
  },
  
  "layers": [
    {
      "id": "layer_bg_shape",
      "type": "shape",
      "name": "Background Accent Shape",
      "position": {
        "x": 800,
        "y": 200,
        "width": 400,
        "height": 400,
        "rotation": 45,
        "z_index": 1,
        "origin_x": "center",
        "origin_y": "center"
      },
      "shape": {
        "shape_type": "rectangle",
        "fill": "#FF6B6B",
        "border_radius": 20
      },
      "effects": {
        "opacity": 0.15,
        "blend_mode": "normal"
      },
      "locked": false,
      "visible": true
    },
    {
      "id": "layer_product",
      "type": "image",
      "name": "Wireless Headphones Product",
      "position": {
        "x": 540,
        "y": 650,
        "width": 600,
        "height": 600,
        "rotation": 0,
        "z_index": 5,
        "origin_x": "center",
        "origin_y": "center"
      },
      "image": {
        "role": "product",
        "generation_prompt": {
          "prompt": "premium wireless headphones in midnight black color, noise-canceling over-ear design, professional product photography, centered composition, isolated product, front-facing three-quarter view, studio lighting with dramatic side lighting, soft shadows, sleek modern design, high-end consumer electronics, high resolution, sharp focus, professional quality, commercial photography, 8K detail, transparent background, PNG with alpha channel, isolated on white",
          "negative_prompt": "blurry, low quality, distorted, watermark, text, background clutter, cheap looking, plastic, toy-like",
          "style_modifiers": ["photorealistic", "premium product photography", "dramatic lighting"],
          "quality_modifiers": ["high resolution", "8K detail", "professional quality", "sharp focus"],
          "aspect_ratio": "1:1",
          "requires_transparent_bg": true
        }
      },
      "effects": {
        "opacity": 1.0,
        "blend_mode": "normal",
        "shadow": {
          "offset_x": 0,
          "offset_y": 20,
          "blur": 40,
          "color": "rgba(0, 0, 0, 0.4)",
          "opacity": 1.0
        }
      },
      "locked": false,
      "visible": true
    },
    {
      "id": "layer_headline",
      "type": "text",
      "name": "Main Headline",
      "position": {
        "x": 540,
        "y": 180,
        "width": 900,
        "height": 120,
        "rotation": 0,
        "z_index": 10,
        "origin_x": "center",
        "origin_y": "center"
      },
      "text": {
        "content": "50% OFF",
        "font_family": "Inter",
        "font_size": 96,
        "font_weight": 800,
        "line_height": 1.0,
        "letter_spacing": -2,
        "text_align": "center",
        "color": "#FF6B6B",
        "text_transform": "uppercase"
      },
      "effects": {
        "opacity": 1.0,
        "blend_mode": "normal",
        "shadow": {
          "offset_x": 0,
          "offset_y": 4,
          "blur": 12,
          "color": "rgba(255, 107, 107, 0.5)",
          "opacity": 1.0
        }
      },
      "locked": false,
      "visible": true
    },
    {
      "id": "layer_subheadline",
      "type": "text",
      "name": "Subheadline",
      "position": {
        "x": 540,
        "y": 280,
        "width": 800,
        "height": 60,
        "rotation": 0,
        "z_index": 10,
        "origin_x": "center",
        "origin_y": "center"
      },
      "text": {
        "content": "Premium Noise-Canceling",
        "font_family": "DM Sans",
        "font_size": 32,
        "font_weight": 500,
        "line_height": 1.3,
        "letter_spacing": 0,
        "text_align": "center",
        "color": "#FFFFFF"
      },
      "effects": {
        "opacity": 0.9,
        "blend_mode": "normal"
      },
      "locked": false,
      "visible": true
    },
    {
      "id": "layer_cta",
      "type": "text",
      "name": "Call to Action",
      "position": {
        "x": 540,
        "y": 980,
        "width": 600,
        "height": 50,
        "rotation": 0,
        "z_index": 10,
        "origin_x": "center",
        "origin_y": "center"
      },
      "text": {
        "content": "LIMITED TIME • BLACK FRIDAY",
        "font_family": "Inter",
        "font_size": 20,
        "font_weight": 600,
        "line_height": 1.2,
        "letter_spacing": 2,
        "text_align": "center",
        "color": "#FFE66D",
        "text_transform": "uppercase"
      },
      "effects": {
        "opacity": 1.0,
        "blend_mode": "normal"
      },
      "locked": false,
      "visible": true
    },
    {
      "id": "layer_logo",
      "type": "image",
      "name": "Brand Logo",
      "position": {
        "x": 100,
        "y": 100,
        "width": 150,
        "height": 50,
        "rotation": 0,
        "z_index": 15,
        "origin_x": "left",
        "origin_y": "top"
      },
      "image": {
        "role": "logo",
        "asset_id": "asset_logo_audiotech"
      },
      "effects": {
        "opacity": 1.0,
        "blend_mode": "normal"
      },
      "locked": false,
      "visible": true
    },
    {
      "id": "layer_accent_circle",
      "type": "shape",
      "name": "Accent Circle",
      "position": {
        "x": 950,
        "y": 950,
        "width": 200,
        "height": 200,
        "rotation": 0,
        "z_index": 2,
        "origin_x": "center",
        "origin_y": "center"
      },
      "shape": {
        "shape_type": "circle",
        "fill": "#FFE66D"
      },
      "effects": {
        "opacity": 0.2,
        "blend_mode": "normal"
      },
      "locked": false,
      "visible": true
    }
  ],

  "metadata": {
    "created_at": "2025-11-25T10:00:00Z",
    "updated_at": "2025-11-25T10:00:00Z",
    "source": "ai_generated",
    "ai_prompt": "Create an Instagram post for our new wireless headphones launch...",
    "design_style": "modern and bold",
    "visual_hierarchy": ["layer_headline", "layer_product", "layer_subheadline", "layer_cta", "layer_logo"]
  },

  "constraints": {
    "safe_zone_margin": 0.05,
    "min_font_size": 14,
    "max_layers": 20,
    "text_contrast_ratio": 4.5
  },

  "campaign_id": null
}
```

---

## Image Generation Details

### Product Image Prompt

**Layer:** `layer_product`

**Full Prompt:**
```
premium wireless headphones in midnight black color, noise-canceling over-ear design,
professional product photography, centered composition, isolated product,
front-facing three-quarter view, studio lighting with dramatic side lighting,
soft shadows, sleek modern design, high-end consumer electronics,
high resolution, sharp focus, professional quality, commercial photography, 8K detail,
transparent background, PNG with alpha channel, isolated on white
```

**Negative Prompt:**
```
blurry, low quality, distorted, watermark, text, background clutter,
cheap looking, plastic, toy-like
```

**Parameters:**
- Aspect Ratio: 1:1
- Transparent Background: Yes
- Style: Photorealistic, premium product photography
- Quality: High resolution, 8K detail

---

## Design Analysis

### Visual Hierarchy

1. **Primary Focus:** "50% OFF" headline (largest, brightest, top-center)
2. **Secondary Focus:** Product image (center, large, with shadow)
3. **Tertiary Elements:** Subheadline and CTA text
4. **Supporting Elements:** Logo, decorative shapes

### Color Application (60-30-10 Rule)

- **60% Dominant:** Black background (#1A1A1A)
- **30% Secondary:** Red accent (#FF6B6B) in headline and shape
- **10% Accent:** Yellow (#FFE66D) in CTA and circle

### Composition

- **Rule of Thirds:** Headline in upper third, product in center, CTA in lower third
- **Safe Zones:** All text 5-10% from edges
- **Balance:** Decorative shapes balance the composition
- **Alignment:** All elements center-aligned for cohesion

### Typography

- **Headline:** 96px, bold (800), high contrast
- **Subheadline:** 32px, medium (500), readable
- **CTA:** 20px, semi-bold (600), uppercase with letter spacing
- **Contrast Ratios:** All text meets WCAG AA standards (≥4.5:1)

### Effects

- **Shadows:** Used on headline and product for depth
- **Opacity:** Decorative shapes at 15-20% for subtlety
- **Blend Modes:** Normal for all layers (simple, performant)

---

## Next Steps After Generation

1. **Validate JSON:** Use Pydantic schema validation
2. **Generate Product Image:** Send prompt to image generation API
3. **Inject Image URL:** Update `layer_product.image.url` with generated image
4. **Convert to Fabric.js:** Use canonical-to-fabric converter
5. **Render in Canvas:** Display in frontend editor
6. **Allow Editing:** User can refine the design
7. **Export:** Generate final PNG/JPG for publishing

---

## Key Takeaways

✅ **Structured Prompt:** Clear role, principles, constraints, and task
✅ **Chain-of-Thought:** AI thinks through strategy before generating
✅ **Detailed Image Prompts:** Specific, optimized for quality generation
✅ **Brand Consistency:** Uses brand colors, fonts, and logo
✅ **Technical Validity:** All coordinates within bounds, proper z-index
✅ **Design Quality:** Follows visual hierarchy, composition, and readability principles
✅ **Transparent Backgrounds:** All generated images specify PNG with alpha
✅ **Extensible:** Easy to modify, refine, or regenerate

---

**This is a production-ready prompt system that generates professional, conversion-focused ad creatives!**

