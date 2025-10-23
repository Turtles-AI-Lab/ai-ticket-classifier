"""
Core ticket classification engine using pattern matching
"""

import re
import logging
from typing import List, Dict, Tuple, Optional
from .categories import TicketCategory, DEFAULT_CATEGORIES


class ClassificationResult:
    """Result of ticket classification"""

    def __init__(self, category: TicketCategory, confidence: float, matched_patterns: List[str]):
        # Validate category
        if category is None:
            raise ValueError("category cannot be None")
        if not isinstance(category, TicketCategory):
            raise TypeError(f"category must be TicketCategory, not {type(category).__name__}")

        # Validate confidence
        if confidence is None:
            raise ValueError("confidence cannot be None")
        if not isinstance(confidence, (int, float)):
            raise TypeError(f"confidence must be numeric, not {type(confidence).__name__}")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"confidence must be between 0.0 and 1.0, got {confidence}")

        # Validate matched_patterns
        if matched_patterns is None:
            raise ValueError("matched_patterns cannot be None")
        if not isinstance(matched_patterns, list):
            raise TypeError(f"matched_patterns must be list, not {type(matched_patterns).__name__}")

        self.category = category
        self.confidence = float(confidence)
        self.matched_patterns = matched_patterns

    def __repr__(self):
        return f"ClassificationResult(category='{self.category.name}', confidence={self.confidence:.2f})"

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "category": self.category.name,
            "description": self.category.description,
            "confidence": round(self.confidence, 2),
            "priority": self.category.priority,
            "auto_resolvable": self.category.auto_resolvable,
            "matched_patterns": self.matched_patterns
        }


class TicketClassifier:
    """
    Lightweight ticket classifier using pattern matching and keyword analysis.

    Example:
        >>> classifier = TicketClassifier()
        >>> result = classifier.classify("I forgot my password and can't log in")
        >>> print(result.category.name)
        password_reset
        >>> print(result.confidence)
        0.95
    """

    def __init__(self, categories: Optional[List[TicketCategory]] = None):
        """
        Initialize classifier with categories

        Args:
            categories: List of TicketCategory objects. If None, uses DEFAULT_CATEGORIES
        """
        if categories is not None:
            if not isinstance(categories, list):
                raise TypeError(f"categories must be list, not {type(categories).__name__}")
            for i, category in enumerate(categories):
                if not isinstance(category, TicketCategory):
                    raise TypeError(f"categories[{i}] must be TicketCategory, not {type(category).__name__}")

        self.categories = categories if categories is not None else DEFAULT_CATEGORIES
        if not self.categories:
            raise ValueError("categories list cannot be empty")

    def classify(self, ticket_text: str, threshold: float = 0.25) -> ClassificationResult:
        """
        Classify a ticket based on its text content

        Args:
            ticket_text: The ticket subject/description text
            threshold: Minimum confidence threshold (0.0 to 1.0)

        Returns:
            ClassificationResult with the best matching category
        """
        # Input validation
        if ticket_text is None:
            raise ValueError("ticket_text cannot be None")
        if not isinstance(ticket_text, str):
            raise TypeError(f"ticket_text must be str, not {type(ticket_text).__name__}")
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(f"threshold must be between 0.0 and 1.0, got {threshold}")

        # Limit text length for performance (avoid catastrophic backtracking)
        MAX_TEXT_LENGTH = 5000
        if len(ticket_text) > MAX_TEXT_LENGTH:
            ticket_text = ticket_text[:MAX_TEXT_LENGTH]

        ticket_text_lower = ticket_text.lower()
        scores = []

        for category in self.categories:
            score, matched = self._calculate_score(ticket_text_lower, category)
            scores.append((category, score, matched))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        # Get best match
        best_category, best_score, best_matches = scores[0]

        # If score is below threshold and not "other", return "other"
        if best_score < threshold and best_category.name != "other":
            other_category = next((c for c in self.categories if c.name == "other"), best_category)
            return ClassificationResult(other_category, best_score, [])

        return ClassificationResult(best_category, best_score, best_matches)

    def classify_batch(self, tickets: List[str], threshold: float = 0.25) -> List[ClassificationResult]:
        """
        Classify multiple tickets

        Args:
            tickets: List of ticket texts
            threshold: Minimum confidence threshold

        Returns:
            List of ClassificationResult objects
        """
        if tickets is None:
            raise ValueError("tickets cannot be None")
        if not isinstance(tickets, list):
            raise TypeError(f"tickets must be list, not {type(tickets).__name__}")
        if not tickets:
            raise ValueError("tickets list cannot be empty")

        return [self.classify(ticket, threshold) for ticket in tickets]

    def _calculate_score(self, text: str, category: TicketCategory) -> Tuple[float, List[str]]:
        """
        Calculate match score for a category

        Args:
            text: Lowercase ticket text
            category: Category to match against

        Returns:
            Tuple of (score, matched_patterns)
        """
        score = 0.0
        matched_patterns = []

        # Skip scoring for "other" category
        if category.name == "other":
            return 0.0, []

        # Check regex patterns (higher weight)
        pattern_matches = 0
        for pattern in category.patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_matches += 1
                    matched_patterns.append(pattern)
            except re.error as e:
                # Skip invalid regex patterns with warning
                logging.warning(f"Invalid regex pattern '{pattern}' in category '{category.name}': {e}")

        # Check keywords (lower weight)
        keyword_matches = 0
        for keyword in category.keywords:
            if keyword.lower() in text:
                keyword_matches += 1

        # Calculate weighted score
        # Each pattern match is worth 0.5, each keyword match is worth 0.1
        # This rewards matches without penalizing categories with many patterns
        pattern_score = min(pattern_matches * 0.5, 1.0)
        keyword_score = min(keyword_matches * 0.1, 0.5)

        score = min(pattern_score + keyword_score, 1.0)

        # Boost score if multiple matches found
        if pattern_matches >= 2:
            score = min(score + 0.1, 1.0)
        if keyword_matches >= 3:
            score = min(score + 0.05, 1.0)

        return score, matched_patterns

    def add_category(self, category: TicketCategory):
        """Add a custom category"""
        if category is None:
            raise ValueError("category cannot be None")
        if not isinstance(category, TicketCategory):
            raise TypeError(f"category must be TicketCategory, not {type(category).__name__}")

        # Check for duplicate category names
        if any(c.name == category.name for c in self.categories):
            raise ValueError(f"Category with name '{category.name}' already exists")

        self.categories.append(category)

    def remove_category(self, category_name: str):
        """Remove a category by name"""
        if category_name is None:
            raise ValueError("category_name cannot be None")
        if not isinstance(category_name, str):
            raise TypeError(f"category_name must be str, not {type(category_name).__name__}")
        if not category_name:
            raise ValueError("category_name cannot be empty")

        # Don't allow removing 'other' category
        if category_name == "other":
            raise ValueError("Cannot remove 'other' category - it is required as fallback")

        original_count = len(self.categories)
        self.categories = [c for c in self.categories if c.name != category_name]

        if len(self.categories) == original_count:
            raise ValueError(f"Category '{category_name}' not found")

        if not self.categories:
            raise ValueError("Cannot remove last category")

    def get_categories(self) -> List[TicketCategory]:
        """Get all categories"""
        return self.categories.copy()
