"""
Python Router (NO LLM!)

Pure Python routing logic with strict business rules.
This is NOT an AI agent - just deterministic decision tree.

NO OpenAI calls - Pure Python performance!

NEDERLANDSE TERMINOLOGIE:
- SIU = Fraudeonderzoek Team
- Standard Adjuster = Claims Behandelaar
- Senior Adjuster = Senior Claims Behandelaar
- Junior Adjuster = Junior Claims Behandelaar
"""

from typing import Dict, Any


class PythonRouter:
    """
    Python Router: Routes claims using deterministic logic
    
    NO AI - Pure Python business rules
    Output: route_path, team, priority, SLA, template
    """
    
    def __init__(self):
        """Initialize router with business thresholds"""
        # Auto-approve thresholds
        self.AUTO_APPROVE_AMOUNT_THRESHOLD = 750
        self.AUTO_APPROVE_FRAUD_THRESHOLD = 0.3
        self.AUTO_APPROVE_MIN_CONFIDENCE = 0.8
        self.AUTO_APPROVE_MAX_RED_FLAGS = 1
        
        # Value thresholds
        self.EXTREME_HIGH_VALUE = 100000
        self.HIGH_VALUE_THRESHOLD = 25000
        self.MEDIUM_VALUE_THRESHOLD = 10000
        
        # Fraud thresholds
        self.FRAUD_SIU_THRESHOLD = 0.6  # High fraud → Always SIU
        self.FRAUD_MEDIUM_THRESHOLD = 0.4  # Medium fraud + flags → SIU
        self.FRAUD_MEDIUM_MIN_FLAGS = 3  # Need 3+ red flags for medium fraud SIU
    
    def route(
        self,
        type_data: Dict[str, Any],
        urgency_data: Dict[str, Any],
        fraud_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Route claim using strict business rules
        
        Args:
            type_data: Output from Agent 1
            urgency_data: Output from Agent 2
            fraud_data: Output from Agent 3
            
        Returns:
            Routing decision dict
        """
        
        # Extract values
        amount = type_data.get('amount_euros', 0) or 0
        claim_type = type_data.get('type', 'Unknown')
        is_total_loss = type_data.get('is_total_loss', False)
        type_confidence = type_data.get('confidence', 0)
        
        urgency_level = urgency_data.get('urgency_level', 'Medium')
        has_immediate_danger = urgency_data.get('has_immediate_danger', False)
        sla_hours = urgency_data.get('sla_hours', 72)
        
        fraud_risk = fraud_data.get('risk_score', 0)
        risk_level = fraud_data.get('risk_level', 'Low')
        red_flags = fraud_data.get('red_flags', [])
        red_flag_count = len(red_flags)
        
        # ═══════════════════════════════════════════════
        # LEVEL 1: CRITICAL CONDITIONS (Override everything)
        # ═══════════════════════════════════════════════
        
        # 1A: High Fraud Risk → Fraudeonderzoek (SIU)
        if fraud_risk >= self.FRAUD_SIU_THRESHOLD:
            return {
                "route_path": "Fraudeonderzoek",
                "route_to_team": "Fraudeonderzoek Team",
                "priority": 1,
                "sla_hours": 24,
                "requires_manager_approval": True,
                "requires_inspection": False,
                "response_template_type": "D",
                "escalation_flags": ["hoog_frauderisico"],
                "reasoning": f"Frauderisico {fraud_risk:.2f} overschrijdt drempel {self.FRAUD_SIU_THRESHOLD}. Automatische doorverwijzing naar fraudeonderzoek. Rode vlaggen: {red_flag_count}"
            }
        
        # 1B: Medium Fraud Risk + Multiple Red Flags → Fraudeonderzoek (SIU)
        # NEW: Catch medium fraud with many red flags
        if fraud_risk >= self.FRAUD_MEDIUM_THRESHOLD and red_flag_count >= self.FRAUD_MEDIUM_MIN_FLAGS:
            return {
                "route_path": "Fraudeonderzoek",
                "route_to_team": "Fraudeonderzoek Team",
                "priority": 1,
                "sla_hours": 24,
                "requires_manager_approval": True,
                "requires_inspection": False,
                "response_template_type": "D",
                "escalation_flags": ["verhoogd_frauderisico", "meerdere_rode_vlaggen"],
                "reasoning": f"Frauderisico {fraud_risk:.2f} met {red_flag_count} rode vlaggen (≥{self.FRAUD_MEDIUM_MIN_FLAGS}). Doorverwijzing naar fraudeonderzoek voor verder onderzoek."
            }
        
        # 1C: Critical Urgency + Immediate Danger → Spoed
        if urgency_level == "Critical" and has_immediate_danger:
            return {
                "route_path": "Spoed-Senior-Behandelaar",
                "route_to_team": "Senior Claims Team",
                "priority": 1,
                "sla_hours": 2,
                "requires_manager_approval": False,
                "requires_inspection": True,
                "response_template_type": "D",
                "escalation_flags": ["kritieke_urgentie", "direct_gevaar"],
                "reasoning": "Kritieke urgentie met direct gevaar gedetecteerd. Spoed protocol."
            }
        
        # 1D: Extreme High Value → Senior Review
        if amount > self.EXTREME_HIGH_VALUE:
            return {
                "route_path": "Senior-Behandelaar-Hoge-Waarde",
                "route_to_team": "Senior Claims Team",
                "priority": 1,
                "sla_hours": 8,
                "requires_manager_approval": True,
                "requires_inspection": True,
                "response_template_type": "C",
                "escalation_flags": ["extreem_hoge_waarde"],
                "reasoning": f"Bedrag €{amount:,.2f} overschrijdt €{self.EXTREME_HIGH_VALUE:,} drempel. Senior beoordeling vereist."
            }
        
        # ═══════════════════════════════════════════════
        # LEVEL 2: AUTO-APPROVE CHECK
        # ═══════════════════════════════════════════════
        
        # ALL criteria must be met for auto-approve
        auto_approve_eligible = (
            amount < self.AUTO_APPROVE_AMOUNT_THRESHOLD and
            amount > 0 and
            fraud_risk < self.AUTO_APPROVE_FRAUD_THRESHOLD and
            type_confidence > self.AUTO_APPROVE_MIN_CONFIDENCE and
            not is_total_loss and
            urgency_level != "Critical" and
            red_flag_count <= self.AUTO_APPROVE_MAX_RED_FLAGS
        )
        
        if auto_approve_eligible:
            red_flag_note = ""
            if red_flag_count == 1:
                red_flag_note = f" (1 kleine rode vlag acceptabel: {red_flags[0]})"
            
            return {
                "route_path": "Auto-Goedkeuring",
                "route_to_team": "Geautomatiseerde Verwerking",
                "priority": 3,
                "sla_hours": 2,
                "requires_manager_approval": False,
                "requires_inspection": False,
                "response_template_type": "A",
                "escalation_flags": [],
                "reasoning": f"Auto-goedkeuring: Bedrag €{amount:.2f} < €{self.AUTO_APPROVE_AMOUNT_THRESHOLD}, fraude {fraud_risk:.2f} < {self.AUTO_APPROVE_FRAUD_THRESHOLD}, vertrouwen {type_confidence:.2f} > {self.AUTO_APPROVE_MIN_CONFIDENCE}, {red_flag_count} rode vlag(gen){red_flag_note}."
            }
        
        # ═══════════════════════════════════════════════
        # LEVEL 3: VALUE-BASED ROUTING
        # ═══════════════════════════════════════════════
        
        # 3A: High Value (>€25k)
        if amount > self.HIGH_VALUE_THRESHOLD:
            return {
                "route_path": "Senior-Behandelaar",
                "route_to_team": "Senior Claims Team",
                "priority": 2,
                "sla_hours": 48,
                "requires_manager_approval": False,
                "requires_inspection": True,
                "response_template_type": "C",
                "escalation_flags": ["hoge_waarde"],
                "reasoning": f"Hoge waarde claim (€{amount:,.2f} > €{self.HIGH_VALUE_THRESHOLD:,}). Senior behandelaar toewijzing."
            }
        
        # 3B: Medium Value (€10k-€25k)
        if amount > self.MEDIUM_VALUE_THRESHOLD:
            if fraud_risk >= 0.3:
                route_team = "Claims-Behandelaar"
                flags = ["verhoogd_frauderisico"]
            else:
                route_team = "Claims-Behandelaar"
                flags = []
            
            return {
                "route_path": route_team,
                "route_to_team": "Claims Behandelaars",
                "priority": 2 if fraud_risk >= 0.3 else 3,
                "sla_hours": 72,
                "requires_manager_approval": False,
                "requires_inspection": False,
                "response_template_type": "B",
                "escalation_flags": flags,
                "reasoning": f"Gemiddelde waarde (€{amount:,.2f}). {'Verhoogd frauderisico.' if fraud_risk >= 0.3 else 'Standaard verwerking.'} Rode vlaggen: {red_flag_count}"
            }
        
        # 3C: Low-Medium Value (€750-€10k)
        if amount >= self.AUTO_APPROVE_AMOUNT_THRESHOLD:
            if fraud_risk >= 0.3 or red_flag_count > 1:
                return {
                    "route_path": "Claims-Behandelaar",
                    "route_to_team": "Claims Behandelaars",
                    "priority": 3,
                    "sla_hours": 72,
                    "requires_manager_approval": False,
                    "requires_inspection": False,
                    "response_template_type": "B",
                    "escalation_flags": ["handmatige_beoordeling_nodig"],
                    "reasoning": f"Net boven auto-goedkeuring drempel (€{amount:.2f}) met fraudezorgen (risico: {fraud_risk:.2f}, rode vlaggen: {red_flag_count})."
                }
            else:
                return {
                    "route_path": "Junior-Behandelaar",
                    "route_to_team": "Junior Claims Team",
                    "priority": 3,
                    "sla_hours": 72,
                    "requires_manager_approval": False,
                    "requires_inspection": False,
                    "response_template_type": "B",
                    "escalation_flags": [],
                    "reasoning": f"Lage-gemiddelde waarde (€{amount:.2f}), laag frauderisico. Junior behandelaar geschikt."
                }
        
        # ═══════════════════════════════════════════════
        # LEVEL 4: URGENCY OVERRIDE
        # ═══════════════════════════════════════════════
        
        if urgency_level == "Critical":
            return {
                "route_path": "Senior-Behandelaar-Urgent",
                "route_to_team": "Senior Claims Team",
                "priority": 1,
                "sla_hours": 8,
                "requires_manager_approval": False,
                "requires_inspection": False,
                "response_template_type": "D",
                "escalation_flags": ["kritieke_urgentie"],
                "reasoning": "Kritieke urgentie gedetecteerd. Escalatie naar senior team."
            }
        
        # ═══════════════════════════════════════════════
        # LEVEL 5: TOTAL LOSS HANDLING
        # ═══════════════════════════════════════════════
        
        if is_total_loss:
            return {
                "route_path": "Senior-Behandelaar",
                "route_to_team": "Senior Claims Team",
                "priority": 2,
                "sla_hours": 48,
                "requires_manager_approval": False,
                "requires_inspection": True,
                "response_template_type": "C",
                "escalation_flags": ["total_loss"],
                "reasoning": "Total loss gedetecteerd. Vereist senior beoordeling en inspectie."
            }
        
        # ═══════════════════════════════════════════════
        # LEVEL 6: LOW CONFIDENCE → MANUAL CLASSIFICATION
        # ═══════════════════════════════════════════════
        
        if type_confidence < 0.5:
            return {
                "route_path": "Handmatige-Classificatie",
                "route_to_team": "Claims Triage Team",
                "priority": 3,
                "sla_hours": 48,
                "requires_manager_approval": False,
                "requires_inspection": False,
                "response_template_type": "B",
                "escalation_flags": ["type_onduidelijk"],
                "reasoning": f"Laag type vertrouwen ({type_confidence:.2f}). Handmatige classificatie nodig."
            }
        
        # ═══════════════════════════════════════════════
        # DEFAULT FALLBACK
        # ═══════════════════════════════════════════════
        
        return {
            "route_path": "Claims-Behandelaar",
            "route_to_team": "Claims Behandelaars",
            "priority": 3,
            "sla_hours": 72,
            "requires_manager_approval": False,
            "requires_inspection": False,
            "response_template_type": "B",
            "escalation_flags": ["standaard_routing"],
            "reasoning": f"Geen specifieke routing criteria. Standaard behandelaar. (Rode vlaggen: {red_flag_count})"
        }
