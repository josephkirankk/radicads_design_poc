from fastapi import APIRouter, Depends, HTTPException
from app.services.ai_image import image_ai
from app.schemas.design import SmartImageRecipe
from app.core.auth import get_current_user, get_user_id
from app.core.logging import get_logger
from app.core.exceptions import AIServiceError

router = APIRouter()
logger = get_logger(__name__)


@router.post("/generate-image")
async def generate_image(
    recipe: SmartImageRecipe,
    current_user=Depends(get_current_user)
):
    """
    Generate an image using AI based on a SmartImageRecipe.

    Args:
        recipe: SmartImageRecipe with prompt and generation parameters
        current_user: Authenticated user

    Returns:
        Generated asset ID
    """
    try:
        user_id = get_user_id(current_user)
        logger.info(f"Generating image for user {user_id} with recipe type: {recipe.type}")

        asset_id = await image_ai.generate_image(recipe, user_id)
        logger.info(f"Generated image {asset_id} for user {user_id}")

        return {"assetId": asset_id}

    except Exception as e:
        logger.error(f"Error generating image for user {user_id}: {str(e)}")
        raise AIServiceError(f"Failed to generate image: {str(e)}")
