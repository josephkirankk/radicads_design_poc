# Nano Banana Pro Examples

This directory contains examples demonstrating how to use Google's **Nano Banana Pro** model on Replicate to generate images for ad creatives.

## About Nano Banana Pro

**Nano Banana Pro** is Google DeepMind's state-of-the-art image generation model built on Gemini 3 Pro. It excels at:

- 🎨 **Accurate text rendering** in multiple languages
- 📊 **Real-world knowledge** integration via Google Search
- 🎯 **Professional creative controls** (lighting, composition, camera angles)
- 🖼️ **High-resolution output** up to 4K
- 🌐 **Multiple aspect ratios** support

**Model ID**: `google/nano-banana-pro`

## Prerequisites

1. **Replicate API Token**: Get yours at [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)

2. **Set Environment Variable**:
   ```powershell
   # In .env file
   REPLICATE_API_TOKEN=r8_your_token_here
   ```

3. **Install Dependencies**:
   ```powershell
   cd backend
   .\.venv\Scripts\Activate.ps1
   uv pip install replicate requests
   ```

## Examples

### 1. Simple Example (`nano_banana_pro_simple.py`)

A minimal example that generates a product shot of headphones.

**Run it:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python examples/nano_banana_pro_simple.py
```

**What it does:**
- Uses a single prompt from the design recipe
- Generates one image with 4:3 aspect ratio
- Saves the output as `generated_images/headphones_product_shot.png`

### 2. Full Example (`nano_banana_pro_example.py`)

A comprehensive example that:
- Parses a complete design JSON specification
- Extracts smartImageRecipe by ID
- Builds an enhanced prompt with brand context
- Generates and saves the image

**Run it:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python examples/nano_banana_pro_example.py
```

**What it does:**
1. Loads the design spec for "Premium Headphones Holiday Sale"
2. Finds the recipe with ID `recipe_headphones_01`
3. Enhances the prompt with brand tone and color palette
4. Generates the image using Nano Banana Pro
5. Saves output as `generated_images/recipe_headphones_01_generated.png`

## Design Specification

Both examples use the same design specification for a Premium Headphones Holiday Sale ad:

- **Format**: Instagram Post (1080x1080)
- **Brand Colors**: Dark theme (#121212) with gold accents (#D4AF37)
- **Tone**: Premium Dark
- **Product**: Wireless over-ear headphones with matte black finish

## Recipe Details

```json
{
  "id": "recipe_headphones_01",
  "type": "product_shot",
  "model": "nano_banana_pro",
  "options": {
    "aspectRatio": "4:3",
    "resolution": "1024"
  },
  "prompt": "Premium wireless over-ear headphones, sleek matte black finish with subtle gold accents, floating in a dark moody studio space, soft rim lighting highlighting curves, minimalistic high-tech vibe, 8k resolution, photorealistic"
}
```

## Output

Generated images are saved to the `generated_images/` directory:

- `headphones_product_shot.png` - From simple example
- `recipe_headphones_01_generated.png` - From full example

## Nano Banana Pro Input Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `prompt` | string | Detailed description of the image to generate | "Premium wireless headphones..." |
| `aspect_ratio` | string | Image aspect ratio | "4:3", "16:9", "1:1" |
| `num_outputs` | integer | Number of images to generate | 1 |

## Tips for Best Results

1. **Be specific**: Include details about materials, lighting, composition
2. **Add style keywords**: "photorealistic", "studio lighting", "8k resolution"
3. **Use brand context**: Include color palette and aesthetic tone
4. **Specify quality**: "high-tech vibe", "professional photography"

## Troubleshooting

### Error: "REPLICATE_API_TOKEN not found"
- Make sure you've set the token in your `.env` file
- Verify the virtual environment is activated

### Error: Model not responding
- Check your Replicate account has credits
- Verify the model ID is correct: `google/nano-banana-pro`

### Images not saving
- Ensure the `generated_images/` directory exists or can be created
- Check file permissions in the output directory

## Cost

Nano Banana Pro costs approximately **$0.01-0.02 per image** depending on resolution and complexity. Check [Replicate's pricing](https://replicate.com/google/nano-banana-pro) for current rates.

## Related Files

- `../app/services/replicate_service.py` - Replicate API service layer
- `../app/schemas/replicate_models.py` - Pydantic models for requests/responses
- `../app/core/config.py` - Configuration including Replicate settings

## Learn More

- [Replicate Python Docs](https://replicate.com/docs/get-started/python)
- [Nano Banana Pro Model Page](https://replicate.com/google/nano-banana-pro)
- [Replicate API Reference](https://replicate.com/docs/reference/http)
