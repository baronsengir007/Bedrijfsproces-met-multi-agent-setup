"""
Agents package - Updated architecture

Agent 1: TypeAmountExtractorAgent (LLM)
Agent 2: UrgencyAnalyzerAgent (LLM)
Agent 3: FraudRiskDetectorAgent (LLM)
Router: PythonRouter (NO LLM - pure Python!)
Agent 5: ResponseGeneratorAgent (Hybrid: Template + optional LLM)
"""

from agents.type_amount_extractor import TypeAmountExtractorAgent
from agents.urgency_analyzer import UrgencyAnalyzerAgent
from agents.fraud_detector import FraudRiskDetectorAgent
from agents.router import PythonRouter
from agents.response_generator_hybrid import ResponseGeneratorAgent

__all__ = [
    "TypeAmountExtractorAgent",
    "UrgencyAnalyzerAgent",
    "FraudRiskDetectorAgent",
    "PythonRouter",
    "ResponseGeneratorAgent"
]
