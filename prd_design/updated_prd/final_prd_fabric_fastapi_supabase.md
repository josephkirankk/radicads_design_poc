# Final Product Requirements Document (PRD)
## Project: Radic Pro — AI‑Powered Creative Layout Engine

### 1. Overview
Radic Pro is an AI-assisted design generation system that produces editable, layered compositions using Fabric.js. The system ingests structured user input, generates a validated Design JSON (v1.3), and renders it in an in-browser editor. All textual content must remain editable unless stylistically impossible, in which case it becomes an image with a SmartImageRecipe.

---

## 2. Objectives
- Generate professional layouts automatically.
- Maintain editability for real text.
- Support decorative wordmarks via SmartImageRecipes.
- Preserve vector shapes when possible.
- Ensure consistency, validation, and reproducibility.

---

## 3. Core Features
### 3.1 AI Layout Engine
- Converts user input into a structured layout.
- Always produces JSON conforming to schema v1.3.
- Headline, subheadline, bullets, CTA → **TextLayer**.
- Decorative text → **ImageLayer** with SmartImageRecipe.

### 3.2 Design JSON v1.3
Every canvas has:
- `canvas`: dimensions, background.
- `layers`: ordered stack of text, images, shapes.
- `smartAssets`: metadata for reproducibility.

### 3.3 Roles for Layers
- `headline`, `subheadline`, `cta`, `bullets`
- `decorative_text`, `product_image`, `logo`
- `shape_badge`, `background_shape`

---

## 4. Layer Types
### 4.1 TextLayer
Editable text.
```
{
  "id": "headline",
  "type": "text",
  "content": "Holiday Sale — 40% OFF",
  "fontFamily": "Inter",
  "fontSize": 72,
  "fontWeight": 700,
  "color": "#111111",
  "textAlign": "center",
  "x": 100,
  "y": 80,
  "role": "headline"
}
```

### 4.2 ShapeLayer
Vectors only.
```
{
  "id": "shape_badge",
  "type": "shape",
  "shape": "circle",
  "radius": 90,
  "fill": "#FF4444",
  "stroke": "#FFFFFF",
  "strokeWidth": 4,
  "x": 780,
  "y": 60
}
```

### 4.3 ImageLayer
Used for product images or decorative text.
```
{
  "id": "decorative_wordmark",
  "type": "image",
  "role": "decorative_text",
  "smartImage": {
    "recipeId": "wordmark_vintage_12421",
    "prompt": "gold embossed vintage text 'Luxury'",
    "model": "gpt-image-1"
  },
  "width": 400,
  "height": 120,
  "x": 300,
  "y": 40
}
```

---

## 5. SmartImageRecipe Specification
Ensures all images created via AI can be recomputed, cached, and reused.

```
smartImage: {
  "recipeId": "unique_hash",
  "prompt": "product photo...",
  "model": "gpt-image-1",
  "lastGeneratedAssetId": "asset_1234",
  "references": []
}
```

---

## 6. FastAPI Validation Pipeline
### 6.1 Steps
1. JSON parsing → Pydantic model validation  
2. Required layers: headline, product image  
3. Text-as-image detection → reject  
4. Decorative text rule enforcement  
5. Shape type restrictions (circle, rectangle)  
6. Overlap detection  
7. SmartImageRecipe presence for generated images  

### 6.2 Auto-repair Rules
- If headline was output as an image → attempt extraction from prompt.
- If no text layers exist for bullets → create stub layers.
- If shapes provided as images → convert to vector shapes when simple.

---

## 7. Polotno/Fabric.js Rendering Rules
- `TextLayer` → fabric.IText
- `ShapeLayer` → fabric.Circle / fabric.Rect
- `ImageLayer` → fabric.Image
- For decorative wordmarks → show a “Image text” badge overlay
- Hidden text layers (for accessibility) → `visible: false`

---

## 8. System Components
- **Frontend**: Svelte/React + Fabric.js editor
- **Backend**: FastAPI + Pydantic models
- **Database**: Supabase Postgres
- **Storage**: Supabase Storage
- **AI**: OpenAI GPT‑5.1 + GPT‑Image‑1
- **Device Optimization**: Nano Banana Pro acceleration layer

---

## 9. API Endpoints
### `POST /generate-design`
Returns Design JSON.

### `POST /validate`
Runs validation pipeline.

### `POST /export`
Returns PNG/JPG/PDF.

---

## 10. User Flow
1. User inputs product, message, brand theme.  
2. Backend constructs structured prompt.  
3. AI generates Design JSON v1.3.  
4. FastAPI validates + repairs.  
5. Editor renders JSON.  
6. User edits text layers and moves objects.  
7. Final export.

---

# END PRD
