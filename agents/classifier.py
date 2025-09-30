"""
Agent 1: Email Classifier
Classificeert emails in voorgedefinieerde categorieën
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, MODEL_NAME, CATEGORIES


class EmailClassifierAgent:
    """
    Agent die emails classificeert in categorieën zoals:
    - Spam
    - Klacht
    - Verzoek
    - Informatieaanvraag
    - Feedback
    - Overig
    """
    
    def __init__(self):
        """Initialize the classifier agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with proper configuration"""
        config = AGENT_CONFIG["classifier"]
        
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
        Analyseer de volgende email en classificeer deze in één van de volgende categorieën:
        {categories_str}
        
        Email om te analyseren:
        ---
        {email_text}
        ---
        
        Geef ALLEEN de categorie terug als output, niets anders.
        
        Richtlijnen:
        - Spam: Ongewenste marketing, phishing, of irrelevante content
        - Klacht: Uitingen van ontevredenheid of problemen
        - Verzoek: Vragen om actie of hulp
        - Informatieaanvraag: Vragen om informatie of uitleg
        - Feedback: Positieve of constructieve terugkoppeling
        - Overig: Emails die niet in bovenstaande categorieën passen
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output=f"Een enkele categorie uit: {categories_str}"
        )
