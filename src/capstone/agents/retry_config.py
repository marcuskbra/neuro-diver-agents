"""Shared retry configuration for all agents following ADK best practices."""

from google.genai.types import GenerateContentConfig, HttpOptions, HttpRetryOptions


def get_retry_config() -> GenerateContentConfig:
    """Get standard retry configuration for handling 429 rate limit errors.

    Follows ADK best practices from:
    https://google.github.io/adk-docs/agents/models/#error-code-429-resource_exhausted

    Returns:
        GenerateContentConfig with retry options configured for 429 errors
    """
    return GenerateContentConfig(
        http_options=HttpOptions(
            retry_options=HttpRetryOptions(
                attempts=3,  # Maximum 3 retry attempts
                initial_delay=10.0,  # Start with 10 second delay
                max_delay=60.0,  # Cap at 60 seconds
                exp_base=2.0,  # Exponential backoff with base 2
                jitter=0.2,  # 20% jitter to prevent thundering herd
                http_status_codes=[429],  # Only retry on 429 RESOURCE_EXHAUSTED errors
            )
        )
    )
