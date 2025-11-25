"""
Image Generation Prompt Templates
Optimized for various image generation models (DALL-E, Midjourney, Stable Diffusion, Flux, etc.)
Following 2025 best practices for high-quality, consistent results.
"""

from typing import Dict, Any, List
from enum import Enum


class ImageGenerationModel(str, Enum):
    """Supported image generation models."""
    DALLE_3 = "dall-e-3"
    MIDJOURNEY = "midjourney"
    STABLE_DIFFUSION = "stable-diffusion"
    FLUX = "flux"
    NANO_BANANA = "nano-banana"


class PromptTemplate:
    """Base class for prompt templates."""
    
    @staticmethod
    def build_base_prompt(
        subject: str,
        style: str,
        composition: str,
        lighting: str,
        quality_modifiers: List[str],
        negative_prompt: List[str] | None = None
    ) -> Dict[str, str]:
        """
        Build a structured image generation prompt.
        
        Format: [Subject] + [Style] + [Composition] + [Lighting] + [Quality]
        
        Args:
            subject: Main subject of the image
            style: Visual style (photorealistic, 3D, illustration, etc.)
            composition: Composition details (centered, rule of thirds, etc.)
            lighting: Lighting description (studio, natural, dramatic, etc.)
            quality_modifiers: Quality keywords (high detail, 8K, etc.)
            negative_prompt: Things to avoid
        
        Returns:
            Dict with 'prompt' and 'negative_prompt'
        """
        prompt_parts = [
            subject,
            style,
            composition,
            lighting,
            ", ".join(quality_modifiers)
        ]
        
        prompt = ", ".join(filter(None, prompt_parts))
        
        return {
            "prompt": prompt,
            "negative_prompt": ", ".join(negative_prompt) if negative_prompt else ""
        }


class ProductImagePrompts:
    """Prompts for product images."""
    
    @staticmethod
    def ecommerce_product(
        product_name: str,
        product_category: str,
        style: str = "photorealistic",
        background: str = "transparent"
    ) -> Dict[str, str]:
        """
        Generate prompt for e-commerce product image.
        
        Best for: Product showcases, catalog images, hero shots
        """
        subject = f"{product_name}, {product_category} product"
        
        style_desc = {
            "photorealistic": "professional product photography, photorealistic",
            "3d": "3D rendered product, clean CGI, octane render",
            "minimalist": "minimalist product shot, clean aesthetic",
            "lifestyle": "lifestyle product photography, in-use context"
        }.get(style, style)
        
        composition = "centered composition, isolated product, front-facing view"
        lighting = "studio lighting, soft shadows, even illumination"
        quality = [
            "high resolution",
            "sharp focus",
            "professional quality",
            "commercial photography",
            "8K detail"
        ]
        
        negative = [
            "blurry",
            "low quality",
            "distorted",
            "watermark",
            "text",
            "background clutter"
        ]
        
        base = PromptTemplate.build_base_prompt(
            subject, style_desc, composition, lighting, quality, negative
        )
        
        # Add transparent background requirement
        base["prompt"] += ", transparent background, PNG with alpha channel, isolated on white"
        
        return base
    
    @staticmethod
    def product_with_context(
        product_name: str,
        context: str,
        mood: str = "aspirational"
    ) -> Dict[str, str]:
        """
        Generate prompt for product in lifestyle context.
        
        Best for: Lifestyle ads, contextual product shots
        """
        subject = f"{product_name} in {context}"
        style = "lifestyle photography, natural setting, authentic feel"
        composition = f"product prominently featured, {mood} mood"
        lighting = "natural lighting, warm tones, inviting atmosphere"
        quality = [
            "high quality",
            "professional photography",
            "sharp details",
            "commercial grade"
        ]
        
        negative = [
            "artificial",
            "staged",
            "low quality",
            "blurry",
            "distorted"
        ]
        
        base = PromptTemplate.build_base_prompt(
            subject, style, composition, lighting, quality, negative
        )
        
        base["prompt"] += ", transparent background, cutout style, PNG format"
        
        return base


class PersonImagePrompts:
    """Prompts for person/model images."""
    
    @staticmethod
    def model_portrait(
        demographics: str,
        expression: str,
        style: str = "professional"
    ) -> Dict[str, str]:
        """
        Generate prompt for person/model portrait.
        
        Best for: Testimonials, lifestyle ads, brand ambassadors
        """
        subject = f"{demographics} person, {expression} expression"
        
        style_desc = {
            "professional": "professional portrait photography, studio quality",
            "casual": "casual lifestyle photography, natural candid style",
            "editorial": "editorial fashion photography, high-end magazine style"
        }.get(style, style)
        
        composition = "portrait orientation, centered subject, upper body visible"
        lighting = "soft portrait lighting, flattering illumination, professional setup"
        quality = [
            "high resolution",
            "sharp focus on face",
            "professional photography",
            "detailed features",
            "8K quality"
        ]
        
        negative = [
            "blurry",
            "distorted features",
            "unnatural",
            "low quality",
            "artificial",
            "watermark"
        ]
        
        base = PromptTemplate.build_base_prompt(
            subject, style_desc, composition, lighting, quality, negative
        )
        
        base["prompt"] += ", transparent background, isolated subject, PNG with alpha"

        return base


class BackgroundImagePrompts:
    """Prompts for background images and textures."""

    @staticmethod
    def abstract_background(
        color_scheme: List[str],
        mood: str,
        complexity: str = "medium"
    ) -> Dict[str, str]:
        """
        Generate prompt for abstract background.

        Best for: Canvas backgrounds, decorative layers
        """
        colors = " and ".join(color_scheme)
        subject = f"abstract background with {colors} colors"
        style = f"{mood} mood, modern design, {complexity} complexity"
        composition = "full canvas coverage, balanced composition, no focal point"
        lighting = "even lighting, soft gradients, smooth transitions"
        quality = [
            "high resolution",
            "seamless",
            "professional design",
            "clean aesthetic"
        ]

        negative = [
            "busy",
            "cluttered",
            "distracting",
            "low quality",
            "pixelated"
        ]

        return PromptTemplate.build_base_prompt(
            subject, style, composition, lighting, quality, negative
        )

    @staticmethod
    def textured_background(
        texture_type: str,
        color: str
    ) -> Dict[str, str]:
        """
        Generate prompt for textured background.

        Best for: Adding depth and interest to designs
        """
        subject = f"{texture_type} texture background in {color}"
        style = "subtle texture, professional design, modern aesthetic"
        composition = "seamless pattern, full coverage, uniform distribution"
        lighting = "soft lighting, minimal shadows, even tone"
        quality = [
            "high resolution",
            "tileable",
            "professional quality",
            "clean design"
        ]

        negative = [
            "harsh",
            "distracting",
            "low quality",
            "obvious repeats"
        ]

        return PromptTemplate.build_base_prompt(
            subject, style, composition, lighting, quality, negative
        )


class IconGraphicPrompts:
    """Prompts for icons and graphic elements."""

    @staticmethod
    def icon(
        icon_subject: str,
        style: str = "modern",
        color_scheme: str = "monochrome"
    ) -> Dict[str, str]:
        """
        Generate prompt for icon/graphic element.

        Best for: Decorative elements, infographics, visual accents
        """
        subject = f"{icon_subject} icon"

        style_desc = {
            "modern": "modern flat design, clean lines, minimalist",
            "3d": "3D icon, isometric style, depth and dimension",
            "outline": "outline style icon, line art, simple",
            "filled": "filled icon, solid shapes, bold"
        }.get(style, style)

        composition = f"centered, {color_scheme} color scheme, simple composition"
        lighting = "flat lighting, no shadows" if style == "modern" else "soft lighting"
        quality = [
            "vector quality",
            "crisp edges",
            "professional design",
            "scalable"
        ]

        negative = [
            "blurry",
            "pixelated",
            "complex",
            "cluttered",
            "low quality"
        ]

        base = PromptTemplate.build_base_prompt(
            subject, style_desc, composition, lighting, quality, negative
        )

        base["prompt"] += ", transparent background, PNG format, isolated icon"

        return base


class ComplexTextPrompts:
    """Prompts for text with complex effects (rendered as images)."""

    @staticmethod
    def text_with_effects(
        text_content: str,
        effect_type: str,
        color_scheme: List[str]
    ) -> Dict[str, str]:
        """
        Generate prompt for text with complex visual effects.

        Best for: Headlines with gradients, 3D text, text with textures
        """
        colors = " and ".join(color_scheme)

        effect_descriptions = {
            "gradient": f"gradient text effect with {colors} colors, smooth blend",
            "3d": f"3D text effect, depth and dimension, {colors} colors",
            "metallic": f"metallic text effect, {colors} metallic finish, reflective",
            "neon": f"neon glow effect, {colors} neon colors, glowing",
            "outlined": f"bold outline effect, {colors} colors, strong borders"
        }

        subject = f'text saying "{text_content}"'
        style = effect_descriptions.get(effect_type, f"{effect_type} text effect")
        composition = "centered text, clear legibility, professional typography"
        lighting = "dramatic lighting, emphasis on effect" if effect_type in ["3d", "metallic"] else "even lighting"
        quality = [
            "high resolution",
            "crisp text",
            "professional design",
            "clear and readable"
        ]

        negative = [
            "blurry text",
            "illegible",
            "distorted letters",
            "low quality",
            "pixelated"
        ]

        base = PromptTemplate.build_base_prompt(
            subject, style, composition, lighting, quality, negative
        )

        base["prompt"] += ", transparent background, PNG format, isolated text"

        return base


def optimize_prompt_for_model(
    base_prompt: Dict[str, str],
    model: ImageGenerationModel,
    aspect_ratio: str = "1:1"
) -> Dict[str, Any]:
    """
    Optimize prompt for specific image generation model.

    Different models have different prompt styles and parameters.

    Args:
        base_prompt: Base prompt dict with 'prompt' and 'negative_prompt'
        model: Target image generation model
        aspect_ratio: Desired aspect ratio (e.g., "1:1", "16:9", "9:16")

    Returns:
        Optimized prompt with model-specific parameters
    """

    if model == ImageGenerationModel.DALLE_3:
        # DALL-E 3: Natural language, detailed descriptions
        return {
            "prompt": base_prompt["prompt"],
            "model": "dall-e-3",
            "size": _aspect_ratio_to_dalle_size(aspect_ratio),
            "quality": "hd",
            "style": "natural"
        }

    elif model == ImageGenerationModel.MIDJOURNEY:
        # Midjourney: Comma-separated keywords, parameters at end
        prompt = base_prompt["prompt"]
        if base_prompt.get("negative_prompt"):
            prompt += f" --no {base_prompt['negative_prompt']}"
        prompt += f" --ar {aspect_ratio} --quality 2 --stylize 100"
        return {"prompt": prompt}

    elif model == ImageGenerationModel.STABLE_DIFFUSION:
        # Stable Diffusion: Detailed prompt + negative prompt
        return {
            "prompt": base_prompt["prompt"],
            "negative_prompt": base_prompt.get("negative_prompt", ""),
            "width": _aspect_ratio_to_dimensions(aspect_ratio)[0],
            "height": _aspect_ratio_to_dimensions(aspect_ratio)[1],
            "steps": 30,
            "cfg_scale": 7.5,
            "sampler": "DPM++ 2M Karras"
        }

    elif model == ImageGenerationModel.FLUX:
        # Flux: Natural language, high quality
        return {
            "prompt": base_prompt["prompt"],
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "safety_tolerance": 2
        }

    elif model == ImageGenerationModel.NANO_BANANA:
        # Nano Banana: Custom model, flexible parameters
        return {
            "prompt": base_prompt["prompt"],
            "negative_prompt": base_prompt.get("negative_prompt", ""),
            "aspect_ratio": aspect_ratio,
            "quality": "high",
            "transparent_background": True
        }

    else:
        # Default: return base prompt
        return base_prompt


def _aspect_ratio_to_dalle_size(aspect_ratio: str) -> str:
    """Convert aspect ratio to DALL-E 3 size parameter."""
    mapping = {
        "1:1": "1024x1024",
        "16:9": "1792x1024",
        "9:16": "1024x1792"
    }
    return mapping.get(aspect_ratio, "1024x1024")


def _aspect_ratio_to_dimensions(aspect_ratio: str) -> tuple[int, int]:
    """Convert aspect ratio to pixel dimensions."""
    mapping = {
        "1:1": (1024, 1024),
        "16:9": (1024, 576),
        "9:16": (576, 1024),
        "4:3": (1024, 768),
        "3:4": (768, 1024)
    }
    return mapping.get(aspect_ratio, (1024, 1024))

