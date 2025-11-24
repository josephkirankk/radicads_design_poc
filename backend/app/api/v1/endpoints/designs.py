from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.supabase import get_supabase
from supabase import Client
from app.schemas.design import DesignJSON, DesignCreate, DesignUpdate
from app.core.auth import get_current_user, get_user_id
from app.core.logging import get_logger
from app.core.exceptions import NotFoundError, DatabaseError, AuthorizationError

router = APIRouter()
logger = get_logger(__name__)

@router.get("/", response_model=List[dict])
async def get_designs(
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get all designs for the current user."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Fetching designs for user {user_id}")

        res = supabase.table("designs").select("*").eq("owner_id", user_id).order("created_at", desc=True).execute()
        logger.info(f"Found {len(res.data)} designs for user {user_id}")
        return res.data
    except Exception as e:
        logger.error(f"Error fetching designs: {str(e)}")
        raise DatabaseError(f"Failed to fetch designs: {str(e)}")

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_design(
    design: DesignCreate,
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Create a new design."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Creating design for user {user_id}")

        design_data = design.dict()
        design_data["owner_id"] = user_id

        res = supabase.table("designs").insert(design_data).execute()

        if not res.data:
            raise DatabaseError("Failed to create design")

        logger.info(f"Created design {res.data[0]['id']} for user {user_id}")
        return res.data[0]
    except Exception as e:
        logger.error(f"Error creating design: {str(e)}")
        raise DatabaseError(f"Failed to create design: {str(e)}")

@router.get("/{id}", response_model=dict)
async def get_design(
    id: str,
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Get a specific design by ID."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Fetching design {id} for user {user_id}")

        res = supabase.table("designs").select("*").eq("id", id).eq("owner_id", user_id).execute()

        if not res.data:
            logger.warning(f"Design {id} not found for user {user_id}")
            raise NotFoundError(f"Design {id} not found")

        return res.data[0]
    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error fetching design {id}: {str(e)}")
        raise DatabaseError(f"Failed to fetch design: {str(e)}")

@router.patch("/{id}", response_model=dict)
async def update_design(
    id: str,
    design: DesignUpdate,
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Update a design."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Updating design {id} for user {user_id}")

        # First check if design exists and belongs to user
        existing = supabase.table("designs").select("id").eq("id", id).eq("owner_id", user_id).execute()
        if not existing.data:
            raise NotFoundError(f"Design {id} not found")

        # Update only provided fields
        update_data = design.dict(exclude_unset=True)
        res = supabase.table("designs").update(update_data).eq("id", id).execute()

        if not res.data:
            raise DatabaseError("Failed to update design")

        logger.info(f"Updated design {id} for user {user_id}")
        return res.data[0]
    except (NotFoundError, DatabaseError):
        raise
    except Exception as e:
        logger.error(f"Error updating design {id}: {str(e)}")
        raise DatabaseError(f"Failed to update design: {str(e)}")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_design(
    id: str,
    current_user=Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    """Delete a design."""
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Deleting design {id} for user {user_id}")

        # Check if design exists and belongs to user
        existing = supabase.table("designs").select("id").eq("id", id).eq("owner_id", user_id).execute()
        if not existing.data:
            raise NotFoundError(f"Design {id} not found")

        supabase.table("designs").delete().eq("id", id).execute()
        logger.info(f"Deleted design {id} for user {user_id}")

    except NotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error deleting design {id}: {str(e)}")
        raise DatabaseError(f"Failed to delete design: {str(e)}")
