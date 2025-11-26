# Technical Architecture & Final Tech Stack

## 1. Overview
The system is designed for speed, scalability, cost efficiency, and ease of maintenance. We use Supabase for backend infrastructure and FastAPI for business logic. Fabric.js powers the design editor.

---

## 2. Frontend Stack
### 2.1 Framework
- **SvelteKit** or **React** (either supported)
- Highly responsive, ideal for visual applications

### 2.2 Canvas Editor
- **Fabric.js**
  - Rich object manipulation (scale, rotate, move)
  - Perfect for custom JSON‑based rendering
  - Extensible and configurable

### 2.3 UI Toolkit
- TailwindCSS
- Shadcn

---

## 3. Backend Stack
### 3.1 Framework
- **FastAPI**  
  - High-performance async Python API  
  - Pydantic V2 models for strict schema enforcement  

### 3.2 Validation Layer
- Auto‑repair engine  
- Image/text rule enforcement  
- Shape vector extraction rules  

### 3.3 Image Generation
- **Replicate Platform Models - Nano Banana or Nano Banana Pro or any suitable Image generation model **  
- SmartImageRecipes ensure re-renderability  

---

## 4. Database & Storage
### 4.1 Database
- **Supabase Postgres**
  - Schemas for Users, Projects, Assets, Recipes

### 4.2 Storage
- Supabase Storage for images and static assets

---

## 5. AI Components
### 5.1 Layout Generation
- GPT‑5.1 with structured prompting
- Semantic guarantees via system instructions

### 5.2 Image Generation
- **Replicate Platform Models - Nano Banana or Nano Banana Pro or any suitable Image generation model **    
- SmartImageRecipe → deterministic image regeneration  

---

## 8. Security
- JWT‑based auth  
- Supabase Row‑Level Security  
- Signed URLs for image delivery

---

## 9. DevOps
- GitHub Actions CI/CD  
- Automated snapshot tests for layout outputs  
- Visual regression suite  

---

## 10. Testing
### 10.1 Unit Tests
- Validation rules  
- Text‑vs‑image enforcement  
- Recipe hashing  

### 10.2 Integration
- Layout → Validation → Editor rendering flow  

### 10.3 Visual Regression
- Baseline snapshots for all canonical prompts  

---

# END TECH STACK
