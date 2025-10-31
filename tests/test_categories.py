"""
Tests for TicketCategory
"""

import pytest
from ticket_classifier.categories import TicketCategory, DEFAULT_CATEGORIES


class TestTicketCategory:
    """Test the TicketCategory class"""

    def test_category_creation(self):
        """Test creating a basic category"""
        category = TicketCategory(
            name="test",
            description="Test category",
            keywords=["test"],
            patterns=[r"test"],
            priority="medium",
            auto_resolvable=False
        )

        assert category.name == "test"
        assert category.description == "Test category"
        assert category.priority == "medium"
        assert category.auto_resolvable is False

    def test_default_categories_exist(self):
        """Test that default categories are defined"""
        assert len(DEFAULT_CATEGORIES) > 0

        category_names = [cat.name for cat in DEFAULT_CATEGORIES]
        assert "password_reset" in category_names
        assert "disk_space" in category_names
        assert "printer_issue" in category_names
        assert "other" in category_names

    def test_category_has_required_fields(self):
        """Test that all default categories have required fields"""
        for category in DEFAULT_CATEGORIES:
            assert hasattr(category, 'name')
            assert hasattr(category, 'description')
            assert hasattr(category, 'keywords')
            assert hasattr(category, 'patterns')
            assert hasattr(category, 'priority')
            assert hasattr(category, 'auto_resolvable')

            assert isinstance(category.keywords, list)
            assert isinstance(category.patterns, list)
            assert category.priority in ['low', 'medium', 'high', 'critical']
            assert isinstance(category.auto_resolvable, bool)

    def test_category_repr(self):
        """Test category string representation"""
        category = TicketCategory(
            name="test",
            description="Test category",
            keywords=["test"],
            patterns=[r"test"],
            priority="medium",
            auto_resolvable=False
        )

        repr_str = repr(category)
        assert "test" in repr_str
