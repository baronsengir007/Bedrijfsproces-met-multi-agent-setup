"""
Agent 1: Claim Type Classifier

Classifies insurance claims into Auto, Woning, Inboedel, or Aansprakelijkheid.
Also extracts policy number and incident date when available.
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, AGENT_SETTINGS, CLAIM_TYPES
from models import ClaimType


class ClaimTypeClassifierAgent:
    """
    Agent 1: Classifies insurance claim types
    
    Specialization: Identifying claim category and extracting structured data
    Output: ClaimType (Pydantic model)
    """
    
    def __init__(self):
        """Initialize the claim type classifier agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with configuration"""
        config = AGENT_CONFIG["claim_type_classifier"]
        
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
        Create a classification task for the given claim
        
        Args:
            claim_text: The insurance claim text to classify
            
        Returns:
            Task: CrewAI task object
        """
        
        claim_types_str = ", ".join(CLAIM_TYPES)
        
        description = f"""
        TAAK: Classificeer de volgende verzekeringsclaim in één van deze categorieën:
        {claim_types_str}
        
        CLAIM TEKST:
        ---
        {claim_text}
        ---
        
        CLASSIFICATIE RICHTLIJNEN:
        
        **Auto:**
        - Keywords: aanrijding, autoschade, bumper, koplamp, kenteken, parkeerplaats, 
          rijden, WA verzekering, voertuig, auto
        - Kenmerken: Schade aan motorvoertuigen, verkeersongelukken
        
        **Woning:**
        - Keywords: brand, waterschade, lekkage, storm, stormschade, dak, gevel, 
          woning, huis, appartement, gebouw
        - Kenmerken: Schade aan gebouwen en woningen
        
        **Inboedel:**
        - Keywords: inbraak, diefstal, gestolen, laptop, inventaris, meubels, 
          inboedel, spullen, bezittingen
        - Kenmerken: Schade aan of verlies van persoonlijke eigendommen binnen de woning
        
        **Aansprakelijkheid:**
        - Keywords: schade veroorzaakt, aansprakelijk, schade aan, derde partij, 
          WA schade, iemand anders, andermans
        - Kenmerken: Schade die de verzekerde heeft veroorzaakt aan derden
        
        EXTRACTIE:
        - Zoek naar POLISNUMMER: vaak in format "AUTO-2024-12345", "POL12345", 
          "Polis: 123456", etc.
        - Zoek naar INCIDENT DATUM: "30 september 2025", "gisteren", "vorige week", 
          etc. → Converteer naar YYYY-MM-DD format
        
        CONFIDENCE SCORE:
        - 0.9-1.0: Zeer duidelijk (meerdere specifieke keywords + context)
        - 0.7-0.9: Duidelijk (enkele specifieke keywords)
        - 0.5-0.7: Waarschijnlijk (algemene keywords, context suggereert type)
        - 0.0-0.5: Onduidelijk (weinig of vage indicatoren)
        
        OUTPUT FORMAT (JSON):
        Geef ALLEEN een JSON object terug in dit exacte format:
        
        {{
            "type": "Auto" | "Woning" | "Inboedel" | "Aansprakelijkheid",
            "confidence": 0.95,
            "keywords": ["keyword1", "keyword2", "keyword3"],
            "policy_number": "AUTO-2024-12345" of null,
            "incident_date": "2025-09-30" of null,
            "reasoning": "Gedetailleerde uitleg waarom dit type gekozen is, welke keywords 
                         doorslaggevend waren, en waarom de confidence score op dit niveau is."
        }}
        
        BELANGRIJK:
        - Gebruik ALLEEN de 4 types hierboven
        - Confidence moet tussen 0.0 en 1.0 liggen
        - Keywords moeten daadwerkelijk uit de tekst komen
        - Reasoning moet helder uitleggen waarom
        - Als datum relatief is ("gisteren"), converteer naar absolute datum
        - Als policy nummer niet gevonden: null
        - Als datum niet gevonden: null
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met claim type classificatie volgens ClaimType model"
        )
