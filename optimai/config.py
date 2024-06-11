# optimai/config.py

from dataclasses import dataclass

@dataclass
class Config:
    """Config class for OptimAI"""
    llm: str = ""
    key: str = ""
    mode: str = "online"
    model: str = ""

config = Config()
