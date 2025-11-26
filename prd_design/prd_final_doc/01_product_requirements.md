# Radic Pro — Product Requirements Document

> **Version**: 2.0  
> **Last Updated**: November 2025

---

## 1. Product Overview

### 1.1 Problem Statement

Marketers and agencies currently:
- Run many ads for each campaign (10+ variations)
- Need creatives tailored for different funnel stages (Awareness, Consideration, Conversion)
- Must manually reference brand guidelines, past ads, and competitor ads
- Repeat the same tasks across brands/products
- Waste money on creatives that don't align with persona or funnel
- Require fast iteration and creative testing
- Find existing AI tools produce non-editable flat images with illegible text

### 1.2 Solution

Radic Pro is an **AI-Driven Creative Intelligence Platform** that:
1. Converts natural language prompts into **block-based, fully editable** designs
2. Uses **Creative Concepts** to structure layouts (Product Highlight, Offer Focus, etc.)
3. Generates images with **legible text rendering** using Nano Banana Pro
4. Provides a browser-based block editor for refinement
5. Ensures brand consistency through brand kits
6. Enables rapid iteration with multiple design variants

### 1.3 V1 MVP Focus

V1 focuses on **proving the core value proposition**: AI generates professional, editable ad creatives with legible text. Advanced features (competitor intelligence, persona engine, campaign funnels) are deferred to V2.

---

## 2. User Personas

### Primary: Solo Marketer (Maya)
- **Role**: Marketing lead at a D2C skincare brand
- **Goals**: Create 10-15 social ads per week, maintain brand consistency
- **Pain Points**: Limited design budget, Canva templates feel generic
- **Tech Comfort**: Comfortable with web apps, not technical

### Secondary: Small Business Owner (Raj)
- **Role**: Owner of an electronics retail store
- **Goals**: Promote sales and new products on Instagram/Facebook
- **Pain Points**: No time to learn design tools, hires freelancers occasionally
- **Tech Comfort**: Basic, prefers simple interfaces

---

## 3. User Flows

### 3.1 Flow 1: Generate New Design

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Login     │───▶│ Enter Prompt│───▶│  Select     │───▶│   View      │
│             │    │ + Brand     │    │  Variants   │    │   Editor    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Steps:**
1. User logs in (email/OAuth)
2. Lands on prompt page
3. Selects brand kit (optional, can use default)
4. Enters natural language prompt:
   > "Instagram ad for Diwali electronics sale, 40% OFF, premium dark theme, show headphones"
5. Clicks "Generate Designs"
6. Sees loading state (10-15 seconds)
7. Views 2-3 design variants as thumbnails
8. Clicks preferred design → Opens in editor

### 3.2 Flow 2: Edit Design

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Editor    │───▶│  Make       │───▶│   Save/     │
│   Opens     │    │  Changes    │    │   Export    │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Editing Capabilities:**
- **Text**: Click to edit inline, change font/size/color/alignment
- **Layers**: Drag to move, handles to resize, rotate
- **Images**: Replace, regenerate with AI, adjust fit
- **Shapes**: Change fill/stroke, resize
- **Canvas**: Change background color/image

### 3.3 Flow 3: AI-Assisted Edit

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  In Editor  │───▶│ Enter AI    │───▶│  Review &   │
│             │    │ Instruction │    │  Apply      │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Example Instructions:**
- "Make it more minimal"
- "Change the color scheme to blue"
- "Make the headline bigger"
- "Remove the subheadline"

### 3.4 Flow 4: Export

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Click      │───▶│  Select     │───▶│  Download   │
│  Export     │    │  Format     │    │  File       │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Export Options (V1):**
- PNG (recommended for social)
- JPG (smaller file size)
- Resolution: 1x (1080px) or 2x (2160px)

---

## 4. Feature Specifications

### 4.1 Prompt Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Prompt | Text (max 500 chars) | Yes | Natural language description |
| Brand | Dropdown | No | Select from user's brand kits |
| Format | Dropdown | Yes | V1: Instagram Post only |
| Creative Concept | Dropdown | No | Optional: Product Highlight, Offer Focus, etc. |

**Prompt Best Practices (shown to user):**
- Include the occasion/theme (Diwali, Black Friday)
- Mention key copy (40% OFF, Free Shipping)
- Describe visual style (dark, minimal, vibrant)
- Note any required elements (product, logo)

### 4.2 Creative Concepts (V1)

Every creative is based on a **Creative Concept** that defines the layout structure and required blocks.

**V1 Concepts (3 to start):**

| Concept | Description | Required Blocks | Use Case |
|---------|-------------|-----------------|----------|
| **Product Highlight** | Hero product with supporting text | Background, Product Image, Headline, CTA, Logo | Product launches, features |
| **Offer Focus** | Discount/promotion front and center | Background, Headline, Offer Tag, CTA, Badge, Logo | Sales, discounts, deals |
| **Problem-Solution** | Before/after or pain-point messaging | Background, Headline, Subhead, Product Image, CTA | Educational, benefits |

**Future Concepts (V2):**
- Ingredients/Features
- Testimonial/Social Proof
- Seasonal/Event
- Before-After
- Routine/How-To

### 4.3 Block System (Core USP)

Every design is composed of **predefined blocks** instead of freeform layers. This ensures consistency and makes AI generation more reliable.

#### V1 Blocks (10 Core Blocks)

| Block | Type | Required | Description |
|-------|------|----------|-------------|
| **Background** | Image/Color | Always | Canvas background |
| **Headline** | Text | Always | Main message (largest text) |
| **Subhead** | Text | Optional | Supporting text |
| **Product Image** | Image | Concept-dependent | Hero product shot |
| **CTA Button** | Shape+Text | Usually | Call to action ("Shop Now") |
| **Logo** | Image | Usually | Brand logo placement |
| **Offer Tag** | Shape+Text | Concept-dependent | "40% OFF", "Free Shipping" |
| **Price** | Text | Optional | Product pricing |
| **Badge/Shape** | Shape | Optional | Decorative elements, frames |
| **Footer** | Text | Optional | Fine print, compliance |

#### Block Properties

Each block has:
- **blockType**: Identifier (headline, cta, product_image, etc.)
- **required**: Whether concept mandates this block
- **constraints**: Size limits, position zones, font ranges
- **content**: The actual data (text, image reference, colors)

#### V2 Blocks (Future)
- Ingredient Image
- Before/After Frame
- Social Proof (ratings, reviews)
- Compliance Text
- Overlay Gradient

### 4.4 Design Generation

**Input Processing (Gemini 3 Pro):**
1. Parse prompt for key elements
2. Select or confirm Creative Concept
3. Extract: headline, subheadline, CTA, offer, visual focus
4. Apply brand kit defaults
5. Generate 3 variants with same concept, different layouts

**Output:**
- Array of Design JSON objects
- Each variant uses same blocks, different positioning
- All share same copy and brand

**Variant Strategies:**
1. **Text-Left, Product-Right** — Classic product showcase
2. **Centered Text, Background Focus** — Bold statement
3. **Stacked Vertical** — Mobile-optimized hierarchy

### 4.5 Block-Based Editor

#### Canvas
- Fixed size: 1080×1080 pixels
- Background: Solid color, gradient, or image
- Zoom: 50%, 75%, 100%, 150%, 200%
- Pan: Click and drag on empty area

#### Block Editing

**Text Blocks (Headline, Subhead, CTA, Price, Footer)**
| Property | Editable | UI Control |
|----------|----------|------------|
| Content | Yes | Inline editing |
| Font Family | Yes | Dropdown |
| Font Size | Yes | Slider + Input |
| Font Weight | Yes | Dropdown |
| Color | Yes | Color picker |
| Alignment | Yes | Button group |
| Position | Yes | Drag |
| Size | Yes | Handles |

**Image Blocks (Product Image, Logo, Background)**
| Property | Editable | UI Control |
|----------|----------|------------|
| Image | Yes | Upload / AI Regenerate |
| Position | Yes | Drag |
| Size | Yes | Handles |
| Fit | Yes | Dropdown (cover/contain/fill) |
| Opacity | Yes | Slider |

**Shape Blocks (Badge, Offer Tag, CTA Button)**
| Property | Editable | UI Control |
|----------|----------|------------|
| Shape Type | No | Set by block type |
| Fill Color | Yes | Color picker |
| Stroke Color | Yes | Color picker |
| Corner Radius | Yes | Slider |
| Position | Yes | Drag |
| Size | Yes | Handles |
| Text (if applicable) | Yes | Inline editing |

#### Toolbar Actions
- Undo / Redo
- Delete block
- Duplicate block
- Bring forward / Send backward
- Lock / Unlock
- Show / Hide block

#### Side Panels
- **Left**: Block list with visibility toggles
- **Right**: Properties panel for selected block
- **Bottom** (optional): AI instruction input (V1.5)

### 4.6 Brand Kit

**Brand Kit Schema:**
```
Brand Kit
├── Name (e.g., "VoltSound")
├── Colors
│   ├── Primary (#FFCC00)
│   ├── Secondary (#050816)
│   ├── Accent (#FF4D00)
│   └── Text (#FFFFFF)
├── Fonts
│   ├── Primary (Inter, weights: 400, 700, 800)
│   └── Secondary (DM Sans, weights: 400, 500)
└── Logo (uploaded image asset)
```

**Usage:**
- AI uses brand colors/fonts by default
- "Apply Brand" button in editor recolors design
- Logo auto-included in designs (configurable)

### 4.7 Smart Images (Nano Banana Pro)

Smart Images are AI-generated images using **Nano Banana Pro (Gemini 3 Pro Image)**, which excels at:
- **Legible text rendering** — CTAs, offers, headlines render clearly
- **Studio-quality control** — Lighting, angles, depth of field
- **Multi-image fusion** — Blend up to 14 images
- **Character consistency** — Maintain identity across edits
- **Up to 4K resolution**

**Smart Image Types:**
| Type | Description | Example |
|------|-------------|---------|
| `product_shot` | AI-enhanced product photo | Studio lighting, clean background |
| `background` | Full-canvas background | Abstract patterns, gradients |
| `text_render` | Stylized text in image | Neon effect, 3D text, calligraphy |
| `composite` | Multi-image blend | Product + lifestyle scene |

**Holistic Context Prompting:**

Every Smart Image generation includes full design context for seamless blending:

```json
{
  "smartImagePrompt": "studio product shot of wireless headphones",
  "model": "nano-banana-pro",
  "resolution": "2k",
  "holisticContext": {
    "designPurpose": "Instagram ad for Diwali electronics sale",
    "overallTheme": "premium dark, festive gold accents",
    "adjacentBlocks": [
      "Headline: 'Diwali Mega Sale' in gold Inter font",
      "Offer Tag: Orange badge with '40% OFF'",
      "Background: Dark purple (#050816)"
    ],
    "brandColors": ["#FFCC00", "#050816", "#FF4D00"],
    "compositionHints": "Product should face left, warm lighting from right",
    "textToRender": null
  }
}
```

**Text-in-Image Generation:**

For blocks requiring stylized text (decorative headlines, CTAs), Nano Banana Pro generates the text directly:

```json
{
  "smartImagePrompt": "Create a promotional badge",
  "textToRender": "40% OFF",
  "style": "bold gold text with black outline, festive sparkles",
  "resolution": "1k"
}
```

### 4.8 Export

**Process:**
1. User clicks "Export"
2. Select format (PNG/JPG) and resolution
3. System renders full-resolution canvas
4. Smart images regenerated at high-res if needed
5. Download triggered or link provided

**Export Settings:**
| Setting | Options | Default |
|---------|---------|---------|
| Format | PNG, JPG | PNG |
| Resolution | 1x, 2x | 1x |
| Quality (JPG) | 80%, 90%, 100% | 90% |

---

## 5. Non-Functional Requirements

### 5.1 Performance
| Metric | Target |
|--------|--------|
| Design generation | < 15 seconds |
| Editor initial load | < 3 seconds |
| Layer manipulation | < 100ms response |
| Export (1x) | < 5 seconds |
| Export (2x) | < 10 seconds |

### 5.2 Reliability
- 99.5% uptime for web app
- Graceful degradation if AI services are slow
- Auto-save designs every 30 seconds
- Design recovery on browser crash

### 5.3 Security
- JWT-based authentication
- All API calls over HTTPS
- User data isolated (multi-tenant)
- No design data used for AI training without consent

### 5.4 Scalability (V1 Targets)
- Support 1,000 concurrent users
- Handle 10,000 design generations/day
- Store 100,000 designs

---

## 6. Out of Scope (V1)

| Feature | Rationale | Future Version |
|---------|-----------|----------------|
| **Brand Intelligence Engine** | Auto-scraping adds complexity | V1.5 |
| **Persona Engine** | Requires user research data | V2 |
| **Competitor Intelligence** | Legal/API complexity | V2 |
| **Campaign Builder** | Funnel stages are V2 | V2 |
| Multiple formats | Simplify V1 | V1.5 |
| Video/animation | Different tech stack | V2 |
| Mobile apps | Focus on web first | V2 |
| Real-time collaboration | Complexity | V2 |
| Template marketplace | Need user base first | V2 |
| API access | B2B feature | V2 |
| Bulk generation | Power user feature | V1.5 |
| AI Edit Instructions | Requires more prompt engineering | V1.5 |
| All 18 blocks | Start with 10, expand later | V1.5 |
| 40 creative concepts | Start with 3, expand later | V1.5 |

---

## 7. Success Criteria

### Launch (V1.0)
- [ ] User can sign up and log in
- [ ] User can create and manage brand kits
- [ ] User can generate 3 design variants from prompts
- [ ] User can edit all block types in editor
- [ ] User can export PNG/JPG at 1x and 2x resolution
- [ ] Smart images blend naturally with designs
- [ ] **Text in generated images is legible (>98% accuracy)**
- [ ] Designs use correct brand colors and fonts

### Quality Gates
- [ ] 95% of generations produce valid, renderable designs
- [ ] No data loss on save/load cycles
- [ ] Editor handles 20+ blocks without lag
- [ ] All text blocks remain editable (not rasterized)
- [ ] Text rendered in images is readable at 1080px
- [ ] Generation completes in < 15 seconds

---

## 8. Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| AI generates invalid JSON | High | Medium | Strict schema validation + auto-repair (Gemini 3 Pro) |
| Smart images don't blend | Medium | Low | Holistic context prompting (Nano Banana Pro) |
| Text in images illegible | High | Low | Nano Banana Pro excels at text rendering |
| Editor performance issues | High | Low | Lazy loading, virtualization |
| AI costs exceed budget | High | Medium | 1K resolution in editor, 2K/4K on export only |
| User prompt quality varies | Medium | High | Prompt suggestions, concept selection UI |
| Nano Banana Pro API limits | Medium | Low | FLUX 1.1 Pro fallback for non-text images |
| Gemini 3 Pro downtime | High | Low | GPT-5 Structured fallback for JSON generation |

---

## 9. AI Model Configuration

### Primary Models (via Replicate)

| Task | Model | Pricing |
|------|-------|---------|
| Layout/JSON | Gemini 3 Pro | ~$0.02/1K output tokens |
| Copy Generation | Gemini 3 Pro | (same) |
| Image Generation | Nano Banana Pro | ~$0.04 (1K) / ~$0.13 (2K) |
| Vision/Analysis | Gemini 3 Pro | (same) |

### Fallback Models

| Task | Model | When to Use |
|------|-------|-------------|
| Images (no text) | FLUX 1.1 Pro ($0.04) | Backgrounds, product shots |
| Fast Preview | FLUX Schnell ($0.003) | Editor drafts |
| JSON Generation | GPT-5 Structured | Gemini failures |
| Complex Layouts | Claude 4.5 Sonnet | Multi-step reasoning |

### Cost Per Generation (3 variants)

| Component | Cost |
|-----------|------|
| Layout JSON | ~$0.04 |
| Copy | ~$0.01 |
| Images (1K × 3) | ~$0.12 |
| **Total** | **~$0.17 - $0.30** |
