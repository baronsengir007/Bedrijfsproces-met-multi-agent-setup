"""
Pydantic Models voor Structured Output tussen Agents
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==========================================
# AGENT 1: CATEGORIZER OUTPUT
# ==========================================

class EmailCategory(BaseModel):
    """Output van de Categorizer Agent"""
    category: str = Field(
        description="Email categorie: Klacht, Verzoek, Informatieaanvraag, Feedback, Spam, Overig"
    )
    confidence: float = Field(
        ge=0.0, 
        le=1.0, 
        description="Confidence score tussen 0 en 1"
    )
    keywords: list[str] = Field(
        description="Key woorden die tot classificatie hebben geleid"
    )
    reasoning: str = Field(
        description="Waarom deze categorie is gekozen"
    )


# ==========================================
# AGENT 2: URGENCY ANALYZER OUTPUT
# ==========================================

class UrgencyAnalysis(BaseModel):
    """Output van de Urgency Analyzer Agent"""
    urgency_level: str = Field(
        description="Urgency level: Critical, High, Medium, Low"
    )
    has_deadline: bool = Field(
        description="Of er een expliciete deadline in de email staat"
    )
    deadline_date: Optional[str] = Field(
        default=None,
        description="Deadline datum als gevonden (format: YYYY-MM-DD)"
    )
    time_sensitive_keywords: list[str] = Field(
        description="Tijdgevoelige woorden zoals 'urgent', 'zo snel mogelijk', 'vandaag'"
    )
    recommended_response_time: int = Field(
        description="Aanbevolen response tijd in uren"
    )
    reasoning: str = Field(
        description="Waarom dit urgency level"
    )


# ==========================================
# AGENT 3: SENTIMENT ANALYZER OUTPUT
# ==========================================

class SentimentAnalysis(BaseModel):
    """Output van de Sentiment Analyzer Agent"""
    sentiment: str = Field(
        description="Sentiment: Positive, Neutral, Negative, Very_Negative"
    )
    emotion_score: float = Field(
        ge=-1.0, 
        le=1.0,
        description="Emotie score: -1 (zeer negatief) tot +1 (zeer positief)"
    )
    escalation_risk: bool = Field(
        description="Of deze email risico heeft op escalatie"
    )
    tone_indicators: list[str] = Field(
        description="Woorden die sentiment aangeven"
    )
    customer_satisfaction_indicator: str = Field(
        description="Tevreden, Neutraal, Ontevreden, Zeer_Ontevreden"
    )
    reasoning: str = Field(
        description="Waarom dit sentiment"
    )


# ==========================================
# COMBINED: INPUT VOOR AGENT 4 (ROUTER)
# ==========================================

class EmailAnalysis(BaseModel):
    """Gecombineerde output van Agent 1, 2, 3 - Input voor Agent 4"""
    category: EmailCategory
    urgency: UrgencyAnalysis
    sentiment: SentimentAnalysis
    original_email: str = Field(
        description="De originele email tekst"
    )


# ==========================================
# AGENT 4: ROUTING DECISION OUTPUT
# ==========================================

class RoutingDecision(BaseModel):
    """Output van de Routing Decision Agent (Orchestrator)"""
    route_to_team: str = Field(
        description="Team: Senior_Customer_Service, Junior_Customer_Service, Technical_Support, Sales, Management"
    )
    priority: int = Field(
        ge=1, 
        le=5,
        description="Priority level: 1 (hoogste) tot 5 (laagste)"
    )
    sla_hours: int = Field(
        description="Service Level Agreement: response binnen X uren"
    )
    requires_escalation: bool = Field(
        description="Of deze email geëscaleerd moet worden naar management"
    )
    requires_manager_approval: bool = Field(
        description="Of response goedkeuring nodig heeft van manager"
    )
    suggested_action: str = Field(
        description="Voorgestelde actie: Reply, Forward, Escalate, Archive"
    )
    reasoning: str = Field(
        description="Waarom deze routing beslissing is genomen"
    )
    risk_flags: list[str] = Field(
        description="Eventuele risk indicators (legal, PR, churn risk, etc)"
    )


# ==========================================
# AGENT 5: RESPONSE GENERATOR OUTPUT
# ==========================================

class EmailResponse(BaseModel):
    """Output van de Response Generator Agent"""
    response_text: str = Field(
        description="De gegenereerde email response"
    )
    tone: str = Field(
        description="Tone van response: Formal, Friendly, Apologetic, Professional, Empathetic"
    )
    response_type: str = Field(
        description="Type response: Full_Answer, Acknowledgment, Escalation_Notice, Request_More_Info"
    )
    includes_apology: bool = Field(
        description="Of de response een excuses bevat"
    )
    includes_solution: bool = Field(
        description="Of de response een concrete oplossing bevat"
    )
    follow_up_required: bool = Field(
        description="Of er follow-up nodig is"
    )
    follow_up_date: Optional[str] = Field(
        default=None,
        description="Wanneer follow-up moet gebeuren"
    )
    cc_manager: bool = Field(
        description="Of manager in CC gezet moet worden"
    )


# ==========================================
# FINAL OUTPUT: COMPLETE WORKFLOW RESULT
# ==========================================

class CompleteEmailWorkflow(BaseModel):
    """Complete output van de hele multi-agent workflow"""
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp van verwerking"
    )
    original_email: str
    analysis: EmailAnalysis
    routing: RoutingDecision
    response: EmailResponse
    processing_notes: Optional[str] = Field(
        default=None,
        description="Eventuele notes over de verwerking"
    )
