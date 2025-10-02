"""
Pydantic Models for Insurance Claims Processing (NEW - OpenAI SDK)

These models ensure type safety and validation for all data flowing through the pipeline.
All models use Pydantic v2 for validation.

NOTE: This file contains NEW models for the OpenAI SDK-based agents.
The old CrewAI models are in claim_models.py (legacy).
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re


class ClaimTypeOutput(BaseModel):
    """
    Output from Agent 1: Type & Amount Extractor
    
    Validates claim type classification and extracted metadata.
    """
    type: str = Field(description="Claim type: Auto, Woning, Inboedel, or Aansprakelijkheid")
    confidence: float = Field(ge=0.0, le=1.0, description="Classification confidence (0.0-1.0)")
    amount_euros: Optional[float] = Field(default=None, description="Damage amount in euros")
    amount_confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Amount extraction confidence")
    keywords: List[str] = Field(default_factory=list, description="Keywords used for classification")
    policy_number: Optional[str] = Field(default=None, description="Policy number if found")
    incident_date: Optional[str] = Field(default=None, description="Incident date (YYYY-MM-DD)")
    is_total_loss: bool = Field(default=False, description="Whether this is a total loss")
    reasoning: str = Field(description="Explanation of classification decision")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Normalize and validate claim type"""
        v = v.strip().capitalize()
        valid_types = {"Auto", "Woning", "Inboedel", "Aansprakelijkheid"}
        if v not in valid_types:
            # Try to match partial
            for valid in valid_types:
                if v.lower() in valid.lower() or valid.lower() in v.lower():
                    return valid
            # Fallback to Unknown
            return "Unknown"
        return v
    
    @field_validator('amount_euros', mode='before')
    @classmethod
    def parse_amount(cls, v) -> Optional[float]:
        """Parse amount from various formats"""
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            # Remove currency symbols and text
            cleaned = re.sub(r'[€$,]', '', v)
            numbers = re.findall(r'\d+\.?\d*', cleaned)
            if numbers:
                return float(numbers[0])
        return None
    
    @field_validator('incident_date', mode='before')
    @classmethod
    def validate_date(cls, v) -> Optional[str]:
        """Validate date format"""
        if v is None:
            return None
        if isinstance(v, str):
            # Check if already in YYYY-MM-DD format
            if re.match(r'\d{4}-\d{2}-\d{2}', v):
                return v
            # Try to parse common formats
            # For now, just accept what LLM gives us
            return v
        return None


class UrgencyOutput(BaseModel):
    """
    Output from Agent 2: Urgency Analyzer
    
    Validates urgency assessment and SLA determination.
    """
    urgency_level: str = Field(description="Urgency level: Critical, High, Medium, or Low")
    sla_hours: int = Field(gt=0, description="Service Level Agreement in hours")
    has_explicit_deadline: bool = Field(default=False, description="Whether explicit deadline mentioned")
    deadline_date: Optional[str] = Field(default=None, description="Deadline date if specified")
    deadline_time: Optional[str] = Field(default=None, description="Deadline time if specified")
    time_keywords: List[str] = Field(default_factory=list, description="Time-pressure keywords found")
    has_immediate_danger: bool = Field(default=False, description="Whether immediate physical danger exists")
    reasoning: str = Field(description="Explanation of urgency assessment")
    
    @field_validator('urgency_level')
    @classmethod
    def validate_urgency(cls, v: str) -> str:
        """Normalize and validate urgency level"""
        v = v.strip().capitalize()
        valid_levels = {"Critical", "High", "Medium", "Low"}
        if v not in valid_levels:
            # Default to Medium if unclear
            return "Medium"
        return v
    
    @field_validator('sla_hours', mode='before')
    @classmethod
    def validate_sla(cls, v) -> int:
        """Ensure SLA is a positive integer"""
        if isinstance(v, str):
            v = int(re.sub(r'\D', '', v))
        return max(1, int(v))


class FraudRiskOutput(BaseModel):
    """
    Output from Agent 3: Fraud Risk Detector
    
    Validates fraud risk assessment.
    """
    risk_score: float = Field(ge=0.0, le=1.0, description="Fraud risk score (0.0-1.0)")
    risk_level: str = Field(description="Risk level: Low, Medium, or High")
    red_flags: List[str] = Field(default_factory=list, description="Specific red flags detected")
    suspicious_patterns: List[str] = Field(default_factory=list, description="Suspicious patterns observed")
    recommendation: str = Field(description="Action recommendation")
    reasoning: str = Field(description="Detailed fraud assessment reasoning")
    
    @field_validator('risk_level')
    @classmethod
    def validate_risk_level(cls, v: str) -> str:
        """Normalize and validate risk level"""
        v = v.strip().capitalize()
        valid_levels = {"Low", "Medium", "High"}
        if v not in valid_levels:
            # Default to Medium if unclear
            return "Medium"
        return v
    
    @field_validator('risk_score', mode='before')
    @classmethod
    def validate_score(cls, v) -> float:
        """Ensure risk score is between 0 and 1"""
        if isinstance(v, str):
            v = float(re.sub(r'[^\d.]', '', v))
        return max(0.0, min(1.0, float(v)))


class RoutingDecision(BaseModel):
    """
    Output from Router: Python-based routing decision
    
    This is NOT validated from LLM output, but generated by Python code.
    Included here for consistency and type safety.
    """
    route_path: str = Field(description="Routing path name")
    route_to_team: str = Field(description="Team assignment")
    priority: int = Field(ge=1, le=3, description="Priority level (1=highest, 3=lowest)")
    sla_hours: int = Field(gt=0, description="SLA in hours")
    requires_manager_approval: bool = Field(description="Whether manager approval needed")
    requires_inspection: bool = Field(description="Whether physical inspection needed")
    response_template_type: str = Field(description="Response template to use (A, B, C, D)")
    escalation_flags: List[str] = Field(default_factory=list, description="Escalation flags")
    reasoning: str = Field(description="Routing decision reasoning")


class CustomerResponse(BaseModel):
    """
    Output from Agent 5: Response Generator
    
    Validates customer-facing response.
    """
    response_text: str = Field(description="Complete customer response email")
    template_used: str = Field(description="Template type used (A, B, C, D)")
    tone: str = Field(description="Response tone")
    includes_approval: bool = Field(description="Whether response includes approval")
    includes_next_steps: bool = Field(description="Whether next steps are included")
    estimated_processing_time: str = Field(description="Estimated processing time mentioned")
    claim_reference_number: str = Field(description="Unique claim reference")
    sentiment_detected: str = Field(description="Customer sentiment detected")
    llm_enhanced: bool = Field(description="Whether LLM was used for enhancement")
    
    @field_validator('response_text')
    @classmethod
    def validate_response(cls, v: str) -> str:
        """Ensure response is not empty"""
        v = v.strip()
        if not v:
            raise ValueError("Response text cannot be empty")
        return v


class PipelineResult(BaseModel):
    """
    Complete pipeline output
    
    Aggregates all agent outputs into single validated structure.
    """
    claim_type: ClaimTypeOutput
    urgency: UrgencyOutput
    fraud_risk: FraudRiskOutput
    routing: RoutingDecision
    response: CustomerResponse
    meta: dict = Field(default_factory=dict, description="Metadata like processing time, LLM calls")
    
    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "claim_type": {
                    "type": "Auto",
                    "confidence": 0.95,
                    "amount_euros": 400.0,
                    "keywords": ["autoschade", "bumper"]
                },
                "urgency": {
                    "urgency_level": "Low",
                    "sla_hours": 120
                },
                "fraud_risk": {
                    "risk_score": 0.15,
                    "risk_level": "Low",
                    "red_flags": []
                },
                "routing": {
                    "route_path": "Auto-Approve",
                    "priority": 3
                },
                "response": {
                    "response_text": "Beste klant, ...",
                    "template_used": "A"
                }
            }
        }


# Export all NEW models
__all__ = [
    "ClaimTypeOutput",
    "UrgencyOutput", 
    "FraudRiskOutput",
    "RoutingDecision",
    "CustomerResponse",
    "PipelineResult"
]
