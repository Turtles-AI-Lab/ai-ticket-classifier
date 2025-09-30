"""
AI Ticket Classifier
A lightweight Python library for classifying support tickets using pattern matching and optional LLM integration.
"""

__version__ = "0.1.0"
__author__ = "Turtles AI Lab"

from .classifier import TicketClassifier
from .categories import TicketCategory, DEFAULT_CATEGORIES
from .llm_classifier import LLMClassifier

__all__ = [
    "TicketClassifier",
    "TicketCategory",
    "DEFAULT_CATEGORIES",
    "LLMClassifier"
]
