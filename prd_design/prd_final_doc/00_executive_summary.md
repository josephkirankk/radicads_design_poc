# Radic Pro — Executive Summary

> **Version**: 2.0  
> **Last Updated**: November 2025  
> **Status**: Final Specification

---

## Vision

Radic Pro is an **AI-Driven Creative Intelligence & Campaign Creation Platform** that enables marketers and agencies to generate professional, fully-editable ad creatives at scale. The platform automates brand understanding, creative concepts, layout structuring, and final creative assembly using a **block-based design system**.

Unlike traditional AI image generators that produce flat images, Radic Pro outputs **structured, editable designs** built from predefined blocks that users can customize in a browser-based editor.

**The product sits at the creative layer** — not replacing DSPs or agencies — but supercharging them with high-quality creative generation and intelligence.

---

## Core Value Proposition

| Traditional Approach | Radic Pro |
|---------------------|-----------|
| Flat PNG/JPG output | Block-based, layered designs |
| No text editing after generation | Full text editability with legible rendering |
| Regenerate entire image for changes | Modify individual blocks |
| Inconsistent brand application | Auto-extracted or uploaded brand kit |
| Single output | Multiple variants for funnel stages |
| Manual concept ideation | AI-powered creative concepts |
| Generic images | Studio-quality with text rendering |

---

## Target Users

### V1 (MVP)
- **Solo founders & marketers** at D2C/e-commerce brands
- **Small business owners** needing quick, professional social media ads
- **Content creators** producing promotional materials

### V2+ (Future)
- **Performance Marketing Agencies** — Rapid creative variations, competitor insights
- **Mid/Large Brands Using DSPs** — Strict brand guidelines, multi-format consistency

---

## Key Features

### V1 MVP Features

#### 1. Creative Generation Engine
- Natural language input → 3 editable design variants
- AI generates structured Design JSON using **Creative Concepts**
- Brand kit integration for consistent outputs
- **Block-based layout** (10 core blocks)

#### 2. Block-Based Editor
- Canva-like editing experience
- **10 predefined blocks**: Background, Headline, Subhead, Product Image, CTA Button, Logo, Offer Tag, Price, Badge/Shape, Footer
- Drag, resize, rotate blocks
- Inline text editing with font/color controls
- Block visibility and lock controls

#### 3. Smart Image System (Nano Banana Pro)
- AI-generated images with **legible text rendering**
- Studio-quality control (lighting, angles, depth)
- **Holistic context prompting** — Images blend naturally with design
- Up to 4K resolution on export

#### 4. Brand Kit
- Manual upload: Logo, colors, fonts
- Applied automatically to generated designs

#### 5. Export
- PNG/JPG export (1x, 2x resolution)
- Instagram 1080×1080 in V1

### V2+ Features (Future)
- Brand Intelligence Engine (auto-scraping)
- Audience & Persona Engine
- Competitor Intelligence Engine
- Campaign Builder with funnel stages
- Multiple formats (Story, Facebook, etc.)
- Video storyboards

---

## AI Model Stack

| Task | Model | Provider |
|------|-------|----------|
| **Image Generation** | Nano Banana Pro (Gemini 3 Pro Image) | Google via Replicate |
| **Layout/JSON Generation** | Gemini 3 Pro | Google via Replicate |
| **Copy Generation** | Gemini 3 Pro | Google |
| **Vision/Brand Analysis** | Gemini 3 Pro | Google |
| **Fallback Images** | FLUX 1.1 Pro | Replicate |
| **Fallback JSON** | GPT-5 Structured | OpenAI via Replicate |

**Why This Stack:**
- **Nano Banana Pro**: Best-in-class text rendering in images (critical for ad CTAs)
- **Gemini 3 Pro**: Native structured output, multimodal, excellent reasoning
- **Single ecosystem**: Simpler integration, better coherence

---

## Technical Highlights

### Block-Based Design System
- **10 predefined blocks** with semantic roles
- **Creative Concepts** define which blocks are required
- Blocks are an abstraction over the canonical Design JSON

### Editor-Agnostic Architecture
- **Canonical Design JSON** — Platform-owned format independent of any editor
- **Adapter Pattern** — Bidirectional conversion (Design JSON ↔ Fabric.js)
- **Future-proof** — Editor can be swapped without data migration

### AI-First Design
- Two-stage AI pipeline: Prompt → Brief → Design JSON
- Structured outputs with strict JSON schema validation
- Auto-repair for malformed AI responses

### Performance & Cost Optimized
- 1K resolution in editor, 2K/4K on export
- Smart image caching and recipe reuse
- Lazy-loaded editor bundle

---

## Success Metrics (V1)

| Metric | Target |
|--------|--------|
| Prompt → Design latency | < 15 seconds |
| Editor load time | < 3 seconds |
| Design generation success rate | > 95% |
| Text legibility in images | > 98% |
| User can export edited design | 100% |

---

## Cost Per Generation

| Component | Cost |
|-----------|------|
| Layout JSON (Gemini 3 Pro) | ~$0.04 |
| Copy Generation | ~$0.01 |
| Images (Nano Banana Pro 1K × 3) | ~$0.12 |
| **Total per generation (3 variants)** | **~$0.30** |

---

## Not in Scope (V1)

- Mobile apps
- Multi-user collaboration
- Video/animation
- Formats beyond Instagram (1080×1080)
- Template marketplace
- White-label/API access
- Brand auto-extraction (scraping)
- Competitor intelligence
- Persona engine
- Campaign builder with funnels

---

## Document Index

| Document | Description |
|----------|-------------|
| `01_product_requirements.md` | Full PRD with user flows, V1 MVP scope |
| `02_design_json_spec.md` | Canonical Design JSON + Block system |
| `03_tech_stack_spec.md` | Tech stack with Nano Banana Pro + Gemini 3 Pro |
| `04_architecture_spec.md` | System architecture and AI providers |
| `05_api_spec.md` | API endpoints and contracts |
| `06_implementation_roadmap.md` | Phased development plan (13 weeks) |
| `07_setup_guide.md` | **Practical setup: uv, venv, restart scripts** |
| `08_ui_design_guidelines.md` | **Modern UI patterns, Tailwind + Shadcn** |

---

## Key Design Principles

1. **KISS** — Simple solutions first, complexity only when justified
2. **Block-First** — Structured blocks over freeform layers
3. **Editor-Agnostic** — Design JSON is the source of truth
4. **AI-Assisted, Human-Controlled** — AI generates, humans refine
5. **Brand-First** — Every output should feel on-brand
6. **Text Matters** — Legible text in images is non-negotiable for ads
7. **Fail Gracefully** — Auto-repair, sensible defaults, clear error states

---

## Phased Roadmap Summary

| Phase | Focus | Duration |
|-------|-------|----------|
| **V1 MVP** | Core generation + Block editor + Export | 8-10 weeks |
| **V1.5** | Multi-format, Brand auto-extraction | 4-6 weeks |
| **V2** | Campaign builder, Competitor intel, Personas | 8-12 weeks |
