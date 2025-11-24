from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.ai_layout import layout_ai
from app.core.auth import get_current_user_optional, get_user_id
from app.core.logging import get_logger
from app.core.exceptions import AIServiceError, DatabaseError
from app.db.supabase import get_supabase
from supabase import Client

router = APIRouter()
logger = get_logger(__name__)


class GenerateRequest(BaseModel):
    prompt: str
    brand_id: str = None


@router.post("/generate", response_model=dict)
async def generate_design(
    request: GenerateRequest,
    current_user=Depends(get_current_user_optional),
    supabase: Client = Depends(get_supabase)
):
    """
    Generate a design from a text prompt.

    For authenticated users: Saves design to database and returns the saved design.
    For anonymous users: Returns the generated design JSON without saving.

    Args:
        request: Generation request with prompt and optional brand_id
        current_user: Optional authenticated user
        supabase: Supabase client

    Returns:
        Generated design JSON (with database ID if authenticated)
    """
    user_id = "anonymous"
    try:
        user_id = get_user_id(current_user) if current_user else "anonymous"
        is_authenticated = current_user is not None
        prompt_preview = request.prompt[:50]
        logger.info(
            f"Generating design for user {user_id} (authenticated: {is_authenticated}) "
            f"with prompt: {prompt_preview}..."
        )

        # 1. Generate Brief from prompt
        brief = await layout_ai.prompt_to_brief(request.prompt)
        logger.info(f"Generated brief for user {user_id}")

        # 2. Generate Design JSON from brief
        # TODO: Pass brand info if brand_id provided
        design = await layout_ai.brief_to_design(
            brief, brand_id=request.brand_id
        )
        logger.info(f"Generated design for user {user_id}")

        # 3. Save design to database ONLY if user is authenticated
        if is_authenticated:
            design_data = {
                "title": "AI Generated Design",
                "format": "instagram_post",
                "owner_id": user_id,
                "brand_id": request.brand_id,
                "design_json": design,
            }

            res = supabase.table("designs").insert(design_data).execute()

            if not res.data:
                raise DatabaseError("Failed to save generated design to database")

            saved_design = res.data[0]
            logger.info(f"Saved design {saved_design['id']} to database for user {user_id}")

            # Return the saved design with the database ID
            return saved_design
        else:
            # For anonymous users, return design in same format as DB record
            # but with a mock ID (not saved to database)
            logger.info(f"Returning generated design for anonymous user (not saved to database)")
            return {
                "id": "mock_design_1",
                "title": "AI Generated Design",
                "format": "instagram_post",
                "owner_id": "anonymous",
                "brand_id": request.brand_id,
                "design_json": design,
            }

    except DatabaseError:
        raise
    except Exception as e:
        logger.error(f"Error generating design for user {user_id}: {str(e)}")
        raise AIServiceError(f"Failed to generate design: {str(e)}")
