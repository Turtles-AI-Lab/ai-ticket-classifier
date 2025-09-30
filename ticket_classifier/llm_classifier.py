"""
LLM-based ticket classification using OpenAI, Azure OpenAI, or local LLMs
"""

import json
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
        try:
            # Make LLM call
            response = self._call_llm(ticket_text)

            # Parse response
            category_name = response.get("category", "other")
            confidence = response.get("confidence", 0.5)
            reasoning = response.get("reasoning", "")

            # Get category object
            category = get_category_by_name(category_name)
            if not category:
                category = get_category_by_name("other")

            return ClassificationResult(
                category=category,
                confidence=confidence,
                matched_patterns=[reasoning] if reasoning else []
            )

        except Exception as e:
            # Fallback to "other" category on error
            print(f"LLM classification error: {e}")
            other_category = get_category_by_name("other")
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
        """Call OpenAI API"""
        try:
            import openai
            openai.api_key = self.api_key

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a support ticket classification system. Respond only with JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )

            content = response.choices[0].message.content.strip()
            return json.loads(content)

        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

    def _call_azure(self, prompt: str) -> Dict[str, Any]:
        """Call Azure OpenAI API"""
        try:
            import openai
            openai.api_type = "azure"
            openai.api_key = self.api_key
            openai.api_base = self.api_base
            openai.api_version = "2023-05-15"

            response = openai.ChatCompletion.create(
                engine=self.model,
                messages=[
                    {"role": "system", "content": "You are a support ticket classification system. Respond only with JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )

            content = response.choices[0].message.content.strip()
            return json.loads(content)

        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

    def _call_local(self, prompt: str) -> Dict[str, Any]:
        """Call local LLM (LM Studio, Ollama, etc.)"""
        try:
            import requests

            api_url = self.api_base or "http://127.0.0.1:1234/v1"

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
                timeout=30
            )

            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"].strip()

            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            return json.loads(content)

        except ImportError:
            raise ImportError("requests package required. Install with: pip install requests")
