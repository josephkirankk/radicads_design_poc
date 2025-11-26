"""
Usage Examples for Replicate Service

This file contains practical examples of how to use the ReplicateService
in your application. These examples demonstrate common use cases and patterns.

NOTE: This file is for reference only and should not be imported in production code.
"""

from app.services.replicate_service import get_replicate_service
from app.core.logging import get_logger

logger = get_logger(__name__)


# Example 1: Generate an image with SDXL
def example_generate_image():
    """
    Generate an image using Stable Diffusion XL.
    
    This is a synchronous operation that waits for the model to complete.
    """
    service = get_replicate_service()
    
    try:
        response = service.run_model(
            model="stability-ai/sdxl",
            input={
                "prompt": "A serene landscape with mountains and a lake at sunset",
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "num_inference_steps": 50,
            }
        )
        
        logger.info(f"Image generated successfully: {response.status}")
        
        # Handle FileOutput objects
        if response.output:
            for idx, image in enumerate(response.output):
                # Save the image
                with open(f"output_{idx}.png", "wb") as f:
                    f.write(image.read())
                logger.info(f"Saved image to output_{idx}.png")
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to generate image: {e}")
        raise


# Example 2: Run a model asynchronously
def example_async_generation():
    """
    Start a model prediction asynchronously and check status later.
    
    This is useful for long-running models where you don't want to block.
    """
    service = get_replicate_service()
    
    try:
        # Start the prediction
        response = service.run_model_async(
            model="stability-ai/sdxl",
            input={
                "prompt": "A futuristic city with flying cars",
                "num_outputs": 1,
            }
        )
        
        logger.info(f"Prediction started: {response.prediction_id}")
        
        # Later, check the status
        status = service.get_prediction_status(response.prediction_id)
        logger.info(f"Current status: {status.status}")
        
        # Wait for completion
        if status.status not in ["succeeded", "failed", "canceled"]:
            result = service.wait_for_prediction(response.prediction_id)
            logger.info(f"Prediction completed: {result.status}")
            return result
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to run async prediction: {e}")
        raise


# Example 3: Generate text with LLaMA
def example_generate_text():
    """
    Generate text using Meta's LLaMA model.
    
    This demonstrates streaming text output.
    """
    service = get_replicate_service()
    
    try:
        response = service.run_model(
            model="meta/meta-llama-3-70b-instruct",
            input={
                "prompt": "Write a short poem about artificial intelligence",
                "max_tokens": 200,
                "temperature": 0.7,
            }
        )
        
        logger.info("Text generated successfully")
        
        # The output is typically a list of strings for text models
        if response.output:
            full_text = "".join(response.output)
            logger.info(f"Generated text: {full_text}")
            return full_text
        
        return None
        
    except Exception as e:
        logger.error(f"Failed to generate text: {e}")
        raise


# Example 4: Get model information
def example_get_model_info():
    """
    Retrieve information about a model including its input schema.
    
    This is useful for validating inputs before running a model.
    """
    service = get_replicate_service()
    
    try:
        info = service.get_model_info("stability-ai/sdxl")
        
        logger.info(f"Model: {info.owner}/{info.name}")
        logger.info(f"Description: {info.description}")
        logger.info(f"Latest version: {info.version}")
        
        if info.input_schema:
            required_inputs = info.input_schema.get("required", [])
            logger.info(f"Required inputs: {required_inputs}")
        
        return info
        
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise


# Example 5: Cancel a running prediction
def example_cancel_prediction():
    """
    Cancel a long-running prediction.
    
    This is useful if you need to stop a prediction that's taking too long.
    """
    service = get_replicate_service()
    
    try:
        # Start a prediction
        response = service.run_model_async(
            model="stability-ai/sdxl",
            input={"prompt": "A complex scene"}
        )
        
        prediction_id = response.prediction_id
        logger.info(f"Started prediction: {prediction_id}")
        
        # Cancel it
        success = service.cancel_prediction(prediction_id)
        
        if success:
            logger.info(f"Successfully canceled prediction {prediction_id}")
        
        return success
        
    except Exception as e:
        logger.error(f"Failed to cancel prediction: {e}")
        raise

