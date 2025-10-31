"""
Tests for TicketClassifier
"""

import pytest
from ticket_classifier import TicketClassifier, TicketCategory


class TestTicketClassifier:
    """Test the basic TicketClassifier functionality"""

    def test_classifier_initialization(self):
        """Test that classifier initializes correctly"""
        classifier = TicketClassifier()
        assert classifier is not None
        assert len(classifier.categories) > 0

    def test_password_reset_classification(self):
        """Test password reset classification"""
        classifier = TicketClassifier()

        test_cases = [
            "I forgot my password",
            "Need to reset password",
            "Can't log in - forgot password",
            "I was locked out of my account"
        ]

        for ticket in test_cases:
            result = classifier.classify(ticket)
            assert result.category.name == "password_reset", f"Failed for: {ticket} -> {result.category.name}"
            assert result.confidence > 0.5

    def test_disk_space_classification(self):
        """Test disk space issue classification"""
        classifier = TicketClassifier()

        test_cases = [
            "C drive is full",
            "My disk is full",
            "Out of disk space on C:",
            "Running low on disk space"
        ]

        for ticket in test_cases:
            result = classifier.classify(ticket)
            assert result.category.name == "disk_space", f"Failed for: {ticket} -> {result.category.name}"
            assert result.confidence > 0.5

    def test_printer_issue_classification(self):
        """Test printer issue classification"""
        classifier = TicketClassifier()

        test_cases = [
            "Printer not working",
            "Can't print documents",
            "Printer is broken",
            "Printer down - cannot print"
        ]

        for ticket in test_cases:
            result = classifier.classify(ticket)
            assert result.category.name == "printer_issue", f"Failed for: {ticket} -> {result.category.name}"
            assert result.confidence > 0.5

    def test_batch_classification(self):
        """Test batch classification"""
        classifier = TicketClassifier()

        tickets = [
            "I forgot my password and can't log in",
            "Printer not working",
            "My disk is full"
        ]

        results = classifier.classify_batch(tickets)
        assert len(results) == 3
        assert results[0].category.name == "password_reset"
        assert results[1].category.name == "printer_issue"
        assert results[2].category.name == "disk_space"

    def test_custom_category(self):
        """Test adding custom categories"""
        classifier = TicketClassifier()

        custom_category = TicketCategory(
            name="test_category",
            description="Test category",
            keywords=["test", "example"],
            patterns=[r"test.*issue"],
            priority="low",
            auto_resolvable=False
        )

        classifier.add_category(custom_category)

        result = classifier.classify("test issue")
        assert result.category.name == "test_category"

    def test_confidence_score(self):
        """Test that confidence scores are valid"""
        classifier = TicketClassifier()

        result = classifier.classify("I forgot my password")
        assert 0.0 <= result.confidence <= 1.0

    def test_classification_result_to_dict(self):
        """Test ClassificationResult to_dict method"""
        classifier = TicketClassifier()

        result = classifier.classify("I forgot my password")
        result_dict = result.to_dict()

        assert "category" in result_dict
        assert "confidence" in result_dict
        assert "priority" in result_dict
        assert "auto_resolvable" in result_dict
        assert isinstance(result_dict["confidence"], (int, float))

    def test_empty_ticket(self):
        """Test classification of empty ticket"""
        classifier = TicketClassifier()

        result = classifier.classify("")
        assert result.category.name == "other"

    def test_unknown_ticket(self):
        """Test classification of unknown/ambiguous ticket"""
        classifier = TicketClassifier()

        result = classifier.classify("xyz abc random words")
        assert result.category.name == "other"
