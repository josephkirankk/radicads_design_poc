from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.supabase import get_supabase
from supabase import Client
from app.schemas.brand import BrandKit, BrandKitCreate, BrandKitUpdate
from app.core.auth import get_current_user, get_user_id
from app.core.logging import get_logger
from app.core.exceptions import NotFoundError, DatabaseError

router = APIRouter()
logger = get_logger(__name__)

@router.get("/", response_model=List[dict])
async def get_brands(
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get all brand kits for the current user."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Fetching brands for user {user_id}")

        res = supabase.table("brands").select("*").eq("owner_id", user_id).order("created_at", desc=True).execute()
        logger.info(f"Found {len(res.data)} brands for user {user_id}")
        return res.data
    except Exception as e:
        logger.error(f"Error fetching brands: {str(e)}")
        raise DatabaseError(f"Failed to fetch brands: {str(e)}")

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand: BrandKitCreate,
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Create a new brand kit."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Creating brand for user {user_id}")

        brand_data = brand.dict()
        brand_data["owner_id"] = user_id

        res = supabase.table("brands").insert(brand_data).execute()

        if not res.data:
            raise DatabaseError("Failed to create brand")

        logger.info(f"Created brand {res.data[0]['id']} for user {user_id}")
        return res.data[0]
    except Exception as e:
        logger.error(f"Error creating brand: {str(e)}")
        raise DatabaseError(f"Failed to create brand: {str(e)}")

@router.get("/{id}", response_model=dict)
async def get_brand(
    id: str,
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get a specific brand kit by ID."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Fetching brand {id} for user {user_id}")

        res = supabase.table("brands").select("*").eq("id", id).eq("owner_id", user_id).execute()

        if not res.data:
            logger.warning(f"Brand {id} not found for user {user_id}")
            raise NotFoundError(f"Brand {id} not found")

        return res.data[0]
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error fetching brand {id}: {str(e)}")
        raise DatabaseError(f"Failed to fetch brand: {str(e)}")

@router.patch("/{id}", response_model=dict)
async def update_brand(
    id: str,
    brand: BrandKitUpdate,
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Update a brand kit."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Updating brand {id} for user {user_id}")

        # Check if brand exists and belongs to user
        existing = supabase.table("brands").select("id").eq("id", id).eq("owner_id", user_id).execute()
        if not existing.data:
            raise NotFoundError(f"Brand {id} not found")

        # Update only provided fields
        update_data = brand.dict(exclude_unset=True)
        res = supabase.table("brands").update(update_data).eq("id", id).execute()

        if not res.data:
            raise DatabaseError("Failed to update brand")

        logger.info(f"Updated brand {id} for user {user_id}")
        return res.data[0]
    except (NotFoundError, DatabaseError):
        raise
    except Exception as e:
        logger.error(f"Error updating brand {id}: {str(e)}")
        raise DatabaseError(f"Failed to update brand: {str(e)}")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    id: str,
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Delete a brand kit."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Deleting brand {id} for user {user_id}")

        # Check if brand exists and belongs to user
        existing = supabase.table("brands").select("id").eq("id", id).eq("owner_id", user_id).execute()
        if not existing.data:
            raise NotFoundError(f"Brand {id} not found")

        supabase.table("brands").delete().eq("id", id).execute()
        logger.info(f"Deleted brand {id} for user {user_id}")

    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting brand {id}: {str(e)}")
        raise DatabaseError(f"Failed to delete brand: {str(e)}")
