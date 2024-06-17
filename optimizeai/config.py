# optimizeai/config.py

from dataclasses import dataclass

@dataclass
class Config:
    """Config class for OptimAI"""
    llm: str
    key: str = "Enter your API key here"
    model: str
    mode: str = "online"
