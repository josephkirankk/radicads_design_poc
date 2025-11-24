# AI Design App – Nano Banana Pro Enhanced Design (KISS, Extensible, Performant)

> Goal: Build a **DesignLumo-class AI design app** that uses **Nano Banana Pro** + a **Canva-style editor** to generate *fully editable* marketing creatives, infographics, and UGC-style visuals — while staying simple enough for a small team to implement and evolve.

This document is written so you can hand it directly to your **product + engineering team**.

---

## 1. Positioning & How Nano Banana Pro Fits In

### 1.1 What We’re Building

Baseline functionality (from the previous spec):

- User writes a **prompt** (e.g. “Instagram ad for Diwali electronics sale, premium dark theme, 40% OFF”).
- App generates **2–3 editable designs** (layers: text, shapes, images).
- User edits them in a **browser-based editor** (Polotno/Konva).
- User **exports** PNG/JPG (later: PDF, video, etc.).

We now **upgrade** the design with Nano Banana Pro:

### 1.2 Nano Banana Pro Capabilities (Relevant Highlights)

From Google’s and third‑party docs and reviews: citeturn0search3turn0search6turn0search20turn0search23turn0search22  

- Built on **Gemini 3 Pro Image** (a visual reasoning system, not just a diffusion model).
- **High‑quality images** up to 2K–4K, with:
  - Very **accurate text rendering** in images (posters, diagrams, infographics).
  - Strong **layout and composition understanding** (diagrams, slide-like layouts).
  - **Character consistency** across multiple images (great for “AI models” / mascots / UGC).
  - **Precise edits** (lighting, camera angle, object insertion/removal).
  - **Multi‑image blending** (merge up to many reference images).
  - **Search grounding** (through Gemini APIs) for more accurate factual infographics.

In short: Nano Banana Pro is ideal for **photo-style and infographic raster content**, while our editor excels at **vector/text layouts and brand control**.

### 1.3 Product Position vs. Other Tools

We combine:

- **Polotno/Canva‑style editor** → editable vector/text layout. citeturn0search21turn0search7  
- **Nano Banana Pro** → high‑quality **photo & infographic generation/editing**.
- **Template + brand kit system** → consistency and speed. citeturn0search2turn0search9turn0search14  

Your edge vs typical AI image tools:

- Produce **editable designs** (not just flat images).
- Have **AI‑powered photo/UGC and infographic blocks** inside those designs powered by Nano Banana Pro.
- Offer **campaign‑level consistency** (same persona, same brand, many sizes).

---

## 2. Design Principles (KISS + “Pro” Ready)

### 2.1 KISS Scope for V1

To remain realistic:

- **Web app only** (no native mobile).
- **One core format** to start:
  - `instagram_post` 1080×1080 (later: story, LinkedIn, banners).
- **Monolith backend** (FastAPI or NestJS) with clean module separation.
- **Polotno SDK** for editor instead of building a canvas engine. citeturn0search21turn0search7  
- **Nano Banana Pro** used in **three clear ways**:
  1. **Photo/UGC blocks** – photoreal product shots, AI influencers, backgrounds.
  2. **Infographic blocks** – complex charts/timelines as raster panels.
  3. **Smart image edits** – non‑destructive edits on uploaded product shots.

### 2.2 Extensibility & Maintainability

- Versioned **Design JSON schema** (e.g., `schemaVersion: "1.1"`).
- A distinct **Image AI subsystem** that talks to the **Gemini Image API (Nano Banana Pro)**. citeturn0search20turn0search10  
- Templates stored as JSON (Polotno schema) with **dynamic variables** to scale campaigns from data. citeturn0search2turn0search5turn0search9turn0search14  
- Keep **LLM layout logic** separate from **image generation logic**.

### 2.3 Performance & Cost

- Rendering and UI performance handled via **Polotno/Konva best practices**: few layers, small stage, selective caching. citeturn0search0turn0search3turn0search18turn0search21  
- Nano Banana Pro calls are:
  - **Explicit** (background generation, persona creation).
  - **Cached** (avoid regenerating same prompt+refs).
  - **Quota-aware** (track usage per workspace).

---

## 3. High-Level Architecture (Updated for Nano Banana Pro)

### 3.1 Components

- **Frontend (Next.js + React)**
  - Marketing pages.
  - App shell (auth, navigation).
  - Prompt & campaign dashboard.
  - Editor (Polotno).
  - Image generation side panels (Nano Banana Pro actions).

- **Backend (FastAPI / NestJS, Monolith)**
  - Modules:
    - `auth` – users, sessions.
    - `brands` – brand kits.
    - `designs` – Design JSON CRUD.
    - `templates` – template JSON & previews.
    - `ai_layout` – text + layout LLM logic.
    - `ai_image` – Nano Banana Pro integration.
    - `assets` – file uploads (logos, refs, generated images).
    - `export` – PNG/JPG/PDF.

- **Storage**
  - Postgres – relational data and Design JSON.
  - S3‑compatible object store – images, exports, reference assets.

- **External AI**
  - **LLM** (Gemini/GPT/Claude) → prompts → briefs → layout Design JSON.
  - **Nano Banana Pro** (Gemini 3 Pro Image) → image generation/editing. citeturn0search3turn0search6turn0search20turn0search23  

### 3.2 “Smart Image Block” Concept

We introduce a **Smart Image Block** as a type of `image` layer that knows **how it was generated**:

- Source = `"nano_banana_pro"` or `"upload"`.
- Stores its **generation recipe**:
  - Prompt.
  - References (product photo IDs, persona IDs).
  - Model options (aspect, style hints).

This allows:

- Non‑destructive edits (regenerate same block with a new prompt).
- Campaign‑wide consistency (reuse same persona/product style).

---

## 4. Data Model Design (v1.1 with Smart Images)

### 4.1 Core Entities (DB)

Same base entities as before:

- `User`
- `BrandKit`
- `Asset`
- `Design`
- `Template`

Plus two new ones:

- `SmartImageRecipe`
  - `id`
  - `ownerId`
  - `type`: `"persona" | "product_shot | "infographic" | "background"`
  - `prompt`
  - `referenceAssetIds` (array)
  - `model`: `"nano_banana_pro"`
  - `options` (JSON: aspect ratio, style tags, etc.)
  - `lastGeneratedAssetId`
  - `createdAt`, `updatedAt`.

- `Campaign` (for grouping designs/personas later)
  - `id`, `ownerId`, `name`, `brandId`, `createdAt`, `updatedAt`.

### 4.2 Design JSON v1.1

Main changes vs previous:

- Add `smartImage` metadata to `image` layers.
- Add `campaignId` (optional) at top level.

```jsonc
{
  "id": "design_123",
  "schemaVersion": "1.1",
  "ownerId": "user_42",
  "campaignId": "camp_9",
  "title": "Diwali Electronics Sale",
  "format": "instagram_post",
  "size": { "width": 1080, "height": 1080, "unit": "px" },

  "background": {
    "type": "color",
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
      "type": "text",
      "content": "Diwali Mega Sale",
      "fontFamily": "Inter",
      "fontSize": 64,
      "fontWeight": 800,
      "lineHeight": 1.1,
      "color": "#FFFFFF",
      "textAlign": "left",
      "x": 80,
      "y": 150,
      "width": 920,
      "rotation": 0,
      "zIndex": 10
    },
    {
      "id": "product_image",
      "type": "image",
      "imageId": "asset_1234",
      "x": 580,
      "y": 320,
      "width": 420,
      "height": 420,
      "rotation": 0,
      "zIndex": 5,
      "smartImage": {
        "recipeId": "recipe_89",
        "source": "nano_banana_pro",
        "role": "product_shot"
      }
    },
    {
      "id": "infographic_panel",
      "type": "image",
      "imageId": "asset_567",
      "x": 80,
      "y": 620,
      "width": 920,
      "height": 280,
      "rotation": 0,
      "zIndex": 6,
      "smartImage": {
        "recipeId": "recipe_90",
        "source": "nano_banana_pro",
        "role": "infographic"
      }
    }
  ],

  "meta": {
    "source": "ai_v1",
    "createdAt": "ISO_DATE",
    "updatedAt": "ISO_DATE"
  }
}
```

### 4.3 Patch Format

Unchanged conceptually:

```jsonc
{
  "operations": [
    {
      "op": "update_layer",
      "layerId": "headline",
      "changes": { "content": "Big Diwali Sale", "fontSize": 72 }
    },
    {
      "op": "update_layer",
      "layerId": "product_image",
      "changes": { "x": 560, "width": 440, "height": 440 }
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

- Strict schema validation (Pydantic/JSON Schema).
- Reject invalid coordinates/sizes.
- Maintain patch history per design.

---

## 5. AI Subsystems (Layout LLM + Nano Banana Pro)

### 5.1 Layout & Copy LLM (unchanged core)

**Flow** (KISS):

1. **Prompt → Brief**
   - LLM extracts:
     - Headline, subheadline, body, CTA.
     - Tone, layout style, visual focus.
2. **Brief → Design JSON skeleton**
   - LLM chooses:
     - Layout zones.
     - Text layers.
     - Where image blocks sit (background/product/infographic).
   - It **does not** generate photo pixels; it just decides *where images should go* and what *kind* of image each slot should hold (`role` field: `background`, `product_shot`, `persona`, `infographic`).

Output of step 2:

- A Design JSON **with image placeholders**:
  - Some placeholders are `smartImage` blocks referencing planned Nano Banana Pro recipes that don’t exist yet.

### 5.2 Nano Banana Pro Image Pipeline

We use Nano Banana Pro via the **Gemini Image API**. citeturn0search20turn0search6turn0search10turn0search23  

We define **three core “modes”**:

1. **Product/UGC Mode**
   - Inputs:
     - Uploaded product photos (assets).
     - Brand style (colors, tone).
     - Campaign prompt (e.g. “young urban, moody lighting, studio feel”).
   - Nano Banana Pro output:
     - Photoreal product shots or UGC‑style images with consistent look.
   - Stored as `SmartImageRecipe(type="product_shot" | "persona")`.

2. **Infographic Mode**
   - Inputs:
     - Short structured brief from LLM: key stats, labels, timeline.
     - Possibly search‑grounded data (Gemini text model + Search).
   - Nano Banana Pro output:
     - A visual **infographic panel** with clear text, icons, layout.
   - Great for quick **explainers and education posts**.

3. **Smart Edit Mode (Image‑to‑Image)**
   - Inputs:
     - Existing asset (user upload or previous Nano Banana Pro image).
     - Edit prompt (“remove background and replace with abstract blue waves”).
   - Nano Banana Pro output:
     - Edited version of the same image (same composition, improved background, etc.).
   - Stored as updated `SmartImageRecipe` with new `lastGeneratedAssetId`.

Each mode maps directly onto user‑facing actions in the editor (see UX in §6).

### 5.3 Orchestration: End‑to‑End Flow (Step-by-Step)

1. **User prompt**
   - “Instagram ad for my coffee brand. Show a latte, warm cozy vibe, include a ‘Buy 1 Get 1’ badge and a small infographic of our sustainability stats.”

2. **LLM: Prompt → Brief**
   - Extracts:
     - Copy for headline, badge, CTA.
     - Visual focus: `["latte", "badge", "infographic"]`.
     - Layout: e.g. text left, product right, infographic bottom.

3. **LLM: Brief → Design JSON skeleton**
   - Chooses layout and defines layers:
     - Text layers.
     - `image` layers with roles:
       - `role = "product_shot"` for latte photo.
       - `role = "infographic"` for sustainability panel.
   - Leaves `imageId` empty for those roles and defines `smartImage` metadata (planned recipe).

4. **Backend: Create SmartImageRecipes**
   - For each `smartImage` placeholder:
     - Create a `SmartImageRecipe` (type, prompt, references).
     - Queue a job for `ai_image` module.

5. **ai_image module: call Nano Banana Pro**
   - For each recipe:
     - Compose prompt:
       - Combine role, brand style, campaign context, short description.
     - Call Gemini Image API (Nano Banana Pro).
     - Store image in object storage, link `assetId`.
     - Update:
       - `SmartImageRecipe.lastGeneratedAssetId`.
       - `DesignJSON.layers[i].imageId`.

6. **Frontend updates**
   - Poll or subscribe to design updates.
   - Once image assets are ready, the placeholders show the **final images in the editor**.

7. **User edits**
   - Moves layers, tweaks text.
   - Can click a Smart Image block → “Refine with AI”:
     - Enter a new prompt.
     - Backend regenerates via Nano Banana Pro with same recipe ID.

Everything is still driven by **Design JSON + SmartImageRecipes**, keeping the architecture simple and explicit.

---

## 6. Frontend & UX (Nano Banana Pro Features Surfaced Simply)

### 6.1 Screens (Same core as before, with added image actions)

1. **Prompt Page**
   - Same as before:
     - Prompt textarea.
     - Brand selector.
     - Format selector (locked to Instagram post in V1).
   - Optional toggles:
     - “Use AI photo blocks” (on by default).
     - “Include infographic where relevant” (on by default).

2. **Design Selection Page**
   - Shows 2–3 thumbnails.
   - Under the hood:
     - Each design may have Smart Image blocks that are still generating.
   - Show small “AI image loading” indicator in thumbnails.

3. **Editor Page**
   - Center: Polotno workspace. citeturn0search21turn0search7  
   - Left: Layers list (text, shapes, images, smart images).
   - Right: Properties panel.
   - Top:
     - Design title.
     - Export button.
     - “Explain design” (later).
   - Additional UI:
     - Clicking an image layer with `smartImage`:
       - Shows **Nano Banana Pro panel**:
         - Prompt used.
         - “Regenerate” button.
         - “Make more minimal / more vibrant / change background” quick chips.

4. **Persona / UGC Screen (Optional V1.5)**
   - Simple page to generate:
     - Brand persona (consistent human/mascot).
   - Internally:
     - One or more `SmartImageRecipe(type="persona")`.

### 6.2 Canvas Performance

We keep the same Konva best practices: citeturn0search0turn0search3turn0search18turn0search21  

- Stage at 1080×1080 logical pixels.
- Very limited number of display layers.
- Only Smart Image blocks are high‑res images; others are vector.
- For high‑res (2K/4K) images:
  - Use a downsampled version in editor; full‑res only at export.

---

## 7. Backend API (Extended for Nano Banana Pro)

### 7.1 Existing API (Short Recap)

- `POST /auth/signup`, `/auth/login`, `/auth/me`
- `GET/POST/PATCH /brands`
- `GET/POST/PATCH/DELETE /designs`
- `POST /ai/generate-designs`
- `POST /ai/edit-design`
- `POST /assets`
- `GET /assets/{id}`
- `POST /export`

### 7.2 New/Extended Endpoints

**Smart Images**

- `POST /smart-images`
  - Input:
    ```jsonc
    {
      "type": "product_shot",
      "prompt": "Moody studio shot of our coffee bag next to a latte, warm lighting",
      "referenceAssetIds": ["asset_11"],
      "model": "nano_banana_pro",
      "options": {
        "aspectRatio": "1:1"
      }
    }
    ```
  - Output:
    ```jsonc
    {
      "recipeId": "recipe_89",
      "assetId": "asset_1234",
      "status": "completed"
    }
    ```

- `POST /smart-images/{recipeId}/regenerate`
  - Regenerates image using existing recipe with an optional updated prompt.

**AI Layout (updated)**

- `POST /ai/generate-designs`
  - Same signature, but now:
    - Returns Design JSONs with Smart Image placeholders.
    - Optionally triggers Smart Image generation in background.

**Campaigns**

- `POST /campaigns`
- `GET /campaigns`
- `GET /campaigns/{id}`

Campaigns help group multiple designs and share personas/recipes.

---

## 8. Best Practices: Performance, Cost, Safety

### 8.1 Performance & Cost Controls

- **Nano Banana Pro Quota Awareness**: citeturn0search6turn0search10turn0search20  
  - Track image generations per user/workspace.
  - Graceful fallback:
    - If Pro quota is exceeded, optionally:
      - Use standard Nano Banana (lower quality, cheaper).
      - Or queue jobs instead of synchronous generation.

- **Caching**
  - Cache `SmartImageRecipe` → `assetId` mapping.
  - If prompt + references are identical, reuse the existing image.

- **Resolution Strategy**
  - Use **lower resolution** (e.g. 1024×1024) in editor.
  - At export:
    - Optionally regenerate at 2K–4K using same recipe for high‑end output.

### 8.2 Safety & Content Controls

Based on early Nano Banana Pro reviews and Google’s policies: citeturn0news36turn0search3turn0search23turn0search20  

- Respect:
  - Google’s safety API responses.
  - Your own content filters (no explicit, hateful, or disallowed content).
- Add a **safety layer**:
  - Check user prompts against a basic policy.
  - Reject or ask for rephrasing before calling Nano Banana Pro.

---

## 9. Implementation Roadmap (Step-by-Step with Nano Banana Pro)

### Phase 0 – Foundations (1–2 weeks)

- Stack:
  - Next.js + Polotno.
  - FastAPI/NestJS.
  - Postgres + S3.
- Implement:
  - Auth.
  - BrandKit CRUD.
  - Basic Polotno editor with manual design save/load.

**Deliverable:** Basic editor + persistence (no AI yet).

---

### Phase 1 – Layout AI (2–3 weeks)

- Implement:
  - `Design JSON v1.1` schema (no Smart Image usage yet).
  - `POST /ai/generate-designs` using LLM:
    - Prompt → Brief → Design JSON.
- Frontend:
  - Prompt page → call AI → open first design in editor.

**Deliverable:** Prompt → editable design (image placeholders may still be generic uploaded images).

---

### Phase 2 – Nano Banana Pro Integration (3–4 weeks)

- Implement `ai_image` module with Gemini Image API (Nano Banana Pro). citeturn0search20turn0search6turn0search10turn0search23  
- Implement `SmartImageRecipe` model + `POST /smart-images`.
- Update Design JSON to include `smartImage`.
- On design generation:
  - Create recipes for `product_shot` & `background` roles.
  - Generate images and attach `imageId`.

**Deliverable:** Designs include Nano Banana Pro generated product/background images.

---

### Phase 3 – Infographic Blocks (2–3 weeks)

- Extend LLM brief:
  - For suitable prompts, include structured data for infographics.
- Implement **Infographic Smart Image**:
  - `type = "infographic"`.
  - Compose structured prompt for Nano Banana Pro (e.g. “2-column bar chart, labels A/B/C, include percentages”).
- Add “Add infographic panel” button in editor.

**Deliverable:** Users can generate infographic panels inside designs.

---

### Phase 4 – Smart Edit & Persona (3–5 weeks)

- **Smart Edit Mode**:
  - For any `smartImage` layer:
    - Provide “Refine with AI” panel.
    - Call `POST /smart-images/{recipeId}/regenerate` with updated prompt.
- **Persona/UGC Mode**:
  - Simple persona generator UI.
  - Use Nano Banana Pro’s strong identity consistency for a consistent model/look across campaign images. citeturn0search22turn0search8turn0search19  

**Deliverable:** Rich AI edits for Smart Image blocks; basic persona generation.

---

### Phase 5 – Quality & Differentiators (ongoing)

- **Explain‑my‑design**:
  - LLM explains hierarchy, colors, and layout.
- **Accessibility & Quality Checks**:
  - Contrast, font size, text overflow.
- **Campaign Mode**:
  - Generate multiple designs in a campaign with shared persona/recipes.

---

## 10. Summary

This enhanced design:

- **Keeps KISS**:
  - Monolith backend, one main format, clear subsystems.
- **Leverages Nano Banana Pro correctly**:
  - For **photo/UGC, infographics, and smart edits**, not as a replacement for your layout editor.
  - Uses official Gemini Image APIs, which support high‑res, grounded, text‑accurate image generation. citeturn0search20turn0search6turn0search23turn0search3  
- **Builds on strong editor foundations**:
  - Polotno templates, dynamic variables, automation, and exports. citeturn0search2turn0search5turn0search7turn0search9turn0search21  
- **Is extensible and maintainable**:
  - Versioned Design JSON.
  - Smart Image recipes.
  - Clean `ai_layout` vs `ai_image` separation.
- **Provides a clear roadmap** your team can follow step‑by‑step.

Use this document as the **final design spec** for a DesignLumo‑class app that **fully exploits Nano Banana Pro** while remaining practical to build and evolve.

