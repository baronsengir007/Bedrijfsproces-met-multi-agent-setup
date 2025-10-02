"""
Insurance Claims Processing System

NEW ARCHITECTURE:
- Agent 1: Type & Amount Extractor (OpenAI GPT-5)
- Agent 2: Urgency Analyzer (OpenAI GPT-5)
- Agent 3: Fraud Detector (OpenAI GPT-5)
- Router: Pure Python (NO LLM - instant routing!)
- Agent 5: Response Generator (ALWAYS empathetic via GPT-5)

LLM Calls: 4 per claim (Agent 1, 2, 3, 5)
"""

from agents import (
    TypeAmountExtractorAgent,
    UrgencyAnalyzerAgent,
    FraudRiskDetectorAgent,
    PythonRouter,
    ResponseGeneratorAgent
)
import json
from datetime import datetime


class InsuranceClaimsPipeline:
    """
    Multi-Agent Insurance Claims Handler
    
    PHASE 1: Parallel Analysis (3 LLM calls)
    - Agent 1, 2, 3 run independently
    
    PHASE 2: Python Routing (0 LLM calls!)
    - Pure Python decision tree
    
    PHASE 3: Response Generation (1 LLM call)
    - ALWAYS empathetic opening via LLM + structured template
    """
    
    def __init__(self):
        """Initialize all agents and router"""
        print("🚀 Initializing Insurance Claims Pipeline...")
        self.agent1 = TypeAmountExtractorAgent()
        self.agent2 = UrgencyAnalyzerAgent()
        self.agent3 = FraudRiskDetectorAgent()
        self.router = PythonRouter()
        self.agent5 = ResponseGeneratorAgent()
        print("✅ All components initialized!")
        print("   - 3 LLM agents (GPT-5)")
        print("   - 1 Python router (instant)")
        print("   - 1 Empathetic response generator")
    
    def process_claim(self, claim_text: str) -> dict:
        """
        Process insurance claim through complete pipeline
        
        Args:
            claim_text: The insurance claim to process
            
        Returns:
            dict: Complete analysis + routing + response
        """
        
        print("\n" + "="*70)
        print("🏥 PROCESSING INSURANCE CLAIM")
        print("="*70)
        
        start_time = datetime.now()
        
        try:
            # ================================================
            # PHASE 1: PARALLEL ANALYSIS (3 LLM calls)
            # ================================================
            
            print("\n🔄 PHASE 1: Running parallel analysis (3 LLM calls)...")
            
            print("  → Agent 1: Extracting type & amount...")
            type_result = self.agent1.analyze(claim_text)
            
            print("  → Agent 2: Analyzing urgency...")
            urgency_result = self.agent2.analyze(claim_text)
            
            print("  → Agent 3: Detecting fraud risk...")
            fraud_result = self.agent3.analyze(claim_text)
            
            print("\n✅ Parallel analysis complete!")
            print(f"  📋 Type: {type_result.get('type', 'Unknown')} (confidence: {type_result.get('confidence', 0):.2f})")
            print(f"  💰 Amount: €{type_result.get('amount_euros', 0):,.2f}")
            print(f"  ⏰ Urgency: {urgency_result.get('urgency_level', 'Unknown')}")
            print(f"  🚨 Fraud Risk: {fraud_result.get('risk_level', 'Unknown')} (score: {fraud_result.get('risk_score', 0):.2f})")
            
            # ================================================
            # PHASE 2: PYTHON ROUTING (0 LLM calls!)
            # ================================================
            
            print("\n🎯 PHASE 2: Making routing decision (pure Python)...")
            
            routing_result = self.router.route(
                type_data=type_result,
                urgency_data=urgency_result,
                fraud_data=fraud_result
            )
            
            print("\n✅ Routing decision made!")
            print(f"  🎯 Route: {routing_result.get('route_path', 'Unknown')}")
            print(f"  👥 Team: {routing_result.get('route_to_team', 'Unknown')}")
            print(f"  🔥 Priority: P{routing_result.get('priority', '?')}")
            print(f"  ⏱️  SLA: {routing_result.get('sla_hours', '?')} hours")
            print(f"  📄 Template: {routing_result.get('response_template_type', '?')}")
            
            # ================================================
            # PHASE 3: RESPONSE GENERATION (1 LLM call)
            # ================================================
            
            print("\n💬 PHASE 3: Generating customer response...")
            
            response_result = self.agent5.generate(
                routing_decision=routing_result,
                type_data=type_result,
                claim_text=claim_text
            )
            
            print(f"\n✅ Response generated! (Always empathetic)")
            print(f"  📝 Template: {response_result.get('template_used', 'Unknown')}")
            print(f"  🎭 Tone: {response_result.get('tone', 'Unknown')}")
            print(f"  📧 Reference: {response_result.get('claim_reference_number', 'Unknown')}")
            
            # ================================================
            # RETURN COMPLETE RESULTS
            # ================================================
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            print("\n" + "="*70)
            print(f"✅ CLAIM PROCESSING COMPLETE ({processing_time:.2f}s)")
            print("="*70 + "\n")
            
            # LLM calls: Always 4 now (Agent 1, 2, 3, 5)
            llm_calls = 4
            
            return {
                'claim_type': type_result,
                'urgency': urgency_result,
                'fraud_risk': fraud_result,
                'routing': routing_result,
                'response': response_result,
                'meta': {
                    'processing_time_seconds': processing_time,
                    'llm_calls_used': llm_calls,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"\n❌ Error in claim processing: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                'error': str(e),
                'claim_type': {'type': 'Error', 'confidence': 0.0},
                'urgency': {'urgency_level': 'Unknown', 'sla_hours': 72},
                'fraud_risk': {'risk_level': 'Unknown', 'risk_score': 0.0},
                'routing': {'route_path': 'Error', 'route_to_team': 'Manual Review'},
                'response': {'response_text': f'Error processing claim: {str(e)}'}
            }


# ================================================
# COMMAND LINE TESTING
# ================================================

def main():
    """Test the pipeline with 5 diverse insurance claims"""
    
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

Was ergens geparkeerd, weet niet precies waar.

Groet
            """
        },
        {
            'name': 'Emotional/Urgent - Daughter in Hospital',
            'claim': """
Beste medewerker,

Ik moet jullie helaas iets vervelends melden. Gisteren was ik onderweg naar het 
ziekenhuis omdat mijn dochter daar met spoed was opgenomen. In mijn haast heb ik 
bij het inparkeren een andere auto geraakt. Er zit nu een flinke deuk in mijn 
portier en de spiegel is eraf.

Ik maak me echt zorgen want ik moet vandaag weer naar het ziekenhuis. Mijn dochter 
moet morgen geopereerd worden en ik wil graag bij haar zijn. Kan dit alsjeblieft 
snel geregeld worden? Ik heb mijn auto hard nodig.

De schade schat ik op ongeveer €1.200.

Polisnummer: AUTO-2024-45678
Datum incident: 1 oktober 2025
Locatie: Parkeerplaats Erasmus MC Rotterdam

Ik hoop van harte dat jullie me kunnen helpen.

Met vriendelijke groet,
Sophie van der Berg
            """
        },
        {
            'name': 'Business/Formal - Company Vehicle',
            'claim': """
Geachte Claims Afdeling,

Ondergetekende dient hierbij een schademelding in namens TransLog B.V. betreffende 
één van onze bedrijfsvoertuigen.

INCIDENT DETAILS:
Op 30 september 2025 omstreeks 14:30 uur heeft chauffeur de heer J. Pieters met 
kenteken BX-123-ZZ een aanrijding veroorzaakt tijdens een leverrit op de A12 
richting Utrecht. Door plotseling remmende verkeer is hij tegen de achterzijde 
van een vrachtwagen gebotst.

SCHADEOVERZICHT:
- Frontschade aan bedrijfswagen
- Geraamde reparatiekosten: €8.500
- Voertuig momenteel niet inzetbaar
- Geen personenschade

POLISGEGEVENS:
- Polisnummer: FLEET-2024-890
- Verzekerde: TransLog B.V.
- Type dekking: Volledig casco + WA

URGENTIE:
Het voertuig wordt dagelijks ingezet voor onze logistieke operaties. 
Graag zien wij de afhandeling binnen 5 werkdagen tegemoet.

Voor aanvullende documentatie of vragen kunt u contact opnemen met 
ondergetekende via kantooruren.

Hoogachtend,

drs. M.J. Verhoeven
Hoofd Operations
TransLog B.V.
m.verhoeven@translog.nl
            """
        }
    ]
    
    pipeline = InsuranceClaimsPipeline()
    
    for i, test in enumerate(test_claims, 1):
        print(f"\n\n{'#'*80}")
        print(f"# TEST {i}: {test['name']}")
        print(f"{'#'*80}")
        print(f"\nCLAIM:\n{test['claim']}\n")
        
        result = pipeline.process_claim(test['claim'])
        
        print("\n" + "="*70)
        print("📊 DETAILED RESULTS:")
        print("="*70)
        
        print(f"\n📋 Claim Type:")
        print(f"   Type: {result['claim_type'].get('type')}")
        print(f"   Amount: €{result['claim_type'].get('amount_euros', 0):,.2f}")
        print(f"   Confidence: {result['claim_type'].get('confidence'):.2f}")
        
        print(f"\n⏰ Urgency:")
        print(f"   Level: {result['urgency'].get('urgency_level')}")
        print(f"   SLA: {result['urgency'].get('sla_hours')}h")
        
        print(f"\n🚨 Fraud Risk:")
        print(f"   Level: {result['fraud_risk'].get('risk_level')}")
        print(f"   Score: {result['fraud_risk'].get('risk_score'):.2f}")
        print(f"   Red Flags: {len(result['fraud_risk'].get('red_flags', []))}")
        
        print(f"\n🎯 Routing:")
        print(f"   Path: {result['routing'].get('route_path')}")
        print(f"   Team: {result['routing'].get('route_to_team')}")
        print(f"   Priority: P{result['routing'].get('priority')}")
        
        print(f"\n📧 Customer Response:")
        print(f"   Template: {result['response'].get('template_used')}")
        print(f"   Empathetic: {result['response'].get('llm_enhanced')}")
        print(f"   Reference: {result['response'].get('claim_reference_number')}")
        print(f"\n{'-'*70}")
        print(result['response'].get('response_text', 'No response generated'))
        print(f"{'-'*70}\n")
        
        if 'meta' in result:
            print(f"⚡ Performance:")
            print(f"   Processing Time: {result['meta']['processing_time_seconds']:.2f}s")
            print(f"   LLM Calls: {result['meta']['llm_calls_used']}")
        
        input("\nPress Enter to continue to next test...")


if __name__ == "__main__":
    main()
