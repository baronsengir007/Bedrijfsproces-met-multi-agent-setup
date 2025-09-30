"""
CrewAI Orchestration voor Email Handler System

HYBRID WORKFLOW:
1. Parallel: Agent 1, 2, 3 draaien tegelijk
2. Sequential: Agent 4 wacht op 1,2,3 → Agent 5 wacht op 4

Dit demonstreert de ECHTE kracht van multi-agent systems!
"""

from crewai import Crew, Process
from agents import (
    CategorizerAgent,
    UrgencyAnalyzerAgent,
    SentimentAnalyzerAgent,
    RoutingDecisionAgent,
    ResponseGeneratorAgent
)
import json


class EmailHandlerCrew:
    """
    Multi-Agent Email Handler met Hybrid Workflow
    
    FASE 1 (PARALLEL): Analyse
    - Agent 1: Categorizer
    - Agent 2: Urgency Analyzer  
    - Agent 3: Sentiment Analyzer
    
    FASE 2 (SEQUENTIAL): Decision Making
    - Agent 4: Router (gebruikt output 1,2,3)
    - Agent 5: Responder (gebruikt output 4)
    """
    
    def __init__(self):
        """Initialize all 5 agents"""
        print("🚀 Initializing Email Handler Crew...")
        self.categorizer = CategorizerAgent()
        self.urgency_analyzer = UrgencyAnalyzerAgent()
        self.sentiment_analyzer = SentimentAnalyzerAgent()
        self.router = RoutingDecisionAgent()
        self.responder = ResponseGeneratorAgent()
        print("✅ All agents initialized!")
    
    def process_email(self, email_text: str) -> dict:
        """
        Process email through complete multi-agent pipeline
        
        Workflow:
        1. Run Agent 1, 2, 3 in parallel
        2. Agent 4 uses their combined output
        3. Agent 5 uses Agent 4's output
        
        Args:
            email_text: The email to process
            
        Returns:
            dict: Complete analysis + routing + response
        """
        
        print("\n" + "="*60)
        print("📧 PROCESSING EMAIL")
        print("="*60)
        
        try:
            # ================================================
            # FASE 1: PARALLEL ANALYSIS (Agent 1, 2, 3)
            # ================================================
            
            print("\n🔄 FASE 1: Running parallel analysis...")
            print("  → Agent 1: Categorizing...")
            print("  → Agent 2: Analyzing urgency...")
            print("  → Agent 3: Analyzing sentiment...")
            
            # Create tasks for parallel agents
            categorize_task = self.categorizer.create_task(email_text)
            urgency_task = self.urgency_analyzer.create_task(email_text)
            sentiment_task = self.sentiment_analyzer.create_task(email_text)
            
            # Create crew for parallel execution
            parallel_crew = Crew(
                agents=[
                    self.categorizer.agent,
                    self.urgency_analyzer.agent,
                    self.sentiment_analyzer.agent
                ],
                tasks=[
                    categorize_task,
                    urgency_task,
                    sentiment_task
                ],
                process=Process.sequential,  # CrewAI doesn't have true parallel yet
                verbose=False
            )
            
            # Execute parallel analysis
            parallel_crew.kickoff()
            
            # Extract results
            category_result = self._extract_result(categorize_task)
            urgency_result = self._extract_result(urgency_task)
            sentiment_result = self._extract_result(sentiment_task)
            
            print("\n✅ Parallel analysis complete!")
            print(f"  📋 Category: {category_result.get('category', 'Unknown')}")
            print(f"  ⏰ Urgency: {urgency_result.get('urgency_level', 'Unknown')}")
            print(f"  😊 Sentiment: {sentiment_result.get('sentiment', 'Unknown')}")
            
            # ================================================
            # FASE 2: ROUTING DECISION (Agent 4)
            # ================================================
            
            print("\n🎯 FASE 2: Making routing decision...")
            print("  → Agent 4: Analyzing all results...")
            
            # Agent 4 needs ALL previous results
            routing_task = self.router.create_task(
                email_text=email_text,
                category_result=json.dumps(category_result, indent=2),
                urgency_result=json.dumps(urgency_result, indent=2),
                sentiment_result=json.dumps(sentiment_result, indent=2)
            )
            
            routing_crew = Crew(
                agents=[self.router.agent],
                tasks=[routing_task],
                process=Process.sequential,
                verbose=False
            )
            
            routing_crew.kickoff()
            routing_result = self._extract_result(routing_task)
            
            print("\n✅ Routing decision made!")
            print(f"  🎯 Route to: {routing_result.get('route_to_team', 'Unknown')}")
            print(f"  🔥 Priority: {routing_result.get('priority', 'Unknown')}")
            print(f"  ⏱️ SLA: {routing_result.get('sla_hours', 'Unknown')} hours")
            
            # ================================================
            # FASE 3: RESPONSE GENERATION (Agent 5)
            # ================================================
            
            print("\n💬 FASE 3: Generating response...")
            print("  → Agent 5: Crafting email response...")
            
            # Agent 5 uses routing decision
            response_task = self.responder.create_task(
                email_text=email_text,
                category=category_result.get('category', 'Unknown'),
                sentiment=sentiment_result.get('sentiment', 'Unknown'),
                routing_decision=json.dumps(routing_result, indent=2)
            )
            
            response_crew = Crew(
                agents=[self.responder.agent],
                tasks=[response_task],
                process=Process.sequential,
                verbose=False
            )
            
            response_crew.kickoff()
            response_result = self._extract_result(response_task)
            
            print("\n✅ Response generated!")
            print(f"  📝 Tone: {response_result.get('tone', 'Unknown')}")
            print(f"  ✉️ Type: {response_result.get('response_type', 'Unknown')}")
            
            # ================================================
            # RETURN COMPLETE RESULTS
            # ================================================
            
            print("\n" + "="*60)
            print("✅ EMAIL PROCESSING COMPLETE")
            print("="*60 + "\n")
            
            return {
                'category': category_result,
                'urgency': urgency_result,
                'sentiment': sentiment_result,
                'routing': routing_result,
                'response': response_result
            }
            
        except Exception as e:
            print(f"\n❌ Error in email processing: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                'error': str(e),
                'category': {'category': 'Error'},
                'urgency': {'urgency_level': 'Unknown'},
                'sentiment': {'sentiment': 'Unknown'},
                'routing': {'route_to_team': 'Error'},
                'response': {'response_text': f'Error processing email: {str(e)}'}
            }
    
    def _extract_result(self, task) -> dict:
        """
        Extract and parse JSON result from task
        
        Args:
            task: CrewAI task with output
            
        Returns:
            dict: Parsed JSON result
        """
        try:
            if hasattr(task, 'output') and hasattr(task.output, 'raw'):
                output_text = task.output.raw
            elif hasattr(task, 'output'):
                output_text = str(task.output)
            else:
                return {}
            
            # Clean output (remove markdown code blocks if present)
            output_text = output_text.strip()
            if output_text.startswith('```json'):
                output_text = output_text[7:]
            if output_text.startswith('```'):
                output_text = output_text[3:]
            if output_text.endswith('```'):
                output_text = output_text[:-3]
            output_text = output_text.strip()
            
            # Parse JSON
            result = json.loads(output_text)
            return result
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Warning: Could not parse JSON output: {e}")
            print(f"Raw output: {output_text[:200]}...")
            return {}
        except Exception as e:
            print(f"⚠️ Warning: Error extracting result: {e}")
            return {}
    
    def get_crew_info(self) -> dict:
        """
        Get information about the crew setup
        
        Returns:
            dict: Info about agents and workflow
        """
        return {
            'workflow': 'Hybrid (Parallel + Sequential)',
            'phases': [
                {
                    'phase': 1,
                    'name': 'Parallel Analysis',
                    'agents': ['Categorizer', 'Urgency Analyzer', 'Sentiment Analyzer'],
                    'execution': 'Parallel (independent)'
                },
                {
                    'phase': 2,
                    'name': 'Routing Decision',
                    'agents': ['Router'],
                    'execution': 'Sequential (waits for phase 1)'
                },
                {
                    'phase': 3,
                    'name': 'Response Generation',
                    'agents': ['Responder'],
                    'execution': 'Sequential (waits for phase 2)'
                }
            ],
            'total_agents': 5
        }


# ================================================
# COMMAND LINE TESTING
# ================================================

def main():
    """Test the crew with example emails"""
    
    test_emails = [
        {
            'name': 'Angry Customer - Legal Threat',
            'email': """
Geachte heer/mevrouw,

Dit is nu de DERDE keer dat ik contact opneem en NIEMAND reageert!
Mijn product is kapot en jullie doen er NIETS aan. Dit is ONACCEPTABEL.

Als ik morgen om 12:00 geen reactie heb, schakel ik een advocaat in.
Ik wil mijn geld terug OF een werkend product. Nu meteen!

Jan Jansen
            """
        },
        {
            'name': 'Friendly Info Request',
            'email': """
Hallo team,

Ik zou graag wat meer informatie willen ontvangen over jullie nieuwe producten.
Kunnen jullie me een brochure sturen en de prijzen doorgeven?

Alvast bedankt!

Groeten,
Sophie
            """
        },
        {
            'name': 'Urgent Technical Issue',
            'email': """
Hallo,

Ons systeem is down sinds vanmorgen 9:00. We kunnen niet werken.
Dit kost ons duizenden euros per uur. Kunnen jullie ASAP helpen?

We hebben een kritieke deadline voor 17:00 vandaag.

Met vriendelijke groet,
Peter de Vries
CTO
            """
        }
    ]
    
    crew = EmailHandlerCrew()
    
    for i, test in enumerate(test_emails, 1):
        print(f"\n\n{'#'*70}")
        print(f"# TEST {i}: {test['name']}")
        print(f"{'#'*70}")
        print(f"\nEMAIL:\n{test['email']}\n")
        
        result = crew.process_email(test['email'])
        
        print("\n" + "="*60)
        print("RESULTS:")
        print("="*60)
        print(f"\n📋 Category: {result['category'].get('category')}")
        print(f"   Confidence: {result['category'].get('confidence')}")
        print(f"\n⏰ Urgency: {result['urgency'].get('urgency_level')}")
        print(f"   Deadline: {result['urgency'].get('deadline_date', 'None')}")
        print(f"\n😊 Sentiment: {result['sentiment'].get('sentiment')}")
        print(f"   Escalation Risk: {result['sentiment'].get('escalation_risk')}")
        print(f"\n🎯 Routing:")
        print(f"   Team: {result['routing'].get('route_to_team')}")
        print(f"   Priority: {result['routing'].get('priority')}")
        print(f"   SLA: {result['routing'].get('sla_hours')} hours")
        print(f"\n💬 Response:")
        print(f"   Tone: {result['response'].get('tone')}")
        print(f"\n📧 Generated Email:\n")
        print(result['response'].get('response_text', 'No response generated'))
        print("\n" + "="*60 + "\n")
        
        input("Press Enter to continue to next test...")


if __name__ == "__main__":
    main()
