"""
Agents module voor Email Handler Multi-Agent System
"""

from .classifier import EmailClassifierAgent
from .sentiment import SentimentAnalyzerAgent
from .responder import ResponseGeneratorAgent

__all__ = [
    'EmailClassifierAgent',
    'SentimentAnalyzerAgent', 
    'ResponseGeneratorAgent'
]
