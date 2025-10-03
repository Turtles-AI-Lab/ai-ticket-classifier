from setuptools import setup, find_packages
import os

# Read README with proper exception handling
long_description = ""
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    print("Warning: README.md not found, using default description")
    long_description = "A lightweight Python library for classifying support tickets using AI"
except IOError as e:
    print(f"Warning: Could not read README.md: {e}")
    long_description = "A lightweight Python library for classifying support tickets using AI"
except Exception as e:
    print(f"Warning: Unexpected error reading README.md: {e}")
    long_description = "A lightweight Python library for classifying support tickets using AI"

setup(
    name="ai-ticket-classifier",
    version="0.1.1",
    author="Turtles AI Lab",
    author_email="jgreenia@jandraisolutions.com",
    description="A lightweight Python library for classifying support tickets using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Turtles-AI-Lab/ai-ticket-classifier",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No required dependencies for basic pattern matching
    ],
    extras_require={
        "llm": [
            "openai>=1.0.0",
            "requests>=2.31.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    keywords="ticket classification, support tickets, ai, nlp, helpdesk, automation",
    project_urls={
        "Bug Reports": "https://github.com/Turtles-AI-Lab/ai-ticket-classifier/issues",
        "Source": "https://github.com/Turtles-AI-Lab/ai-ticket-classifier",
        "Documentation": "https://github.com/Turtles-AI-Lab/ai-ticket-classifier#readme",
    },
)
