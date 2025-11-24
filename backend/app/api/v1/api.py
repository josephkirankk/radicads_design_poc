from fastapi import APIRouter
from app.api.v1.endpoints import auth, designs, brands, ai_layout, ai_image

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(designs.router, prefix="/designs", tags=["designs"])
api_router.include_router(brands.router, prefix="/brands", tags=["brands"])
api_router.include_router(ai_layout.router, prefix="/ai/layout", tags=["ai-layout"])
api_router.include_router(ai_image.router, prefix="/ai/image", tags=["ai-image"])
