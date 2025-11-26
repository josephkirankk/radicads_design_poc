# Radic Pro — Architecture Specification

> **Version**: 2.0  
> **Last Updated**: November 2025

---

## 1. Architecture Overview

### 1.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                  CLIENT                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                         Next.js Application                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │ │
│  │  │   Pages/     │  │   Editor     │  │   Shared     │                   │ │
│  │  │   Routes     │  │   Module     │  │   Components │                   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                   │ │
│  │         │                 │                 │                            │ │
│  │         └────────────────┼─────────────────┘                            │ │
│  │                          ▼                                               │ │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │ │
│  │  │                    State Management Layer                          │  │ │
│  │  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  │ │
│  │  │   │   React     │  │   TanStack  │  │   Zustand   │               │  │ │
│  │  │   │   Context   │  │   Query     │  │   (Editor)  │               │  │ │
│  │  │   │   (Auth)    │  │   (Server)  │  │             │               │  │ │
│  │  │   └─────────────┘  └─────────────┘  └─────────────┘               │  │ │
│  │  └───────────────────────────────────────────────────────────────────┘  │ │
│  │                          │                                               │ │
│  │                          ▼                                               │ │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │ │
│  │  │                    Editor Adapter Layer                            │  │ │
│  │  │   Design JSON (Canonical) ◄──► Fabric.js (Editor-Specific)        │  │ │
│  │  └───────────────────────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ HTTPS / REST
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                                  SERVER                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                         FastAPI Application                              │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐   │ │
│  │  │                         API Layer                                 │   │ │
│  │  │   /auth    /designs    /brands    /ai    /assets    /export      │   │ │
│  │  └──────────────────────────────────────────────────────────────────┘   │ │
│  │                          │                                               │ │
│  │                          ▼                                               │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐   │ │
│  │  │                      Service Layer                                │   │ │
│  │  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │ │
│  │  │   │ Design   │  │ Brand    │  │ Asset    │  │ Export   │        │   │ │
│  │  │   │ Service  │  │ Service  │  │ Service  │  │ Service  │        │   │ │
│  │  │   └──────────┘  └──────────┘  └──────────┘  └──────────┘        │   │ │
│  │  └──────────────────────────────────────────────────────────────────┘   │ │
│  │                          │                                               │ │
│  │                          ▼                                               │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐   │ │
│  │  │                       AI Layer                                    │   │ │
│  │  │   ┌──────────────────┐      ┌──────────────────┐                 │   │ │
│  │  │   │  Layout Engine   │      │  Image Engine    │                 │   │ │
│  │  │   │  (Brief→Design)  │      │  (SmartImages)   │                 │   │ │
│  │  │   └──────────────────┘      └──────────────────┘                 │   │ │
│  │  │             │                        │                            │   │ │
│  │  │             ▼                        ▼                            │   │ │
│  │  │   ┌──────────────────────────────────────────────────────────┐   │   │ │
│  │  │   │         AI Providers (via Replicate)                      │   │   │ │
│  │  │   │   Gemini 3 Pro │ Nano Banana Pro │ FLUX │ GPT-5          │   │   │ │
│  │  │   └──────────────────────────────────────────────────────────┘   │   │ │
│  │  └──────────────────────────────────────────────────────────────────┘   │ │
│  │                          │                                               │ │
│  │                          ▼                                               │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐   │ │
│  │  │                    Validation Layer                               │   │ │
│  │  │   Schema Validation  │  Auto-Repair  │  Constraint Checks        │   │ │
│  │  └──────────────────────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                                DATA LAYER                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │    Supabase     │  │    Supabase     │  │    Supabase     │              │
│  │    Postgres     │  │    Storage      │  │    Auth         │              │
│  │    (Data)       │  │    (Files)      │  │    (Identity)   │              │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Architectural Patterns

### 2.1 Editor Adapter Pattern

The most critical architectural decision: **Design JSON is canonical and editor-agnostic**.

```
┌─────────────────────────────────────────────────────────────────┐
│                   CANONICAL DESIGN JSON                          │
│                   (Source of Truth)                              │
│                                                                  │
│   • Stored in database                                          │
│   • Sent over API                                               │
│   • Used by AI for generation                                   │
│   • Used for validation                                         │
│   • Version controlled                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Bidirectional Conversion
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ADAPTER LAYER                               │
│                                                                  │
│   interface EditorAdapter {                                     │
│     toEditorFormat(design: DesignJSON): void;                   │
│     fromEditorFormat(): DesignJSON;                             │
│     applyPatch(patch: DesignPatch): void;                       │
│     exportImage(options): Promise<Blob>;                        │
│   }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │ FabricAdapter │ │PolotnoAdapter │ │ KonvaAdapter  │
    │               │ │  (future)     │ │  (future)     │
    └───────────────┘ └───────────────┘ └───────────────┘
```

**Key Benefits:**
1. **Editor Swappable** — Change from Fabric.js to Polotno without data migration
2. **AI-Friendly** — AI generates canonical format, not editor-specific
3. **Validation** — Single schema to validate against
4. **Portable** — Designs can be exported/imported across systems

### 2.2 AI Provider Abstraction

```python
# Abstract interface for all AI providers
class LayoutAIProvider(Protocol):
    async def generate_brief(self, prompt: str, brand: dict) -> dict: ...
    async def generate_design(self, brief: dict) -> dict: ...
    async def edit_design(self, design: dict, instruction: str) -> dict: ...

class ImageAIProvider(Protocol):
    async def generate(self, prompt: str, context: dict, options: dict) -> bytes: ...
    async def edit(self, image: bytes, instruction: str) -> bytes: ...

# Factory for provider selection
class AIProviderFactory:
    def get_layout_provider(self, provider: str = None) -> LayoutAIProvider:
        provider = provider or settings.layout_model
        if "gpt" in provider:
            return OpenAILayoutProvider()
        elif "gemini" in provider:
            return GeminiLayoutProvider()
        elif "claude" in provider:
            return AnthropicLayoutProvider()
    
    def get_image_provider(self, provider: str = None) -> ImageAIProvider:
        provider = provider or settings.image_model
        if "flux" in provider or "sdxl" in provider:
            return ReplicateImageProvider()
        elif "gpt-image" in provider:
            return OpenAIImageProvider()
        elif "imagen" in provider:
            return GeminiImageProvider()
```

**Benefits:**
- Easy to add new providers
- A/B testing different models
- Fallback on provider failures
- Cost optimization by routing to cheaper models

### 2.3 Validation Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI-Generated Design JSON                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Stage 1: JSON Parsing                         │
│   • Valid JSON syntax                                           │
│   • If invalid: attempt JSON repair                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Stage 2: Schema Validation                      │
│   • Pydantic model validation                                   │
│   • Type checking                                               │
│   • Required fields present                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Stage 3: Auto-Repair                          │
│   • Clamp values to valid ranges                                │
│   • Add missing defaults                                        │
│   • Normalize zIndex values                                     │
│   • Extract text from image-rendered headlines                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Stage 4: Constraint Validation                   │
│   • Required layers present (headline)                          │
│   • No overlapping critical elements                            │
│   • Text within canvas bounds                                   │
│   • SmartImage recipes have holistic context                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Validated Design JSON                         │
│                    + Repair Log                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow Diagrams

### 3.1 Design Generation Flow

```
┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐
│  User   │      │ Frontend│      │ Backend │      │   AI    │
└────┬────┘      └────┬────┘      └────┬────┘      └────┬────┘
     │                │                │                │
     │ Enter prompt   │                │                │
     │───────────────▶│                │                │
     │                │                │                │
     │                │ POST /ai/generate-designs       │
     │                │───────────────▶│                │
     │                │                │                │
     │                │                │ Prompt + Brand │
     │                │                │───────────────▶│
     │                │                │                │
     │                │                │◀───────────────│
     │                │                │     Brief      │
     │                │                │                │
     │                │                │ Brief + Schema │
     │                │                │───────────────▶│
     │                │                │                │
     │                │                │◀───────────────│
     │                │                │  Design JSON   │
     │                │                │                │
     │                │                │───┐ Validate   │
     │                │                │   │ + Repair   │
     │                │                │◀──┘            │
     │                │                │                │
     │                │                │ Create Smart   │
     │                │                │ Image Recipes  │
     │                │                │───────────────▶│
     │                │                │                │
     │                │                │◀───────────────│
     │                │                │   Images       │
     │                │                │                │
     │                │◀───────────────│                │
     │                │ Design JSON[]  │                │
     │                │                │                │
     │◀───────────────│                │                │
     │ Show variants  │                │                │
     │                │                │                │
```

### 3.2 Smart Image Generation with Holistic Context

```
┌─────────────────────────────────────────────────────────────────┐
│                      Design JSON Context                         │
│                                                                  │
│   {                                                             │
│     "meta": { "title": "Diwali Sale" },                        │
│     "canvas": { "background": { "color": "#050816" } },        │
│     "brand": { "colors": { "primary": "#FFCC00" } },           │
│     "layers": [                                                 │
│       { "type": "text", "content": "Diwali Mega Sale" },       │
│       { "type": "shape", "fill": "#FF4D00" }                   │
│     ]                                                           │
│   }                                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Holistic Context Builder                            │
│                                                                  │
│   function buildHolisticContext(design, layer) {                │
│     return {                                                    │
│       designPurpose: design.meta.title,                        │
│       overallTheme: extractTheme(design),                      │
│       adjacentElements: describeAdjacentLayers(design, layer), │
│       brandColors: design.brand.colors,                        │
│       compositionHints: inferComposition(design, layer),       │
│       styleKeywords: extractStyleKeywords(design)              │
│     };                                                          │
│   }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Smart Image Recipe                            │
│                                                                  │
│   {                                                             │
│     "prompt": "professional studio shot of headphones",         │
│     "holisticContext": {                                        │
│       "designPurpose": "Diwali electronics sale ad",           │
│       "overallTheme": "premium dark with gold accents",        │
│       "adjacentElements": [                                     │
│         "Golden headline 'Diwali Mega Sale'",                  │
│         "Orange discount badge",                                │
│         "Dark purple background"                                │
│       ],                                                        │
│       "brandColors": ["#FFCC00", "#050816", "#FF4D00"],        │
│       "compositionHints": "Product on right, warm lighting",   │
│       "styleKeywords": ["premium", "dramatic", "festive"]      │
│     }                                                           │
│   }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Enhanced Prompt for AI                        │
│                                                                  │
│   "professional studio shot of headphones. Style: premium       │
│    dark with gold accents. Product on right, warm lighting.     │
│    Keywords: premium, dramatic, festive. Color palette          │
│    harmony with: #FFCC00, #050816, #FF4D00"                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Generated Image                               │
│        (Blends naturally with overall design)                    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Editor Load/Save Flow

```
┌───────────────────────────────────────────────────────────────────────────┐
│                           LOAD DESIGN                                      │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   1. Fetch Design JSON from API                                          │
│      GET /designs/{id}                                                   │
│      ↓                                                                   │
│   2. Store in TanStack Query cache                                       │
│      queryClient.setQueryData(['design', id], designJSON)                │
│      ↓                                                                   │
│   3. Pass to Editor Adapter                                              │
│      adapter.toEditorFormat(designJSON)                                  │
│      ↓                                                                   │
│   4. Adapter creates Fabric.js objects                                   │
│      - TextLayer → fabric.IText                                          │
│      - ImageLayer → fabric.Image                                         │
│      - ShapeLayer → fabric.Rect/Circle                                   │
│      ↓                                                                   │
│   5. Initialize Zustand editor state                                     │
│      - selectedLayerId: null                                             │
│      - history: [initial state]                                          │
│      - isDirty: false                                                    │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────┐
│                           SAVE DESIGN                                      │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   1. User triggers save (auto-save or manual)                            │
│      ↓                                                                   │
│   2. Adapter extracts canonical Design JSON                              │
│      const designJSON = adapter.fromEditorFormat()                       │
│      ↓                                                                   │
│   3. Validate before save                                                │
│      validateDesignJSON(designJSON) // client-side                       │
│      ↓                                                                   │
│   4. Send to API                                                         │
│      PATCH /designs/{id}                                                 │
│      body: { design_json: designJSON }                                   │
│      ↓                                                                   │
│   5. Server validates again                                              │
│      ValidationPipeline.validate(designJSON)                             │
│      ↓                                                                   │
│   6. Update database                                                     │
│      supabase.from('designs').update({ design_json })                    │
│      ↓                                                                   │
│   7. Invalidate query cache                                              │
│      queryClient.invalidateQueries(['design', id])                       │
│      ↓                                                                   │
│   8. Update editor state                                                 │
│      store.setIsDirty(false)                                             │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Architecture

### 4.1 Frontend Component Tree

```
App (Next.js)
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   ├── Navigation
│   │   └── UserMenu
│   └── Sidebar (contextual)
│
├── Pages
│   ├── / (Landing)
│   ├── /login
│   ├── /signup
│   ├── /dashboard
│   │   └── DashboardPage
│   │       ├── DesignGrid
│   │       │   └── DesignCard[]
│   │       └── NewDesignButton
│   │
│   ├── /create
│   │   └── CreatePage
│   │       ├── PromptInput
│   │       ├── BrandSelector
│   │       ├── FormatSelector
│   │       └── GenerateButton
│   │
│   ├── /designs/[id]/variants
│   │   └── VariantsPage
│   │       ├── VariantGrid
│   │       │   └── VariantCard[]
│   │       └── ActionBar
│   │
│   ├── /editor/[id]
│   │   └── EditorPage
│   │       ├── EditorProvider (context)
│   │       ├── EditorToolbar
│   │       │   ├── UndoRedo
│   │       │   ├── ZoomControls
│   │       │   └── ExportButton
│   │       ├── EditorCanvas
│   │       │   └── FabricCanvas
│   │       ├── LayerPanel
│   │       │   └── LayerItem[]
│   │       └── PropertiesPanel
│   │           ├── TextProperties
│   │           ├── ImageProperties
│   │           └── ShapeProperties
│   │
│   └── /brands
│       └── BrandsPage
│           ├── BrandGrid
│           │   └── BrandCard[]
│           └── BrandEditor
│
└── Providers
    ├── AuthProvider
    ├── QueryProvider
    └── ThemeProvider
```

### 4.2 Backend Module Structure

```
app/
├── main.py                    # FastAPI app entry
├── config.py                  # Settings
├── dependencies.py            # Shared DI
│
├── api/                       # Route handlers
│   ├── auth.py               # POST /auth/*
│   ├── designs.py            # CRUD /designs/*
│   ├── brands.py             # CRUD /brands/*
│   ├── assets.py             # /assets/*
│   ├── ai.py                 # /ai/*
│   └── export.py             # /export/*
│
├── models/                    # Pydantic models
│   ├── design.py             # DesignJSON, Layer types
│   ├── brand.py              # BrandKit
│   ├── asset.py              # Asset
│   ├── user.py               # User, Profile
│   └── ai.py                 # Brief, SmartImageRecipe
│
├── services/                  # Business logic
│   ├── design_service.py     # Design CRUD + patching
│   ├── brand_service.py      # Brand management
│   ├── asset_service.py      # File handling
│   └── export_service.py     # Image rendering
│
├── ai/                        # AI integrations
│   ├── providers/
│   │   ├── base.py           # Protocol definitions
│   │   ├── openai.py
│   │   ├── gemini.py
│   │   └── replicate.py
│   ├── layout_engine.py      # Prompt → Design
│   ├── image_engine.py       # Smart images
│   ├── context_builder.py    # Holistic context
│   └── prompts/
│       ├── brief.txt
│       ├── design.txt
│       └── edit.txt
│
├── validation/                # Design validation
│   ├── pipeline.py
│   ├── validators.py
│   └── repairers.py
│
└── db/                        # Data access
    ├── supabase.py
    └── queries.py
```

---

## 5. Security Architecture

### 5.1 Authentication Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                      Authentication Flow                          │
└──────────────────────────────────────────────────────────────────┘

1. User Login (Frontend)
   ┌─────────┐
   │ Browser │ ──► Supabase Auth ──► JWT (access + refresh)
   └─────────┘
        │
        │ Store tokens in httpOnly cookies
        ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                    Next.js Middleware                        │
   │   • Validate JWT on protected routes                        │
   │   • Refresh token if expired                                │
   │   • Redirect to login if invalid                            │
   └─────────────────────────────────────────────────────────────┘

2. API Requests (Frontend → Backend)
   ┌─────────┐         ┌─────────┐         ┌─────────┐
   │ Browser │ ──JWT──▶│ FastAPI │ ──verify─▶│Supabase │
   └─────────┘         └─────────┘         └─────────┘
                            │
                            │ Extract user_id from JWT
                            ▼
                       ┌─────────┐
                       │ Handler │
                       │ (scoped │
                       │ to user)│
                       └─────────┘

3. Row Level Security (Database)
   ┌─────────────────────────────────────────────────────────────┐
   │   CREATE POLICY "Users can manage own designs" ON designs   │
   │   FOR ALL USING (auth.uid() = owner_id);                    │
   └─────────────────────────────────────────────────────────────┘
```

### 5.2 Authorization Model

```
┌─────────────────────────────────────────────────────────────────┐
│                     Resource Access Control                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   User ─────owns─────► Designs                                  │
│        ─────owns─────► Brand Kits                               │
│        ─────owns─────► Assets                                   │
│        ─────owns─────► Campaigns                                │
│        ─────owns─────► Smart Image Recipes                      │
│                                                                  │
│   Access Rule: User can only access resources where             │
│                owner_id = current_user.id                       │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                         Future: Teams                            │
│                                                                  │
│   User ─────member_of─────► Team ─────owns─────► Resources      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Error Handling Strategy

### 6.1 Error Categories

| Category | HTTP Code | Handling |
|----------|-----------|----------|
| Validation Error | 400 | Show field-level errors |
| Authentication | 401 | Redirect to login |
| Authorization | 403 | Show access denied |
| Not Found | 404 | Show 404 page |
| AI Generation Failed | 500 | Show retry option |
| Rate Limited | 429 | Show cooldown timer |

### 6.2 Error Response Format

```typescript
interface APIError {
  error: {
    code: string;           // Machine-readable code
    message: string;        // Human-readable message
    details?: unknown;      // Additional context
    retryable: boolean;     // Can user retry?
    retryAfter?: number;    // Seconds until retry (if rate limited)
  };
}

// Example
{
  "error": {
    "code": "GENERATION_FAILED",
    "message": "Design generation failed. Please try again.",
    "details": {
      "stage": "brief_to_design",
      "modelError": "Token limit exceeded"
    },
    "retryable": true
  }
}
```

### 6.3 AI Error Recovery

```python
# ai/layout_engine.py

async def generate_design_with_recovery(
    brief: dict,
    max_retries: int = 2
) -> dict:
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            # Attempt generation
            raw_output = await provider.generate_design(brief)
            
            # Parse JSON (may fail)
            design_json = json.loads(raw_output)
            
            # Validate and repair
            validated, repairs = await validation_pipeline.validate(design_json)
            
            return {"design": validated, "repairs": repairs}
            
        except json.JSONDecodeError as e:
            # Try to repair JSON
            repaired = await attempt_json_repair(raw_output)
            if repaired:
                design_json = json.loads(repaired)
                validated, repairs = await validation_pipeline.validate(design_json)
                repairs.append("JSON syntax repaired")
                return {"design": validated, "repairs": repairs}
            last_error = e
            
        except ValidationError as e:
            # Log for analysis
            logger.warning(f"Validation failed attempt {attempt}: {e}")
            last_error = e
            
        except ProviderError as e:
            # Try fallback provider
            if attempt < max_retries:
                provider = get_fallback_provider()
            last_error = e
    
    # All retries exhausted
    raise GenerationError(
        "Design generation failed after retries",
        cause=last_error,
        retryable=True
    )
```

---

## 7. Caching Strategy

### 7.1 Cache Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend Caching                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   TanStack Query                                                │
│   ├── Design list: staleTime=30s, cacheTime=5min               │
│   ├── Single design: staleTime=0 (always fresh in editor)      │
│   ├── Brand kits: staleTime=5min                               │
│   └── Assets: staleTime=1hour (rarely change)                  │
│                                                                  │
│   Browser Cache (via CDN headers)                               │
│   ├── Static assets: max-age=1year                             │
│   ├── Images: max-age=1day, stale-while-revalidate             │
│   └── API responses: no-cache (dynamic)                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      Backend Caching                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   In-Memory (lru_cache)                                         │
│   ├── Prompt templates: permanent                               │
│   ├── Settings: permanent (restart to refresh)                  │
│   └── Common briefs: TTL=1hour                                  │
│                                                                  │
│   Smart Image Recipe Cache                                      │
│   ├── Key: hash(prompt + holistic_context + options)           │
│   ├── Value: asset_id                                          │
│   ├── Storage: Database (smart_image_recipes table)            │
│   └── Reuse: If identical recipe exists, return cached image   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Smart Image Deduplication

```python
# ai/image_engine.py

async def get_or_generate_smart_image(
    recipe: SmartImageRecipe,
    user_id: str
) -> str:
    """Returns asset_id, using cache if identical recipe exists."""
    
    # Generate cache key from recipe content
    cache_key = generate_recipe_hash(recipe)
    
    # Check for existing recipe with same hash
    existing = await db.smart_image_recipes.find_one({
        "owner_id": user_id,
        "cache_key": cache_key,
        "last_generated_asset_id": {"$ne": None}
    })
    
    if existing:
        logger.info(f"Cache hit for smart image: {cache_key[:8]}")
        return existing["last_generated_asset_id"]
    
    # Generate new image
    image_bytes = await image_provider.generate(
        prompt=recipe.prompt,
        holistic_context=recipe.holistic_context,
        options=recipe.options
    )
    
    # Upload to storage
    asset_id = await asset_service.upload(
        file=image_bytes,
        type="generated",
        user_id=user_id
    )
    
    # Save recipe for future cache hits
    await db.smart_image_recipes.insert({
        **recipe.dict(),
        "owner_id": user_id,
        "cache_key": cache_key,
        "last_generated_asset_id": asset_id,
        "generated_at": datetime.utcnow()
    })
    
    return asset_id
```

---

## 8. Scalability Considerations

### 8.1 Horizontal Scaling

```
┌─────────────────────────────────────────────────────────────────┐
│                    Load Balancer (CDN Edge)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │   FastAPI     │ │   FastAPI     │ │   FastAPI     │
    │   Instance 1  │ │   Instance 2  │ │   Instance N  │
    └───────────────┘ └───────────────┘ └───────────────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │        Supabase Postgres       │
              │     (Connection Pooling)       │
              └───────────────────────────────┘
```

**Stateless Design:**
- No session state on servers
- JWT tokens for authentication
- Database for all persistence
- AI calls are independent

### 8.2 Rate Limiting

```python
# app/middleware/rate_limit.py
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Different limits for different endpoints
RATE_LIMITS = {
    "generate_designs": "10/hour",
    "smart_image": "50/hour",
    "export": "100/hour",
    "api_default": "1000/hour"
}
```

---

## 9. Monitoring & Observability

### 9.1 Metrics to Track

| Category | Metrics |
|----------|---------|
| **Performance** | Request latency (p50, p95, p99), DB query time |
| **AI** | Generation success rate, latency by model, cost per request |
| **Business** | Designs created, exports completed, active users |
| **Errors** | Error rate by endpoint, AI failures, validation failures |

### 9.2 Logging Strategy

```python
# Structured logging format
{
    "timestamp": "2025-11-26T15:30:00Z",
    "level": "INFO",
    "service": "radic-backend",
    "trace_id": "abc123",
    "user_id": "user_456",
    "endpoint": "POST /ai/generate-designs",
    "duration_ms": 12500,
    "ai_model": "gpt-4.1",
    "tokens_used": 2500,
    "designs_generated": 3,
    "message": "Design generation completed"
}
```
