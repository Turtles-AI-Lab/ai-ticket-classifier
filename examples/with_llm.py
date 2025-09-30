"""
Example using LLM for more accurate classification
Requires OpenAI API key or local LLM setup
"""

import os
from ticket_classifier import LLMClassifier

# Option 1: OpenAI
# classifier = LLMClassifier(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     provider="openai",
#     model="gpt-3.5-turbo"
# )

# Option 2: Azure OpenAI
# classifier = LLMClassifier(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     provider="azure",
#     api_base="https://your-resource.openai.azure.com/",
#     model="gpt-35-turbo"
# )

# Option 3: Local LLM (LM Studio, Ollama, etc.)
classifier = LLMClassifier(
    provider="local",
    api_base="http://127.0.0.1:1234/v1",  # LM Studio default
    model="local-model"
)

# Test tickets with nuanced language
tickets = [
    "Hey, I've been trying to get into my account for the last 30 minutes but it keeps saying invalid credentials. I'm pretty sure I'm using the right password but maybe I locked myself out?",
    "The application has been really sluggish lately, taking forever to load. Sometimes it just freezes completely and I have to force quit it.",
    "We need to get Sarah set up with the same access that John has for the client database. She starts working on that project next week.",
    "My laptop battery isn't charging anymore. I've tried different outlets and even a different charger but nothing works.",
]

print("=" * 70)
print("LLM-Based Classification Example")
print("=" * 70)
print("Note: Make sure you have configured your LLM provider")
print("=" * 70)

try:
    for i, ticket in enumerate(tickets, 1):
        print(f"\n{i}. Ticket: {ticket[:80]}...")
        result = classifier.classify(ticket)

        print(f"   Category: {result.category.name}")
        print(f"   Description: {result.category.description}")
        print(f"   Confidence: {result.confidence:.2%}")
        print(f"   Priority: {result.category.priority}")
        if result.matched_patterns:
            print(f"   Reasoning: {result.matched_patterns[0]}")

except Exception as e:
    print(f"\nError: {e}")
    print("\nMake sure you have:")
    print("1. Installed required packages: pip install openai requests")
    print("2. Set up your API key or local LLM server")
    print("3. Configured the correct provider settings")
