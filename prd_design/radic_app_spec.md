# AI Design App – Detailed Product & Technical Design (KISS, Extensible, Performant)

> Goal: A **Canva-style editor** where a user types a prompt and gets **fully editable** ad/social designs (not flat images), with a simple but solid architecture that a small team can build and extend.

This document is written so you can hand it directly to your product + engineering team.

---

## 1. Goals & Design Principles

### 1.1 Product Goals (V1)

- User can:
  1. **Type a prompt** (“Instagram ad for Diwali electronics sale, premium dark theme, 40% OFF”).
  2. Get **2–3 editable designs** (layers, text, shapes, images).
  3. Open one in a **browser-based editor** (Canva-like).
  4. Make manual tweaks (drag, resize, change text/colours/fonts).
  5. **Export** PNG/JPG.

- Focus niche for V1: **social ads for D2C / e-commerce brands**.

This mirrors what Canva AI / Magic Design and similar tools do: a prompt → multiple editable layouts you can immediately tweak.

### 1.2 Design Principles (KISS + Best Practices)

1. **KISS**  
   - Single web app (no mobile apps in V1).
   - Single main format (Instagram square 1080×1080).
   - Only 3 layer types: `text | shape | image`.
   - Monolith backend (logically modular, but one deployable).

2. **Extensible**
   - Versioned **Design JSON schema**.
   - Clean separation:
     - Editor vs Design JSON data model.
     - AI orchestration vs core app logic.
   - Templates and brand kits from day 1.

3. **Maintainable**
   - Typed schemas (TypeScript / Pydantic).
   - Clear module boundaries (auth, designs, AI, assets, export).
   - Avoid overengineering (no microservices until needed).

4. **Performant**
   - Use proven canvas libraries (Polotno/Konva).
   - Follow Konva performance guidance: small canvas, few layers, caching used carefully, minimize listeners.
   - AI calls are the bottleneck → keep them predictable and structured.

5. **Trust & Privacy**
   - Don’t silently use user designs for training without explicit opt-in.

---

## 2. Product Scope & User Flows (V1)

### 2.1 User Types

- **Solo founders / marketers** at small D2C brands.
- Need quick, on-brand social ads, without hiring a designer.

### 2.2 Main Flows

1. **Prompt → Designs**
   - User logs in.
   - Selects brand (optional).
   - Enters natural language prompt.
   - Clicks “Generate designs”.
   - Sees 2–3 generated design thumbnails.

2. **Edit Design**
   - Click a design → opens the editor.
   - User:
     - Edits text inline.
     - Drags/moves layers.
     - Changes colors/fonts in a side panel.
   - (Optional in V1) Uses AI “tweak” command (“make it more minimal”).

3. **Export**
   - Click “Export” → PNG/JPG.
   - Download or copy link.

4. **Brand Kit**
   - Define a brand:
     - Primary/secondary/accent colors.
     - Primary/secondary fonts.
     - Logo.
   - AI uses this by default when generating designs.

V1 avoids multiple formats, bulk generation, collaboration, etc. Those go into later phases.

---

## 3. System Architecture (High-level)

### 3.1 Components

- **Frontend (Next.js + React)**
  - Marketing site + app shell.
  - Prompt page.
  - Design gallery.
  - Editor (Polotno-based).
  - Brand kit screens.

- **Backend (FastAPI or NestJS – monolith)**
  - Auth (JWT / session).
  - REST APIs: designs, brands, assets, AI, export.
  - AI orchestration: LLM calls to generate/modify designs.
  - DB & storage integration.

- **Storage**
  - **Postgres** – users, brands, designs, campaigns, logs.
  - **Object storage (S3-compatible)** – uploaded logos, product images, exported PNGs.

- **Third-party**
  - LLM provider (Gemini/GPT/Claude).
  - Optional: hosted image generation (future).

### 3.2 Technology Choices (Why)

- **Polotno SDK** on top of Konva + React:
  - Purpose-built for white-label design editors (ads, banners, social posts).
  - Provides ready-made editor UI (workspace, panels, toolbar, zoom, pages).
  - Has built-in template support (`store.toJSON()` for template JSON library).

- **Konva performance guidance**:
  - Minimize stage size and layers.
  - Use `layer.listening(false)` for non-interactive layers.
  - Use shape caching carefully and only for complex grouped shapes.

This keeps your editor both powerful and performant, without reinventing a canvas engine.

---

## 4. Data Model Design

### 4.1 Core Entities

**User**
- `id`, `email`, `name`, `plan`, `createdAt`, `updatedAt`.

**BrandKit**
- `id`, `ownerId`
- `name`
- `colors`: `{ primary, secondary, accent }`
- `fonts`: `{ primary, secondary }`
- `logoImageId`

**Asset**
- `id`, `ownerId`, `type` (logo, product_image, background), `url`, `createdAt`.

**Design**
- DB record:
  - `id`, `ownerId`, `title`, `format` (instagram_post), `brandId` (nullable), `designJson` (JSONB), `createdAt`, `updatedAt`.

---

### 4.2 Design JSON v1 (Canonical Format)

This is the **single source of truth** for a design.  
All AI, editor operations, and exports operate on this model.

```jsonc
{
  "id": "design_123",
  "schemaVersion": "1.0",
  "ownerId": "user_42",
  "title": "Diwali Electronics Sale",
  "format": "instagram_post",       // v1: only 'instagram_post'
  "size": { "width": 1080, "height": 1080, "unit": "px" },

  "background": {
    "type": "color",                // 'color' | 'gradient' | 'image'
    "color": "#050816",
    "imageId": null
  },

  "brand": {
    "brandId": "brand_7",
    "primaryColor": "#FFCC00",
    "secondaryColor": "#050816",
    "accentColor": "#FF4D00",
    "fontPrimary": "Inter",
    "fontSecondary": "DM Sans",
    "logoImageId": "img_logo_1"
  },

  "layers": [
    {
      "id": "headline",
      "type": "text",              // 'text' | 'shape' | 'image'
      "content": "Diwali Mega Sale",
      "fontFamily": "Inter",
      "fontSize": 64,
      "fontWeight": 800,
      "lineHeight": 1.1,
      "color": "#FFFFFF",
      "textAlign": "left",         // 'left' | 'center' | 'right'
      "x": 80,
      "y": 150,
      "width": 920,
      "rotation": 0,
      "zIndex": 10
    },
    {
      "id": "product_image",
      "type": "image",
      "imageId": "img_prod_1",
      "x": 600,
      "y": 320,
      "width": 380,
      "height": 380,
      "rotation": 0,
      "zIndex": 5
    },
    {
      "id": "discount_badge",
      "type": "shape",
      "shape": "circle",           // 'rectangle' | 'circle'
      "fill": "#FF4D00",
      "stroke": null,
      "strokeWidth": 0,
      "x": 120,
      "y": 420,
      "width": 180,
      "height": 180,
      "radius": 90,
      "rotation": 0,
      "zIndex": 8
    }
  ],

  "meta": {
    "source": "ai_v1",
    "createdAt": "ISO_DATE",
    "updatedAt": "ISO_DATE"
  }
}
```

**KISS choices:**

- Only 3 layer types (`text`, `shape`, `image`) in V1.
- Absolute positioning (no auto-layout/constraints yet).
- Embedded brand block so designs are portable and self-contained.
- `schemaVersion` so future migrations don’t break old designs.

---

### 4.3 Patch Format (for AI + Undo/Redo)

All changes (AI or manual) can be represented as **patch operations**:

```jsonc
{
  "operations": [
    {
      "op": "update_layer",
      "layerId": "headline",
      "changes": { "content": "Big Diwali Sale", "fontSize": 72 }
    },
    {
      "op": "add_layer",
      "layer": { /* full layer definition */ }
    },
    {
      "op": "remove_layer",
      "layerId": "discount_badge"
    },
    {
      "op": "update_design",
      "changes": {
        "background": { "type": "color", "color": "#000000", "imageId": null }
      }
    }
  ]
}
```

Backend responsibilities:

- Validate patches against schema.
- Reject ops that would break layout (e.g. negative width/height).
- Maintain patch history to support undo/redo.

---

## 5. AI Design Engine

### 5.1 Overview

We use a **two-step AI flow**:

1. **Prompt → Structured Brief**  
   - Extracts goals, copy, tone, layout hints.

2. **Brief → Design JSON**  
   - Converts the brief into a concrete layout (positions, layers).

Plus an **edit mode**:

3. **Design + Instruction → Patch**  
   - Applies changes via structured patch operations.

### 5.2 Step 1: Prompt → Brief

**Input**

```jsonc
{
  "prompt": "Instagram post for my D2C electronics brand for Diwali sale: 40% OFF, premium dark theme, highlight headphones, mention free shipping.",
  "format": "instagram_post",
  "brand": {
    "colors": { "primary": "#FFCC00", "secondary": "#050816", "accent": "#FF4D00" },
    "fonts": { "primary": "Inter", "secondary": "DM Sans" }
  }
}
```

**LLM System Prompt (summary)**

- “You are a senior marketing designer.”
- “Return strictly valid JSON. No comments, no trailing commas.”
- “Extract copy (headline, subheadline, CTA), tone, visual emphasis, color mood.”

**LLM Output**

```jsonc
{
  "format": "instagram_post",
  "size": { "width": 1080, "height": 1080 },
  "headline": "Diwali Electronics Sale",
  "subheadline": "40% OFF on Premium Headphones",
  "body": "Free shipping on all orders this Diwali.",
  "cta": "Shop Now",
  "tone": "premium_dark",
  "visual_focus": ["headphones", "discount_badge"],
  "layout_style": "product_right_text_left",
  "color_mood": ["dark_purple", "gold", "white"],
  "constraints": [
    "must show 40% OFF",
    "mention free shipping",
    "keep copy concise"
  ]
}
```

### 5.3 Step 2: Brief → Design JSON

**Input**

- Brief JSON.
- Brand kit.
- Design schema description (few-shot examples help a lot).

**LLM responsibilities**

- Decide:
  - Background.
  - Layer list (headline, subheadline, CTA, badge, logo, product image).
  - Coordinates and sizes (within canvas).
  - Use brand fonts/colors where possible.

**Backend validation**

- Clamp font sizes to reasonable range (e.g. 12–120).
- Ensure text boxes don’t exceed canvas.
- Ensure layer IDs are unique, `zIndex` is normalized.

### 5.4 Step 3: AI Edit (Design + Instruction → Patch)

**Input**

```jsonc
{
  "design": { /* Design JSON v1 */ },
  "instruction": "Make it more minimal, remove the subheadline and make the product image bigger."
}
```

**LLM Output**

- Patch only:

```jsonc
{
  "operations": [
    { "op": "remove_layer", "layerId": "subheadline" },
    {
      "op": "update_layer",
      "layerId": "product_image",
      "changes": {
        "x": 300,
        "y": 260,
        "width": 520,
        "height": 520
      }
    }
  ]
}
```

This **patch-only approach** keeps AI behavior predictable, easy to debug, and supports undo/redo naturally.

### 5.5 Failure Handling

- If LLM returns invalid JSON:
  - Try one automatic “fix JSON” pass with a small helper prompt.
  - If still invalid → show a friendly error, log input/output, and allow user to try again.
- If layout is broken (validation fails):
  - Apply simple fallback: center everything and use default font.

---

## 6. Frontend & Editor

### 6.1 Tech & Libraries

- **Next.js (React)** for SPA + SSR.
- **Polotno SDK** for editor:
  - Provides a full canvas editor workspace (side panel, toolbar, zoom, etc.).
  - Supports saving/loading designs via `store.toJSON()` and `store.loadJSON()`.

### 6.2 Screens

1. **Prompt Page**
   - Simple layout:
     - Large textarea.
     - Brand selector (dropdown).
     - One format dropdown (locked to Instagram post in V1).
     - “Generate designs” button.
   - Show loading state with skeleton cards.

2. **Design Selection Page**
   - Grid of 2–3 thumbnails.
   - Actions:
     - “Open in editor”.
     - “Regenerate”.

3. **Editor Page**
   - Layout:
     - Left sidebar: layers list.
     - Center: Polotno workspace canvas.
     - Right sidebar: properties panel (text, fill color, fonts, alignment, etc.).
     - Top bar: design title, format, export button.
     - (Optional V1) small “AI tweak” input box.

**KISS UX**: no infinite controls; just the essentials needed for ads.

### 6.3 Canvas Performance Best Practices

- **Keep stage small**:
  - Use 1080×1080 logical size; scale for HiDPI, but don’t create huge canvases.
- **Minimize layers**:
  - Typically 2–3 layers:
    - Background.
    - Main design objects.
    - UI overlays (selection boxes, guides).
- **Limit node count**:
  - Encourage simple shapes, not dozens of tiny elements.
- **Optimize hit detection**:
  - Turn off listening for non-interactive layers: `layer.listening(false)`.
- **Use caching selectively**:
  - Cache complex groups (e.g. a badge with multiple shapes).
  - Avoid caching everything.

Polotno encapsulates a lot of this, but your team should respect these constraints when adding custom elements.

### 6.4 Serialization & State

- Use a **thin adapter** between Design JSON and Polotno’s internal store:
  - `designJson -> polotnoStore` on load.
  - `polotnoStore -> designJson` on save.
- Maintain your own logical `state` and use create/update functions, not naive `toJSON()` round-trips for everything.

---

## 7. Backend API & Modules

### 7.1 Modules (Logical)

Within a monolith:

- `auth`
- `brands`
- `designs`
- `ai`
- `assets`
- `export`

### 7.2 REST Endpoints (Minimal V1)

**Auth**

- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`

**Brands**

- `GET /brands`
- `POST /brands`
- `GET /brands/{id}`
- `PATCH /brands/{id}`

**Designs**

- `GET /designs`
- `POST /designs`           – create from editor.
- `GET /designs/{id}`
- `PATCH /designs/{id}`     – apply patch or replace JSON.
- `DELETE /designs/{id}`

**AI**

- `POST /ai/generate-designs`
  - Input: `{ prompt, format, brandId? }`
  - Output: `{ designs: [DesignJSON, ...] }`
- `POST /ai/edit-design`
  - Input: `{ design, instruction }`
  - Output: `{ patch }`

**Assets**

- `POST /assets` – upload file, returns `assetId`.
- `GET /assets/{id}` – returns signed URL.

**Export**

- `POST /export`
  - Input: `{ designId, format: "png" | "jpg" }`
  - Output: `{ url }`.

### 7.3 Security & Multi-tenancy

- Every request is tied to `userId`.
- All DB queries scoped by `ownerId`.
- No design or assets shared across users unless explicitly implemented later (e.g. team accounts).

---

## 8. Templates & Brand Kits

### 8.1 Brand Kits

**Schema**

```jsonc
{
  "id": "brand_7",
  "ownerId": "user_42",
  "name": "VoltSound",
  "colors": {
    "primary": "#FFCC00",
    "secondary": "#050816",
    "accent": "#FF4D00"
  },
  "fonts": {
    "primary": "Inter",
    "secondary": "DM Sans"
  },
  "logoImageId": "img_logo_1"
}
```

**Usage**

- AI must use brand colors/fonts as defaults.
- “Apply brand” button in editor to recolor design according to a chosen brand (either via simple rules or LLM-generated patches).

### 8.2 Template Library (Using Polotno)

Polotno’s recommended flow for templates:

1. Create designs in Polotno Studio or your own editor.
2. Export each template via `store.toJSON()` (Polotno JSON).
3. Save a preview image per template (`saveAsImage()` or Cloud Render API).
4. Store templates in your DB (`id`, `category`, `tags`, `json`, `previewUrl`).

**At generation time**:

- Use a lightweight retrieval:
  - Match prompt keywords and tone with template tags (e.g. `["sale", "premium", "dark"]`).
- LLM can then **adapt** a chosen template’s JSON (text & colors) rather than generating layout from scratch.

This hybrid approach (template + AI) helps ensure consistently good-looking outputs while staying fast and predictable.

---

## 9. Differentiating Features

You can introduce these progressively as “V1.5 / V2” features.

### 9.1 Explain-my-design Mode

Button: **“Explain this design”**

- Send Design JSON to LLM with a “design critic” prompt:
  - Explain visual hierarchy (what stands out first).
  - Explain color contrast / brand consistency.
  - Suggest improvements (optional patch).

Educational and builds user trust.

### 9.2 Accessibility & Quality Checks

Automatic checks:

- Text contrast vs background (WCAG).
- Minimum font sizes for legibility.

Optional auto-fix:

- Increase contrast (darken text/lighten background).
- Increase small font sizes slightly.

### 9.3 Simple “Campaign Mode”

- Users create a “campaign” (Diwali Sale).
- System generates:
  - 2–3 **coherent designs** (same brand, tone).

Future extension:

- Multi-format (post, story, banner) from single brief.

---

## 10. Implementation Roadmap

### Phase 0 – Setup (1–2 weeks)

- Choose stack:
  - Frontend: Next.js, Polotno.
  - Backend: FastAPI/NestJS, Postgres, S3.
- Set up:
  - Auth (basic email/password).
  - CI/CD.
  - Basic logging + error tracking.

**Deliverable:** Hello world app with login + empty editor.

---

### Phase 1 – Editor & Design JSON (2–3 weeks)

- Integrate **Polotno Full Editor** into the app shell.
- Implement:
  - `Design JSON v1` schema in TS/Pydantic.
  - Adapter: `DesignJSON <-> Polotno store`.
  - Save/load design from DB.

**Deliverable:** Users can manually create, save, and reopen designs (no AI yet).

---

### Phase 2 – AI: Prompt → Single Design (3–4 weeks)

- Implement `POST /ai/generate-designs`:
  - LLM step: Prompt → Brief.
  - LLM step: Brief → Design JSON.
  - Validation layer.
- Wire Prompt Page → AI → open first design in editor.

**Deliverable:** User types a prompt → gets at least one good editable design.

---

### Phase 3 – Multiple Designs & Brand Kits (3–4 weeks)

- Extend AI endpoint to return 2–3 variants.
- Add Design Selection page.
- Implement BrandKit CRUD.
- Include brand in AI prompts; ensure colors/fonts are respected.

**Deliverable:** Brand kits exist, and prompt → 2–3 brand-consistent designs.

---

### Phase 4 – Templates & AI Edits (4–6 weeks)

- Build a starter template library using Polotno JSON.
- Add template retrieval to AI flow (template + adaptation).
- Implement `POST /ai/edit-design` (patch-based).
- Add simple “AI tweak” input in editor.

**Deliverable:** Users can:
- Get better-looking outputs from templates.
- Ask AI to tweak existing designs.

---

### Phase 5 – Quality & Differentiators (ongoing)

- UX polish.
- Export optimizations.
- Add:
  - Explain-my-design.
  - Accessibility checks.
  - Basic campaign concept.

---

## 11. Summary

This design:

- **Keeps it simple**:
  - One format, one editor, one monolith backend for V1.
- **Leverages proven tools** (Polotno/Konva) instead of custom canvas engines.
- **Aligns with best practices** from Canva/Figma-style AI tools: prompt → editable layouts, templates + AI, not just flat image gen.
- **Is extensible**:
  - Versioned Design JSON.
  - Clean AI service interface.
  - Template & brand kit structure that scales.

You can now give this document to your design & dev team as a **step-by-step blueprint** to build an MVP and evolve it without painting yourself into a corner.
