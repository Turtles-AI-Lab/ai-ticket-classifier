"""
Basic usage example for AI Ticket Classifier
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ticket_classifier import TicketClassifier

# Create classifier with default categories
classifier = TicketClassifier()

# Example tickets
tickets = [
    "I forgot my password and can't log in to my computer",
    "My C drive is full and I need more space",
    "The printer on the 3rd floor is not working",
    "I can't send emails from Outlook",
    "Please install Microsoft Teams on my laptop",
    "The wifi is not working in the conference room",
    "I need a license for Office 365",
    "My monitor is broken",
    "I need access to the shared drive",
    "Excel keeps crashing when I open large files"
]

print("=" * 70)
print("AI Ticket Classifier - Basic Usage Example")
print("=" * 70)

# Classify each ticket
for i, ticket in enumerate(tickets, 1):
    result = classifier.classify(ticket)

    print(f"\n{i}. Ticket: {ticket}")
    print(f"   Category: {result.category.name}")
    print(f"   Description: {result.category.description}")
    print(f"   Confidence: {result.confidence:.2%}")
    print(f"   Priority: {result.category.priority}")
    print(f"   Auto-resolvable: {result.category.auto_resolvable}")

# Batch classification
print("\n" + "=" * 70)
print("Batch Classification Example")
print("=" * 70)

results = classifier.classify_batch(tickets)
print(f"\nClassified {len(results)} tickets:")

# Count by category
from collections import Counter
categories = [r.category.name for r in results]
category_counts = Counter(categories)

for category, count in category_counts.most_common():
    print(f"  {category}: {count}")
