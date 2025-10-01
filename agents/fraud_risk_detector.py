"""
Agent 3: Fraud Risk Detector

Assesses fraud risk based on textual patterns, completeness, and inconsistencies.
Works WITHOUT database access - purely text-based analysis.
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, AGENT_SETTINGS
from models import FraudRiskAnalysis


class FraudRiskDetectorAgent:
    """
    Agent 3: Detects fraud risk patterns in claims
    
    Specialization: Pattern-based fraud detection from text only
    Output: FraudRiskAnalysis (Pydantic model)
    """
    
    def __init__(self):
        """Initialize the fraud risk detector agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with configuration"""
        config = AGENT_CONFIG["fraud_risk_detector"]
        
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
        Create a fraud risk detection task
        
        Args:
            claim_text: The insurance claim text to analyze
            
        Returns:
            Task: CrewAI task object
        """
        
        description = f"""
        TAAK: Analyseer deze verzekeringsclaim op frauderisico ZONDER database access.
        Je werkt ALLEEN met wat in de tekst staat.
        
        CLAIM TEKST:
        ---
        {claim_text}
        ---
        
        FRAUD RISK ANALYSE FRAMEWORK:
        
        Je bouwt een risk score op van 0.0 tot 1.0 door verschillende patronen te detecteren.
        
        ═══════════════════════════════════════════════════════════════
        1. COMPLETENESS CHECK (0-0.3 punten)
        ═══════════════════════════════════════════════════════════════
        
        Ontbreekt cruciale informatie?
        
        **Incident datum ontbreekt** (+0.15):
        - Geen specifieke datum genoemd
        - Alleen "recent", "laatst", "pas geleden"
        
        **Locatie ontbreekt** (+0.10):
        - Geen specifieke locatie (stad, straat, plaats)
        - Alleen "ergens", "onderweg"
        
        **Vage beschrijving** (+0.15):
        - Zeer minimale details
        - "Een beetje schade", "iets kapot"
        - Geen concrete omschrijving van wat er gebeurd is
        
        Bij autoschade specifiek:
        - Geen kenteken
        - Geen andere partij info (bij aanrijding)
        - Geen politie rapport nummer (bij diefstal)
        
        ═══════════════════════════════════════════════════════════════
        2. TIMING SIGNALEN (0-0.3 punten)
        ═══════════════════════════════════════════════════════════════
        
        **Recent afgesloten polis** (+0.25):
        - "Polis net afgesloten"
        - "Vorige week contract"
        - "Pas verzekerd sinds..."
        - Melding van polis < 30 dagen oud
        
        **Herhaalde claims melding** (+0.20):
        - "Dit is alweer de Xe keer dit jaar"
        - "Weer schade"
        - "Opnieuw een claim"
        - Suggestie van frequent claimen
        
        ═══════════════════════════════════════════════════════════════
        3. BEDRAG POSITIONERING (0-0.2 punten)
        ═══════════════════════════════════════════════════════════════
        
        **Strategisch bedrag** (+0.20):
        - Bedragen net onder bekende drempels:
          - €9.900 - €9.999 (net onder €10k)
          - €24.500 - €24.999 (net onder €25k)
          - €740 - €749 (net onder €750 auto-approve)
        - Opvallend precieze bedragen zonder onderbouwing
        
        ═══════════════════════════════════════════════════════════════
        4. INCONSISTENTIES (0-0.3 punten)
        ═══════════════════════════════════════════════════════════════
        
        **Taal vs Bedrag mismatch** (+0.15):
        - "Totale ramp", "alles kapot", "complete vernietiging" + klein bedrag (€200)
        - Zeer emotionele taal voor kleine schade
        - Minimaliserende taal voor hoog bedrag
        
        **Tegenstrijdige statements** (+0.25):
        - "Geen getuigen" maar later "iemand heeft het gezien"
        - Tijdstippen die niet kloppen
        - Inconsistente beschrijvingen in dezelfde claim
        
        ═══════════════════════════════════════════════════════════════
        RISK SCORE BEREKENING
        ═══════════════════════════════════════════════════════════════
        
        Tel alle punten op, cap bij 1.0:
        
        risk_score = min(
            completeness_penalties + 
            timing_signals + 
            amount_positioning + 
            inconsistencies,
            1.0
        )
        
        ═══════════════════════════════════════════════════════════════
        RISK LEVEL MAPPING
        ═══════════════════════════════════════════════════════════════
        
        - **Low** (0.0 - 0.3): Geen significante rode vlaggen
        - **Medium** (0.3 - 0.6): Enkele zorgen, manual review aanbevolen
        - **High** (0.6 - 1.0): Meerdere rode vlaggen, SIU investigation
        
        ═══════════════════════════════════════════════════════════════
        RECOMMENDATION
        ═══════════════════════════════════════════════════════════════
        
        Gebaseerd op risk_level:
        - Low: "Auto-approve mogelijk (bij andere criteria OK)"
        - Medium: "Manual review aanbevolen"
        - High: "SIU investigation vereist"
        
        OUTPUT FORMAT (JSON):
        Geef ALLEEN een JSON object terug in dit exacte format:
        
        {{
            "risk_score": 0.25,
            "risk_level": "Low" | "Medium" | "High",
            "red_flags": [
                "Geen incident datum vermeld",
                "Recent afgesloten polis gemeld"
            ],
            "suspicious_patterns": [
                "Vage beschrijving zonder details",
                "Strategisch bedrag net onder threshold"
            ],
            "recommendation": "Auto-approve mogelijk (bij andere criteria OK)" | 
                            "Manual review aanbevolen" | 
                            "SIU investigation vereist",
            "reasoning": "Gedetailleerde uitleg: welke checks zijn uitgevoerd, 
                         welke patronen zijn gedetecteerd, hoe de score is opgebouwd,
                         waarom wel/geen rode vlaggen, en de totale risk assessment."
        }}
        
        BELANGRIJK VOOR SCORE BUILDING:
        
        ✅ BIJ NORMALE CLAIMS:
        - Volledige details aanwezig → 0 punten completeness
        - Geen timing signalen → 0 punten timing
        - Normaal bedrag → 0 punten amount
        - Geen inconsistenties → 0 punten inconsistencies
        - **TOTAAL: 0.0-0.2 (Low risk)**
        
        ⚠️ BIJ VERDACHTE CLAIMS:
        - Meerdere details ontbreken → 0.3-0.4 punten
        - Timing red flags → +0.2-0.25 punten
        - Strategisch bedrag → +0.2 punten
        - Inconsistenties → +0.15-0.25 punten
        - **TOTAAL: 0.6+ (High risk)**
        
        BELANGRIJK:
        - Wees NIET paranoia - normale claims krijgen lage scores
        - Wees WEL alert - echte red flags moet je oppakken
        - red_flags lijst bevat specifieke problemen gevonden
        - suspicious_patterns zijn subtielere zorgen
        - reasoning moet helder uitleggen hoe je tot de score komt
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met fraud risk analysis volgens FraudRiskAnalysis model"
        )
