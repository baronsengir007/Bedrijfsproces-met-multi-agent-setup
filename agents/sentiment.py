"""
Agent 2: Sentiment Analyzer
Analyseert het sentiment en de emotionele toon van emails
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, MODEL_NAME, SENTIMENTS


class SentimentAnalyzerAgent:
    """
    Agent die het sentiment van emails analyseert:
    - Positive (vriendelijk, positief, opbouwend)
    - Neutral (zakelijk, neutraal)
    - Negative (boos, gefrustreerd, ontevreden)
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
    
    def create_task(self, email_text: str, category: str) -> Task:
        """
        Create a sentiment analysis task for the given email
        
        Args:
            email_text: The email content to analyze
            category: The classified category (from Agent 1)
            
        Returns:
            Task: CrewAI task object
        """
        sentiments_str = ", ".join(SENTIMENTS)
        
        description = f"""
        Analyseer het sentiment van de volgende email.
        Deze email is geclassificeerd als: {category}
        
        Email om te analyseren:
        ---
        {email_text}
        ---
        
        Bepaal het sentiment: {sentiments_str}
        
        Geef ALLEEN het sentiment terug als output, niets anders.
        
        Richtlijnen:
        - Positive: Vriendelijke toon, dankbaar, opbouwend, tevreden
        - Neutral: Zakelijke toon, informatief, geen sterke emoties
        - Negative: Boze toon, gefrustreerd, ontevreden, veeleisend
        
        Let op nuances:
        - Een klacht kan positief geformuleerd zijn
        - Een verzoek kan dringend maar niet negatief zijn
        - Spam is meestal neutraal (tenzij aggressive marketing)
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output=f"Een enkel sentiment uit: {sentiments_str}",
            context=[category]
        )
