"""
Simple Example: Generate Image with Nano Banana Pro

This is a minimal example showing how to generate an image using
Google's Nano Banana Pro model on Replicate.

Based on the recipe_headphones_01 from the design specification.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.replicate_service import get_replicate_service
from app.core.logging import get_logger

logger = get_logger(__name__)


def main():
    """Generate a product shot of premium headphones."""
    
    # The prompt from recipe_headphones_01
    prompt = (
        "Premium wireless over-ear headphones, sleek matte black finish with "
        "subtle gold accents, floating in a dark moody studio space, soft rim "
        "lighting highlighting curves, minimalistic high-tech vibe, 8k resolution, "
        "photorealistic. Style: premium dark aesthetic, promotional photography, "
        "color palette: #121212 with #D4AF37 accents"
    )
    
    logger.info("🚀 Generating image with Nano Banana Pro...")
    logger.info(f"📝 Prompt: {prompt}")
    
    try:
        # Initialize service
        service = get_replicate_service()
        
        # Run the model
        response = service.run_model(
            model="google/nano-banana-pro",
            input={
                "prompt": prompt,
                "aspect_ratio": "4:3",  # From recipe options
                "num_outputs": 1,
            },
            wait=True
        )
        
        # Check result
        if response.status == "succeeded" and response.output:
            logger.info("✅ Image generated successfully!")
            
            # Save the image
            output_file = Path("generated_images") / "headphones_product_shot.png"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Handle the output - can be FileOutput object, list, or URL string
            output_data = response.output
            
            # If it's a list, get the first item
            if isinstance(output_data, list):
                output_data = output_data[0]
            
            # Now handle the actual data
            if hasattr(output_data, 'read'):
                # FileOutput object
                with open(output_file, 'wb') as f:
                    f.write(output_data.read())
                logger.info(f"💾 Saved to: {output_file}")
            elif isinstance(output_data, str) and output_data.startswith('http'):
                # URL string
                import requests
                img_response = requests.get(output_data)
                with open(output_file, 'wb') as f:
                    f.write(img_response.content)
                logger.info(f"💾 Downloaded and saved to: {output_file}")
            
        else:
            logger.error(f"❌ Generation failed: {response.error}")
            
    except Exception as e:
        logger.exception(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
