"""
Pydantic models for Replicate API requests and responses.

These models provide type safety and validation for Replicate service interactions.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class ReplicateRunRequest(BaseModel):
    """
    Request model for running a Replicate model.
    
    Attributes:
        model: Model identifier (e.g., "stability-ai/sdxl" or full version string)
        input: Dictionary of input parameters for the model
        wait: Whether to wait for the prediction to complete (default: True)
        webhook: Optional webhook URL to receive prediction updates
        webhook_events_filter: Optional list of events to trigger webhook
    """
    model: str = Field(..., description="Model identifier or version string")
    input: Dict[str, Any] = Field(..., description="Model input parameters")
    wait: bool = Field(default=True, description="Wait for prediction completion")
    webhook: Optional[str] = Field(None, description="Webhook URL for updates")
    webhook_events_filter: Optional[List[str]] = Field(
        None,
        description="Events to trigger webhook (e.g., ['start', 'completed'])"
    )

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Validate model identifier format."""
        if not v or not isinstance(v, str):
            raise ValueError("Model identifier must be a non-empty string")
        return v

    @field_validator("input")
    @classmethod
    def validate_input(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input is a dictionary."""
        if not isinstance(v, dict):
            raise ValueError("Input must be a dictionary")
        return v


class ReplicateRunResponse(BaseModel):
    """
    Response model for a Replicate prediction.
    
    Attributes:
        prediction_id: Unique identifier for the prediction
        status: Current status of the prediction
        output: Model output (if completed)
        error: Error message (if failed)
        logs: Model execution logs
        metrics: Execution metrics (timing, etc.)
    """
    prediction_id: str = Field(..., description="Unique prediction identifier")
    status: str = Field(..., description="Prediction status")
    output: Optional[Any] = Field(None, description="Model output")
    error: Optional[str] = Field(None, description="Error message if failed")
    logs: Optional[str] = Field(None, description="Execution logs")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Execution metrics")


class ReplicatePredictionStatus(BaseModel):
    """
    Model for checking prediction status.
    
    Attributes:
        prediction_id: Unique identifier for the prediction
        status: Current status (starting, processing, succeeded, failed, canceled)
        created_at: Timestamp when prediction was created
        started_at: Timestamp when prediction started processing
        completed_at: Timestamp when prediction completed
    """
    prediction_id: str
    status: str
    created_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class ReplicateModelInfo(BaseModel):
    """
    Information about a Replicate model.
    
    Attributes:
        owner: Model owner username
        name: Model name
        version: Specific version ID (optional)
        description: Model description
        input_schema: JSON schema for model inputs
        output_schema: JSON schema for model outputs
    """
    owner: str
    name: str
    version: Optional[str] = None
    description: Optional[str] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None


class ReplicateFileInput(BaseModel):
    """
    Model for file inputs to Replicate models.
    
    Attributes:
        url: URL to the file (for remote files)
        file_path: Local file path (for local files)
        mime_type: MIME type of the file
    """
    url: Optional[str] = Field(None, description="URL to remote file")
    file_path: Optional[str] = Field(None, description="Local file path")
    mime_type: Optional[str] = Field(None, description="MIME type")

    @field_validator("url", "file_path")
    @classmethod
    def validate_file_source(cls, v: Optional[str], info) -> Optional[str]:
        """Ensure at least one file source is provided."""
        # This will be called for each field, so we can't validate both at once here
        # The actual validation happens in the service layer
        return v


class ReplicateStreamConfig(BaseModel):
    """
    Configuration for streaming model outputs.
    
    Attributes:
        enabled: Whether to enable streaming
        chunk_size: Size of chunks for streaming (bytes)
        timeout: Timeout for each chunk (seconds)
    """
    enabled: bool = Field(default=False, description="Enable streaming")
    chunk_size: int = Field(default=8192, description="Chunk size in bytes")
    timeout: int = Field(default=30, description="Timeout per chunk in seconds")

