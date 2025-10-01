"""
Agent 4: Smart Router (Orchestrator)

Makes routing decisions based on combined analysis from Agents 1, 2, and 3.
This is the CORE decision-making agent that determines the claim path.
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, AGENT_SETTINGS, ROUTE_PATHS, TEAMS
from models import RoutingDecision


class SmartRouterAgent:
    """
    Agent 4: Routing Decision Orchestrator
    
    Specialization: Combining all analyses to make optimal routing decisions
    Output: RoutingDecision (Pydantic model)
    
    This is the CORE of the multi-agent system!
    """
    
    def __init__(self):
        """Initialize the smart router agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with configuration"""
        config = AGENT_CONFIG["smart_router"]
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=AGENT_SETTINGS["verbose"],
            allow_delegation=AGENT_SETTINGS["allow_delegation"],
            llm=AGENT_SETTINGS["llm"]
        )
    
    def create_task(
        self,
        claim_text: str,
        claim_type_result: str,
        urgency_amount_result: str,
        fraud_risk_result: str
    ) -> Task:
        """
        Create a routing decision task based on all previous analyses
        
        Args:
            claim_text: Original claim text
            claim_type_result: JSON output from Agent 1
            urgency_amount_result: JSON output from Agent 2
            fraud_risk_result: JSON output from Agent 3
            
        Returns:
            Task: CrewAI task object
        """
        
        description = f"""
        TAAK: Maak de OPTIMALE routing beslissing voor deze claim op basis van ALLE analyses.
        
        ═══════════════════════════════════════════════════════════════
        ORIGINELE CLAIM
        ═══════════════════════════════════════════════════════════════
        {claim_text}
        
        ═══════════════════════════════════════════════════════════════
        AGENT 1: CLAIM TYPE ANALYSE
        ═══════════════════════════════════════════════════════════════
        {claim_type_result}
        
        ═══════════════════════════════════════════════════════════════
        AGENT 2: URGENCY & AMOUNT ANALYSE
        ═══════════════════════════════════════════════════════════════
        {urgency_amount_result}
        
        ═══════════════════════════════════════════════════════════════
        AGENT 3: FRAUD RISK ANALYSE
        ═══════════════════════════════════════════════════════════════
        {fraud_risk_result}
        
        ═══════════════════════════════════════════════════════════════
        JOUW ROUTING BESLISSING - VOLG DEZE DECISION TREE EXACT
        ═══════════════════════════════════════════════════════════════
        
        **LEVEL 1: CRITICAL CONDITIONS (Override alles anders)**
        
        CHECK 1A: High Fraud Risk?
        IF fraud_risk_score >= 0.6:
           → route_path = "SIU-Investigation"
           → route_to_team = "Special Investigations Unit"
           → priority = 1
           → sla_hours = 24
           → response_template_type = "D"
           → requires_manager_approval = true
           → escalation_flags = ["high_fraud_risk"]
           STOP - Geen verdere checks nodig
        
        CHECK 1B: Critical Urgency + Immediate Danger?
        IF urgency_level == "Critical" AND has_immediate_danger == true:
           → route_path = "Senior-Adjuster-Emergency"
           → route_to_team = "Senior Claims Team"
           → priority = 1
           → sla_hours = 2
           → response_template_type = "D"
           → requires_inspection = true
           → escalation_flags = ["critical_urgency", "immediate_danger"]
           STOP
        
        CHECK 1C: Extreme High Value?
        IF amount_euros > 100000:
           → route_path = "Senior-Adjuster-High-Value"
           → route_to_team = "Senior Claims Team"
           → priority = 1
           → sla_hours = 8
           → response_template_type = "C"
           → requires_manager_approval = true
           → requires_inspection = true
           → escalation_flags = ["extreme_high_value"]
           STOP
        
        **LEVEL 2: AUTO-APPROVE CHECK (Straight-Through Processing)**
        
        CHECK 2: Voldoet aan ALLE auto-approve criteria?
        IF ALL of these are TRUE:
           - amount_euros < 750
           - fraud_risk_score < 0.3
           - type_confidence > 0.8
           - is_total_loss == false
           - urgency_level != "Critical"
           - len(red_flags) == 0
        THEN:
           → route_path = "Auto-Approve"
           → route_to_team = "Automated Processing"
           → priority = 3
           → sla_hours = 2
           → response_template_type = "A"
           → requires_manager_approval = false
           → requires_inspection = false
           → escalation_flags = []
           STOP - Auto-approved!
        
        **LEVEL 3: STANDARD ROUTING (Amount & Fraud Based)**
        
        CHECK 3A: High Value + Medium-High Fraud?
        IF amount_euros > 10000 AND fraud_risk_score >= 0.3:
           → route_path = "Senior-Adjuster"
           → route_to_team = "Senior Claims Team"
           → priority = 2
           → sla_hours = 48
           → response_template_type = "C"
           → requires_inspection = true
           → escalation_flags = ["high_value_with_risk"]
           STOP
        
        CHECK 3B: High Value + Low Fraud?
        IF amount_euros > 10000 AND fraud_risk_score < 0.3:
           → route_path = "Senior-Adjuster"
           → route_to_team = "Senior Claims Team"
           → priority = 2
           → sla_hours = 48
           → response_template_type = "C"
           → requires_inspection = true
           → escalation_flags = []
           STOP
        
        CHECK 3C: Medium Value + Medium Fraud?
        IF 750 <= amount_euros <= 10000 AND 0.3 <= fraud_risk_score < 0.6:
           → route_path = "Standard-Adjuster"
           → route_to_team = "Claims Adjusters"
           → priority = 3
           → sla_hours = 72
           → response_template_type = "B"
           → escalation_flags = ["manual_review_needed"]
           STOP
        
        CHECK 3D: Medium Value + Low Fraud?
        IF 750 <= amount_euros <= 10000 AND fraud_risk_score < 0.3:
           → route_path = "Junior-Adjuster"
           → route_to_team = "Junior Claims Team"
           → priority = 3
           → sla_hours = 72
           → response_template_type = "B"
           → escalation_flags = []
           STOP
        
        **LEVEL 4: URGENCY OVERRIDE**
        
        CHECK 4A: Critical Urgency (not yet routed)?
        IF urgency_level == "Critical":
           → route_path = "Senior-Adjuster-Urgent"
           → route_to_team = "Senior Claims Team"
           → priority = 1
           → sla_hours = 8
           → response_template_type = "D"
           → escalation_flags = ["critical_urgency"]
           STOP
        
        CHECK 4B: High Urgency?
        IF urgency_level == "High":
           → Upgrade priority by 1 (bijv. 3 → 2)
           → Reduce SLA by 50%
           → Add escalation_flag = "high_urgency"
        
        **LEVEL 5: TYPE CONFIDENCE CHECK**
        
        CHECK 5: Low Type Confidence?
        IF type_confidence < 0.5:
           → route_path = "Manual-Classification"
           → route_to_team = "Claims Triage Team"
           → priority = 3
           → sla_hours = 48
           → response_template_type = "B"
           → escalation_flags = ["type_unclear"]
           STOP
        
        **LEVEL 6: TOTAL LOSS HANDLING**
        
        CHECK 6: Total Loss?
        IF is_total_loss == true:
           → Upgrade to Senior-Adjuster (minimum)
           → priority = min(current_priority, 2)
           → requires_inspection = true
           → Add escalation_flag = "total_loss"
           → response_template = "C"
        
        **LEVEL 7: DEFAULT FALLBACK**
        
        IF geen van bovenstaande:
           → route_path = "Standard-Adjuster"
           → route_to_team = "Claims Adjusters"
           → priority = 3
           → sla_hours = 72
           → response_template_type = "B"
           → escalation_flags = ["default_routing"]
        
        ═══════════════════════════════════════════════════════════════
        OUTPUT FORMAT (JSON)
        ═══════════════════════════════════════════════════════════════
        
        Geef ALLEEN een JSON object terug in dit exacte format:
        
        {{
            "route_path": "Auto-Approve" | "Junior-Adjuster" | "Standard-Adjuster" | 
                         "Senior-Adjuster" | "SIU-Investigation" | etc.,
            "route_to_team": "Automated Processing" | "Junior Claims Team" | 
                            "Claims Adjusters" | "Senior Claims Team" | 
                            "Special Investigations Unit",
            "priority": 1-5 (integer, 1 = hoogste),
            "sla_hours": integer (2, 8, 24, 48, 72, 120),
            "requires_manager_approval": true/false,
            "requires_inspection": true/false,
            "response_template_type": "A" | "B" | "C" | "D",
            "escalation_flags": [
                "high_fraud_risk",
                "critical_urgency",
                etc.
            ],
            "reasoning": "Gedetailleerde uitleg: welke decision tree path gevolgd, 
                         waarom deze route gekozen, hoe de verschillende factoren 
                         (type, amount, urgency, fraud) hebben meegewogen, en waarom 
                         deze specifieke team/priority/SLA is toegewezen. Referentie 
                         expliciet naar de CHECK nummers die van toepassing zijn."
        }}
        
        KRITIEKE HERINNERINGEN:
        
        1. Volg de decision tree EXACT - checks in volgorde
        2. Als een check matched, STOP tenzij er upgrades zijn (urgency, total loss)
        3. Auto-approve vereist ALLE 6 criteria - als één faalt, geen auto-approve
        4. Priority en SLA moeten logisch matched zijn
        5. Template selectie: A=auto-approve, B=standard, C=manual review, D=escalation
        6. Escalation flags zijn belangrijk voor auditing
        7. Reasoning moet duidelijk maken WELKE CHECKS zijn doorlopen
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met routing decision volgens RoutingDecision model"
        )
