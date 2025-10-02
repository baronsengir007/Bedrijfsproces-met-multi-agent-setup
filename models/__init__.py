"""
Models package initialization

Exports both legacy CrewAI models and new Pydantic models for OpenAI SDK agents.
"""

# Legacy CrewAI models (old)
from models.claim_models import (
    ClaimType,
    UrgencyAmountAnalysis,
    FraudRiskAnalysis,
    RoutingDecision as LegacyRoutingDecision,
    ClaimResponse,
    CompleteClaimAnalysis
)

# NEW Pydantic models for OpenAI SDK agents
from models.pydantic_models import (
    ClaimTypeOutput,
    UrgencyOutput,
    FraudRiskOutput,
    RoutingDecision,
    CustomerResponse,
    PipelineResult
)

# Export NEW models (used by current agents)
__all__ = [
    # NEW models (priority)
    "ClaimTypeOutput",
    "UrgencyOutput",
    "FraudRiskOutput",
    "RoutingDecision",
    "CustomerResponse",
    "PipelineResult",
    
    # Legacy models (kept for backward compatibility)
    "ClaimType",
    "UrgencyAmountAnalysis",
    "FraudRiskAnalysis",
    "LegacyRoutingDecision",
    "ClaimResponse",
    "CompleteClaimAnalysis"
]
