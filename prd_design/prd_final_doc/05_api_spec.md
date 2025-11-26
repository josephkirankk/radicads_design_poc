# Radic Pro — API Specification

> **Version**: 2.0  
> **Base URL**: `https://api.radicpro.com/v1`  
> **Last Updated**: November 2025

---

## 1. Overview

### 1.1 Authentication

All API requests (except auth endpoints) require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

### 1.2 Response Format

**Success Response:**
```json
{
  "data": { ... },
  "meta": {
    "requestId": "req_abc123"
  }
}
```

**Error Response:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { ... },
    "retryable": false
  },
  "meta": {
    "requestId": "req_abc123"
  }
}
```

### 1.3 Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request / Validation Error |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Internal Server Error |

---

## 2. Authentication Endpoints

### 2.1 Sign Up

```
POST /auth/signup
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "fullName": "John Doe"
}
```

**Response (201):**
```json
{
  "data": {
    "user": {
      "id": "user_123",
      "email": "user@example.com",
      "fullName": "John Doe"
    },
    "session": {
      "accessToken": "eyJ...",
      "refreshToken": "eyJ...",
      "expiresAt": 1700000000
    }
  }
}
```

### 2.2 Login

```
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "data": {
    "user": {
      "id": "user_123",
      "email": "user@example.com",
      "fullName": "John Doe",
      "plan": "free"
    },
    "session": {
      "accessToken": "eyJ...",
      "refreshToken": "eyJ...",
      "expiresAt": 1700000000
    }
  }
}
```

### 2.3 Refresh Token

```
POST /auth/refresh
```

**Request Body:**
```json
{
  "refreshToken": "eyJ..."
}
```

**Response (200):**
```json
{
  "data": {
    "accessToken": "eyJ...",
    "refreshToken": "eyJ...",
    "expiresAt": 1700000000
  }
}
```

### 2.4 Get Current User

```
GET /auth/me
```

**Response (200):**
```json
{
  "data": {
    "id": "user_123",
    "email": "user@example.com",
    "fullName": "John Doe",
    "avatarUrl": "https://...",
    "plan": "pro",
    "createdAt": "2025-01-15T10:00:00Z"
  }
}
```

---

## 3. Designs Endpoints

### 3.1 List Designs

```
GET /designs
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `limit` | integer | 20 | Items per page (max 100) |
| `campaignId` | string | - | Filter by campaign |
| `archived` | boolean | false | Include archived |
| `sort` | string | "updatedAt" | Sort field |
| `order` | string | "desc" | Sort order (asc/desc) |

**Response (200):**
```json
{
  "data": {
    "designs": [
      {
        "id": "design_123",
        "title": "Diwali Sale Banner",
        "format": "instagram_post",
        "thumbnailUrl": "https://...",
        "isArchived": false,
        "createdAt": "2025-11-20T10:00:00Z",
        "updatedAt": "2025-11-25T15:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 45,
      "totalPages": 3
    }
  }
}
```

### 3.2 Get Design

```
GET /designs/{designId}
```

**Response (200):**
```json
{
  "data": {
    "id": "design_123",
    "ownerId": "user_456",
    "campaignId": "camp_789",
    "title": "Diwali Sale Banner",
    "format": "instagram_post",
    "thumbnailUrl": "https://...",
    "designJson": {
      "schemaVersion": "1.4",
      "id": "design_123",
      "meta": { ... },
      "canvas": { ... },
      "brand": { ... },
      "layers": [ ... ],
      "smartAssets": { ... }
    },
    "isArchived": false,
    "createdAt": "2025-11-20T10:00:00Z",
    "updatedAt": "2025-11-25T15:30:00Z"
  }
}
```

### 3.3 Create Design (Manual)

```
POST /designs
```

**Request Body:**
```json
{
  "title": "My New Design",
  "format": "instagram_post",
  "brandKitId": "brand_123",
  "campaignId": "camp_456"
}
```

**Response (201):**
```json
{
  "data": {
    "id": "design_new123",
    "title": "My New Design",
    "format": "instagram_post",
    "designJson": {
      "schemaVersion": "1.4",
      "canvas": {
        "width": 1080,
        "height": 1080,
        "background": { "type": "color", "color": "#FFFFFF" }
      },
      "layers": []
    },
    "createdAt": "2025-11-26T10:00:00Z",
    "updatedAt": "2025-11-26T10:00:00Z"
  }
}
```

### 3.4 Update Design

```
PATCH /designs/{designId}
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "designJson": {
    "schemaVersion": "1.4",
    ...
  }
}
```

**Response (200):**
```json
{
  "data": {
    "id": "design_123",
    "title": "Updated Title",
    "updatedAt": "2025-11-26T16:00:00Z"
  }
}
```

### 3.5 Delete Design

```
DELETE /designs/{designId}
```

**Response (204):** No content

### 3.6 Duplicate Design

```
POST /designs/{designId}/duplicate
```

**Request Body:**
```json
{
  "title": "Copy of Diwali Sale Banner"
}
```

**Response (201):**
```json
{
  "data": {
    "id": "design_newcopy123",
    "title": "Copy of Diwali Sale Banner",
    "createdAt": "2025-11-26T10:00:00Z"
  }
}
```

---

## 4. AI Endpoints

### 4.1 Generate Designs

```
POST /ai/generate-designs
```

**Request Body:**
```json
{
  "prompt": "Instagram ad for Diwali electronics sale, 40% OFF, premium dark theme, show headphones",
  "format": "instagram_post",
  "brandKitId": "brand_123",
  "creativeConcept": "offer_focus",
  "options": {
    "variants": 3,
    "imageResolution": "1k",
    "imageModel": "nano-banana-pro"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Natural language description |
| `format` | string | Yes | `instagram_post` (V1 only) |
| `brandKitId` | string | No | Brand kit to apply |
| `creativeConcept` | string | No | `product_highlight`, `offer_focus`, `problem_solution` |
| `options.variants` | number | No | Number of variants (default: 3) |
| `options.imageResolution` | string | No | `1k`, `2k`, `4k` (default: `1k`) |
| `options.imageModel` | string | No | `nano-banana-pro`, `flux-1.1-pro` |

**Response (200):**
```json
{
  "data": {
    "designs": [
      {
        "id": "design_gen_001",
        "title": "Diwali Electronics Sale - Variant 1",
        "thumbnailUrl": "https://...",
        "creativeConcept": "offer_focus",
        "designJson": {
          "schemaVersion": "2.0",
          "blocks": [...],
          "smartAssets": {...}
        },
        "smartImageStatus": {
          "total": 2,
          "completed": 2,
          "pending": 0
        }
      },
      {
        "id": "design_gen_002",
        "title": "Diwali Electronics Sale - Variant 2",
        "thumbnailUrl": "https://...",
        "creativeConcept": "offer_focus",
        "designJson": {...},
        "smartImageStatus": {
          "total": 2,
          "completed": 2,
          "pending": 0
        }
      }
    ],
    "generation": {
      "prompt": "Instagram ad for Diwali electronics sale...",
      "creativeConcept": "offer_focus",
      "briefSummary": {
        "headline": "Diwali Mega Sale",
        "subhead": "Premium Headphones at Unbeatable Prices",
        "offer": "40% OFF",
        "cta": "Shop Now"
      },
      "models": {
        "layout": "gemini-3-pro",
        "image": "nano-banana-pro"
      },
      "processingTime": 12500,
      "cost": {
        "layout": 0.04,
        "images": 0.12,
        "total": 0.16
      }
    }
  }
}
```

### 4.2 Edit Design with AI

```
POST /ai/edit-design
```

**Request Body:**
```json
{
  "designId": "design_123",
  "instruction": "Make it more minimal, remove the subheadline"
}
```

**Response (200):**
```json
{
  "data": {
    "patch": {
      "operations": [
        {
          "op": "remove_layer",
          "layerId": "layer_subheadline"
        },
        {
          "op": "update_layer",
          "layerId": "layer_headline",
          "changes": {
            "position": { "y": 200 }
          }
        }
      ]
    },
    "explanation": "Removed subheadline and repositioned headline for a cleaner look."
  }
}
```

### 4.3 Generate Smart Image

```
POST /ai/smart-image
```

**Request Body:**
```json
{
  "designId": "design_123",
  "layerId": "layer_product",
  "recipe": {
    "type": "product_shot",
    "prompt": "professional studio shot of wireless headphones",
    "options": {
      "aspectRatio": "1:1",
      "style": "photo",
      "quality": "high"
    }
  },
  "holisticContext": {
    "designPurpose": "Diwali electronics sale advertisement",
    "overallTheme": "premium dark with gold accents",
    "adjacentElements": [
      "Golden headline 'Diwali Mega Sale'",
      "Orange discount badge"
    ],
    "brandColors": ["#FFCC00", "#050816", "#FF4D00"],
    "compositionHints": "Product on right side, facing left"
  }
}
```

**Response (200):**
```json
{
  "data": {
    "recipeId": "recipe_abc123",
    "assetId": "asset_img_456",
    "assetUrl": "https://storage.../asset_img_456.png",
    "cached": false,
    "processingTime": 8500
  }
}
```

### 4.4 Regenerate Smart Image

```
POST /ai/smart-image/{recipeId}/regenerate
```

**Request Body:**
```json
{
  "promptOverride": "same headphones but with blue lighting instead"
}
```

**Response (200):**
```json
{
  "data": {
    "recipeId": "recipe_abc123",
    "assetId": "asset_img_789",
    "assetUrl": "https://storage.../asset_img_789.png"
  }
}
```

---

## 5. Brand Kits Endpoints

### 5.1 List Brand Kits

```
GET /brands
```

**Response (200):**
```json
{
  "data": {
    "brands": [
      {
        "id": "brand_123",
        "name": "VoltSound",
        "colors": {
          "primary": "#FFCC00",
          "secondary": "#050816",
          "accent": "#FF4D00",
          "text": "#FFFFFF"
        },
        "fonts": {
          "primary": { "family": "Inter", "weights": [400, 700, 800] },
          "secondary": { "family": "DM Sans", "weights": [400, 500] }
        },
        "logoUrl": "https://...",
        "isDefault": true,
        "createdAt": "2025-10-01T10:00:00Z"
      }
    ]
  }
}
```

### 5.2 Create Brand Kit

```
POST /brands
```

**Request Body:**
```json
{
  "name": "My Brand",
  "colors": {
    "primary": "#0066FF",
    "secondary": "#001133",
    "accent": "#00FF88",
    "text": "#FFFFFF"
  },
  "fonts": {
    "primary": { "family": "Poppins", "weights": [400, 600, 700] },
    "secondary": { "family": "Open Sans", "weights": [400, 500] }
  },
  "isDefault": false
}
```

**Response (201):**
```json
{
  "data": {
    "id": "brand_new456",
    "name": "My Brand",
    "colors": { ... },
    "fonts": { ... },
    "isDefault": false,
    "createdAt": "2025-11-26T10:00:00Z"
  }
}
```

### 5.3 Update Brand Kit

```
PATCH /brands/{brandId}
```

**Request Body:**
```json
{
  "name": "Updated Brand Name",
  "colors": {
    "primary": "#FF0066"
  }
}
```

**Response (200):**
```json
{
  "data": {
    "id": "brand_123",
    "name": "Updated Brand Name",
    "updatedAt": "2025-11-26T16:00:00Z"
  }
}
```

### 5.4 Upload Brand Logo

```
POST /brands/{brandId}/logo
```

**Request:** `multipart/form-data`
- `file`: Image file (PNG, JPG, SVG)

**Response (200):**
```json
{
  "data": {
    "logoAssetId": "asset_logo_789",
    "logoUrl": "https://..."
  }
}
```

### 5.5 Delete Brand Kit

```
DELETE /brands/{brandId}
```

**Response (204):** No content

---

## 6. Assets Endpoints

### 6.1 Upload Asset

```
POST /assets
```

**Request:** `multipart/form-data`
- `file`: Image file
- `type`: "logo" | "product" | "reference"

**Response (201):**
```json
{
  "data": {
    "id": "asset_789",
    "type": "product",
    "filename": "headphones.png",
    "mimeType": "image/png",
    "url": "https://...",
    "sizeBytes": 245000,
    "createdAt": "2025-11-26T10:00:00Z"
  }
}
```

### 6.2 List Assets

```
GET /assets
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Filter by type |
| `page` | integer | Page number |
| `limit` | integer | Items per page |

**Response (200):**
```json
{
  "data": {
    "assets": [
      {
        "id": "asset_789",
        "type": "product",
        "filename": "headphones.png",
        "url": "https://...",
        "createdAt": "2025-11-26T10:00:00Z"
      }
    ],
    "pagination": { ... }
  }
}
```

### 6.3 Delete Asset

```
DELETE /assets/{assetId}
```

**Response (204):** No content

---

## 7. Export Endpoints

### 7.1 Export Design

```
POST /export
```

**Request Body:**
```json
{
  "designId": "design_123",
  "format": "png",
  "resolution": "2x",
  "quality": 90
}
```

**Response (200):**
```json
{
  "data": {
    "exportId": "export_abc",
    "url": "https://...",
    "format": "png",
    "resolution": "2x",
    "sizeBytes": 1250000,
    "expiresAt": "2025-11-27T10:00:00Z"
  }
}
```

### 7.2 Export Multiple Formats (Future)

```
POST /export/batch
```

**Request Body:**
```json
{
  "designId": "design_123",
  "exports": [
    { "format": "png", "resolution": "1x" },
    { "format": "jpg", "resolution": "2x", "quality": 85 }
  ]
}
```

**Response (200):**
```json
{
  "data": {
    "exports": [
      { "exportId": "export_1", "format": "png", "url": "https://..." },
      { "exportId": "export_2", "format": "jpg", "url": "https://..." }
    ]
  }
}
```

---

## 8. Campaigns Endpoints (V1.5)

### 8.1 List Campaigns

```
GET /campaigns
```

**Response (200):**
```json
{
  "data": {
    "campaigns": [
      {
        "id": "camp_123",
        "name": "Diwali 2025",
        "brandKitId": "brand_456",
        "designCount": 5,
        "createdAt": "2025-11-01T10:00:00Z"
      }
    ]
  }
}
```

### 8.2 Create Campaign

```
POST /campaigns
```

**Request Body:**
```json
{
  "name": "Black Friday 2025",
  "brandKitId": "brand_456",
  "description": "All Black Friday promotional materials"
}
```

**Response (201):**
```json
{
  "data": {
    "id": "camp_new789",
    "name": "Black Friday 2025",
    "createdAt": "2025-11-26T10:00:00Z"
  }
}
```

---

## 9. Webhooks (Future)

### 9.1 Webhook Events

| Event | Description |
|-------|-------------|
| `design.created` | New design created |
| `design.exported` | Design exported |
| `smart_image.completed` | Smart image generation done |
| `smart_image.failed` | Smart image generation failed |

### 9.2 Webhook Payload

```json
{
  "event": "smart_image.completed",
  "timestamp": "2025-11-26T10:00:00Z",
  "data": {
    "recipeId": "recipe_123",
    "designId": "design_456",
    "assetId": "asset_789"
  }
}
```

---

## 10. Rate Limits

| Endpoint Category | Limit |
|------------------|-------|
| Authentication | 10/minute |
| Design CRUD | 100/minute |
| AI Generation | 10/hour |
| Smart Images | 50/hour |
| Export | 100/hour |
| Asset Upload | 50/hour |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1700000000
```

---

## 11. Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request body validation failed |
| `INVALID_JSON` | 400 | Malformed JSON in request |
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | No access to resource |
| `NOT_FOUND` | 404 | Resource not found |
| `DESIGN_NOT_FOUND` | 404 | Design does not exist |
| `BRAND_NOT_FOUND` | 404 | Brand kit does not exist |
| `RATE_LIMITED` | 429 | Too many requests |
| `GENERATION_FAILED` | 500 | AI generation error |
| `EXPORT_FAILED` | 500 | Export rendering error |
| `STORAGE_ERROR` | 500 | File storage error |

---

## 12. SDK Examples

### 12.1 TypeScript/JavaScript

```typescript
// Using fetch
async function generateDesigns(prompt: string, brandKitId?: string) {
  const response = await fetch('https://api.radicpro.com/v1/ai/generate-designs', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt,
      brandKitId,
      format: 'instagram_post',
      options: { variants: 3 }
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error.message);
  }
  
  return response.json();
}
```

### 12.2 Python

```python
import httpx

async def generate_designs(
    prompt: str,
    brand_kit_id: str | None = None,
    access_token: str
) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.radicpro.com/v1/ai/generate-designs",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "prompt": prompt,
                "brandKitId": brand_kit_id,
                "format": "instagram_post",
                "options": {"variants": 3}
            }
        )
        response.raise_for_status()
        return response.json()
```
