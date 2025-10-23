"""
LLM-based ticket classification using OpenAI, Azure OpenAI, or local LLMs
"""

import json
import logging
from typing import Optional, Dict, Any
from .classifier import ClassificationResult
from .categories import TicketCategory, DEFAULT_CATEGORIES, get_category_by_name


class LLMClassifier:
    """
    Ticket classifier using Large Language Models.
    Supports OpenAI, Azure OpenAI, and local LLMs (via LM Studio, Ollama, etc.)

    Example:
        >>> classifier = LLMClassifier(api_key="your-key", provider="openai")
        >>> result = classifier.classify("My computer is running very slow")
        >>> print(result.category.name)
        application_error
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "openai",
        api_base: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        categories: Optional[list] = None
    ):
        """
        Initialize LLM classifier

        Args:
            api_key: API key for OpenAI/Azure (not needed for local LLMs)
            provider: "openai", "azure", or "local"
            api_base: Base URL for API (required for Azure and local LLMs)
            model: Model name to use
            categories: Custom categories (defaults to DEFAULT_CATEGORIES)
        """
        self.api_key = api_key
        self.provider = provider.lower()
        self.api_base = api_base
        self.model = model
        self.categories = categories if categories is not None else DEFAULT_CATEGORIES

        # Validate configuration
        if self.provider in ["openai", "azure"] and not api_key:
            raise ValueError(f"{provider} provider requires an api_key")

        if self.provider == "azure" and not api_base:
            raise ValueError("Azure provider requires api_base URL")

    def classify(self, ticket_text: str) -> ClassificationResult:
        """
        Classify ticket using LLM

        Args:
            ticket_text: The ticket subject/description

        Returns:
            ClassificationResult
        """
        # Input validation
        if ticket_text is None:
            raise ValueError("ticket_text cannot be None")
        if not isinstance(ticket_text, str):
            raise TypeError(f"ticket_text must be str, not {type(ticket_text).__name__}")
        if not ticket_text.strip():
            raise ValueError("ticket_text cannot be empty")

        try:
            # Make LLM call
            response = self._call_llm(ticket_text)

            # Validate response structure
            if not isinstance(response, dict):
                raise ValueError(f"LLM response must be a dict, got {type(response).__name__}")

            # Parse and validate response fields
            category_name = response.get("category")
            if category_name is None:
                category_name = "other"
            if not isinstance(category_name, str):
                category_name = "other"

            confidence = response.get("confidence")
            if confidence is None:
                confidence = 0.5

            # Validate and clamp confidence value
            try:
                confidence = float(confidence)
                confidence = max(0.0, min(1.0, confidence))
            except (ValueError, TypeError):
                confidence = 0.5

            reasoning = response.get("reasoning", "")
            if not isinstance(reasoning, str):
                reasoning = ""

            # Get category object
            category = get_category_by_name(category_name)
            if category is None:
                category = get_category_by_name("other")

            # Final safety check - should never happen but prevents crash
            if category is None:
                raise ValueError("Could not find 'other' category in DEFAULT_CATEGORIES")

            return ClassificationResult(
                category=category,
                confidence=confidence,
                matched_patterns=[reasoning] if reasoning else []
            )

        except Exception as e:
            # Fallback to "other" category on error
            logging.warning(f"LLM classification error: {e}", exc_info=True)
            other_category = get_category_by_name("other")
            if other_category is None:
                raise ValueError("Could not find 'other' category in DEFAULT_CATEGORIES")
            return ClassificationResult(other_category, 0.0, [str(e)])

    def _call_llm(self, ticket_text: str) -> Dict[str, Any]:
        """
        Make LLM API call

        Args:
            ticket_text: Ticket text to classify

        Returns:
            Dict with classification results
        """
        # Build category list for prompt
        category_list = "\n".join([
            f"- {cat.name}: {cat.description}"
            for cat in self.categories if cat.name != "other"
        ])

        prompt = f"""Classify the following support ticket into one of these categories:

{category_list}

Ticket: "{ticket_text}"

Respond with a JSON object containing:
- category: the category name (exactly as listed above, or "other" if no match)
- confidence: a number between 0 and 1 indicating confidence
- reasoning: brief explanation of classification

Example response:
{{"category": "password_reset", "confidence": 0.95, "reasoning": "User explicitly mentions forgot password"}}

Your response (JSON only):"""

        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "azure":
            return self._call_azure(prompt)
        elif self.provider == "local":
            return self._call_local(prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _call_openai(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI API (using v1.x API)"""
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError("openai package required. Install with: pip install openai>=1.0.0") from e

        try:
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a support ticket classification system. Respond only with JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150,
                timeout=30.0
            )

            content = response.choices[0].message.content.strip()

            # Validate response structure
            if not content:
                raise ValueError("Empty response from OpenAI API")

            # Try to parse JSON with error handling
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response from OpenAI: {content[:100]}") from e

            # Validate response is a dictionary
            if not isinstance(parsed, dict):
                raise ValueError(f"Expected JSON object, got {type(parsed).__name__}")

            return parsed

        except Exception as e:
            # Re-raise with context
            raise RuntimeError(f"OpenAI API call failed: {str(e)}") from e

    def _call_azure(self, prompt: str) -> Dict[str, Any]:
        """Call Azure OpenAI API (using v1.x API)"""
        try:
            from openai import AzureOpenAI
        except ImportError as e:
            raise ImportError("openai package required. Install with: pip install openai>=1.0.0") from e

        try:
            client = AzureOpenAI(
                api_key=self.api_key,
                api_version="2023-05-15",
                azure_endpoint=self.api_base
            )

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a support ticket classification system. Respond only with JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150,
                timeout=30.0
            )

            content = response.choices[0].message.content.strip()

            # Validate response structure
            if not content:
                raise ValueError("Empty response from Azure OpenAI API")

            # Try to parse JSON with error handling
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response from Azure: {content[:100]}") from e

            # Validate response is a dictionary
            if not isinstance(parsed, dict):
                raise ValueError(f"Expected JSON object, got {type(parsed).__name__}")

            return parsed

        except Exception as e:
            # Re-raise with context
            raise RuntimeError(f"Azure OpenAI API call failed: {str(e)}") from e

    def _call_local(self, prompt: str) -> Dict[str, Any]:
        """Call local LLM (LM Studio, Ollama, etc.)"""
        try:
            import requests
        except ImportError as e:
            raise ImportError("requests package required. Install with: pip install requests") from e

        try:
            api_url = self.api_base or "http://127.0.0.1:1234/v1"

            # Security warning for HTTP connections
            if api_url.startswith("http://") and not api_url.startswith("http://127.0.0.1") and not api_url.startswith("http://localhost"):
                import warnings
                warnings.warn(
                    "Using insecure HTTP connection to remote LLM. "
                    "This exposes data to man-in-the-middle attacks. "
                    "Use HTTPS for production deployments.",
                    SecurityWarning,
                    stacklevel=3
                )

            # Verify SSL for HTTPS connections (disable only if explicitly set)
            verify_ssl = True
            if api_url.startswith("http://127.0.0.1") or api_url.startswith("http://localhost"):
                # localhost HTTP is acceptable for development
                verify_ssl = False

            response = requests.post(
                f"{api_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a support ticket classification system. Respond only with JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 150
                },
                timeout=30,
                verify=verify_ssl
            )

            response.raise_for_status()

            # Validate response structure
            try:
                response_data = response.json()
            except ValueError as e:
                raise ValueError(f"Invalid JSON response from local LLM API: {response.text[:100]}") from e

            # Validate response has expected structure
            if not isinstance(response_data, dict):
                raise ValueError(f"Expected JSON object from API, got {type(response_data).__name__}")

            if "choices" not in response_data:
                raise ValueError("Response missing 'choices' field")

            if not response_data["choices"] or len(response_data["choices"]) == 0:
                raise ValueError("Response 'choices' array is empty")

            content = response_data["choices"][0]["message"]["content"].strip()

            # Validate content
            if not content:
                raise ValueError("Empty response content from local LLM")

            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Try to parse JSON with error handling
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response from local LLM: {content[:100]}") from e

            # Validate response is a dictionary
            if not isinstance(parsed, dict):
                raise ValueError(f"Expected JSON object, got {type(parsed).__name__}")

            return parsed

        except requests.RequestException as e:
            raise RuntimeError(f"Local LLM API request failed: {str(e)}") from e
        except Exception as e:
            # Re-raise with context for any other errors
            raise RuntimeError(f"Local LLM API call failed: {str(e)}") from e
