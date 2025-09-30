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
            r"install.*software",
            r"install.*\w+.*on",
            r"need.*install",
            r"install.*application",
            r"download.*and.*install",
            r"please.*install",
            r"need.*\w+.*on.*laptop",
            r"need.*\w+.*on.*computer",
            r"install.*teams",
            r"install.*zoom",
            r"install.*office"
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
            r"hardware.*fail",
            r"monitor.*broken",
            r"monitor.*not.*work\w*",
            r"keyboard.*not.*work\w*",
            r"mouse.*not.*work\w*",
            r"laptop.*broken",
            r"screen.*broken",
            r"\w+.*is.*broken"
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
            r"application.*crash",
            r"program.*error",
            r"not.*responding",
            r"software.*slow",
            r"keeps.*crashing",
            r"\w+.*crash",
            r"\w+.*keeps.*crash",
            r"\w+.*frozen",
            r"\w+.*error"
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
