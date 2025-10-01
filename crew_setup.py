"""
CrewAI Orchestration for Insurance Claims Multi-Agent System

WORKFLOW:
Phase 1 (Parallel): Agent 1, 2, 3 analyze claim independently
Phase 2 (Sequential): Agent 4 makes routing decision based on 1, 2, 3
Phase 3 (Sequential): Agent 5 generates customer response based on 4

This demonstrates real multi-agent orchestration with intelligent routing!
"""

from crewai import Crew, Process
from agents import (
    ClaimTypeClassifierAgent,
    UrgencyAmountAnalyzerAgent,
    FraudRiskDetectorAgent,
    SmartRouterAgent,
    ResponseGeneratorAgent
)
import json


class InsuranceClaimsCrew:
    """
    Multi-Agent Insurance Claims Handler
    
    PHASE 1 (PARALLEL): Analysis
    - Agent 1: Claim Type Classifier
    - Agent 2: Urgency & Amount Analyzer
    - Agent 3: Fraud Risk Detector
    
    PHASE 2 (SEQUENTIAL): Routing Decision
    - Agent 4: Smart Router (uses output 1, 2, 3)
    
    PHASE 3 (SEQUENTIAL): Customer Communication
    - Agent 5: Response Generator (uses output 4)
    """
    
    def __init__(self):
        """Initialize all 5 agents"""
        print("🚀 Initializing Insurance Claims Crew...")
        self.type_classifier = ClaimTypeClassifierAgent()
        self.urgency_amount_analyzer = UrgencyAmountAnalyzerAgent()
        self.fraud_detector = FraudRiskDetectorAgent()
        self.router = SmartRouterAgent()
        self.response_generator = ResponseGeneratorAgent()
        print("✅ All 5 agents initialized!")
    
    def process_claim(self, claim_text: str) -> dict:
        """
        Process insurance claim through complete multi-agent pipeline
        
        Workflow:
        1. Run Agent 1, 2, 3 in parallel
        2. Agent 4 uses their combined output for routing
        3. Agent 5 generates customer response
        
        Args:
            claim_text: The insurance claim to process
            
        Returns:
            dict: Complete analysis + routing + response
        """
        
        print("\n" + "="*70)
        print("🏥 PROCESSING INSURANCE CLAIM")
        print("="*70)
        
        try:
            # ================================================
            # PHASE 1: PARALLEL ANALYSIS (Agents 1, 2, 3)
            # ================================================
            
            print("\n🔄 PHASE 1: Running parallel analysis...")
            print("  → Agent 1: Classifying claim type...")
            print("  → Agent 2: Analyzing urgency & extracting amount...")
            print("  → Agent 3: Detecting fraud risk...")
            
            # Create tasks for parallel agents
            type_task = self.type_classifier.create_task(claim_text)
            urgency_amount_task = self.urgency_amount_analyzer.create_task(claim_text)
            fraud_task = self.fraud_detector.create_task(claim_text)
            
            # Create crew for parallel execution
            # Note: CrewAI doesn't have true parallel yet, but agents are independent
            parallel_crew = Crew(
                agents=[
                    self.type_classifier.agent,
                    self.urgency_amount_analyzer.agent,
                    self.fraud_detector.agent
                ],
                tasks=[
                    type_task,
                    urgency_amount_task,
                    fraud_task
                ],
                process=Process.sequential,
                verbose=False
            )
            
            # Execute parallel analysis
            parallel_crew.kickoff()
            
            # Extract results
            type_result = self._extract_result(type_task)
            urgency_amount_result = self._extract_result(urgency_amount_task)
            fraud_result = self._extract_result(fraud_task)
            
            print("\n✅ Parallel analysis complete!")
            print(f"  📋 Type: {type_result.get('type', 'Unknown')} (confidence: {type_result.get('confidence', 0):.2f})")
            print(f"  ⏰ Urgency: {urgency_amount_result.get('urgency_level', 'Unknown')}")
            print(f"  💰 Amount: €{urgency_amount_result.get('amount_euros', 0):.2f}")
            print(f"  🚨 Fraud Risk: {fraud_result.get('risk_level', 'Unknown')} (score: {fraud_result.get('risk_score', 0):.2f})")
            
            # ================================================
            # PHASE 2: ROUTING DECISION (Agent 4)
            # ================================================
            
            print("\n🎯 PHASE 2: Making routing decision...")
            print("  → Agent 4: Orchestrating routing...")
            
            # Agent 4 needs ALL previous results
            routing_task = self.router.create_task(
                claim_text=claim_text,
                claim_type_result=json.dumps(type_result, indent=2),
                urgency_amount_result=json.dumps(urgency_amount_result, indent=2),
                fraud_risk_result=json.dumps(fraud_result, indent=2)
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
            print(f"  🎯 Route: {routing_result.get('route_path', 'Unknown')}")
            print(f"  👥 Team: {routing_result.get('route_to_team', 'Unknown')}")
            print(f"  🔥 Priority: P{routing_result.get('priority', '?')}")
            print(f"  ⏱️  SLA: {routing_result.get('sla_hours', '?')} hours")
            print(f"  📄 Template: {routing_result.get('response_template_type', '?')}")
            
            # ================================================
            # PHASE 3: RESPONSE GENERATION (Agent 5)
            # ================================================
            
            print("\n💬 PHASE 3: Generating customer response...")
            print("  → Agent 5: Crafting email...")
            
            # Agent 5 uses routing decision
            response_task = self.response_generator.create_task(
                claim_text=claim_text,
                claim_type=type_result.get('type', 'Unknown'),
                routing_decision_result=json.dumps(routing_result, indent=2)
            )
            
            response_crew = Crew(
                agents=[self.response_generator.agent],
                tasks=[response_task],
                process=Process.sequential,
                verbose=False
            )
            
            response_crew.kickoff()
            response_result = self._extract_result(response_task)
            
            print("\n✅ Response generated!")
            print(f"  📝 Template Used: {response_result.get('template_used', 'Unknown')}")
            print(f"  🎭 Tone: {response_result.get('tone', 'Unknown')}")
            print(f"  📧 Reference: {response_result.get('claim_reference_number', 'Unknown')}")
            
            # ================================================
            # RETURN COMPLETE RESULTS
            # ================================================
            
            print("\n" + "="*70)
            print("✅ CLAIM PROCESSING COMPLETE")
            print("="*70 + "\n")
            
            return {
                'claim_type': type_result,
                'urgency_amount': urgency_amount_result,
                'fraud_risk': fraud_result,
                'routing': routing_result,
                'response': response_result
            }
            
        except Exception as e:
            print(f"\n❌ Error in claim processing: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                'error': str(e),
                'claim_type': {'type': 'Error', 'confidence': 0.0},
                'urgency_amount': {'urgency_level': 'Unknown', 'amount_euros': None},
                'fraud_risk': {'risk_level': 'Unknown', 'risk_score': 0.0},
                'routing': {'route_path': 'Error', 'route_to_team': 'Manual Review'},
                'response': {'response_text': f'Error processing claim: {str(e)}'}
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
            print(f"⚠️  Warning: Could not parse JSON output: {e}")
            print(f"Raw output: {output_text[:200]}...")
            return {}
        except Exception as e:
            print(f"⚠️  Warning: Error extracting result: {e}")
            return {}


# ================================================
# COMMAND LINE TESTING
# ================================================

def main():
    """Test the crew with example insurance claims"""
    
    test_claims = [
        {
            'name': 'Simple Auto Claim - Should Auto-Approve',
            'claim': """
Beste verzekering,

Gisteren heb ik een kleine kras op mijn bumper gekregen door een winkelwagentje 
op de parkeerplaats. De schade is minimaal.

Geschatte schade: €400
Polisnummer: AUTO-2024-12345
Datum incident: 30 september 2025

Met vriendelijke groet,
Jan Janssen
            """
        },
        {
            'name': 'High Value Total Loss - Should Route to Senior',
            'claim': """
Geachte heer/mevrouw,

Na een ernstige aanrijding op de A2 is mijn auto total loss. De auto is niet meer 
te repareren en moet naar de sloop.

Cataloguswaarde: €28.000
Polisnummer: AUTO-2024-67890
Datum: 29 september 2025
Kenteken: XX-123-YY

De andere partij is doorgereden, ik heb het kenteken genoteerd.
Politie is gewaarschuwd, rapportnummer: PL-2025-9876.

Met vriendelijke groet,
Maria de Vries
            """
        },
        {
            'name': 'Suspicious Fraud Pattern - Should Route to SIU',
            'claim': """
Hallo,

Schade aan mijn laptop, gestolen uit mijn auto.

Schatting: €2.200
Polis: NET-2025-111 (vorige week afgesloten)

Was ergens geparkeerd, weet niet precies waar. Laptop was er ineens niet meer.

Groet
            """
        }
    ]
    
    crew = InsuranceClaimsCrew()
    
    for i, test in enumerate(test_claims, 1):
        print(f"\n\n{'#'*80}")
        print(f"# TEST {i}: {test['name']}")
        print(f"{'#'*80}")
        print(f"\nCLAIM:\n{test['claim']}\n")
        
        result = crew.process_claim(test['claim'])
        
        print("\n" + "="*70)
        print("📊 DETAILED RESULTS:")
        print("="*70)
        print(f"\n📋 Claim Type:")
        print(f"   Type: {result['claim_type'].get('type')}")
        print(f"   Confidence: {result['claim_type'].get('confidence')}")
        print(f"   Policy: {result['claim_type'].get('policy_number', 'N/A')}")
        
        print(f"\n⏰ Urgency & Amount:")
        print(f"   Urgency: {result['urgency_amount'].get('urgency_level')}")
        print(f"   Amount: €{result['urgency_amount'].get('amount_euros', 0)}")
        print(f"   Total Loss: {result['urgency_amount'].get('is_total_loss')}")
        
        print(f"\n🚨 Fraud Risk:")
        print(f"   Risk Level: {result['fraud_risk'].get('risk_level')}")
        print(f"   Risk Score: {result['fraud_risk'].get('risk_score')}")
        print(f"   Red Flags: {len(result['fraud_risk'].get('red_flags', []))}")
        
        print(f"\n🎯 Routing:")
        print(f"   Path: {result['routing'].get('route_path')}")
        print(f"   Team: {result['routing'].get('route_to_team')}")
        print(f"   Priority: P{result['routing'].get('priority')}")
        print(f"   SLA: {result['routing'].get('sla_hours')}h")
        
        print(f"\n📧 Customer Response:")
        print(f"   Template: {result['response'].get('template_used')}")
        print(f"   Reference: {result['response'].get('claim_reference_number')}")
        print(f"\n{'-'*70}")
        print(result['response'].get('response_text', 'No response generated'))
        print(f"{'-'*70}\n")
        
        input("\nPress Enter to continue to next test...")


if __name__ == "__main__":
    main()
