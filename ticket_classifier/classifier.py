"""
Core ticket classification engine using pattern matching
"""

import re
from typing import List, Dict, Tuple, Optional
from .categories import TicketCategory, DEFAULT_CATEGORIES


class ClassificationResult:
    """Result of ticket classification"""

    def __init__(self, category: TicketCategory, confidence: float, matched_patterns: List[str]):
        self.category = category
        self.confidence = confidence
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
        self.categories = categories if categories is not None else DEFAULT_CATEGORIES

    def classify(self, ticket_text: str, threshold: float = 0.3) -> ClassificationResult:
        """
        Classify a ticket based on its text content

        Args:
            ticket_text: The ticket subject/description text
            threshold: Minimum confidence threshold (0.0 to 1.0)

        Returns:
            ClassificationResult with the best matching category
        """
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

    def classify_batch(self, tickets: List[str], threshold: float = 0.3) -> List[ClassificationResult]:
        """
        Classify multiple tickets

        Args:
            tickets: List of ticket texts
            threshold: Minimum confidence threshold

        Returns:
            List of ClassificationResult objects
        """
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
            if re.search(pattern, text, re.IGNORECASE):
                pattern_matches += 1
                matched_patterns.append(pattern)

        # Check keywords (lower weight)
        keyword_matches = 0
        for keyword in category.keywords:
            if keyword.lower() in text:
                keyword_matches += 1

        # Calculate weighted score
        # Pattern matches are worth more than keyword matches
        if category.patterns:
            pattern_score = (pattern_matches / len(category.patterns)) * 0.7
        else:
            pattern_score = 0

        if category.keywords:
            keyword_score = (keyword_matches / len(category.keywords)) * 0.3
        else:
            keyword_score = 0

        score = pattern_score + keyword_score

        # Boost score if multiple patterns/keywords matched
        if pattern_matches >= 2:
            score = min(score + 0.1, 1.0)
        if keyword_matches >= 3:
            score = min(score + 0.05, 1.0)

        return score, matched_patterns

    def add_category(self, category: TicketCategory):
        """Add a custom category"""
        self.categories.append(category)

    def remove_category(self, category_name: str):
        """Remove a category by name"""
        self.categories = [c for c in self.categories if c.name != category_name]

    def get_categories(self) -> List[TicketCategory]:
        """Get all categories"""
        return self.categories.copy()
