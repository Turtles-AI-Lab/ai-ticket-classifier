"""
Example showing how to add custom categories
"""

from ticket_classifier import TicketClassifier, TicketCategory

# Create classifier
classifier = TicketClassifier()

# Add custom categories for your business
custom_categories = [
    TicketCategory(
        name="phone_system",
        description="VoIP or phone system issues",
        keywords=["phone", "voip", "call", "dial tone", "extension"],
        patterns=[
            r"phone.*not.*work",
            r"no.*dial.*tone",
            r"can'?t.*make.*call",
            r"voip.*issue"
        ],
        priority="high",
        auto_resolvable=False
    ),

    TicketCategory(
        name="pos_system",
        description="Point of sale system issues",
        keywords=["pos", "point of sale", "register", "cash register", "checkout"],
        patterns=[
            r"pos.*system",
            r"cash.*register",
            r"checkout.*not.*work",
            r"card.*reader"
        ],
        priority="critical",
        auto_resolvable=False
    ),

    TicketCategory(
        name="crm_issue",
        description="CRM system problems",
        keywords=["crm", "salesforce", "hubspot", "contacts", "deals"],
        patterns=[
            r"crm.*not.*work",
            r"salesforce.*error",
            r"can'?t.*access.*crm"
        ],
        priority="medium",
        auto_resolvable=False
    )
]

# Add custom categories
for category in custom_categories:
    classifier.add_category(category)

# Test with custom scenarios
test_tickets = [
    "The phone system is down and we can't make calls",
    "The POS system at register 3 is frozen",
    "I can't log into Salesforce CRM",
    "My password expired and I need it reset"
]

print("=" * 70)
print("Custom Categories Example")
print("=" * 70)

for ticket in test_tickets:
    result = classifier.classify(ticket)
    print(f"\nTicket: {ticket}")
    print(f"Category: {result.category.name}")
    print(f"Confidence: {result.confidence:.2%}")
    print(f"Priority: {result.category.priority}")

print("\n" + "=" * 70)
print(f"Total categories: {len(classifier.get_categories())}")
