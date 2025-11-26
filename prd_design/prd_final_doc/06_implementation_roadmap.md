# Radic Pro — Implementation Roadmap

> **Version**: 2.0  
> **Last Updated**: November 2025

---

## 1. Development Phases Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     V1 MVP IMPLEMENTATION TIMELINE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 0    Phase 1       Phase 2        Phase 3       Phase 4      Phase 5 │
│  ───────    ───────       ───────        ───────       ───────      ─────── │
│  SETUP     BLOCK SYSTEM  AI GENERATION   SMART IMG    POLISH       LAUNCH  │
│            + EDITOR      (Gemini 3 Pro)  (Nano Banana)                      │
│                                                                              │
│  Week 1-2   Week 3-5      Week 6-8       Week 9-10    Week 11-12   Week 13 │
│                                                                              │
│  ████       ██████        ██████         ████          ████         ██      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Total Estimated Duration: 13 weeks** (optimized for MVP)

### V1 MVP Scope Summary

| Feature | Status |
|---------|--------|
| Block-based Editor (10 blocks) | ✅ V1 |
| Creative Concepts (3 concepts) | ✅ V1 |
| AI Generation (Gemini 3 Pro) | ✅ V1 |
| Smart Images (Nano Banana Pro) | ✅ V1 |
| Manual Brand Kit | ✅ V1 |
| Export (PNG/JPG) | ✅ V1 |
| Brand Intelligence Engine | ❌ V1.5 |
| Persona Engine | ❌ V2 |
| Competitor Intelligence | ❌ V2 |
| Campaign Builder | ❌ V2 |

---

## 2. Phase 0: Foundation Setup (Weeks 1-2)

### 2.1 Objectives
- Set up development environment
- Initialize project structure
- Establish CI/CD pipeline
- Basic auth flow working

### 2.2 Deliverables

#### Frontend
- [ ] Next.js 14 project with App Router
- [ ] TypeScript configuration
- [ ] Tailwind CSS + Shadcn UI setup
- [ ] ESLint + Prettier configuration
- [ ] Basic layout (Header, Sidebar shell)
- [ ] Auth pages (Login, Signup)
- [ ] Supabase Auth integration
- [ ] Protected route middleware

#### Backend
- [ ] FastAPI project structure
- [ ] Pydantic v2 configuration
- [ ] Supabase client setup
- [ ] Environment configuration
- [ ] Health check endpoint
- [ ] Auth endpoints (verify JWT)
- [ ] Basic error handling middleware

#### Infrastructure
- [ ] Supabase project created
- [ ] Database schema (initial)
- [ ] Storage buckets configured
- [ ] RLS policies (basic)
- [ ] Vercel project (frontend)
- [ ] Railway/Render project (backend)
- [ ] GitHub Actions CI pipeline

### 2.3 Success Criteria
- [ ] User can sign up and log in
- [ ] Protected routes require auth
- [ ] Health check returns 200
- [ ] CI runs on every PR

### 2.4 Technical Tasks

```markdown
## Week 1

### Day 1-2: Project Setup
- [ ] Create GitHub repo with monorepo structure
- [ ] Initialize Next.js: `pnpm create next-app@latest frontend --typescript --tailwind --app`
- [ ] Initialize FastAPI with uv: `cd backend && uv init --name radic-backend`
- [ ] Set Python version: `uv python pin 3.12`
- [ ] Add dependencies: `uv add fastapi uvicorn[standard] pydantic supabase`
- [ ] Create restart scripts (see `07_setup_guide.md`)

### Day 3-4: Supabase Setup
- [ ] Create Supabase project
- [ ] Set up database tables
- [ ] Configure auth providers
- [ ] Create storage buckets

### Day 5: CI/CD Setup
- [ ] Configure GitHub Actions
- [ ] Set up Vercel deployment
- [ ] Set up Railway deployment

## Week 2

### Day 1-2: Frontend Auth
- [ ] Install Supabase JS client
- [ ] Create AuthContext
- [ ] Build Login page
- [ ] Build Signup page
- [ ] Add auth middleware

### Day 3-4: Backend Auth
- [ ] JWT verification middleware
- [ ] User profile endpoint
- [ ] Error handling

### Day 5: Integration Testing
- [ ] Test auth flow end-to-end
- [ ] Fix issues
- [ ] Document setup process
```

---

## 3. Phase 1: Editor Core (Weeks 3-5)

### 3.1 Objectives
- Implement canonical Design JSON schema
- Build Fabric.js adapter
- Create functional editor UI
- Enable manual design creation/editing

### 3.2 Deliverables

#### Design JSON Schema v2.0
- [ ] TypeScript types for Design JSON v2.0 with blocks
- [ ] Block type definitions (10 V1 blocks)
- [ ] Creative Concept type definitions
- [ ] Pydantic models for Design JSON
- [ ] Zod validation schemas
- [ ] JSON Schema export for documentation

#### Block Adapter
- [ ] `BlockAdapter` interface definition
- [ ] `FabricBlockAdapter` implementation
  - [ ] `toEditorFormat()` — Design JSON blocks → Fabric objects
  - [ ] `fromEditorFormat()` — Fabric objects → Design JSON blocks
  - [ ] Text block conversion (headline, subhead, cta, price, footer)
  - [ ] Image block conversion (background, product_image, logo)
  - [ ] Shape block conversion (badge, offer_tag)
- [ ] Unit tests for adapter

#### Block-Based Editor UI
- [ ] EditorPage layout
- [ ] FabricCanvas component
- [ ] EditorToolbar
  - [ ] Selection tool
  - [ ] Undo/Redo buttons
  - [ ] Zoom controls
- [ ] BlockPanel (replaces LayerPanel)
  - [ ] Block list with types
  - [ ] Visibility toggle
  - [ ] Lock toggle
  - [ ] Reorder (drag)
- [ ] PropertiesPanel
  - [ ] TextBlockProperties
  - [ ] ImageBlockProperties
  - [ ] ShapeBlockProperties

#### Editor State (Zustand)
- [ ] `useEditorStore` implementation
  - [ ] selectedLayerId
  - [ ] tool (select, text, shape)
  - [ ] zoom
  - [ ] history stack
  - [ ] isDirty flag
- [ ] Undo/Redo logic
- [ ] Auto-save trigger

#### Backend
- [ ] Design CRUD endpoints
- [ ] Design validation on save
- [ ] Thumbnail generation (basic)

### 3.3 Success Criteria
- [ ] User can create blank design
- [ ] User can add/edit text layers
- [ ] User can add/edit shapes
- [ ] User can upload and place images
- [ ] User can save and reload design
- [ ] Undo/Redo works correctly
- [ ] Design JSON validates correctly

### 3.4 Technical Tasks

```markdown
## Week 3

### Day 1-2: Design JSON Schema
- [ ] Define TypeScript types
- [ ] Create Pydantic models
- [ ] Write validation tests

### Day 3-5: Fabric.js Setup
- [ ] Install Fabric.js
- [ ] Create FabricCanvas component
- [ ] Implement basic canvas operations
- [ ] Test canvas rendering

## Week 4

### Day 1-3: Adapter Implementation
- [ ] Build toEditorFormat()
- [ ] Build fromEditorFormat()
- [ ] Handle all layer types
- [ ] Write adapter tests

### Day 4-5: Editor UI Shell
- [ ] Build EditorPage layout
- [ ] Add EditorToolbar
- [ ] Add LayerPanel skeleton
- [ ] Add PropertiesPanel skeleton

## Week 5

### Day 1-2: Properties Panels
- [ ] TextProperties component
- [ ] ShapeProperties component
- [ ] Wire to Fabric events

### Day 3-4: State & History
- [ ] Implement useEditorStore
- [ ] Add undo/redo
- [ ] Add auto-save

### Day 5: Backend Integration
- [ ] Design CRUD API
- [ ] Test save/load flow
- [ ] Fix any adapter issues
```

---

## 4. Phase 2: AI Design Generation (Weeks 6-8)

### 4.1 Objectives
- Implement AI provider abstraction with Gemini 3 Pro
- Build prompt → brief → design pipeline
- Generate 3 block-based design variants per concept
- Creative concept selection UI

### 4.2 Deliverables

#### AI Provider Abstraction
- [ ] `LayoutAIProvider` protocol
- [ ] `GeminiLayoutProvider` implementation (PRIMARY)
  - [ ] Structured output with JSON schema
  - [ ] Creative concept reasoning
- [ ] `GPT5StructuredProvider` implementation (FALLBACK)
- [ ] Provider factory with fallback logic

#### AI Pipeline (Gemini 3 Pro)
- [ ] Prompt templates (brief, design)
- [ ] Creative concept definitions (3 V1 concepts)
- [ ] `prompt_to_brief()` function with concept selection
- [ ] `brief_to_blocks()` function (block-based output)
- [ ] Response parsing with JSON schema validation
- [ ] Auto-repair for malformed responses

#### Validation Pipeline
- [ ] `ValidationPipeline` class
- [ ] Block schema validators
- [ ] Auto-repair functions
  - [ ] Clamp values
  - [ ] Add missing required blocks
  - [ ] Normalize block positions
  - [ ] Validate block constraints
- [ ] Validation logging

#### Frontend
- [ ] PromptPage UI
  - [ ] Prompt input textarea
  - [ ] Creative concept selector (optional)
  - [ ] Brand selector dropdown
  - [ ] Generate button
  - [ ] Loading state with progress
- [ ] VariantsPage UI
  - [ ] Variant grid
  - [ ] Thumbnail preview
  - [ ] Open in editor button
  - [ ] Regenerate button

#### Backend
- [ ] `POST /ai/generate-designs` endpoint
- [ ] Brief caching (optional)
- [ ] Generation logging
- [ ] Error recovery

### 4.3 Success Criteria
- [ ] User enters prompt → gets 3 valid designs
- [ ] Each design opens correctly in editor
- [ ] All text is editable (not images)
- [ ] Generation takes < 15 seconds
- [ ] Failed generations show meaningful error

### 4.4 Technical Tasks

```markdown
## Week 6

### Day 1-2: AI Provider Setup
- [ ] Define LayoutAIProvider protocol
- [ ] Implement OpenAI provider
- [ ] Configure API keys
- [ ] Test basic calls

### Day 3-5: Prompt Templates
- [ ] Write brief prompt template
- [ ] Write design prompt template
- [ ] Test with sample inputs
- [ ] Iterate on prompt quality

## Week 7

### Day 1-3: Pipeline Implementation
- [ ] Build prompt_to_brief()
- [ ] Build brief_to_design()
- [ ] Handle JSON parsing
- [ ] Add JSON repair logic

### Day 4-5: Validation Pipeline
- [ ] Implement validators
- [ ] Implement repairers
- [ ] Write tests
- [ ] Log validation results

## Week 8

### Day 1-2: API Endpoint
- [ ] Create /ai/generate-designs
- [ ] Add error handling
- [ ] Add rate limiting
- [ ] Test with various prompts

### Day 3-5: Frontend UI
- [ ] Build PromptPage
- [ ] Build VariantsPage
- [ ] Connect to API
- [ ] Handle loading/error states

## Week 9

### Day 1-3: Quality Iteration
- [ ] Test 50+ prompts
- [ ] Identify failure patterns
- [ ] Improve prompts
- [ ] Add more repairers

### Day 4-5: Performance
- [ ] Optimize API calls
- [ ] Add brief caching
- [ ] Measure latency
- [ ] Document issues
```

---

## 5. Phase 3: Smart Images with Nano Banana Pro (Weeks 9-10)

### 5.1 Objectives
- Implement Smart Image system using Nano Banana Pro
- Build holistic context generation for seamless blending
- Enable legible text rendering in images (CTAs, offers)
- UI for smart image management

### 5.2 Deliverables

#### Image Provider Abstraction
- [ ] `ImageAIProvider` protocol
- [ ] `NanoBananaProProvider` implementation (PRIMARY)
  - [ ] Standard image generation
  - [ ] Text-in-image generation (CTAs, badges)
  - [ ] Multi-image fusion
- [ ] `FluxImageProvider` implementation (FALLBACK)
- [ ] `FluxSchnellProvider` for fast previews
- [ ] Provider factory with text-detection routing

#### Holistic Context System
- [ ] `HolisticContext` schema
- [ ] `build_holistic_context()` function
  - [ ] Extract design purpose
  - [ ] Describe adjacent blocks
  - [ ] Extract brand colors
  - [ ] Generate composition hints
  - [ ] Detect if text rendering needed
- [ ] Enhanced prompt builder for Nano Banana Pro

#### Smart Image Pipeline
- [ ] `SmartImageRecipe` model with `textToRender` field
- [ ] Recipe creation from design blocks
- [ ] Image generation with holistic context
- [ ] Resolution-aware generation (1K editor, 2K+ export)
- [ ] Asset storage integration
- [ ] Recipe caching (deduplication)

#### Frontend
- [ ] Smart Image indicator on image blocks
- [ ] Smart Image panel
  - [ ] Show recipe prompt
  - [ ] Regenerate button
  - [ ] Resolution selector
- [ ] Loading state for pending images

#### Backend
- [ ] `POST /ai/smart-image` endpoint
- [ ] `POST /ai/smart-image/{id}/regenerate`
- [ ] Resolution parameter support
- [ ] Generation status tracking

### 5.3 Success Criteria
- [ ] Product shots blend naturally with design
- [ ] **Text in images is legible (>98% accuracy)**
- [ ] Smart images respect brand colors
- [ ] User can regenerate with modified prompt
- [ ] Identical recipes are cached (not regenerated)
- [ ] Generation < 10 seconds

### 5.4 Technical Tasks

```markdown
## Week 9

### Day 1-2: Image Provider Setup
- [ ] Define ImageAIProvider protocol
- [ ] Implement NanoBananaProProvider (primary)
- [ ] Implement FluxImageProvider (fallback)
- [ ] Configure Replicate API tokens
- [ ] Test basic generation + text rendering

### Day 3-5: Holistic Context
- [ ] Design HolisticContext schema
- [ ] Build context extractor from blocks
- [ ] Build enhanced prompts for Nano Banana
- [ ] Add text-detection routing
- [ ] Validate output quality

## Week 10

### Day 1-3: Smart Image Pipeline
- [ ] Create SmartImageRecipe model
- [ ] Add textToRender field support
- [ ] Implement generation flow
- [ ] Resolution-aware generation
- [ ] Asset storage integration
- [ ] Implement recipe caching

### Day 4-5: API & Frontend Integration
- [ ] Build smart-image endpoints
- [ ] Add smart image indicators to editor
- [ ] Build regenerate UI
- [ ] Test text-in-image quality
- [ ] Test 30+ designs with images
```

---

## 6. Phase 4: Polish & Brand Kits (Weeks 11-12)

### 6.1 Objectives
- Complete brand kit functionality
- Implement export feature
- Polish UI/UX
- Fix bugs and edge cases

### 6.2 Deliverables

#### Brand Kits
- [ ] Brand kit CRUD UI
- [ ] Logo upload
- [ ] Color picker component
- [ ] Font selector
- [ ] Default brand setting
- [ ] Apply brand to design

#### Export
- [ ] PNG export
- [ ] JPG export
- [ ] Resolution options (1x, 2x)
- [ ] Download flow
- [ ] Export history (optional)

#### UI Polish
- [ ] Loading states everywhere
- [ ] Error boundaries
- [ ] Empty states
- [ ] Tooltips
- [ ] Keyboard shortcuts
- [ ] Responsive design (desktop focus)

#### Testing & QA
- [ ] Unit test coverage > 70%
- [ ] E2E tests for critical flows
- [ ] Manual QA checklist
- [ ] Performance profiling

### 6.3 Technical Tasks

```markdown
## Week 11

### Day 1-2: Brand Kit UI
- [ ] Build BrandKit page
- [ ] Color picker component
- [ ] Font selector
- [ ] Logo upload

### Day 3-4: Export Feature
- [ ] Server-side rendering
- [ ] High-res image regeneration (2K/4K)
- [ ] Download endpoint
- [ ] Resolution handling
- [ ] Quality settings

### Day 5: Apply Brand
- [ ] Brand application logic
- [ ] UI button in editor
- [ ] Test with various designs

## Week 12

### Day 1-2: UI Polish (See `08_ui_design_guidelines.md`)
- [ ] Add loading states (skeletons, spinners)
- [ ] Add error boundaries with friendly messages
- [ ] Improve empty states with CTAs
- [ ] Add tooltips and keyboard shortcuts
- [ ] Ensure consistent spacing and typography

### Day 3-4: Testing
- [ ] Write unit tests
- [ ] Write E2E tests
- [ ] Manual QA pass
- [ ] Fix critical bugs

### Day 5: Performance
- [ ] Profile frontend
- [ ] Profile backend
- [ ] Optimize slow paths
- [ ] Document known issues
```

---

## 7. Phase 5: Launch Preparation (Week 13)

### 7.1 Objectives
- Final bug fixes
- Documentation
- Monitoring setup
- Soft launch

### 7.2 Deliverables

#### Documentation
- [ ] User guide
- [ ] API documentation (generated)
- [ ] Deployment guide
- [ ] Runbook for common issues

#### Monitoring
- [ ] Sentry error tracking
- [ ] PostHog analytics
- [ ] API metrics + cost logging
- [ ] Alert thresholds

#### Launch
- [ ] Production environment verified
- [ ] Data backup strategy
- [ ] Rollback plan documented
- [ ] Soft launch to beta users

### 7.3 Technical Tasks

```markdown
## Week 13

### Day 1-2: Final Fixes
- [ ] Fix remaining P0/P1 bugs
- [ ] Code review sweep
- [ ] Security review

### Day 3: Documentation
- [ ] Write user guide
- [ ] Generate API docs
- [ ] Update README

### Day 4: Monitoring
- [ ] Configure Sentry
- [ ] Set up PostHog
- [ ] Create dashboards
- [ ] Set up cost tracking (AI spend)

### Day 5: Launch
- [ ] Final deployment
- [ ] Smoke tests
- [ ] Invite beta users
- [ ] Monitor metrics
```

---

## 8. Post-Launch: V1.5 & V2 Features

### 8.1 V1.5 (Weeks 14-20)

| Feature | Effort | Impact |
|---------|--------|--------|
| AI Edit Designs | 2 weeks | High |
| Multiple Formats (Story, Facebook) | 1 week | Medium |
| Brand Intelligence (auto-extract) | 2 weeks | High |
| More Creative Concepts (10 total) | 1 week | Medium |
| More Blocks (18 total) | 1 week | Medium |

### 8.2 V2 (Months 2-4)

| Feature | Effort | Impact | Notes |
|---------|--------|--------|-------|
| **Persona Engine** | 3 weeks | High | Auto-extract target audience |
| **Competitor Intelligence** | 4 weeks | High | Meta Ad Library API |
| **Campaign Builder** | 3 weeks | High | Funnel stages (Awareness → Conversion) |
| Smart Resize | 2 weeks | Medium | Multi-format from single design |
| Bulk Generation | 2 weeks | Medium | 10+ variants at once |
| Video Storyboards | 4 weeks | High | Static frame sequences |

### 8.3 V3 (Months 5+)

| Feature | Effort | Impact | Notes |
|---------|--------|--------|-------|
| Real-time Collab | 6 weeks | Medium | Agency team features |
| Full Video Synthesis | 8 weeks | High | Animated ads |
| API Access | 3 weeks | Medium | B2B integrations |
| Multi-lingual Support | 2 weeks | Medium | Copy in multiple languages |
| Template Marketplace | 4 weeks | Medium | User-generated templates |

---

## 9. Risk Mitigation

### 9.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AI generates invalid JSON | Medium | High | Gemini 3 Pro structured output, validation pipeline |
| Smart images don't blend | Low | Medium | Holistic context, Nano Banana Pro quality |
| Text in images illegible | Low | High | Nano Banana Pro excels at text rendering |
| Editor performance issues | Low | High | Profiling, lazy loading |
| AI costs exceed budget | Medium | High | 1K resolution in editor, 2K+ on export |
| Nano Banana Pro rate limits | Medium | Medium | FLUX fallback for non-text images |

### 9.2 Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AI prompt iteration takes longer | High | Medium | Parallel tracks, time buffer |
| Fabric.js learning curve | Medium | Low | Early spike, documentation |
| Integration issues | Medium | Medium | Continuous integration |

---

## 10. Team & Resources

### 10.1 Recommended Team (Minimum)

| Role | Count | Focus |
|------|-------|-------|
| Full-stack Engineer | 1-2 | Frontend + Backend |
| AI/ML Engineer | 1 | Prompts, validation, tuning |
| Product/Design | 0.5 | UX, testing, feedback |

### 10.2 Resource Estimates

| Resource | Monthly Cost (Est.) | Notes |
|----------|-------------------|-------|
| Vercel Pro | $20 | Frontend hosting |
| Railway/Render | $25 | Backend hosting |
| Supabase Pro | $25 | Database + Auth + Storage |
| **Replicate (All AI)** | $200-600 | Single provider for all models |
| - Gemini 3 Pro | ~$50-150 | Layout/JSON generation |
| - Nano Banana Pro | ~$100-350 | Image generation |
| - FLUX (fallback) | ~$50-100 | Backgrounds, fast previews |
| Sentry | $26 | Error tracking |
| PostHog | Free tier | Analytics |
| **Total** | **$300-700/mo** |

**Cost per generation (3 variants):** ~$0.17-0.30

---

## 11. Success Metrics (V1 Launch)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to first design | < 2 minutes | Analytics |
| Generation success rate | > 95% | Logs |
| **Text legibility in images** | **> 98%** | Manual QA |
| Editor load time | < 3 seconds | RUM |
| User exports design | > 50% of sessions | Analytics |
| DAU (Day 30) | 100+ | Analytics |
| NPS | > 40 | Survey |
| Cost per generation | < $0.35 | AI spend logs |
