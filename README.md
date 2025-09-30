# 🎫 AI Ticket Classifier

A lightweight, production-ready Python library for automatically classifying support tickets using pattern matching and optional LLM integration.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🚀 **Zero dependencies** for basic classification (pattern-based)
- 🤖 **Optional LLM support** (OpenAI, Azure OpenAI, local LLMs)
- 📦 **Pre-configured categories** for common IT support scenarios
- 🎯 **High accuracy** with confidence scoring
- 🔧 **Fully customizable** - add your own categories and patterns
- ⚡ **Fast** - classify thousands of tickets per second (pattern mode)
- 🔌 **Platform agnostic** - works with any ticketing system

## 📦 Installation

### Basic Installation (Pattern Matching Only)
```bash
pip install ai-ticket-classifier
```

### With LLM Support
```bash
pip install ai-ticket-classifier[llm]
# or
pip install openai requests
```

## 🚀 Quick Start

### Basic Pattern-Based Classification

```python
from ticket_classifier import TicketClassifier

# Create classifier
classifier = TicketClassifier()

# Classify a ticket
ticket = "I forgot my password and can't log in"
result = classifier.classify(ticket)

print(f"Category: {result.category.name}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Priority: {result.category.priority}")
print(f"Auto-resolvable: {result.category.auto_resolvable}")
```

**Output:**
```
Category: password_reset
Confidence: 95%
Priority: high
Auto-resolvable: True
```

### LLM-Based Classification (More Accurate)

```python
from ticket_classifier import LLMClassifier

# Using OpenAI
classifier = LLMClassifier(
    api_key="your-openai-key",
    provider="openai",
    model="gpt-3.5-turbo"
)

# Or use local LLM (LM Studio, Ollama)
classifier = LLMClassifier(
    provider="local",
    api_base="http://127.0.0.1:1234/v1"
)

result = classifier.classify("My computer is really slow")
print(result.category.name)  # application_error
```

### Batch Classification

```python
tickets = [
    "Need password reset",
    "Printer not working",
    "C drive full"
]

results = classifier.classify_batch(tickets)

for ticket, result in zip(tickets, results):
    print(f"{ticket} → {result.category.name}")
```

## 📋 Pre-configured Categories

The library includes 11 common IT support categories:

| Category | Description | Auto-Resolvable |
|----------|-------------|-----------------|
| `password_reset` | Password resets and account unlocks | ✅ Yes |
| `disk_space` | Low disk space issues | ✅ Yes |
| `printer_issue` | Printer problems | ✅ Yes |
| `email_issue` | Email sending/receiving problems | ❌ No |
| `software_install` | Software installation requests | ❌ No |
| `network_issue` | Network/VPN connectivity | ❌ No |
| `license_request` | Software license requests | ✅ Yes |
| `hardware_issue` | Hardware malfunctions | ❌ No |
| `access_request` | File/folder access requests | ✅ Yes |
| `application_error` | Application crashes/errors | ❌ No |
| `other` | Uncategorized issues | ❌ No |

## 🎨 Custom Categories

Add your own categories:

```python
from ticket_classifier import TicketClassifier, TicketCategory

classifier = TicketClassifier()

# Add custom category
custom_category = TicketCategory(
    name="voip_issue",
    description="VoIP phone system problems",
    keywords=["phone", "voip", "call", "extension"],
    patterns=[
        r"phone.*not.*work",
        r"no.*dial.*tone",
        r"can'?t.*make.*call"
    ],
    priority="high",
    auto_resolvable=False
)

classifier.add_category(custom_category)
```

## 🔌 Integration Examples

### With Zendesk
```python
from ticket_classifier import TicketClassifier
from zenpy import Zenpy

classifier = TicketClassifier()
zendesk = Zenpy(**creds)

for ticket in zendesk.tickets():
    result = classifier.classify(ticket.subject + " " + ticket.description)

    # Add tags
    ticket.tags.extend([result.category.name, result.category.priority])

    # Set priority
    ticket.priority = result.category.priority

    zendesk.tickets.update(ticket)
```

### With Atera
```python
import requests
from ticket_classifier import TicketClassifier

classifier = TicketClassifier()

# Get tickets from Atera
response = requests.get(
    "https://app.atera.com/api/v3/tickets",
    headers={"X-API-KEY": "your-key"}
)

for ticket in response.json():
    result = classifier.classify(ticket['Title'])

    # Update ticket with classification
    requests.put(
        f"https://app.atera.com/api/v3/tickets/{ticket['TicketID']}",
        headers={"X-API-KEY": "your-key"},
        json={"Comment": f"Auto-classified as: {result.category.name}"}
    )
```

### With Zoho Desk
```python
from ticket_classifier import TicketClassifier

classifier = TicketClassifier()

# Classify incoming webhook
def classify_webhook(ticket_data):
    result = classifier.classify(ticket_data['subject'])

    return {
        "category": result.category.name,
        "priority": result.category.priority,
        "auto_resolve": result.category.auto_resolvable
    }
```

## 🎯 Use Cases

- **Automated Triage**: Route tickets to the right team automatically
- **Priority Assignment**: Set ticket priority based on classification
- **Auto-Resolution**: Identify tickets that can be auto-resolved
- **Analytics**: Track ticket categories and trends
- **SLA Management**: Different SLAs for different ticket types
- **Chatbot Training**: Use classifications to train support chatbots

## 📊 Performance

**Pattern-based classifier:**
- ~10,000 tickets/second
- Zero API costs
- No external dependencies

**LLM-based classifier:**
- More accurate for complex/nuanced tickets
- ~10-50 tickets/second (depending on LLM provider)
- API costs apply

## 🤝 Contributing

Contributions welcome! Areas where you can help:

- Add more default categories
- Improve pattern matching accuracy
- Add support for more languages
- Create integrations for popular ticketing systems

## 📄 License

MIT License - see LICENSE file

## 🏢 Commercial Support

This is an open-source project by **Turtles AI Lab**.

Need help integrating this into your business?
- Custom category development
- Integration consulting
- Production deployment support

📧 Contact: jgreenia@jandraisolutions.com

## 🌟 Related Projects

- [TicketZero AI - Atera Edition](https://github.com/Turtles-AI-Lab/TicketZero-Atera-Edition) - Full automated ticket resolution for Atera
- [TicketZero AI - Zoho Edition](https://github.com/Turtles-AI-Lab/TicketZero-Zoho-Edition) - Full automated ticket resolution for Zoho Desk

---

**Built with ❤️ by Turtles AI Lab**

⭐ Star this repo if you find it useful!
