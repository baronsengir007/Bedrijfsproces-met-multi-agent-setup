"""
Agents package initialization
"""

from agents.claim_type_classifier import ClaimTypeClassifierAgent
from agents.urgency_amount_analyzer import UrgencyAmountAnalyzerAgent
from agents.fraud_risk_detector import FraudRiskDetectorAgent
from agents.smart_router import SmartRouterAgent
from agents.response_generator import ResponseGeneratorAgent

__all__ = [
    "ClaimTypeClassifierAgent",
    "UrgencyAmountAnalyzerAgent",
    "FraudRiskDetectorAgent",
    "SmartRouterAgent",
    "ResponseGeneratorAgent"
]
