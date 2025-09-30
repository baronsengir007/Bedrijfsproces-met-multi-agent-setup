"""
CrewAI Orchestration voor Email Handler System
Coördineert de 3 agents in een workflow
"""

from crewai import Crew, Process
from agents import EmailClassifierAgent, SentimentAnalyzerAgent, ResponseGeneratorAgent


class EmailHandlerCrew:
    """
    Orchestreert de multi-agent workflow:
    1. Classifier Agent: Categoriseert de email
    2. Sentiment Agent: Analyseert sentiment
    3. Responder Agent: Genereert antwoord
    """
    
    def __init__(self):
        """Initialize all agents"""
        self.classifier = EmailClassifierAgent()
        self.sentiment_analyzer = SentimentAnalyzerAgent()
        self.response_generator = ResponseGeneratorAgent()
    
    def process_email(self, email_text: str) -> dict:
        """
        Process een email door de volledige agent pipeline
        
        Args:
            email_text: De email tekst om te verwerken
            
        Returns:
            dict: Resultaten met category, sentiment en response
        """
        
        # Task 1: Classify email
        classify_task = self.classifier.create_task(email_text)
        
        # Task 2: Analyze sentiment (depends on classification)
        sentiment_task = self.sentiment_analyzer.create_task(
            email_text, 
            category="{classify_task.output}"
        )
        
        # Task 3: Generate response (depends on both previous tasks)
        response_task = self.response_generator.create_task(
            email_text,
            category="{classify_task.output}",
            sentiment="{sentiment_task.output}"
        )
        
        # Create crew with sequential process
        crew = Crew(
            agents=[
                self.classifier.agent,
                self.sentiment_analyzer.agent,
                self.response_generator.agent
            ],
            tasks=[
                classify_task,
                sentiment_task,
                response_task
            ],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        try:
            result = crew.kickoff()
            
            # Parse results
            return {
                'category': classify_task.output.raw if hasattr(classify_task, 'output') else 'Onbekend',
                'sentiment': sentiment_task.output.raw if hasattr(sentiment_task, 'output') else 'Onbekend',
                'response': result.raw if hasattr(result, 'raw') else str(result)
            }
            
        except Exception as e:
            print(f"Error in crew execution: {e}")
            return {
                'category': 'Error',
                'sentiment': 'Error',
                'response': f'Er ging iets mis bij het verwerken van de email: {str(e)}'
            }


# Test function for command line usage
def main():
    """Test the crew with example emails"""
    
    test_emails = [
        """
        Beste klantenservice,
        
        Ik ben zeer ontevreden over jullie product. Het werkt niet zoals beloofd
        en ik heb al 3 keer contact opgenomen zonder oplossing. Dit is echt
        onacceptabel!
        
        Ik verwacht snel een reactie.
        
        Met vriendelijke groet,
        Jan Jansen
        """,
        
        """
        Hallo,
        
        Ik zou graag meer informatie ontvangen over jullie diensten.
        Kunnen jullie mij een prijsopgave sturen?
        
        Bedankt alvast!
        
        Groeten,
        Maria
        """
    ]
    
    crew = EmailHandlerCrew()
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n{'='*60}")
        print(f"TEST EMAIL {i}")
        print(f"{'='*60}")
        print(email)
        print(f"\n{'='*60}")
        print("PROCESSING...")
        print(f"{'='*60}\n")
        
        result = crew.process_email(email)
        
        print(f"Category: {result['category']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"\nResponse:\n{result['response']}")
        print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
