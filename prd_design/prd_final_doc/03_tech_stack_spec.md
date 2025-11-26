# Radic Pro — Tech Stack Specification

> **Version**: 2.0  
> **Last Updated**: November 2025

---

## Quick Start

```bash
# Backend (Python + uv)
cd backend
uv sync                                    # Install dependencies
uv run fastapi dev app/main.py --port 8000 # Start with auto-reload

# Frontend (Next.js + pnpm)  
cd frontend
pnpm install                               # Install dependencies
pnpm dev                                   # Start dev server
```

📖 **See [`07_setup_guide.md`](./07_setup_guide.md) for complete setup instructions, restart scripts, and troubleshooting.**

---

## 1. Stack Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                    │
│  Next.js 14 (App Router) + TypeScript + Tailwind + Shadcn UI            │
│  Canvas: Fabric.js with Custom Block Adapter                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                     │
│  FastAPI (Python 3.12) + Pydantic v2 + httpx                            │
│  Modules: auth, designs, brands, ai_generation, ai_image, export        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              PLATFORM                                    │
│  Supabase: Postgres + Auth + Storage + Realtime                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      AI PROVIDERS (via Replicate)                        │
│                                                                          │
│  Layout/JSON: Gemini 3 Pro (primary) / GPT-5 Structured (fallback)      │
│  Images: Nano Banana Pro (primary) / FLUX 1.1 Pro (fallback)            │
│  Vision: Gemini 3 Pro                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.1 AI Model Stack (Key Decision)

| Task | Primary Model | Fallback | Provider |
|------|--------------|----------|----------|
| **Layout/JSON Generation** | Gemini 3 Pro | GPT-5 Structured | Google/OpenAI via Replicate |
| **Copy Generation** | Gemini 3 Pro | Claude 4.5 Sonnet | Google/Anthropic via Replicate |
| **Image Generation** | Nano Banana Pro | FLUX 1.1 Pro | Google via Replicate |
| **Fast Preview Images** | FLUX Schnell | - | Replicate |
| **Vision/Analysis** | Gemini 3 Pro | GPT-4o mini | Google/OpenAI via Replicate |

**Why Nano Banana Pro for Images:**
- Best-in-class **legible text rendering** (critical for ad CTAs, offers)
- Studio-quality control (lighting, angles, depth)
- Up to 4K resolution
- Multi-image fusion (blend up to 14 images)
- Character consistency across edits

**Why Gemini 3 Pro for JSON:**
- Native structured output with JSON schemas
- Excellent reasoning for creative concepts
- Multimodal (can analyze brand images)
- Same ecosystem as Nano Banana Pro

---

## 2. Frontend Stack

### 2.1 Core Framework

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 14.x | React framework with App Router |
| **TypeScript** | 5.x | Type safety |
| **React** | 18.x | UI library |

**Why Next.js:**
- Server/Client component model for optimal performance
- Built-in image optimization
- API routes for BFF pattern if needed
- Strong ecosystem and community
- App Router for modern patterns

### 2.2 UI & Styling

| Technology | Purpose |
|------------|---------|
| **Tailwind CSS** | Utility-first styling |
| **Shadcn UI** | Pre-built accessible components |
| **Lucide React** | Icon library |
| **Class Variance Authority** | Component variants |

**Component Structure:**
```
src/components/
├── ui/                    # Shadcn UI components
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Dialog.tsx
│   └── ...
├── editor/                # Editor-specific components
│   ├── Canvas.tsx
│   ├── LayerPanel.tsx
│   ├── PropertiesPanel.tsx
│   └── Toolbar.tsx
├── design/                # Design management
│   ├── DesignCard.tsx
│   ├── DesignGrid.tsx
│   └── PromptInput.tsx
└── shared/                # Shared components
    ├── Header.tsx
    ├── Sidebar.tsx
    └── Loading.tsx
```

### 2.3 State Management

| Technology | Purpose |
|------------|---------|
| **React Context** | Global app state (auth, theme) |
| **TanStack Query** | Server state (designs, brands, assets) |
| **Zustand** | Editor state (canvas, selection, tools) |

**State Architecture:**
```typescript
// Global Context (React Context)
- AuthContext: user, session, login/logout
- ThemeContext: dark/light mode

// Server State (TanStack Query)
- useDesigns(): list, create, update, delete
- useBrands(): list, create, update
- useAssets(): upload, list

// Editor State (Zustand)
- useEditorStore(): 
  - selectedLayerId
  - tool (select, text, shape)
  - zoom
  - history (undo/redo stack)
```

### 2.4 Data Fetching & Forms

| Technology | Purpose |
|------------|---------|
| **TanStack Query** | Data fetching, caching, mutations |
| **React Hook Form** | Form state management |
| **Zod** | Schema validation |

**Example Pattern:**
```typescript
// hooks/useDesigns.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';

const DesignSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1),
  // ...
});

export function useDesigns() {
  return useQuery({
    queryKey: ['designs'],
    queryFn: async () => {
      const res = await fetch('/api/designs');
      const data = await res.json();
      return z.array(DesignSchema).parse(data);
    },
  });
}

export function useCreateDesign() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (prompt: string) => {
      const res = await fetch('/api/ai/generate-designs', {
        method: 'POST',
        body: JSON.stringify({ prompt }),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['designs'] });
    },
  });
}
```

### 2.5 Canvas Editor

| Technology | Version | Purpose |
|------------|---------|---------|
| **Fabric.js** | 6.x | Canvas manipulation |
| **Custom Adapter** | - | Design JSON ↔ Fabric conversion |

**Why Fabric.js:**
- Mature, well-documented
- Rich object model (text, shapes, images)
- Good performance with proper configuration
- Active maintenance
- MIT license (free)

**Editor Architecture:**
```typescript
// adapters/fabric-adapter.ts
class FabricAdapter implements EditorAdapter {
  toEditorFormat(design: DesignJSON): void;
  fromEditorFormat(): DesignJSON;
  applyPatch(patch: DesignPatch): void;
  exportImage(options: ExportOptions): Promise<Blob>;
}

// hooks/useEditor.ts
export function useEditor(canvasRef: RefObject<HTMLCanvasElement>) {
  const adapter = useMemo(() => new FabricAdapter(canvasRef.current), []);
  const store = useEditorStore();
  
  const loadDesign = useCallback((design: DesignJSON) => {
    adapter.toEditorFormat(design);
    store.setLoaded(true);
  }, [adapter]);
  
  const saveDesign = useCallback(() => {
    return adapter.fromEditorFormat();
  }, [adapter]);
  
  return { loadDesign, saveDesign, adapter };
}
```

### 2.6 Frontend Dependencies

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.0",
    
    "@tanstack/react-query": "^5.0.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0",
    
    "zustand": "^4.4.0",
    
    "tailwindcss": "^3.4.0",
    "@radix-ui/react-*": "latest",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "lucide-react": "^0.300.0",
    
    "fabric": "^6.0.0",
    
    "@supabase/supabase-js": "^2.39.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/node": "^20.10.0",
    "eslint": "^8.55.0",
    "eslint-config-next": "^14.0.0",
    "prettier": "^3.1.0",
    "prettier-plugin-tailwindcss": "^0.5.0"
  }
}
```

---

## 3. Backend Stack

### 3.1 Core Framework

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12 | Runtime |
| **FastAPI** | 0.109+ | API framework |
| **Pydantic** | 2.x | Validation & serialization |
| **uvicorn** | 0.25+ | ASGI server |

**Why FastAPI:**
- Native async support
- Pydantic integration for strict typing
- Auto-generated OpenAPI docs
- Excellent performance
- Easy to test

### 3.2 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Settings management
│   ├── dependencies.py         # Shared dependencies
│   │
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── designs.py
│   │   ├── brands.py
│   │   ├── assets.py
│   │   ├── ai.py
│   │   └── export.py
│   │
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── design.py           # Design JSON schema
│   │   ├── brand.py
│   │   ├── asset.py
│   │   ├── user.py
│   │   └── ai.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── design_service.py
│   │   ├── brand_service.py
│   │   ├── asset_service.py
│   │   └── export_service.py
│   │
│   ├── ai/                     # AI integrations
│   │   ├── __init__.py
│   │   ├── providers/
│   │   │   ├── base.py         # Abstract interfaces
│   │   │   ├── openai.py
│   │   │   ├── gemini.py
│   │   │   └── replicate.py
│   │   ├── layout_engine.py    # Prompt → Design
│   │   ├── image_engine.py     # Smart image generation
│   │   └── prompts/            # Prompt templates
│   │       ├── brief.txt
│   │       ├── design.txt
│   │       └── edit.txt
│   │
│   ├── validation/             # Design validation
│   │   ├── __init__.py
│   │   ├── pipeline.py
│   │   ├── validators.py
│   │   └── repairers.py
│   │
│   └── db/                     # Database access
│       ├── __init__.py
│       ├── supabase.py         # Supabase client
│       └── queries.py          # Query functions
│
├── tests/
│   ├── __init__.py
│   ├── test_designs.py
│   ├── test_ai.py
│   └── test_validation.py
│
├── pyproject.toml              # uv/poetry config
├── .env.example
└── Dockerfile
```

### 3.3 Key Dependencies

```toml
# pyproject.toml
[project]
name = "radic-backend"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.25.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    
    "httpx>=0.26.0",           # Async HTTP client
    "python-multipart>=0.0.6", # File uploads
    
    "supabase>=2.3.0",         # Supabase client
    
    "openai>=1.6.0",           # OpenAI SDK
    "google-generativeai>=0.3.0",  # Gemini SDK
    "replicate>=0.22.0",       # Replicate SDK
    
    "pillow>=10.1.0",          # Image processing
    "python-jose[cryptography]>=3.3.0",  # JWT
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.1.0",
    "black>=23.12.0",
    "mypy>=1.8.0",
]
```

### 3.4 Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "Radic Pro"
    debug: bool = False
    
    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # AI Providers
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    replicate_api_token: str | None = None
    
    # AI Configuration
    layout_model: str = "gpt-4.1"
    image_model: str = "flux-pro"
    
    # Limits
    max_designs_per_generation: int = 3
    max_image_resolution: int = 2048
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## 4. Database (Supabase)

### 4.1 Why Supabase

| Feature | Benefit |
|---------|---------|
| **Managed Postgres** | No DB ops overhead |
| **Built-in Auth** | OAuth, email, magic links |
| **Storage** | S3-compatible file storage |
| **Realtime** | Live subscriptions (future) |
| **Row Level Security** | Secure multi-tenancy |
| **Edge Functions** | Serverless compute (if needed) |

### 4.2 Database Schema

```sql
-- Users (managed by Supabase Auth)
-- Access via auth.users()

-- Profiles (extended user data)
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'growth')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Brand Kits
CREATE TABLE brand_kits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    colors JSONB NOT NULL DEFAULT '{}',
    fonts JSONB NOT NULL DEFAULT '{}',
    logo_asset_id UUID,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Designs
CREATE TABLE designs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    campaign_id UUID,
    title TEXT NOT NULL,
    format TEXT NOT NULL DEFAULT 'instagram_post',
    design_json JSONB NOT NULL,
    thumbnail_url TEXT,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Assets
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('logo', 'product', 'generated', 'export', 'reference')),
    filename TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    size_bytes INTEGER,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Smart Image Recipes
CREATE TABLE smart_image_recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    design_id UUID REFERENCES designs(id) ON DELETE SET NULL,
    type TEXT NOT NULL CHECK (type IN ('product_shot', 'background', 'decorative_text', 'persona', 'infographic')),
    prompt TEXT NOT NULL,
    holistic_context JSONB NOT NULL DEFAULT '{}',
    model TEXT NOT NULL,
    options JSONB DEFAULT '{}',
    reference_asset_ids UUID[] DEFAULT '{}',
    last_generated_asset_id UUID REFERENCES assets(id),
    generated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Campaigns (for grouping designs)
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    brand_kit_id UUID REFERENCES brand_kits(id),
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_designs_owner ON designs(owner_id, updated_at DESC);
CREATE INDEX idx_designs_campaign ON designs(campaign_id) WHERE campaign_id IS NOT NULL;
CREATE INDEX idx_assets_owner ON assets(owner_id, created_at DESC);
CREATE INDEX idx_brand_kits_owner ON brand_kits(owner_id);

-- Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE brand_kits ENABLE ROW LEVEL SECURITY;
ALTER TABLE designs ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE smart_image_recipes ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;

-- RLS Policies (owner-based access)
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can manage own brand_kits" ON brand_kits
    FOR ALL USING (auth.uid() = owner_id);

CREATE POLICY "Users can manage own designs" ON designs
    FOR ALL USING (auth.uid() = owner_id);

CREATE POLICY "Users can manage own assets" ON assets
    FOR ALL USING (auth.uid() = owner_id);

CREATE POLICY "Users can manage own recipes" ON smart_image_recipes
    FOR ALL USING (auth.uid() = owner_id);

CREATE POLICY "Users can manage own campaigns" ON campaigns
    FOR ALL USING (auth.uid() = owner_id);
```

### 4.3 Storage Buckets

```sql
-- Storage buckets (created via Supabase dashboard or API)
-- bucket: logos (public)
-- bucket: products (private)
-- bucket: generated (private)
-- bucket: exports (private, time-limited URLs)
```

### 4.4 Database Access Pattern

We use **Supabase client** directly (not Prisma) for simplicity:

```python
# app/db/supabase.py
from supabase import create_client, Client
from app.config import get_settings

def get_supabase_client() -> Client:
    settings = get_settings()
    return create_client(
        settings.supabase_url,
        settings.supabase_service_key
    )

# Usage in services
async def get_user_designs(user_id: str) -> list[dict]:
    client = get_supabase_client()
    response = client.table("designs") \
        .select("*") \
        .eq("owner_id", user_id) \
        .order("updated_at", desc=True) \
        .execute()
    return response.data
```

---

## 5. AI Providers

### 5.1 Provider Abstraction

```python
# app/ai/providers/base.py
from abc import ABC, abstractmethod
from typing import Protocol

class LayoutAIProvider(Protocol):
    """Interface for layout generation AI"""
    
    async def generate_brief(
        self, 
        prompt: str, 
        brand: dict | None
    ) -> dict:
        """Convert user prompt to structured brief"""
        ...
    
    async def generate_design(
        self, 
        brief: dict, 
        schema_version: str
    ) -> dict:
        """Convert brief to Design JSON"""
        ...
    
    async def edit_design(
        self, 
        design: dict, 
        instruction: str
    ) -> dict:
        """Apply edit instruction, return patch operations"""
        ...

class ImageAIProvider(Protocol):
    """Interface for image generation AI"""
    
    async def generate(
        self,
        prompt: str,
        holistic_context: dict,
        options: dict
    ) -> bytes:
        """Generate image from prompt with context"""
        ...
    
    async def edit(
        self,
        image: bytes,
        instruction: str,
        mask: bytes | None
    ) -> bytes:
        """Edit existing image"""
        ...
```

### 5.2 Gemini 3 Pro Implementation (Primary for Layout/JSON)

```python
# app/ai/providers/gemini.py
import replicate
from app.config import get_settings

class GeminiLayoutProvider:
    """Primary provider for layout/JSON generation using Gemini 3 Pro via Replicate"""
    
    def __init__(self):
        settings = get_settings()
        self.client = replicate.Client(api_token=settings.replicate_api_token)
        self.model = "google/gemini-3-pro"  # Via Replicate
    
    async def generate_brief(self, prompt: str, brand: dict | None) -> dict:
        """Convert user prompt to structured creative brief"""
        system_prompt = self._load_prompt("brief.txt")
        
        output = await self.client.async_run(
            self.model,
            input={
                "prompt": f"{system_prompt}\n\nUser request: {prompt}\nBrand: {brand}",
                "response_format": {"type": "json_object"},
                "temperature": 0.7,
                "max_tokens": 2000
            }
        )
        
        return json.loads(output)
    
    async def generate_design(
        self, 
        brief: dict, 
        creative_concept: str,
        schema: dict
    ) -> dict:
        """Generate Design JSON from brief using structured output"""
        system_prompt = self._load_prompt("design.txt")
        
        output = await self.client.async_run(
            self.model,
            input={
                "prompt": f"{system_prompt}\n\nBrief: {json.dumps(brief)}\nConcept: {creative_concept}",
                "response_format": {
                    "type": "json_schema",
                    "json_schema": schema
                },
                "temperature": 0.5,
                "max_tokens": 4000
            }
        )
        
        return json.loads(output)
```

### 5.3 Nano Banana Pro Implementation (Primary for Images)

```python
# app/ai/providers/nano_banana.py
import replicate
import httpx
from app.config import get_settings

class NanoBananaProImageProvider:
    """Primary provider for image generation using Nano Banana Pro (Gemini 3 Pro Image)"""
    
    def __init__(self):
        settings = get_settings()
        self.client = replicate.Client(api_token=settings.replicate_api_token)
        self.model = "google/nano-banana-pro"  # Gemini 3 Pro Image
    
    async def generate(
        self, 
        prompt: str, 
        holistic_context: dict, 
        options: dict
    ) -> bytes:
        """Generate image with legible text support"""
        enhanced_prompt = self._build_enhanced_prompt(prompt, holistic_context)
        
        output = await self.client.async_run(
            self.model,
            input={
                "prompt": enhanced_prompt,
                "aspect_ratio": options.get("aspectRatio", "1:1"),
                "output_resolution": options.get("resolution", "1k"),  # 1k, 2k, 4k
                "text_to_render": options.get("textToRender"),  # For text in images
                "style": options.get("style", "photo"),
            }
        )
        
        # Download image
        async with httpx.AsyncClient() as client:
            response = await client.get(output)
            return response.content
    
    async def generate_with_text(
        self,
        prompt: str,
        text_to_render: str,
        style: str,
        holistic_context: dict,
        resolution: str = "1k"
    ) -> bytes:
        """Generate image with legible text (e.g., CTAs, offer badges)"""
        enhanced_prompt = self._build_enhanced_prompt(prompt, holistic_context)
        
        output = await self.client.async_run(
            self.model,
            input={
                "prompt": enhanced_prompt,
                "text_to_render": text_to_render,
                "text_style": style,
                "output_resolution": resolution,
                "aspect_ratio": "1:1"
            }
        )
        
        async with httpx.AsyncClient() as client:
            response = await client.get(output)
            return response.content
    
    def _build_enhanced_prompt(self, prompt: str, context: dict) -> str:
        """Combine specific prompt with holistic context for better blending"""
        parts = [prompt]
        
        if context.get("overallTheme"):
            parts.append(f"Style: {context['overallTheme']}")
        
        if context.get("compositionHints"):
            parts.append(context["compositionHints"])
        
        if context.get("styleKeywords"):
            parts.append(f"Keywords: {', '.join(context['styleKeywords'])}")
        
        if context.get("brandColors"):
            colors = context["brandColors"][:3]
            parts.append(f"Color palette harmony with: {', '.join(colors)}")
        
        return ". ".join(parts)


class FluxImageProvider:
    """Fallback provider for non-text images using FLUX 1.1 Pro"""
    
    def __init__(self):
        settings = get_settings()
        self.client = replicate.Client(api_token=settings.replicate_api_token)
    
    async def generate(
        self, 
        prompt: str, 
        holistic_context: dict, 
        options: dict
    ) -> bytes:
        """Generate image without text (backgrounds, product shots)"""
        enhanced_prompt = self._build_enhanced_prompt(prompt, holistic_context)
        
        model = "black-forest-labs/flux-1.1-pro"
        output = await self.client.async_run(
            model,
            input={
                "prompt": enhanced_prompt,
                "aspect_ratio": options.get("aspectRatio", "1:1"),
                "output_format": "png",
                "output_quality": 90 if options.get("quality") != "high" else 100
            }
        )
        
        async with httpx.AsyncClient() as client:
            response = await client.get(output)
            return response.content
    
    async def generate_fast(self, prompt: str) -> bytes:
        """Fast preview using FLUX Schnell ($0.003/image)"""
        model = "black-forest-labs/flux-schnell"
        output = await self.client.async_run(
            model,
            input={"prompt": prompt, "aspect_ratio": "1:1"}
        )
        
        async with httpx.AsyncClient() as client:
            response = await client.get(output)
            return response.content
    
    def _build_enhanced_prompt(self, prompt: str, context: dict) -> str:
        parts = [prompt]
        if context.get("overallTheme"):
            parts.append(f"Style: {context['overallTheme']}")
        if context.get("brandColors"):
            colors = context["brandColors"][:3]
            parts.append(f"Color palette: {', '.join(colors)}")
        return ". ".join(parts)
```

### 5.4 Provider Factory

```python
# app/ai/providers/factory.py
from app.config import get_settings
from .gemini import GeminiLayoutProvider
from .nano_banana import NanoBananaProImageProvider, FluxImageProvider

class AIProviderFactory:
    """Factory for selecting appropriate AI providers"""
    
    def get_layout_provider(self, provider: str = None) -> LayoutAIProvider:
        provider = provider or get_settings().layout_model
        if "gemini" in provider.lower():
            return GeminiLayoutProvider()
        elif "gpt" in provider.lower():
            return GPT5StructuredProvider()  # Fallback
        elif "claude" in provider.lower():
            return ClaudeSonnetProvider()  # Fallback
        return GeminiLayoutProvider()  # Default
    
    def get_image_provider(
        self, 
        provider: str = None,
        needs_text: bool = False
    ) -> ImageAIProvider:
        provider = provider or get_settings().image_model
        
        # Always use Nano Banana Pro for text-in-image
        if needs_text:
            return NanoBananaProImageProvider()
        
        if "nano-banana" in provider.lower():
            return NanoBananaProImageProvider()
        elif "flux" in provider.lower():
            return FluxImageProvider()
        
        return NanoBananaProImageProvider()  # Default
```

---

## 6. DevOps & Deployment

### 6.1 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Vercel                                │
│                  (Next.js Frontend)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Railway / Render                           │
│                  (FastAPI Backend)                           │
│              - Auto-scaling                                  │
│              - Health checks                                 │
│              - HTTPS termination                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Supabase                               │
│              (Postgres + Auth + Storage)                     │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Environment Configuration

```bash
# Frontend (.env.local)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
NEXT_PUBLIC_API_URL=https://api.radicpro.com

# Backend (.env)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
SUPABASE_SERVICE_KEY=xxx

# All AI via Replicate (single provider)
REPLICATE_API_TOKEN=xxx

# Model Configuration
LAYOUT_MODEL=gemini-3-pro
IMAGE_MODEL=nano-banana-pro
FALLBACK_IMAGE_MODEL=flux-1.1-pro
FALLBACK_LAYOUT_MODEL=gpt-5-structured

# Resolution defaults
DEFAULT_EDITOR_RESOLUTION=1k
DEFAULT_EXPORT_RESOLUTION=2k
```

### 6.3 CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Run tests
        run: uv run pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Railway
        uses: railwayapp/railway-action@v1
        with:
          token: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel
        uses: vercel/action@v25
        with:
          token: ${{ secrets.VERCEL_TOKEN }}
```

---

## 7. Monitoring & Observability

### 7.1 Error Tracking

| Service | Purpose |
|---------|---------|
| **Sentry** | Error tracking (frontend + backend) |
| **PostHog** | Product analytics |
| **Supabase Dashboard** | DB/Auth metrics |

### 7.2 Logging

```python
# app/main.py
import logging
from fastapi import FastAPI, Request
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"duration={process_time:.3f}s"
    )
    
    return response
```

---

## 8. Cost Optimization Guidelines

### 8.1 AI Cost Control

| Strategy | Implementation |
|----------|----------------|
| **Prompt caching** | Cache common prompt templates |
| **Response caching** | Cache identical generation requests |
| **Resolution tiers** | Low-res in editor, high-res on export |
| **Model selection** | Use smaller models for simple tasks |
| **Rate limiting** | Per-user generation limits |

### 8.2 Infrastructure Cost

| Strategy | Implementation |
|----------|----------------|
| **Lazy loading** | Load editor only on `/editor` route |
| **Static generation** | Marketing pages as static HTML |
| **CDN caching** | Cache assets at edge |
| **Auto-scaling** | Scale down during low traffic |
| **DB indexing** | Proper indexes for common queries |

---

## 9. Security Checklist

- [ ] JWT tokens with short expiry + refresh
- [ ] HTTPS everywhere
- [ ] Row Level Security enabled
- [ ] API rate limiting
- [ ] Input validation (Pydantic + Zod)
- [ ] Signed URLs for private assets
- [ ] CORS properly configured
- [ ] Environment variables for secrets
- [ ] Content Security Policy headers
- [ ] Dependency vulnerability scanning
