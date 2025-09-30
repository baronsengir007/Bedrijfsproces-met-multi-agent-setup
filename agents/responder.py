"""
Agent 3: Response Generator
Genereert passende email antwoorden op basis van classificatie en sentiment
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, MODEL_NAME, RESPONSE_TEMPLATES


class ResponseGeneratorAgent:
    """
    Agent die professionele email antwoorden genereert.
    Past de tone en inhoud aan op basis van:
    - Email categorie (Klacht, Verzoek, etc)
    - Sentiment (Positive, Neutral, Negative)
    """
    
    def __init__(self):
        """Initialize the response generator agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with proper configuration"""
        config = AGENT_CONFIG["responder"]
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=True,
            allow_delegation=False,
            llm=MODEL_NAME
        )
    
    def create_task(self, email_text: str, category: str, sentiment: str) -> Task:
        """
        Create a response generation task
        
        Args:
            email_text: The original email content
            category: The classified category
            sentiment: The detected sentiment
            
        Returns:
            Task: CrewAI task object
        """
        # Get template if available
        template = RESPONSE_TEMPLATES.get(category, "")
        
        description = f"""
        Genereer een professioneel en passend antwoord op de volgende email.
        
        CONTEXT:
        - Categorie: {category}
        - Sentiment: {sentiment}
        
        ORIGINELE EMAIL:
        ---
        {email_text}
        ---
        
        INSTRUCTIES:
        1. Schrijf een compleet email antwoord (met aanhef en afsluiting)
        2. Pas de tone aan op basis van het sentiment:
           - Positive: Vriendelijk en enthousiast
           - Neutral: Zakelijk en informatief
           - Negative: Empathisch en oplossingsgericht
        
        3. Zorg voor de juiste aanpak per categorie:
           - Spam: Kort afwijzend bericht (indien nodig)
           - Klacht: Empathisch, erken het probleem, bied oplossing
           - Verzoek: Informatief, geef duidelijk antwoord
           - Informatieaanvraag: Helder en compleet antwoord
           - Feedback: Bedank en toon waardering
           - Overig: Passend bij context
        
        4. Houd het professioneel maar menselijk
        5. Vermijd jargon en complexe zinnen
        6. Wees concreet waar mogelijk
        
        {f"TEMPLATE ALS INSPIRATIE:\\n{template}" if template else ""}
        
        Geef ALLEEN het email antwoord terug, geen extra uitleg.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="Een compleet, professioneel email antwoord",
            context=[category, sentiment]
        )
