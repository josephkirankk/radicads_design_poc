"""
Canonical Layout Generator Service
Generates ad creative layouts in canonical JSON format using AI.
"""

from typing import Dict, Any, Optional
import asyncio
import json
from google import genai
from pydantic import ValidationError

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.canonical_design import CanonicalDesign
from app.prompts.ad_creative_system_prompt import build_generation_prompt

logger = get_logger(__name__)


class CanonicalLayoutGenerator:
    """
    Service for generating ad creative layouts in canonical JSON format.
    
    This service uses AI (Gemini) to generate structured design layouts
    following best practices for ad creative design.
    """
    
    def __init__(self):
        """Initialize the layout generator with Gemini client."""
        try:
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                raise ValueError("GEMINI_API_KEY not configured")
            
            self.client = genai.Client(api_key=api_key)
            self.model_name = settings.GEMINI_MODEL_NAME
            self.timeout = settings.GEMINI_TIMEOUT
            self.max_retries = settings.GEMINI_MAX_RETRIES
            
            logger.info(
                f"Initialized CanonicalLayoutGenerator with model={self.model_name}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            self.client = None
    
    async def generate_layout(
        self,
        user_prompt: str,
        brand_kit: Optional[Dict[str, Any]] = None,
        reference_images: Optional[list[str]] = None,
        preferences: Optional[Dict[str, Any]] = None
    ) -> CanonicalDesign:
        """
        Generate a canonical design layout from user input.
        
        Args:
            user_prompt: Natural language description of desired design
            brand_kit: Brand kit with colors, fonts, logo
            reference_images: List of reference image descriptions
            preferences: User preferences (style, tone, etc.)
        
        Returns:
            CanonicalDesign object with complete layout
        
        Raises:
            ValueError: If generation fails after all retries
        """
        if not self.client:
            raise ValueError("Client not initialized")
        
        logger.info(f"Generating layout for prompt: {user_prompt[:100]}...")
        
        # Build the complete prompt
        prompt = build_generation_prompt(
            user_prompt=user_prompt,
            brand_kit=brand_kit,
            reference_images=reference_images,
            preferences=preferences
        )
        
        # Retry loop with exponential backoff
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries}")
                
                # Generate with structured output
                response = await asyncio.wait_for(
                    self.client.aio.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config={
                            "response_mime_type": "application/json",
                            "response_json_schema": CanonicalDesign.model_json_schema()
                        }
                    ),
                    timeout=self.timeout
                )
                
                if not response.text:
                    raise ValueError("Empty response from API")
                
                # Validate with Pydantic
                canonical_design = CanonicalDesign.model_validate_json(response.text)
                
                # Post-process validation
                self._validate_design(canonical_design)
                
                logger.info(
                    f"Successfully generated layout with {len(canonical_design.layers)} layers"
                )
                return canonical_design
                
            except asyncio.TimeoutError:
                logger.error(f"Timeout after {self.timeout}s (attempt {attempt + 1})")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    
            except ValidationError as e:
                logger.error(f"Validation error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    
            except Exception as e:
                logger.error(f"Generation error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
        
        raise ValueError("Failed to generate layout after all retries")
    
    def _validate_design(self, design: CanonicalDesign) -> None:
        """
        Validate design constraints and fix issues.
        
        Args:
            design: CanonicalDesign to validate
        
        Raises:
            ValueError: If validation fails
        """
        # Check layer count
        if len(design.layers) > design.constraints.max_layers:
            raise ValueError(
                f"Too many layers: {len(design.layers)} > {design.constraints.max_layers}"
            )
        
        if len(design.layers) < 3:
            raise ValueError(f"Too few layers: {len(design.layers)} < 3")
        
        # Validate coordinates
        for layer in design.layers:
            if layer.position.x < 0 or layer.position.x > design.canvas.width:
                logger.warning(
                    f"Layer {layer.id} x position out of bounds, clamping"
                )
                layer.position.x = max(0, min(layer.position.x, design.canvas.width))
            
            if layer.position.y < 0 or layer.position.y > design.canvas.height:
                logger.warning(
                    f"Layer {layer.id} y position out of bounds, clamping"
                )
                layer.position.y = max(0, min(layer.position.y, design.canvas.height))
        
        # Validate text layers
        for layer in design.layers:
            if layer.type == "text":
                if layer.text.font_size < design.constraints.min_font_size:
                    logger.warning(
                        f"Layer {layer.id} font size too small, adjusting"
                    )
                    layer.text.font_size = design.constraints.min_font_size
        
        logger.info("Design validation passed")


# Singleton instance
canonical_layout_generator = CanonicalLayoutGenerator()

