"""
Setup script for the AgentEval Python package.
"""

from setuptools import setup, find_packages

setup(
    name="agenteval",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "litellm>=1.0.0",
        "selenium>=4.0.0",
        "webdriver-manager>=3.0.0",
    ],
    author="AgentEval Team",
    author_email="example@example.com",
    description="A framework for evaluating AI agents using LiteLLM",
    keywords="ai, evaluation, testing, litellm",
    python_requires=">=3.7",
)
