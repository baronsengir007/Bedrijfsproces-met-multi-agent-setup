"""
Agent 1: Email Categorizer
Classificeert emails in voorgedefinieerde categorieën
Draait PARALLEL met Agent 2 en 3
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, MODEL_NAME, CATEGORIES
from models import EmailCategory


class CategorizerAgent:
    """
    Agent die emails classificeert in categorieën zoals:
    - Spam
    - Klacht
    - Verzoek
    - Informatieaanvraag
    - Feedback
    - Overig
    
    Output: EmailCategory (Pydantic model)
    """
    
    def __init__(self):
        """Initialize the categorizer agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with proper configuration"""
        config = AGENT_CONFIG["categorizer"]
        
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
        Create a classification task for the given email
        
        Args:
            email_text: The email content to classify
            
        Returns:
            Task: CrewAI task object
        """
        categories_str = ", ".join(CATEGORIES)
        
        description = f"""
        Analyseer de volgende email en classificeer deze in één van de categorieën.
        
        CATEGORIEËN:
        {categories_str}
        
        EMAIL OM TE ANALYSEREN:
        ---
        {email_text}
        ---
        
        RICHTLIJNEN:
        - Spam: Ongewenste marketing, phishing, of irrelevante content
        - Klacht: Uitingen van ontevredenheid, problemen, klachten over service/product
        - Verzoek: Vragen om actie, hulp, of service (opzeggen, wijzigen, etc)
        - Informatieaanvraag: Vragen om informatie, uitleg, of documentatie
        - Feedback: Positieve of constructieve terugkoppeling, complimenten
        - Overig: Emails die niet in bovenstaande categorieën passen
        
        BELANGRIJKE OVERWEGINGEN:
        - Let op de hoofdintentie van de email
        - Een klacht kan vriendelijk geformuleerd zijn, maar is nog steeds een klacht
        - Een verzoek is specifiek (doe X), informatieaanvraag is algemeen (leg Y uit)
        - Kijk naar keywords maar ook naar context en toon
        
        VERPLICHTE OUTPUT FORMAT (JSON):
        {{
            "category": "één van de categorieën hierboven",
            "confidence": 0.0-1.0 (hoe zeker ben je?),
            "keywords": ["lijst", "van", "keywords", "die", "je", "hielpen"],
            "reasoning": "Korte uitleg waarom je deze categorie hebt gekozen"
        }}
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met category, confidence, keywords en reasoning"
        )
