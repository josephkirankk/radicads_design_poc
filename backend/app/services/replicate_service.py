"""
Replicate API Service Layer

Production-ready service for interacting with Replicate's API.
Follows KISS principle with clear separation of concerns.

Features:
- Simple, modular design with minimal abstractions
- Comprehensive error handling with specific exception types
- Automatic retry logic with exponential backoff for transient failures
- Type-safe interfaces using Pydantic models
- Structured logging for debugging and monitoring
- Support for synchronous operations (async can be added later)
"""

import time
from typing import Any, Dict, List, Optional, Generator

import replicate
from replicate.exceptions import ModelError, ReplicateError, ReplicateException

from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import AIServiceError
from app.schemas.replicate_models import (
    ReplicateRunResponse,
    ReplicatePredictionStatus,
    ReplicateModelInfo,
)

logger = get_logger(__name__)


class ReplicateService:
    """
    Service class for interacting with Replicate API.
    
    This service provides a clean interface for running AI models on Replicate,
    with built-in error handling, retry logic, and logging.
    
    Example:
        ```python
        service = ReplicateService()
        
        # Run a model
        response = service.run_model(
            model="stability-ai/sdxl",
            input={"prompt": "astronaut riding a horse"}
        )
        
        # Check prediction status
        status = service.get_prediction_status(response.prediction_id)
        ```
    """
    
    def __init__(self):
        """
        Initialize the Replicate service.
        
        Raises:
            AIServiceError: If REPLICATE_API_TOKEN is not configured
        """
        self.api_token = settings.REPLICATE_API_TOKEN
        self.timeout = settings.REPLICATE_TIMEOUT
        self.max_retries = settings.REPLICATE_MAX_RETRIES
        self.poll_interval = settings.REPLICATE_POLL_INTERVAL
        
        if not self.api_token:
            error_msg = (
                "REPLICATE_API_TOKEN not found. "
                "Please set it in .env file or environment variables. "
                "Get your token at: https://replicate.com/account/api-tokens"
            )
            logger.error(error_msg)
            raise AIServiceError(error_msg)

        # Configure Replicate client with API token
        # The replicate module uses a default client, so we just need to set the token
        # via environment or by using the client methods directly
        self.client = replicate.Client(api_token=self.api_token)

        logger.info(
            f"Initialized ReplicateService with "
            f"timeout={self.timeout}s, max_retries={self.max_retries}"
        )
    
    def run_model(
        self,
        model: str,
        input: Dict[str, Any],
        wait: bool = True,
        webhook: Optional[str] = None,
        webhook_events_filter: Optional[List[str]] = None,
    ) -> ReplicateRunResponse:
        """
        Run a model on Replicate.
        
        Args:
            model: Model identifier (e.g., "stability-ai/sdxl" or version string)
            input: Dictionary of input parameters for the model
            wait: Whether to wait for prediction completion (default: True)
            webhook: Optional webhook URL for prediction updates
            webhook_events_filter: Optional list of events to trigger webhook
            
        Returns:
            ReplicateRunResponse with prediction details and output
            
        Raises:
            AIServiceError: If the model execution fails
            
        Example:
            ```python
            response = service.run_model(
                model="stability-ai/sdxl",
                input={
                    "prompt": "a beautiful sunset",
                    "num_outputs": 1
                }
            )
            print(f"Generated image: {response.output}")
            ```
        """
        logger.info(
            f"Running model '{model}' with input keys: {list(input.keys())}"
        )
        
        attempt = 0
        last_error = None
        
        while attempt < self.max_retries:
            try:
                # Run the model with retry logic using the client instance
                output = self.client.run(
                    model,
                    input=input,
                )
                
                logger.info(f"Model '{model}' completed successfully")
                
                # Return response
                return ReplicateRunResponse(
                    prediction_id="sync_run",  # Sync runs don't have prediction IDs
                    status="succeeded",
                    output=output,
                    error=None,
                    logs=None,
                    metrics=None,
                )
                
            except ModelError as e:
                # Model execution failed
                logger.error(
                    f"Model execution failed for '{model}': {e.prediction.error}"
                )
                logger.debug(f"Prediction ID: {e.prediction.id}")
                if e.prediction.logs:
                    logger.debug(f"Model logs:\n{e.prediction.logs}")
                
                raise AIServiceError(
                    f"Model execution failed: {e.prediction.error}"
                )

            except ReplicateError as e:
                # API error (RFC 7807 Problem Details)
                logger.error(
                    f"Replicate API error for '{model}': "
                    f"[{e.status}] {e.title} - {e.detail}"
                )

                # Check if this is a retryable error
                if e.status in [429, 503, 504]:
                    attempt += 1
                    last_error = e

                    if attempt < self.max_retries:
                        # Exponential backoff
                        wait_time = min(2 ** attempt, 30)
                        logger.warning(
                            f"Retryable error (attempt {attempt}/{self.max_retries}). "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                        continue

                # Non-retryable error or max retries exceeded
                error_dict = e.to_dict()
                logger.error(f"API error details: {error_dict}")
                raise AIServiceError(
                    f"Replicate API error: {e.title} - {e.detail}"
                )

            except ReplicateException as e:
                # Base exception for all Replicate errors
                logger.error(f"Replicate error for '{model}': {str(e)}")
                raise AIServiceError(f"Replicate error: {str(e)}")

            except Exception as e:
                # Unexpected error
                logger.exception(
                    f"Unexpected error running model '{model}': {type(e).__name__}"
                )
                raise AIServiceError(
                    f"Unexpected error running model: {str(e)}"
                )

        # Max retries exceeded
        if last_error:
            logger.error(
                f"Max retries ({self.max_retries}) exceeded for model '{model}'"
            )
            raise AIServiceError(
                f"Max retries exceeded. Last error: {str(last_error)}"
            )
        
        # Should never reach here, but satisfy type checker
        raise AIServiceError(f"Unexpected state: no output and no error for model '{model}'")

    def run_model_async(
        self,
        model: str,
        input: Dict[str, Any],
        webhook: Optional[str] = None,
        webhook_events_filter: Optional[List[str]] = None,
    ) -> ReplicateRunResponse:
        """
        Run a model asynchronously (non-blocking).

        This creates a prediction and returns immediately without waiting
        for completion. Use get_prediction_status() to check progress.

        Args:
            model: Model identifier
            input: Dictionary of input parameters
            webhook: Optional webhook URL for updates
            webhook_events_filter: Optional list of events to trigger webhook

        Returns:
            ReplicateRunResponse with prediction ID and initial status

        Example:
            ```python
            # Start prediction
            response = service.run_model_async(
                model="stability-ai/sdxl",
                input={"prompt": "sunset"}
            )

            # Check status later
            status = service.get_prediction_status(response.prediction_id)
            ```
        """
        logger.info(
            f"Starting async prediction for model '{model}' "
            f"with input keys: {list(input.keys())}"
        )

        try:
            # Create prediction without waiting using the client instance
            # Build kwargs to only include non-None values
            create_kwargs: Dict[str, Any] = {
                "model": model,
                "input": input,
            }
            if webhook is not None:
                create_kwargs["webhook"] = webhook
            if webhook_events_filter is not None:
                create_kwargs["webhook_events_filter"] = webhook_events_filter

            prediction = self.client.predictions.create(**create_kwargs)

            logger.info(
                f"Created prediction {prediction.id} for model '{model}' "
                f"with status: {prediction.status}"
            )

            return ReplicateRunResponse(
                prediction_id=prediction.id,
                status=prediction.status,
                output=None,
                error=None,
                logs=None,
                metrics=None,
            )

        except ReplicateError as e:
            logger.error(
                f"Failed to create prediction for '{model}': "
                f"[{e.status}] {e.title} - {e.detail}"
            )
            raise AIServiceError(f"Failed to create prediction: {e.detail}")

        except Exception as e:
            logger.exception(
                f"Unexpected error creating prediction for '{model}'"
            )
            raise AIServiceError(
                f"Unexpected error creating prediction: {str(e)}"
            )

    def get_prediction_status(
        self,
        prediction_id: str
    ) -> ReplicatePredictionStatus:
        """
        Get the status of a prediction.

        Args:
            prediction_id: Unique prediction identifier

        Returns:
            ReplicatePredictionStatus with current status and timestamps

        Example:
            ```python
            status = service.get_prediction_status("abc123")
            print(f"Status: {status.status}")
            ```
        """
        logger.debug(f"Checking status for prediction {prediction_id}")

        try:
            prediction = self.client.predictions.get(prediction_id)

            return ReplicatePredictionStatus(
                prediction_id=prediction.id,
                status=prediction.status,
                created_at=str(prediction.created_at) if prediction.created_at else None,
                started_at=str(prediction.started_at) if prediction.started_at else None,
                completed_at=str(prediction.completed_at) if prediction.completed_at else None,
            )

        except ReplicateError as e:
            logger.error(
                f"Failed to get prediction {prediction_id}: "
                f"[{e.status}] {e.detail}"
            )
            raise AIServiceError(f"Failed to get prediction: {e.detail}")

        except Exception as e:
            logger.exception(
                f"Unexpected error getting prediction {prediction_id}"
            )
            raise AIServiceError(
                f"Unexpected error getting prediction: {str(e)}"
            )

    def wait_for_prediction(
        self,
        prediction_id: str,
        timeout: Optional[int] = None,
    ) -> ReplicateRunResponse:
        """
        Wait for a prediction to complete.

        Polls the prediction status until it reaches a terminal state
        (succeeded, failed, or canceled).

        Args:
            prediction_id: Unique prediction identifier
            timeout: Maximum time to wait in seconds (default: service timeout)

        Returns:
            ReplicateRunResponse with final output or error

        Raises:
            AIServiceError: If prediction fails or times out

        Example:
            ```python
            # Start async prediction
            response = service.run_model_async(...)

            # Wait for completion
            result = service.wait_for_prediction(response.prediction_id)
            print(f"Output: {result.output}")
            ```
        """
        timeout = timeout or self.timeout
        start_time = time.time()

        logger.info(
            f"Waiting for prediction {prediction_id} "
            f"(timeout: {timeout}s)"
        )

        try:
            prediction = self.client.predictions.get(prediction_id)

            while prediction.status not in ["succeeded", "failed", "canceled"]:
                # Check timeout
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    logger.error(
                        f"Prediction {prediction_id} timed out after {elapsed:.1f}s"
                    )
                    raise AIServiceError(
                        f"Prediction timed out after {timeout}s"
                    )

                # Wait before polling again
                time.sleep(self.poll_interval)

                # Reload prediction status
                prediction.reload()
                logger.debug(
                    f"Prediction {prediction_id} status: {prediction.status}"
                )

            # Check final status
            if prediction.status == "succeeded":
                logger.info(
                    f"Prediction {prediction_id} succeeded "
                    f"in {time.time() - start_time:.1f}s"
                )

                return ReplicateRunResponse(
                    prediction_id=prediction.id,
                    status=prediction.status,
                    output=prediction.output,
                    error=None,
                    logs=prediction.logs,
                    metrics=prediction.metrics if hasattr(prediction, 'metrics') else None,
                )

            elif prediction.status == "failed":
                logger.error(
                    f"Prediction {prediction_id} failed: {prediction.error}"
                )
                if prediction.logs:
                    logger.debug(f"Prediction logs:\n{prediction.logs}")

                raise AIServiceError(
                    f"Prediction failed: {prediction.error}"
                )

            else:  # canceled
                logger.warning(f"Prediction {prediction_id} was canceled")
                raise AIServiceError("Prediction was canceled")

        except AIServiceError:
            # Re-raise our own exceptions
            raise

        except ReplicateError as e:
            logger.error(
                f"API error while waiting for prediction {prediction_id}: "
                f"[{e.status}] {e.detail}"
            )
            raise AIServiceError(f"API error: {e.detail}")

        except Exception as e:
            logger.exception(
                f"Unexpected error waiting for prediction {prediction_id}"
            )
            raise AIServiceError(
                f"Unexpected error waiting for prediction: {str(e)}"
            )

    def cancel_prediction(self, prediction_id: str) -> bool:
        """
        Cancel a running prediction.

        Args:
            prediction_id: Unique prediction identifier

        Returns:
            True if cancellation was successful

        Example:
            ```python
            service.cancel_prediction("abc123")
            ```
        """
        logger.info(f"Canceling prediction {prediction_id}")

        try:
            prediction = self.client.predictions.get(prediction_id)
            prediction.cancel()

            logger.info(f"Successfully canceled prediction {prediction_id}")
            return True

        except ReplicateError as e:
            logger.error(
                f"Failed to cancel prediction {prediction_id}: "
                f"[{e.status}] {e.detail}"
            )
            raise AIServiceError(f"Failed to cancel prediction: {e.detail}")

        except Exception as e:
            logger.exception(
                f"Unexpected error canceling prediction {prediction_id}"
            )
            raise AIServiceError(
                f"Unexpected error canceling prediction: {str(e)}"
            )

    def get_model_info(self, model: str) -> ReplicateModelInfo:
        """
        Get information about a model.

        Args:
            model: Model identifier (e.g., "stability-ai/sdxl")

        Returns:
            ReplicateModelInfo with model details

        Example:
            ```python
            info = service.get_model_info("stability-ai/sdxl")
            print(f"Description: {info.description}")
            ```
        """
        logger.debug(f"Getting info for model '{model}'")

        try:
            # Parse model identifier
            parts = model.split("/")
            if len(parts) != 2:
                raise ValueError(
                    f"Invalid model identifier: {model}. "
                    "Expected format: 'owner/name'"
                )

            owner, name = parts

            # Get model using the client instance
            model_obj = self.client.models.get(f"{owner}/{name}")
            latest_version = model_obj.latest_version

            # Extract schema if available
            input_schema = None
            output_schema = None

            if latest_version and hasattr(latest_version, 'openapi_schema'):
                schema = latest_version.openapi_schema
                if schema and "components" in schema:
                    schemas = schema["components"].get("schemas", {})
                    input_schema = schemas.get("Input")
                    output_schema = schemas.get("Output")

            return ReplicateModelInfo(
                owner=owner,
                name=name,
                version=latest_version.id if latest_version else None,
                description=model_obj.description,
                input_schema=input_schema,
                output_schema=output_schema,
            )

        except ReplicateError as e:
            logger.error(
                f"Failed to get model info for '{model}': "
                f"[{e.status}] {e.detail}"
            )
            raise AIServiceError(f"Failed to get model info: {e.detail}")

        except Exception as e:
            logger.exception(f"Unexpected error getting model info for '{model}'")
            raise AIServiceError(
                f"Unexpected error getting model info: {str(e)}"
            )

    def stream_model(
        self,
        model: str,
        input: Dict[str, Any],
    ) -> Generator[Any, None, None]:
        """
        Stream output from a model that supports streaming.

        This is useful for text generation models that support token-by-token
        streaming. The output is yielded as it becomes available.

        Args:
            model: Model identifier (e.g., "meta/meta-llama-3-70b-instruct")
            input: Dictionary of input parameters for the model

        Yields:
            Individual output chunks as they become available

        Raises:
            AIServiceError: If the model execution fails

        Example:
            ```python
            # Stream text generation
            for chunk in service.stream_model(
                model="meta/meta-llama-3-70b-instruct",
                input={"prompt": "Write a story"}
            ):
                print(chunk, end="", flush=True)
            ```
        """
        logger.info(
            f"Streaming model '{model}' with input keys: {list(input.keys())}"
        )

        try:
            # Use the stream method for models that support it
            for event in self.client.stream(model, input=input):
                yield event

            logger.info(f"Stream completed for model '{model}'")

        except ModelError as e:
            logger.error(
                f"Model execution failed during streaming for '{model}': "
                f"{e.prediction.error}"
            )
            raise AIServiceError(
                f"Model streaming failed: {e.prediction.error}"
            )

        except ReplicateError as e:
            logger.error(
                f"Replicate API error during streaming for '{model}': "
                f"[{e.status}] {e.title} - {e.detail}"
            )
            raise AIServiceError(
                f"Replicate API error: {e.title} - {e.detail}"
            )

        except ReplicateException as e:
            logger.error(f"Replicate error during streaming for '{model}': {str(e)}")
            raise AIServiceError(f"Replicate streaming error: {str(e)}")

        except Exception as e:
            logger.exception(
                f"Unexpected error streaming model '{model}': {type(e).__name__}"
            )
            raise AIServiceError(
                f"Unexpected error streaming model: {str(e)}"
            )



def get_replicate_service() -> ReplicateService:
    """
    Get or create a ReplicateService instance.

    This function provides lazy initialization to avoid errors
    if the API token is not configured at import time.

    Returns:
        ReplicateService instance

    Example:
        ```python
        from app.services.replicate_service import get_replicate_service

        service = get_replicate_service()
        response = service.run_model(...)
        ```
    """
    return ReplicateService()
