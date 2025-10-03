"""
Ticket categories and their pattern definitions
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TicketCategory:
    """Represents a support ticket category with matching patterns"""

    name: str
    description: str
    keywords: List[str]
    patterns: List[str]
    priority: str = "medium"
    auto_resolvable: bool = False

    def __post_init__(self):
        """Validate TicketCategory fields after initialization"""
        # Validate name
        if not isinstance(self.name, str):
            raise TypeError(f"name must be str, not {type(self.name).__name__}")
        if not self.name:
            raise ValueError("name cannot be empty")

        # Validate description
        if not isinstance(self.description, str):
            raise TypeError(f"description must be str, not {type(self.description).__name__}")
        if not self.description:
            raise ValueError("description cannot be empty")

        # Validate keywords
        if not isinstance(self.keywords, list):
            raise TypeError(f"keywords must be list, not {type(self.keywords).__name__}")
        for i, keyword in enumerate(self.keywords):
            if not isinstance(keyword, str):
                raise TypeError(f"keywords[{i}] must be str, not {type(keyword).__name__}")

        # Validate patterns
        if not isinstance(self.patterns, list):
            raise TypeError(f"patterns must be list, not {type(self.patterns).__name__}")
        for i, pattern in enumerate(self.patterns):
            if not isinstance(pattern, str):
                raise TypeError(f"patterns[{i}] must be str, not {type(pattern).__name__}")

        # Validate priority
        if not isinstance(self.priority, str):
            raise TypeError(f"priority must be str, not {type(self.priority).__name__}")
        valid_priorities = ["low", "medium", "high", "critical"]
        if self.priority not in valid_priorities:
            raise ValueError(f"priority must be one of {valid_priorities}, got '{self.priority}'")

        # Validate auto_resolvable
        if not isinstance(self.auto_resolvable, bool):
            raise TypeError(f"auto_resolvable must be bool, not {type(self.auto_resolvable).__name__}")

    def __repr__(self):
        return f"TicketCategory(name='{self.name}', priority='{self.priority}')"


# Default ticket categories covering common IT support scenarios
DEFAULT_CATEGORIES = [
    TicketCategory(
        name="password_reset",
        description="User needs password reset or unlock",
        keywords=["password", "forgot", "reset", "unlock", "locked out", "can't login", "cannot login"],
        patterns=[
            r"forgot.*password",
            r"reset.*password",
            r"locked.*out",
            r"can'?t.*log.*in",
            r"unlock.*account"
        ],
        priority="high",
        auto_resolvable=True
    ),

    TicketCategory(
        name="disk_space",
        description="Low disk space or storage issues",
        keywords=["disk", "space", "full", "storage", "c drive", "drive full", "out of space"],
        patterns=[
            r"disk.*full",
            r"out.*of.*space",
            r"low.*disk",
            r"storage.*full",
            r"c:?\\?.*full"
        ],
        priority="medium",
        auto_resolvable=True
    ),

    TicketCategory(
        name="printer_issue",
        description="Printer not working or printing problems",
        keywords=["printer", "print", "printing", "queue", "spooler", "jam", "toner"],
        patterns=[
            r"printer.*not.*work\w*",
            r"printer.*is.*not.*work\w*",
            r"printer.*down",
            r"printer.*broken",
            r"can'?t.*print",
            r"print.*not.*work\w*",
            r"print.*queue",
            r"spooler",
            r"paper.*jam",
            r"printer.*issue",
            r"printer.*problem"
        ],
        priority="medium",
        auto_resolvable=True
    ),

    TicketCategory(
        name="email_issue",
        description="Email sending, receiving, or configuration problems",
        keywords=["email", "outlook", "can't send", "can't receive", "mailbox", "smtp", "exchange"],
        patterns=[
            r"email.*not.*work\w*",
            r"can'?t.*send.*email",
            r"can'?t.*receive",
            r"outlook.*error",
            r"mailbox.*full"
        ],
        priority="high",
        auto_resolvable=False
    ),

    TicketCategory(
        name="software_install",
        description="Software installation or update request",
        keywords=["install", "software", "application", "teams", "zoom", "office", "chrome"],
        patterns=[
            r"install\s+software",
            r"install\s+\w+\s+on",
            r"need\s+install",
            r"install\s+application",
            r"download\s+and\s+install",
            r"please\s+install",
            r"need\s+\w+\s+on\s+laptop",
            r"need\s+\w+\s+on\s+computer",
            r"install\s+teams",
            r"install\s+zoom",
            r"install\s+office"
        ],
        priority="medium",
        auto_resolvable=False
    ),

    TicketCategory(
        name="network_issue",
        description="Network connectivity or VPN problems",
        keywords=["network", "internet", "wifi", "vpn", "connection", "ethernet", "lan"],
        patterns=[
            r"no.*internet",
            r"can'?t.*connect",
            r"vpn.*not.*work\w*",
            r"wifi.*down",
            r"wifi.*not.*work\w*",
            r"wifi.*is.*not.*work\w*",
            r"network.*issue",
            r"network.*down",
            r"no.*connection",
            r"internet.*slow",
            r"no.*wifi"
        ],
        priority="high",
        auto_resolvable=False
    ),

    TicketCategory(
        name="license_request",
        description="Software license or Microsoft 365 license request",
        keywords=["license", "office 365", "m365", "microsoft 365", "subscription", "activation"],
        patterns=[
            r"need.*license",
            r"office.*365",
            r"m365",
            r"microsoft.*365",
            r"license.*expired"
        ],
        priority="medium",
        auto_resolvable=True
    ),

    TicketCategory(
        name="hardware_issue",
        description="Hardware malfunction or replacement needed",
        keywords=["hardware", "broken", "monitor", "keyboard", "mouse", "laptop", "computer", "screen"],
        patterns=[
            r"hardware\s+fail",
            r"monitor\s+broken",
            r"monitor\s+not\s+work\w*",
            r"keyboard\s+not\s+work\w*",
            r"mouse\s+not\s+work\w*",
            r"laptop\s+broken",
            r"screen\s+broken",
            r"\w+\s+is\s+broken"
        ],
        priority="medium",
        auto_resolvable=False
    ),

    TicketCategory(
        name="access_request",
        description="Request for access to files, folders, or systems",
        keywords=["access", "permission", "folder", "file", "share", "drive", "denied"],
        patterns=[
            r"need.*access.*to",
            r"permission.*denied",
            r"can'?t.*access",
            r"access.*request",
            r"share.*folder"
        ],
        priority="medium",
        auto_resolvable=True
    ),

    TicketCategory(
        name="application_error",
        description="Application crash, error, or performance issue",
        keywords=["error", "crash", "slow", "frozen", "not responding", "bug", "excel", "word", "outlook"],
        patterns=[
            r"application\s+crash",
            r"program\s+error",
            r"not\s+responding",
            r"software\s+slow",
            r"keeps\s+crashing",
            r"\w+\s+crash",
            r"\w+\s+keeps\s+crash",
            r"\w+\s+frozen",
            r"\w+\s+error"
        ],
        priority="medium",
        auto_resolvable=False
    ),

    TicketCategory(
        name="other",
        description="General inquiry or uncategorized issue",
        keywords=[],
        patterns=[],
        priority="low",
        auto_resolvable=False
    )
]


def get_category_by_name(name: str) -> Optional[TicketCategory]:
    """Get a category by its name"""
    for category in DEFAULT_CATEGORIES:
        if category.name == name:
            return category
    return None
