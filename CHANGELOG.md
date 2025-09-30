# Changelog

All notable changes to the AI Ticket Classifier project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-01-30

### Fixed
- Fixed import paths in example files to work when run directly
- Improved classification accuracy with better regex patterns
- Fixed printer_issue category not matching "printer not working" phrases
- Fixed network_issue category not matching WiFi problems
- Fixed software_install category not matching application installation requests
- Fixed hardware_issue category pattern matching for broken equipment

### Changed
- Lowered default classification threshold from 0.3 to 0.25 for better sensitivity
- Enhanced regex patterns to handle word variations (e.g., "working" vs "work")
- Added more keywords to categories for better keyword matching
- Improved pattern specificity with additional variations

### Added
- Added support for "is not working" variations in patterns
- Added specific software keywords (teams, zoom, chrome, office)
- Added network-related keywords (ethernet, lan)
- Added printer-related keywords (toner, queue, jam)
- Added more application error patterns for common apps (excel, word, outlook)

## [0.1.0] - 2025-01-30

### Added
- Initial release of AI Ticket Classifier
- Pattern-based ticket classification with zero dependencies
- 11 pre-configured IT support categories
- Optional LLM integration (OpenAI, Azure, local)
- Custom category support
- Batch classification support
- Confidence scoring system
- Integration examples for Zendesk, Atera, Zoho Desk
- Comprehensive documentation and README
- MIT License
- Example scripts for basic usage, custom categories, and LLM integration

### Categories Included
- password_reset
- disk_space
- printer_issue
- email_issue
- software_install
- network_issue
- license_request
- hardware_issue
- access_request
- application_error
- other

[0.1.1]: https://github.com/Turtles-AI-Lab/ai-ticket-classifier/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Turtles-AI-Lab/ai-ticket-classifier/releases/tag/v0.1.0
