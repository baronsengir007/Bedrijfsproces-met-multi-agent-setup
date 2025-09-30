"""
Agent 2: Urgency Analyzer
Bepaalt urgentie en tijdgevoeligheid van emails
Draait PARALLEL met Agent 1 en 3
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, MODEL_NAME, URGENCY_LEVELS
from models import UrgencyAnalysis
from datetime import datetime


class UrgencyAnalyzerAgent:
    """
    Agent die urgentie en deadlines analyseert:
    - Critical: Moet binnen 1-2 uur
    - High: Moet vandaag
    - Medium: Moet binnen 48 uur
    - Low: Kan wachten
    
    Output: UrgencyAnalysis (Pydantic model)
    """
    
    def __init__(self):
        """Initialize the urgency analyzer agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with proper configuration"""
        config = AGENT_CONFIG["urgency"]
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=True,
            allow_delegation=False,
            llm=MODEL_NAME
        )
    
    def create_task(self, email_text: str) -> Task:
        """
        Create an urgency analysis task for the given email
        
        Args:
            email_text: The email content to analyze
            
        Returns:
            Task: CrewAI task object
        """
        urgency_str = ", ".join(URGENCY_LEVELS)
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        description = f"""
        Analyseer de urgentie en tijdgevoeligheid van de volgende email.
        
        VANDAAG IS: {current_date}
        
        EMAIL OM TE ANALYSEREN:
        ---
        {email_text}
        ---
        
        URGENCY LEVELS:
        - Critical: Systeem down, blocker, "nu meteen", expliciete crisis
        - High: "Vandaag", "zo snel mogelijk", belangrijke deadline binnen 24 uur
        - Medium: Deadline binnen 2-3 dagen, normaal verzoek met enige tijdsdruk
        - Low: Geen tijdsdruk, algemene vraag, "wanneer het uitkomt"
        
        LET OP:
        1. EXPLICIETE TIJDSINDICATOREN:
           - "urgent", "spoed", "asap", "zo snel mogelijk"
           - Specifieke deadlines: "voor vrijdag", "uiterlijk 15 januari"
           - Tijdsaanduidingen: "vandaag", "morgen", "deze week"
        
        2. IMPLICIETE URGENTIE SIGNALEN:
           - Hoofdletters, uitroeptekens (!!!)
           - Herhaald contact ("Dit is mijn 3e email")
           - Bedreigingen ("anders schakel ik een advocaat in")
           - Business impact ("kan niet werken", "project staat stil")
        
        3. VALSE URGENTIE:
           - Mensen die zeggen "urgent" maar het niet is
           - Marketing emails die "Limited time!" roepen
           - Algemene vragen zonder echte tijdsdruk
        
        4. DEADLINE DETECTIE:
           - Zoek naar datums in formaten: DD-MM-YYYY, DD/MM, "15 januari"
           - Zoek naar "voor [datum]", "uiterlijk [datum]", "deadline [datum]"
           - Bereken dagen tot deadline
        
        VERPLICHTE OUTPUT FORMAT (JSON):
        {{
            "urgency_level": "één van: {urgency_str}",
            "has_deadline": true/false,
            "deadline_date": "YYYY-MM-DD of null",
            "time_sensitive_keywords": ["lijst", "van", "urgency", "keywords"],
            "recommended_response_time": aantal uren (integer),
            "reasoning": "Uitleg waarom dit urgency level, wat zijn de indicatoren"
        }}
        
        RECOMMENDED RESPONSE TIME GUIDELINES:
        - Critical: 1-2 uur
        - High: 4-8 uur
        - Medium: 24 uur
        - Low: 48-72 uur
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met urgency analysis"
        )
