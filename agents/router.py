"""
Agent 4: Routing Decision Maker (ORCHESTRATOR)
Neemt routing beslissingen op basis van ALL analysis van Agent 1, 2, 3
Dit is de KERN van het multi-agent systeem!
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, MODEL_NAME, ROUTING_TEAMS, SLA_BY_PRIORITY
from models import RoutingDecision


class RoutingDecisionAgent:
    """
    ORCHESTRATOR Agent die routing beslissingen neemt.
    
    Input: Gecombineerde resultaten van Agent 1, 2, 3
    - Category (Klacht/Verzoek/etc)
    - Urgency (Critical/High/Medium/Low)
    - Sentiment (Positive/Negative/etc)
    
    Output: RoutingDecision (Pydantic model)
    - Welk team krijgt deze email?
    - Wat is de prioriteit?
    - Moet het geëscaleerd worden?
    """
    
    def __init__(self):
        """Initialize the routing decision agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with proper configuration"""
        config = AGENT_CONFIG["router"]
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=True,
            allow_delegation=False,
            llm=MODEL_NAME
        )
    
    def create_task(
        self, 
        email_text: str,
        category_result: str,
        urgency_result: str,
        sentiment_result: str
    ) -> Task:
        """
        Create a routing decision task based on ALL previous analysis
        
        Args:
            email_text: Original email
            category_result: JSON result from Agent 1
            urgency_result: JSON result from Agent 2  
            sentiment_result: JSON result from Agent 3
            
        Returns:
            Task: CrewAI task object
        """
        teams_str = ", ".join(ROUTING_TEAMS)
        
        description = f"""
        Je bent de DECISION MAKER. Jouw taak is om op basis van ALLE voorgaande analyses
        de beste routing beslissing te nemen.
        
        ORIGINELE EMAIL:
        ---
        {email_text}
        ---
        
        ANALYSE RESULTATEN VAN ANDERE AGENTS:
        
        1. CATEGORIE ANALYSE (Agent 1):
        {category_result}
        
        2. URGENTIE ANALYSE (Agent 2):
        {urgency_result}
        
        3. SENTIMENT ANALYSE (Agent 3):
        {sentiment_result}
        
        ================================================================
        JOUW TAAK: Neem een routing beslissing
        ================================================================
        
        BESCHIKBARE TEAMS:
        {teams_str}
        
        ROUTING LOGICA:
        
        1. TEAM SELECTIE GUIDELINES:
        
        Senior_Customer_Service:
        - Klachten met Very_Negative sentiment
        - High/Critical urgency + Negative sentiment
        - Escalation risk = true
        - Complex cases
        
        Junior_Customer_Service:
        - Standaard Verzoeken (opzeggen, wijzigen)
        - Informatieaanvragen (Medium/Low urgency)
        - Positive/Neutral sentiment
        - Geen escalation risk
        
        Technical_Support:
        - Technische problemen
        - "Werkt niet", "Error", "Bug" keywords
        - Productgerelateerde klachten
        
        Sales:
        - Informatieaanvragen over producten/prijzen
        - Feedback met interesse in meer producten
        - Positive sentiment + commerciële interesse
        
        Management:
        - Legal threats ("advocaat", "rechtszaak")
        - PR risks ("social media", "reviews everywhere")
        - VIP customers (als detecteerbaar)
        - Requires_escalation = true
        
        2. PRIORITY BEREKENING (1-5):
        
        Priority 1 (Highest):
        - Critical urgency + (Negative OR Very_Negative sentiment)
        - Escalation risk + High urgency
        - Legal/PR threats
        
        Priority 2:
        - High urgency + any sentiment
        - Critical urgency + Neutral/Positive sentiment
        - Klacht + Negative sentiment
        
        Priority 3:
        - Medium urgency + Negative sentiment
        - High urgency + Positive sentiment
        - Standaard klachten
        
        Priority 4:
        - Medium urgency + Neutral sentiment
        - Low urgency + Negative sentiment
        - Standaard verzoeken
        
        Priority 5 (Lowest):
        - Low urgency + Neutral/Positive sentiment
        - Spam
        - Algemene informatieaanvragen
        
        3. SLA HOURS (Service Level Agreement):
        Priority 1: 2 hours
        Priority 2: 8 hours
        Priority 3: 24 hours
        Priority 4: 48 hours
        Priority 5: 72 hours
        
        4. ESCALATION FLAGS:
        
        Requires_escalation = TRUE als:
        - Legal threat keywords aanwezig
        - Very_Negative + Critical urgency
        - Escalation risk = true (van sentiment agent)
        - Herhaald contact zonder oplossing
        
        Requires_manager_approval = TRUE als:
        - Refund > €500 (als detecteerbaar)
        - Legal/contractuele zaken
        - Policy exceptions
        - VIP customers
        
        5. RISK FLAGS:
        Detecteer en rapporteer:
        - "legal": Juridische dreigingen
        - "pr_risk": Social media threats, public complaints
        - "churn_risk": Klant wil weg
        - "fraud_suspicion": Verdachte patronen
        - "compliance": Privacy, GDPR, contractueel
        
        VERPLICHTE OUTPUT FORMAT (JSON):
        {{
            "route_to_team": "één van de teams hierboven",
            "priority": 1-5 (integer),
            "sla_hours": aantal uren (integer),
            "requires_escalation": true/false,
            "requires_manager_approval": true/false,
            "suggested_action": "Reply/Forward/Escalate/Archive",
            "reasoning": "Gedetailleerde uitleg: waarom dit team, waarom deze priority, welke factoren wogen mee",
            "risk_flags": ["lijst", "van", "detected", "risks"]
        }}
        
        BELANGRIJKE OVERWEGINGEN:
        - Balanceer customer satisfaction vs efficiency
        - Junior team kan veel, maar niet alles
        - Escaleren is soms nodig, maar niet altijd
        - Snelle response bij urgency/negative sentiment voorkomt escalatie
        - Kijk naar de COMBINATIE van category + urgency + sentiment
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met routing decision",
            context=[category_result, urgency_result, sentiment_result]
        )
