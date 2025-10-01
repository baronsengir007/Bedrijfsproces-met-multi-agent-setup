"""
Pydantic Models for Insurance Claims Multi-Agent System

These models define the structured output for each agent,
ensuring type-safe communication between agents.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==========================================
# AGENT 1: CLAIM TYPE CLASSIFIER OUTPUT
# ==========================================

class ClaimType(BaseModel):
    """Output from Agent 1: Claim Type Classifier"""
    
    type: str = Field(
        description="Claim type: Auto, Woning, Inboedel, Aansprakelijkheid"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score for the classification (0.0 - 1.0)"
    )
    keywords: List[str] = Field(
        description="Keywords that led to this classification"
    )
    policy_number: Optional[str] = Field(
        default=None,
        description="Extracted policy number if found"
    )
    incident_date: Optional[str] = Field(
        default=None,
        description="Extracted incident date if found (format: YYYY-MM-DD)"
    )
    reasoning: str = Field(
        description="Explanation of why this type was chosen"
    )


# ==========================================
# AGENT 2: URGENCY & AMOUNT ANALYZER OUTPUT
# ==========================================

class UrgencyAmountAnalysis(BaseModel):
    """Output from Agent 2: Urgency & Amount Analyzer"""
    
    urgency_level: str = Field(
        description="Urgency level: Critical, High, Medium, Low"
    )
    amount_euros: Optional[float] = Field(
        default=None,
        description="Extracted damage amount in euros"
    )
    amount_confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the extracted amount (0.0 - 1.0)"
    )
    is_total_loss: bool = Field(
        description="Whether this appears to be a total loss claim"
    )
    has_immediate_danger: bool = Field(
        description="Whether there is immediate danger or emergency"
    )
    sla_hours: int = Field(
        description="Recommended Service Level Agreement in hours"
    )
    deadline_detected: Optional[str] = Field(
        default=None,
        description="Explicit deadline if mentioned (format: YYYY-MM-DD)"
    )
    time_sensitive_keywords: List[str] = Field(
        description="Time-sensitive keywords found (urgent, asap, vandaag, etc.)"
    )
    reasoning: str = Field(
        description="Explanation of urgency assessment"
    )


# ==========================================
# AGENT 3: FRAUD RISK DETECTOR OUTPUT
# ==========================================

class FraudRiskAnalysis(BaseModel):
    """Output from Agent 3: Fraud Risk Detector"""
    
    risk_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Overall fraud risk score (0.0 = no risk, 1.0 = high risk)"
    )
    risk_level: str = Field(
        description="Risk level: Low, Medium, High"
    )
    red_flags: List[str] = Field(
        description="List of detected red flags"
    )
    suspicious_patterns: List[str] = Field(
        description="Suspicious patterns identified in the claim"
    )
    recommendation: str = Field(
        description="Recommendation: Auto-approve OK, Manual review, or SIU investigation"
    )
    reasoning: str = Field(
        description="Detailed explanation of fraud risk assessment"
    )


# ==========================================
# AGENT 4: ROUTING DECISION OUTPUT
# ==========================================

class RoutingDecision(BaseModel):
    """Output from Agent 4: Smart Router (Orchestrator)"""
    
    route_path: str = Field(
        description="Route: Auto-Approve, Junior-Adjuster, Standard-Adjuster, Senior-Adjuster, SIU-Investigation"
    )
    route_to_team: str = Field(
        description="Team name: Automated Processing, Junior Claims Team, Claims Adjusters, Senior Claims Team, SIU"
    )
    priority: int = Field(
        ge=1,
        le=5,
        description="Priority level: 1 (highest) to 5 (lowest)"
    )
    sla_hours: int = Field(
        description="Service Level Agreement in hours"
    )
    requires_manager_approval: bool = Field(
        description="Whether manager approval is required"
    )
    requires_inspection: bool = Field(
        description="Whether physical inspection is needed"
    )
    response_template_type: str = Field(
        description="Response template to use: A, B, C, or D"
    )
    escalation_flags: List[str] = Field(
        description="List of escalation flags (e.g., high_fraud_risk, critical_urgency)"
    )
    reasoning: str = Field(
        description="Detailed explanation of the routing decision"
    )


# ==========================================
# AGENT 5: RESPONSE GENERATOR OUTPUT
# ==========================================

class ClaimResponse(BaseModel):
    """Output from Agent 5: Response Generator"""
    
    response_text: str = Field(
        description="Complete email response text"
    )
    template_used: str = Field(
        description="Template used: A (Auto-approve), B (Standard), C (Manual), D (Escalation)"
    )
    tone: str = Field(
        description="Tone of the response: Professional-Positive, Professional, Thoughtful, Empathetic-Urgent"
    )
    includes_approval: bool = Field(
        description="Whether the response includes claim approval"
    )
    includes_next_steps: bool = Field(
        description="Whether next steps are clearly communicated"
    )
    estimated_processing_time: str = Field(
        description="Estimated processing time communicated to customer"
    )
    claim_reference_number: str = Field(
        description="Generated claim reference number (e.g., CLM-20251001-001)"
    )


# ==========================================
# COMPLETE WORKFLOW OUTPUT
# ==========================================

class CompleteClaimAnalysis(BaseModel):
    """Complete output from the entire multi-agent workflow"""
    
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Processing timestamp"
    )
    original_claim_text: str = Field(
        description="Original claim submission text"
    )
    
    # Phase 1 outputs (parallel)
    claim_type: ClaimType = Field(
        description="Output from Agent 1: Claim Type Classifier"
    )
    urgency_amount: UrgencyAmountAnalysis = Field(
        description="Output from Agent 2: Urgency & Amount Analyzer"
    )
    fraud_risk: FraudRiskAnalysis = Field(
        description="Output from Agent 3: Fraud Risk Detector"
    )
    
    # Phase 2 output (orchestrator)
    routing_decision: RoutingDecision = Field(
        description="Output from Agent 4: Smart Router"
    )
    
    # Phase 3 output (response)
    customer_response: ClaimResponse = Field(
        description="Output from Agent 5: Response Generator"
    )
    
    processing_notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the processing"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-10-01T10:30:00",
                "original_claim_text": "Autoschade €600...",
                "claim_type": {
                    "type": "Auto",
                    "confidence": 0.95,
                    "keywords": ["auto", "schade", "bumper"],
                    "policy_number": "AUTO-2024-12345",
                    "incident_date": "2025-09-30",
                    "reasoning": "Clear auto claim based on keywords"
                },
                "urgency_amount": {
                    "urgency_level": "Low",
                    "amount_euros": 600.0,
                    "amount_confidence": 0.85,
                    "is_total_loss": False,
                    "has_immediate_danger": False,
                    "sla_hours": 72,
                    "deadline_detected": None,
                    "time_sensitive_keywords": [],
                    "reasoning": "Standard claim, no urgency indicators"
                },
                "fraud_risk": {
                    "risk_score": 0.15,
                    "risk_level": "Low",
                    "red_flags": [],
                    "suspicious_patterns": [],
                    "recommendation": "Auto-approve mogelijk",
                    "reasoning": "No fraud indicators detected"
                },
                "routing_decision": {
                    "route_path": "Auto-Approve",
                    "route_to_team": "Automated Processing",
                    "priority": 3,
                    "sla_hours": 2,
                    "requires_manager_approval": False,
                    "requires_inspection": False,
                    "response_template_type": "A",
                    "escalation_flags": [],
                    "reasoning": "Meets all auto-approve criteria"
                },
                "customer_response": {
                    "response_text": "Beste klant, Goedgekeurd!...",
                    "template_used": "A",
                    "tone": "Professional-Positive",
                    "includes_approval": True,
                    "includes_next_steps": True,
                    "estimated_processing_time": "2 werkdagen",
                    "claim_reference_number": "CLM-20251001-001"
                }
            }
        }
