"""
Agent 5: Response Generator
Genereert email antwoorden op basis van routing beslissing
Gebruikt output van Agent 4 (routing decision)
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, MODEL_NAME, RESPONSE_TEMPLATES
from models import EmailResponse


class ResponseGeneratorAgent:
    """
    Agent die professionele email antwoorden genereert.
    
    Input: Routing decision van Agent 4
    Output: EmailResponse (Pydantic model)
    
    Past tone en inhoud aan op basis van:
    - Routing team (wie gaat reageren?)
    - Priority level
    - Escalation status
    - Original email sentiment & category
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
    
    def create_task(
        self,
        email_text: str,
        category: str,
        sentiment: str,
        routing_decision: str
    ) -> Task:
        """
        Create a response generation task
        
        Args:
            email_text: Original email
            category: Category from Agent 1
            sentiment: Sentiment from Agent 3
            routing_decision: Routing decision from Agent 4 (JSON)
            
        Returns:
            Task: CrewAI task object
        """
        # Get template if available
        template = RESPONSE_TEMPLATES.get(category, "")
        
        description = f"""
        Genereer een professioneel en passend antwoord op de email.
        
        CONTEXT INFORMATIE:
        
        ORIGINELE EMAIL:
        ---
        {email_text}
        ---
        
        EMAIL CATEGORIE: {category}
        EMAIL SENTIMENT: {sentiment}
        
        ROUTING BESLISSING (van Agent 4):
        {routing_decision}
        
        ================================================================
        RESPONSE GENERATIE INSTRUCTIES:
        ================================================================
        
        1. TONE AANPASSEN OP BASIS VAN SENTIMENT:
        
        Positive sentiment:
        - Vriendelijk en enthousiast
        - Bedank voor positieve feedback
        - Persoonlijke touch
        
        Neutral sentiment:
        - Zakelijk en informatief
        - Helder en to-the-point
        - Professioneel
        
        Negative sentiment:
        - Empathisch en begripvol
        - Erken het probleem
        - Oplossingsgericht
        - Toon dat je serieus neemt
        
        Very_Negative sentiment:
        - Extra empathisch
        - ALTIJD excuses
        - Directe actie/oplossing
        - Escalatie vermelden indien nodig
        - Manager/senior team involvement noemen
        
        2. AANPAK PER CATEGORIE:
        
        Klacht:
        - Start met excuses (als gerechtvaardigd)
        - Erken het probleem specifiek
        - Leg uit wat er fout ging (als relevant)
        - Bied concrete oplossing
        - Vermeld follow-up
        
        Verzoek:
        - Bevestig ontvangst verzoek
        - Geef duidelijk antwoord/status
        - Verwerk het verzoek of leg uit wat nodig is
        - Geef timeline als relevant
        
        Informatieaanvraag:
        - Beantwoord de vraag compleet
        - Wees helder en specifiek
        - Bied extra informatie aan indien relevant
        - Nodig uit voor verdere vragen
        
        Feedback:
        - Bedank hartelijk
        - Toon waardering
        - Vertel wat je met feedback gaat doen
        - Persoonlijke touch
        
        Spam:
        - Kort en zakelijk
        - Wijs af
        - Verwijs naar juiste kanalen indien nodig
        
        3. SPECIALE OVERWEGINGEN:
        
        Als requires_escalation = true:
        - Vermeld dat het wordt doorgegeven aan senior team/management
        - Geef gevoel van serieuze aandacht
        - Noem specifieke follow-up
        
        Als priority = 1 of 2:
        - Benadruk snelle actie
        - Geef concrete timeline
        - Toon urgentie begrip
        
        Als risk_flags aanwezig:
        - Extra voorzichtig met formuleren
        - Geen beloftes die niet kunnen worden waargemaakt
        - Bij legal: neutrale toon, verwijs naar formele procedure
        
        4. RESPONSE STRUCTUUR:
        
        Aanhef:
        - "Beste [naam]," (als naam bekend)
        - "Geachte heer/mevrouw," (formeel)
        - "Hallo [naam]," (vriendelijk, als positief)
        
        Intro:
        - Bedank voor email/contact
        - Erken ontvangst verzoek/klacht
        
        Body:
        - Beantwoord hoofdvraag
        - Bied oplossing/informatie
        - Wees specifiek en concreet
        
        Afsluiting:
        - Nodig uit voor verdere vragen
        - Geef follow-up info indien relevant
        - Groet passend bij tone
        
        Handtekening:
        - "[Teamname] Team" (Junior/Senior CS, Technical Support, etc)
        - Of "Met vriendelijke groet"
        
        5. DONT's:
        - Geen jargon of vaktermen (tenzij technical support)
        - Geen lange, complexe zinnen
        - Geen vage antwoorden
        - Niet defensief (ook niet bij onterechte klacht)
        - Geen beloftes die niet kunnen worden waargemaakt
        - Geen blame op andere teams/collega's
        
        6. DO's:
        - Wees specifiek en concreet
        - Persoonlijk maar professioneel
        - Proactief (anticipeer vervolgvragen)
        - Empathisch en respectvol
        - Oplossingsger icht
        - Call-to-action helder (wat moet klant doen, wat doen wij)
        
        {f"TEMPLATE ALS INSPIRATIE:\\n{template}" if template else ""}
        
        VERPLICHTE OUTPUT FORMAT (JSON):
        {{
            "response_text": "De complete email response (met aanhef, body, afsluiting)",
            "tone": "Formal/Friendly/Apologetic/Professional/Empathetic",
            "response_type": "Full_Answer/Acknowledgment/Escalation_Notice/Request_More_Info",
            "includes_apology": true/false,
            "includes_solution": true/false,
            "follow_up_required": true/false,
            "follow_up_date": "YYYY-MM-DD of null",
            "cc_manager": true/false (als escalatie of high priority)
        }}
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met email response",
            context=[routing_decision]
        )
