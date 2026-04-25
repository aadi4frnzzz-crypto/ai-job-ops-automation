"""OpenAI client wrapper with structured JSON output enforcement.
Handles API errors, token counting, and response validation.
"""
import json
import logging
import os
from typing import Any, Dict

from openai import OpenAI, AuthenticationError, RateLimitError, APIError

from prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

MODEL = "gpt-4o"
MAX_TOKENS = 1500
TEMPERATURE = 0.3  # low temp for structured, consistent output


def _get_client() -> OpenAI:
    """Create and validate the OpenAI client.

    Raises:
        EnvironmentError: If OPENAI_API_KEY is not set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is not set. "
            "Export it before running: export OPENAI_API_KEY=sk-..."
        )
    return OpenAI(api_key=api_key)


def analyze_job_fit(
    job_description: str,
    candidate_profile: str,
) -> Dict[str, Any]:
    """Call GPT-4o and return structured analysis as a Python dict.

    Args:
        job_description: Full text of the job posting.
        candidate_profile: Candidate's background, skills, experience.

    Returns:
        Parsed dict matching the output contract in prompts.py.

    Raises:
        ValueError: If the model returns invalid/unparseable JSON.
        RuntimeError: On API-level errors after retry.
    """
    client = _get_client()

    user_message = ANALYSIS_PROMPT_TEMPLATE.format(
        job_description=job_description.strip(),
        candidate_profile=candidate_profile.strip(),
    )

    logger.info("Calling %s | max_tokens=%d", MODEL, MAX_TOKENS)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"},  # Enforce JSON mode
        )
    except AuthenticationError:
        raise RuntimeError(
            "Invalid API key. Check your OPENAI_API_KEY value."
        )
    except RateLimitError:
        raise RuntimeError(
            "OpenAI rate limit hit. Wait 60s and retry, or upgrade your plan."
        )
    except APIError as exc:
        raise RuntimeError(f"OpenAI API error: {exc}") from exc

    raw = response.choices[0].message.content
    logger.debug("Raw model response: %s", raw[:200])

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Model returned non-JSON output: {raw[:300]}"
        ) from exc

    usage = response.usage
    logger.info(
        "Tokens used: prompt=%d completion=%d total=%d",
        usage.prompt_tokens, usage.completion_tokens, usage.total_tokens
    )
    return result
