"""
Agent 2: Urgency & Amount Analyzer

Determines urgency level and extracts damage amount from claims.
Combines two related analyses for efficiency.
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, AGENT_SETTINGS, URGENCY_LEVELS
from models import UrgencyAmountAnalysis


class UrgencyAmountAnalyzerAgent:
    """
    Agent 2: Analyzes urgency and extracts damage amounts
    
    Specialization: Time-sensitivity assessment and amount extraction
    Output: UrgencyAmountAnalysis (Pydantic model)
    """
    
    def __init__(self):
        """Initialize the urgency & amount analyzer agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with configuration"""
        config = AGENT_CONFIG["urgency_amount_analyzer"]
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=AGENT_SETTINGS["verbose"],
            allow_delegation=AGENT_SETTINGS["allow_delegation"],
            llm=AGENT_SETTINGS["llm"]
        )
    
    def create_task(self, claim_text: str) -> Task:
        """
        Create an urgency & amount analysis task
        
        Args:
            claim_text: The insurance claim text to analyze
            
        Returns:
            Task: CrewAI task object
        """
        
        urgency_levels_str = ", ".join(URGENCY_LEVELS)
        
        description = f"""
        TAAK: Analyseer de urgentie en extraheer het schadebedrag uit deze claim.
        
        CLAIM TEKST:
        ---
        {claim_text}
        ---
        
        URGENTIE BEOORDELING:
        
        **Critical** (SLA: 2-8 uur):
        - Keywords: "total loss", "totaal verloren", "acuut gevaar", "noodgeval", 
          "onmiddellijk", "spoed", "kritiek"
        - Situaties: Systeem down, gevaar voor personen, extreme noodsituatie
        - Kenmerken: Expliciete crisis, direct risico
        
        **High** (SLA: 8-24 uur):
        - Keywords: "zo snel mogelijk", "ASAP", "urgent", "vandaag nog", "spoed"
        - Situaties: Deadline vandaag, dringende toon
        - Kenmerken: Tijdsdruk maar geen noodsituatie
        
        **Medium** (SLA: 72 uur):
        - Keywords: "deze week", "binnen 2-3 dagen", normale urgentie
        - Situaties: Standaard verwachting, redelijke tijdslijn
        - Kenmerken: Geen specifieke urgentie maar ook niet heel relaxed
        
        **Low** (SLA: 120 uur):
        - Keywords: geen urgentie keywords, "wanneer het uitkomt"
        - Situaties: Informatieve claims, algemene vragen
        - Kenmerken: Geen tijdsdruk
        
        BEDRAG EXTRACTIE:
        
        Zoek naar bedragen in verschillende formaten:
        - Directe bedragen: "€500", "€1.500", "€10.000", "1000 euro", "tweeduizend"
        - Schattingen: "ongeveer €2000", "schatting 1500", "rond de 3000"
        - Ranges: "tussen €500-1000" → neem midpoint (€750)
        - Woorden: "vijfhonderd euro", "tweeduizend" → converteer naar cijfers
        
        Confidence score voor bedrag:
        - 0.9-1.0: Exact bedrag genoemd ("€500")
        - 0.7-0.9: Schatting met indicatie ("ongeveer €500")
        - 0.5-0.7: Range of vage indicatie ("een paar honderd euro")
        - 0.0-0.5: Geen concreet bedrag, alleen "schade" genoemd
        
        TOTAL LOSS DETECTIE:
        
        Is er sprake van totaal verlies?
        - Keywords: "total loss", "totaal verloren", "niet meer te repareren", 
          "naar de sloop", "complete vernietiging", "alles kapot"
        - Situaties: Auto total loss, woning onbewoonbaar, complete vernietiging
        
        IMMEDIATE DANGER:
        
        Is er sprake van acuut gevaar?
        - Keywords: "gevaar", "risico voor personen", "acuut", "instortingsgevaar"
        - Situaties: Veiligheidsrisico's, acute noodsituaties
        
        SLA BEREKENING:
        
        Baseer SLA op urgency:
        - Critical: 2-8 uur
        - High: 8-24 uur
        - Medium: 72 uur
        - Low: 120 uur
        
        OUTPUT FORMAT (JSON):
        Geef ALLEEN een JSON object terug in dit exacte format:
        
        {{
            "urgency_level": "Critical" | "High" | "Medium" | "Low",
            "amount_euros": 600.00 of null,
            "amount_confidence": 0.85,
            "is_total_loss": false,
            "has_immediate_danger": false,
            "sla_hours": 72,
            "deadline_detected": "2025-10-05" of null,
            "time_sensitive_keywords": ["urgent", "zo snel mogelijk"],
            "reasoning": "Gedetailleerde uitleg: waarom dit urgency level, hoe bedrag 
                         bepaald is, waarom deze SLA, of er total loss/danger is."
        }}
        
        BELANGRIJK:
        - Urgency moet exact één van: {urgency_levels_str}
        - amount_euros moet float zijn of null (geen bedrag gevonden)
        - amount_confidence tussen 0.0 en 1.0
        - is_total_loss en has_immediate_danger zijn booleans
        - sla_hours moet integer zijn (2, 8, 24, 72, 120, etc.)
        - deadline_detected in YYYY-MM-DD format of null
        - time_sensitive_keywords zijn daadwerkelijke woorden uit de tekst
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met urgency en amount analysis volgens UrgencyAmountAnalysis model"
        )
