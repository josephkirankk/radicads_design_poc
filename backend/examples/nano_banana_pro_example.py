"""
Example: Generate Product Image using Nano Banana Pro on Replicate

This example demonstrates how to:
1. Parse a design JSON specification
2. Extract the smartImageRecipe for a specific ID
3. Generate an image using Google's Nano Banana Pro model on Replicate
4. Save the generated image

The example uses the design specification for a Premium Headphones Holiday Sale ad.
"""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Add parent directory to path to import our service
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.replicate_service import get_replicate_service
from app.core.logging import get_logger

logger = get_logger(__name__)


# Design specification JSON
DESIGN_SPEC = {
    "id": "design_holiday_headphones_01",
    "schemaVersion": "1.3",
    "ownerId": "user_42",
    "campaignId": "camp_1",
    "title": "Premium Headphones Holiday Sale",
    "format": "instagram_post",
    "size": {
        "width": 1080,
        "height": 1080,
        "unit": "px"
    },
    "goal": "promote_discount",
    "tone": "premium_dark",
    "brand": {
        "brandId": "brand_1",
        "primaryColor": "#121212",
        "secondaryColor": "#FFFFFF",
        "accentColor": "#D4AF37",
        "fontPrimary": "Montserrat",
        "fontSecondary": "Lato",
        "logoAssetId": "asset_logo_1"
    },
    "smartImageRecipes": [
        {
            "id": "recipe_headphones_01",
            "ownerId": "user_42",
            "type": "product_shot",
            "prompt": "Premium wireless over-ear headphones, sleek matte black finish with subtle gold accents, floating in a dark moody studio space, soft rim lighting highlighting curves, minimalistic high-tech vibe, 8k resolution, photorealistic",
            "referenceAssetIds": [],
            "model": "nano_banana_pro",
            "options": {
                "aspectRatio": "4:3",
                "resolution": "1024"
            },
            "lastGeneratedAssetId": "asset_prod_hp_01",
            "createdAt": "2023-10-27T10:00:00Z"
        }
    ],
    "meta": {
        "createdAt": "2023-10-27T10:00:00Z",
        "updatedAt": "2023-10-27T10:00:00Z",
        "source": "ai_v1"
    }
}


def extract_recipe_by_id(design_spec: Dict[str, Any], recipe_id: str) -> Optional[Dict[str, Any]]:
    """
    Extract a smartImageRecipe from the design spec by its ID.
    
    Args:
        design_spec: Complete design specification dictionary
        recipe_id: ID of the recipe to extract (e.g., "recipe_headphones_01")
        
    Returns:
        Recipe dictionary if found, None otherwise
    """
    recipes = design_spec.get("smartImageRecipes", [])
    
    for recipe in recipes:
        if recipe.get("id") == recipe_id:
            logger.info(f"Found recipe: {recipe_id}")
            return recipe
    
    logger.warning(f"Recipe not found: {recipe_id}")
    return None


def build_enhanced_prompt(recipe: Dict[str, Any], design_spec: Dict[str, Any]) -> str:
    """
    Build an enhanced prompt by combining the recipe prompt with context from the design.
    
    Args:
        recipe: SmartImageRecipe dictionary
        design_spec: Complete design specification
        
    Returns:
        Enhanced prompt string
    """
    # Get base prompt from recipe
    base_prompt = recipe.get("prompt", "")
    
    # Extract context from design
    tone = design_spec.get("tone", "")
    goal = design_spec.get("goal", "")
    brand = design_spec.get("brand", {})
    
    # Build context hints
    context_parts = []
    
    if tone:
        tone_hint = tone.replace("_", " ")
        context_parts.append(f"{tone_hint} aesthetic")
    
    if goal == "promote_discount":
        context_parts.append("promotional photography")
    
    # Add brand color hints
    primary_color = brand.get("primaryColor", "")
    accent_color = brand.get("accentColor", "")
    
    if primary_color and accent_color:
        context_parts.append(f"color palette: {primary_color} with {accent_color} accents")
    
    # Combine into enhanced prompt
    if context_parts:
        context_str = ", ".join(context_parts)
        enhanced_prompt = f"{base_prompt}. Style: {context_str}"
    else:
        enhanced_prompt = base_prompt
    
    logger.info(f"Enhanced prompt: {enhanced_prompt}")
    return enhanced_prompt


def map_aspect_ratio(aspect_ratio_str: str) -> str:
    """
    Map aspect ratio string to Replicate format.
    
    Args:
        aspect_ratio_str: Aspect ratio like "4:3", "16:9", "1:1"
        
    Returns:
        Aspect ratio string compatible with the model
    """
    # Nano Banana Pro supports various aspect ratios
    # Common formats: "1:1", "16:9", "9:16", "4:3", "3:4", etc.
    return aspect_ratio_str


def generate_image_from_recipe(
    recipe_id: str,
    design_spec: Dict[str, Any],
    output_dir: str = "generated_images"
) -> Optional[str]:
    """
    Generate an image using Nano Banana Pro based on a recipe ID.
    
    Args:
        recipe_id: ID of the recipe to use (e.g., "recipe_headphones_01")
        design_spec: Complete design specification dictionary
        output_dir: Directory to save generated images
        
    Returns:
        Path to the saved image file, or None if generation failed
    """
    # Step 1: Extract the recipe
    recipe = extract_recipe_by_id(design_spec, recipe_id)
    if not recipe:
        logger.error(f"Cannot generate image: recipe '{recipe_id}' not found")
        return None
    
    # Step 2: Build enhanced prompt with context
    prompt = build_enhanced_prompt(recipe, design_spec)
    
    # Step 3: Extract options
    options = recipe.get("options", {})
    aspect_ratio = map_aspect_ratio(options.get("aspectRatio", "1:1"))
    
    # Step 4: Prepare input for Nano Banana Pro
    model_input = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "num_outputs": 1,
    }
    
    logger.info(f"Generating image with Nano Banana Pro...")
    logger.info(f"Input: {json.dumps(model_input, indent=2)}")
    
    try:
        # Step 5: Run the model
        service = get_replicate_service()
        
        response = service.run_model(
            model="google/nano-banana-pro",
            input=model_input,
            wait=True
        )
        
        if response.status != "succeeded":
            logger.error(f"Generation failed with status: {response.status}")
            if response.error:
                logger.error(f"Error: {response.error}")
            return None
        
        # Step 6: Save the output
        if not response.output:
            logger.error("No output generated")
            return None
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save the image
        output_file = output_path / f"{recipe_id}_generated.png"
        
        # Handle different output types - can be FileOutput, list, or URL string
        output_data = response.output
        
        # If it's a list, get the first item
        if isinstance(output_data, list) and len(output_data) > 0:
            output_data = output_data[0]
        
        # Now handle the actual data
        if hasattr(output_data, 'read'):
            # FileOutput object
            with open(output_file, 'wb') as f:
                f.write(output_data.read())
        elif isinstance(output_data, str) and output_data.startswith('http'):
            # URL string
            import requests
            img_response = requests.get(output_data)
            with open(output_file, 'wb') as f:
                f.write(img_response.content)
        else:
            logger.error(f"Unexpected output type: {type(output_data)}")
            return None
        
        logger.info(f"✅ Image saved successfully: {output_file}")
        return str(output_file)
        
    except Exception as e:
        logger.exception(f"Failed to generate image: {str(e)}")
        return None


def main():
    """
    Main function to demonstrate image generation from a design spec.
    """
    logger.info("=" * 80)
    logger.info("Nano Banana Pro Image Generation Example")
    logger.info("=" * 80)
    
    # Recipe ID we want to generate
    recipe_id = "recipe_headphones_01"
    
    logger.info(f"\n📋 Design: {DESIGN_SPEC['title']}")
    logger.info(f"🎯 Target Recipe: {recipe_id}")
    logger.info(f"🎨 Brand Tone: {DESIGN_SPEC['tone']}")
    logger.info(f"📐 Format: {DESIGN_SPEC['format']} ({DESIGN_SPEC['size']['width']}x{DESIGN_SPEC['size']['height']})")
    
    # Generate the image
    logger.info("\n🚀 Starting image generation...")
    output_path = generate_image_from_recipe(
        recipe_id=recipe_id,
        design_spec=DESIGN_SPEC,
        output_dir="generated_images"
    )
    
    if output_path:
        logger.info("\n" + "=" * 80)
        logger.info("✅ SUCCESS!")
        logger.info(f"Generated image saved to: {output_path}")
        logger.info("=" * 80)
    else:
        logger.error("\n" + "=" * 80)
        logger.error("❌ FAILED!")
        logger.error("Image generation did not complete successfully")
        logger.error("=" * 80)


if __name__ == "__main__":
    main()
