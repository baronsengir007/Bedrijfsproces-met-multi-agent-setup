"""
Agent 3: Sentiment & Emotion Analyzer
Analyseert emotionele toon en escalatierisico's
Draait PARALLEL met Agent 1 en 2
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, MODEL_NAME, SENTIMENTS
from models import SentimentAnalysis


class SentimentAnalyzerAgent:
    """
    Agent die sentiment en emoties analyseert:
    - Positive: Vriendelijk, tevreden, dankbaar
    - Neutral: Zakelijk, informatief, neutraal
    - Negative: Ontevreden, gefrustreerd
    - Very_Negative: Boos, woedend, dreigend
    
    Ook detecteert:
    - Escalation risk (churn risk, legal threat, PR risk)
    - Customer satisfaction indicators
    
    Output: SentimentAnalysis (Pydantic model)
    """
    
    def __init__(self):
        """Initialize the sentiment analyzer agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with proper configuration"""
        config = AGENT_CONFIG["sentiment"]
        
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
        Create a sentiment analysis task for the given email
        
        Args:
            email_text: The email content to analyze
            
        Returns:
            Task: CrewAI task object
        """
        sentiments_str = ", ".join(SENTIMENTS)
        
        description = f"""
        Analyseer het sentiment en de emotionele toon van de volgende email.
        
        EMAIL OM TE ANALYSEREN:
        ---
        {email_text}
        ---
        
        SENTIMENT CATEGORIEËN:
        - Positive: Vriendelijk, tevreden, dankbaar, enthousiast, positief
        - Neutral: Zakelijk, informatief, neutraal, geen sterke emoties
        - Negative: Ontevreden, gefrustreerd, teleurgesteld, kritisch
        - Very_Negative: Boos, woedend, dreigend, zeer ontevreden
        
        EMOTIONELE SIGNALEN:
        
        1. TONE INDICATORS (Let op):
           - Hoofdletters = SCHREEUWEN / boos
           - Uitroeptekens!!! = frustratie of enthousiasme
           - Sarcasme = vaak negatief sentiment
           - Formele taal = vaak neutraal
           - Persoonlijke toon = kan positief of negatief zijn
        
        2. WOORD KEUZE:
           Positive: "dank", "geweldig", "tevreden", "blij", "uitstekend"
           Negative: "teleurgesteld", "onacceptabel", "slecht", "nooit meer"
           Very_Negative: "schandalig", "rechtszaak", "advocaat", "oplichters"
        
        3. ESCALATION RISK INDICATORS:
           - Dreigingen: "advocaat", "rechtszaak", "aangifte", "klacht indienen"
           - Churn signals: "contract opzeggen", "concurrent", "nooit meer"
           - Public shaming: "social media", "reviews", "iedereen waarschuwen"
           - Herhaald contact: "al 5x gebeld", "niemand reageert"
        
        4. CUSTOMER SATISFACTION LEVELS:
           - Tevreden: Complimenten, positieve feedback, blijft klant
           - Neutraal: Zakelijke vraag, geen emotie
           - Ontevreden: Klacht maar beheerst, wil oplossing
           - Zeer_Ontevreden: Woede, geen vertrouwen meer, wil weg
        
        5. NUANCES:
           - Een klacht kan vriendelijk geformuleerd zijn (Negative sentiment, maar beleefde toon)
           - Sarcasme is bijna altijd negatief
           - "Met vriendelijke groet" na woedende email = nog steeds Very_Negative
           - Urgentie ≠ negatief sentiment
        
        EMOTION SCORE BEREKENING:
        - +1.0: Zeer positief, enthousiast, dankbaar
        - +0.5: Positief, tevreden
        - 0.0: Neutraal, zakelijk
        - -0.5: Negatief, ontevreden
        - -1.0: Zeer negatief, woedend
        
        VERPLICHTE OUTPUT FORMAT (JSON):
        {{
            "sentiment": "één van: {sentiments_str}",
            "emotion_score": -1.0 tot +1.0 (float),
            "escalation_risk": true/false,
            "tone_indicators": ["lijst", "van", "emotionele", "keywords"],
            "customer_satisfaction_indicator": "Tevreden/Neutraal/Ontevreden/Zeer_Ontevreden",
            "reasoning": "Uitleg sentiment analyse: welke signalen zag je, waarom dit niveau"
        }}
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met sentiment analysis"
        )
