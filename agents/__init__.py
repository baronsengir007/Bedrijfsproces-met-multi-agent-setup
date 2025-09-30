"""
Agents module voor Email Handler Multi-Agent System

5 gespecialiseerde agents:
1. Categorizer - Email classificatie
2. Urgency Analyzer - Urgentie en deadlines
3. Sentiment Analyzer - Emotie en escalatierisico
4. Routing Decision - Orchestrator die routing bepaalt
5. Response Generator - Email antwoorden
"""

from .categorizer import CategorizerAgent
from .urgency import UrgencyAnalyzerAgent
from .sentiment import SentimentAnalyzerAgent
from .router import RoutingDecisionAgent
from .responder import ResponseGeneratorAgent

__all__ = [
    'CategorizerAgent',
    'UrgencyAnalyzerAgent',
    'SentimentAnalyzerAgent',
    'RoutingDecisionAgent',
    'ResponseGeneratorAgent'
]
