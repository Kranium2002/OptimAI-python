# optimizeai/config.py

from dataclasses import dataclass

@dataclass
class Config:
    """Config class for OptimAI"""
    llm: str
    model: str
    key: str = "Enter your API key here"
    mode: str = "online"
