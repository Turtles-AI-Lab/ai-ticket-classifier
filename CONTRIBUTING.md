# Contributing to AI Ticket Classifier

Thank you for your interest in contributing to AI Ticket Classifier! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior vs actual behavior
- Your Python version and environment details
- Any relevant code samples or error messages

### Suggesting Enhancements

We love new ideas! To suggest an enhancement:
- Open an issue with a clear title and description
- Explain why this enhancement would be useful
- Provide examples of how it would work

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes:**
   - Add tests if you're adding functionality
   - Update documentation as needed
   - Follow the existing code style
3. **Test your changes:**
   ```bash
   python examples/basic_usage.py
   python examples/custom_categories.py
   ```
4. **Commit your changes:**
   - Use clear, descriptive commit messages
   - Reference any related issues
5. **Push to your fork** and submit a pull request

## Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Adding New Categories

To add a new ticket category:

```python
from ticket_classifier import TicketCategory

new_category = TicketCategory(
    name="category_name",
    description="Clear description",
    keywords=["keyword1", "keyword2"],
    patterns=[
        r"regex.*pattern1",
        r"regex.*pattern2"
    ],
    priority="high|medium|low",
    auto_resolvable=True|False
)
```

Add it to `ticket_classifier/categories.py` in the `DEFAULT_CATEGORIES` list.

### Testing New Patterns

Test your patterns before submitting:

```python
import re
text = "your test ticket text"
pattern = r"your.*pattern"
if re.search(pattern, text, re.IGNORECASE):
    print("Match!")
```

### Improving Classification Accuracy

When improving patterns:
1. Test with real-world ticket examples
2. Check for false positives and false negatives
3. Balance pattern specificity vs coverage
4. Document why changes improve accuracy

## Areas Where We Need Help

- **More categories:** Healthcare, retail, education-specific categories
- **Better patterns:** Improve regex patterns for existing categories
- **Language support:** Non-English ticket classification
- **LLM providers:** Support for more LLM providers
- **Integrations:** Examples for more ticketing systems
- **Documentation:** Tutorials, guides, and examples
- **Testing:** More comprehensive test suite

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.md following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format
3. The PR will be merged once you have approval from a maintainer

## Community

- **Issues:** [GitHub Issues](https://github.com/Turtles-AI-Lab/ai-ticket-classifier/issues)
- **Discussions:** Start a discussion in Issues for questions
- **Contact:** jgreenia@jandraisolutions.com

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards others

### Not Acceptable

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask questions by opening an issue or contacting us directly.

Thank you for contributing! 🎉
