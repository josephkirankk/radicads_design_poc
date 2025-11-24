from typing import Dict, Any
import asyncio
import json
from google import genai
from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.ai_models import (
    DesignBrief,
    create_mock_design_brief,
    create_mock_fabric_design,
    get_fabric_canvas_dimensions,
)

logger = get_logger(__name__)


class LayoutAI:
    """AI-powered layout generation service using Google Gemini."""
    
    def __init__(self):
        """Initialize Gemini client with API key from settings."""
        try:
            # Debug: Log API key info
            api_key = settings.GEMINI_API_KEY
            logger.info(f"API Key (first 10 chars): {api_key[:10]}... (length: {len(api_key)})")

            self.client = genai.Client(api_key=api_key)
            self.model_name = settings.GEMINI_MODEL_NAME
            self.timeout = settings.GEMINI_TIMEOUT
            self.max_retries = settings.GEMINI_MAX_RETRIES
            logger.info(
                f"Initialized LayoutAI with model={self.model_name}, "
                f"timeout={self.timeout}s, max_retries={self.max_retries}"
            )
            logger.info(f"Client initialized successfully: {self.client is not None}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            logger.warning("Will fall back to mock data for all requests")
            self.client = None

    async def prompt_to_brief(self, prompt: str) -> Dict[str, Any]:
        """
        Convert user prompt to structured design brief using Gemini.

        Uses structured output with Pydantic schema for reliable results.
        Implements retry logic and fallback to mock data on failure.

        Args:
            prompt: User's design request

        Returns:
            Design brief as dict with headline, subheadline, colors, etc.
        """
        logger.info(f"=== prompt_to_brief START === Client is None: {self.client is None}")
        if not self.client:
            logger.warning("Client not initialized, using mock brief")
            return create_mock_design_brief()

        logger.info(f"Client is initialized, proceeding with API call. Client type: {type(self.client)}")
        
        # Enhance prompt with instructions for better results
        enhanced_prompt = f"""
You are a professional graphic designer. Analyze the following design request and create a structured design brief.

Design Request: {prompt}

Create a design brief that includes:
- A catchy, concise headline (max 6 words)
- An optional subheadline for supporting text
- Visual focus elements (what should stand out)
- Layout style (modern, minimal, bold, elegant, playful, etc.)
- Color scheme with primary, secondary, and accent colors (provide hex codes)
- Appropriate format (instagram_post, instagram_story, etc.)

Consider design principles like visual hierarchy, color theory, and target audience appeal.
"""
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"=== ATTEMPT {attempt + 1}/{self.max_retries} ===")
                logger.info(f"Using model: {self.model_name}")
                logger.info(f"About to call self.client.aio.models.generate_content...")
                
                # Use async generate_content with structured output
                response = await self.client.aio.models.generate_content(
                    model=self.model_name,
                    contents=enhanced_prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": DesignBrief.model_json_schema(),
                    }
                )
                
                logger.info(f"=== RECEIVED RESPONSE ===")
                logger.info(f"Response type: {type(response)}")
                logger.info(f"Response text (first 200 chars): {response.text[:200]}")
                
                # Validate response using Pydantic
                brief_obj = DesignBrief.model_validate_json(response.text)
                brief_dict = brief_obj.model_dump()
                
                logger.info(
                    f"Successfully generated brief: headline='{brief_dict.get('headline')}', "
                    f"style={brief_dict.get('layout_style')}"
                )
                return brief_dict
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in response (attempt {attempt + 1}): {str(e)}")
                logger.error(f"Response text: {response.text if 'response' in locals() else 'No response'}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    
            except Exception as e:
                logger.error(f"Error generating brief (attempt {attempt + 1}): {str(e)}")
                logger.error(f"Error type: {type(e).__name__}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        # Fallback to mock data after all retries exhausted
        logger.warning("All attempts failed, falling back to mock brief")
        return create_mock_design_brief()

    async def brief_to_design(
        self, 
        brief: Dict[str, Any], 
        brand_id: str = None
    ) -> Dict[str, Any]:
        """
        Generate Fabric.js compatible design JSON from brief.
        
        Uses Gemini to create layout with proper Fabric.js structure.
        Validates and post-processes output for correctness.
        
        Args:
            brief: Design brief from prompt_to_brief()
            brand_id: Optional brand ID for brand-specific customization
            
        Returns:
            Fabric.js compatible design JSON
        """
        if not self.client:
            logger.warning("Client not initialized, using mock design")
            return create_mock_fabric_design(brief)
        
        # Get canvas dimensions for the format
        dimensions = get_fabric_canvas_dimensions(brief.get("format", "instagram_post"))
        
        # Build detailed prompt for Fabric.js generation
        design_prompt = f"""
You are a professional graphic designer creating a design in Fabric.js format.

Design Brief:
- Headline: {brief.get('headline')}
- Subheadline: {brief.get('subheadline', 'N/A')}
- Layout Style: {brief.get('layout_style')}
- Visual Focus: {', '.join(brief.get('visual_focus', []))}
- Color Scheme:
  Primary: {brief.get('color_scheme', {}).get('primary', '#3b82f6')}
  Secondary: {brief.get('color_scheme', {}).get('secondary', '#1e293b')}
  Accent: {brief.get('color_scheme', {}).get('accent', '#64748b')}
- Canvas Size: {dimensions['width']}x{dimensions['height']} pixels

Create a Fabric.js JSON design that:
1. Has a clean, professional layout matching the style
2. Uses the specified color scheme
3. Includes the headline and subheadline as text objects
4. Adds 2-3 decorative shape objects (rectangles, circles) for visual interest
5. Follows proper Fabric.js object structure
6. Uses coordinates within the canvas bounds (0 to {dimensions['width']} width, 0 to {dimensions['height']} height)

Fabric.js Object Structure Requirements:
- Each text object needs: type, left, top, width, height, text, fontSize, fontFamily, fontWeight, fill, textAlign, originX, originY
- Each shape object needs: type, left, top, width/height or radius, fill, stroke, strokeWidth, opacity
- The root object needs: version (5.3.0), objects (array), background (hex color)

Make the design visually appealing and professionally laid out.
"""

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Generating design (attempt {attempt + 1}/{self.max_retries})")
                
                # Use JSON mode for free-form Fabric.js structure
                response = await self.client.aio.models.generate_content(
                    model=self.model_name,
                    contents=design_prompt,
                    config={
                        "response_mime_type": "application/json",
                    }
                )
                
                # Parse and validate the JSON
                design_json = json.loads(response.text)
                
                # Post-process: Ensure required fields
                if "version" not in design_json:
                    design_json["version"] = "5.3.0"
                if "objects" not in design_json:
                    design_json["objects"] = []
                if "background" not in design_json:
                    design_json["background"] = "#ffffff"
                
                # Validate coordinates are within bounds
                design_json = self._validate_and_fix_coordinates(
                    design_json, 
                    dimensions['width'], 
                    dimensions['height']
                )
                
                logger.info(
                    f"Successfully generated design with {len(design_json.get('objects', []))} objects"
                )
                return design_json
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in design response (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    
            except Exception as e:
                logger.error(f"Error generating design (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
        
        # Fallback to mock design after all retries exhausted
        logger.warning("All attempts failed, falling back to mock design")
        return create_mock_fabric_design(brief)

    def _validate_and_fix_coordinates(
        self, 
        design: Dict[str, Any],
        max_width: int,
        max_height: int
    ) -> Dict[str, Any]:
        """
        Validate and fix object coordinates to be within canvas bounds.
        
        Args:
            design: Fabric.js design JSON
            max_width: Maximum canvas width
            max_height: Maximum canvas height
            
        Returns:
            Design with fixed coordinates
        """
        for obj in design.get("objects", []):
            # Clamp left/top to canvas bounds
            if "left" in obj:
                obj["left"] = max(0, min(obj["left"], max_width))
            if "top" in obj:
                obj["top"] = max(0, min(obj["top"], max_height))
            
            # Ensure reasonable dimensions
            if "width" in obj and obj["width"] > max_width:
                obj["width"] = max_width * 0.8
            if "height" in obj and obj["height"] > max_height:
                obj["height"] = max_height * 0.8
            if "radius" in obj and obj["radius"] > min(max_width, max_height) / 2:
                obj["radius"] = min(max_width, max_height) / 4
        
        return design


# Singleton instance
layout_ai = LayoutAI()
