"""
ImpactForge 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="impactforge",
    version="1.0.0",
    author="ImpactForge Team",
    author_email="team@impactforge.dev",
    description="智能代码变更影响分析引擎 - Smart Code Change Impact Analysis Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/impactforge/impactforge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "impactforge=impactforge.cli:main",
        ],
    },
    keywords=[
        "git",
        "code-analysis",
        "impact-analysis",
        "risk-assessment",
        "cli",
        "developer-tools",
        "code-review",
    ],
    project_urls={
        "Bug Reports": "https://github.com/impactforge/impactforge/issues",
        "Source": "https://github.com/impactforge/impactforge",
        "Documentation": "https://github.com/impactforge/impactforge#readme",
    },
)
