"""
Agent 3: Fraud Risk Detector

Assesses fraud risk based on textual patterns, completeness, and inconsistencies.
Works WITHOUT database access - purely text-based analysis.

Uses OpenAI GPT-5 via official SDK with Pydantic validation.
"""

from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from pydantic import ValidationError
from models import FraudRiskOutput

# Load environment variables from .env file
load_dotenv()


class FraudRiskDetectorAgent:
    """
    Agent 3: Detects fraud risk patterns in claims
    
    Specialization: Pattern-based fraud detection from text only
    Output: FraudRiskOutput (Pydantic validated)
    """
    
    def __init__(self):
        """Initialize with OpenAI client"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
    
    def analyze(self, claim_text: str) -> dict:
        """
        Detect fraud risk from claim
        
        Args:
            claim_text: The insurance claim text
            
        Returns:
            dict: Validated {risk_score, risk_level, red_flags, ...}
        """
        
        prompt = f"""
        TAAK: Analyseer deze verzekeringsclaim op frauderisico ZONDER database access.
        Je werkt ALLEEN met wat in de tekst staat.
        
        CLAIM TEKST:
        ---
        {claim_text}
        ---
        
        FRAUD RISK ANALYSE FRAMEWORK:
        
        Je bouwt een risk score op van 0.0 tot 1.0 door verschillende patronen te detecteren.
        
        ═══════════════════════════════════════════════════════════════
        1. COMPLETENESS CHECK (0-0.3 punten)
        ═══════════════════════════════════════════════════════════════
        
        Ontbreekt cruciale informatie?
        
        **Incident datum ontbreekt** (+0.15):
        - Geen specifieke datum genoemd
        - Alleen "recent", "laatst", "pas geleden"
        
        **Locatie ontbreekt** (+0.10):
        - Geen specifieke locatie (stad, straat, plaats)
        - Alleen "ergens", "onderweg"
        
        **Vage beschrijving** (+0.15):
        - Zeer minimale details
        - "Een beetje schade", "iets kapot"
        - Geen concrete omschrijving van wat er gebeurd is
        
        ═══════════════════════════════════════════════════════════════
        2. TIMING SIGNALEN (0-0.3 punten)
        ═══════════════════════════════════════════════════════════════
        
        **Recent afgesloten polis** (+0.25):
        - "Polis net afgesloten"
        - "Vorige week contract"
        - "Pas verzekerd sinds..."
        
        **Herhaalde claims melding** (+0.20):
        - "Dit is alweer de Xe keer dit jaar"
        - "Weer schade"
        - "Opnieuw een claim"
        
        ═══════════════════════════════════════════════════════════════
        3. BEDRAG POSITIONERING (0-0.2 punten)
        ═══════════════════════════════════════════════════════════════
        
        **Strategisch bedrag** (+0.20):
        - Bedragen net onder bekende drempels:
          - €9.900 - €9.999 (net onder €10k)
          - €24.500 - €24.999 (net onder €25k)
          - €740 - €749 (net onder €750 auto-approve)
        
        ═══════════════════════════════════════════════════════════════
        4. INCONSISTENTIES (0-0.3 punten)
        ═══════════════════════════════════════════════════════════════
        
        **Taal vs Bedrag mismatch** (+0.15):
        - "Totale ramp", "alles kapot" + klein bedrag (€200)
        - Zeer emotionele taal voor kleine schade
        
        **Tegenstrijdige statements** (+0.25):
        - "Geen getuigen" maar later "iemand heeft het gezien"
        - Inconsistente beschrijvingen
        
        ═══════════════════════════════════════════════════════════════
        RISK SCORE BEREKENING
        ═══════════════════════════════════════════════════════════════
        
        Tel alle punten op, cap bij 1.0:
        
        risk_score = min(
            completeness_penalties + 
            timing_signals + 
            amount_positioning + 
            inconsistencies,
            1.0
        )
        
        ═══════════════════════════════════════════════════════════════
        RISK LEVEL MAPPING
        ═══════════════════════════════════════════════════════════════
        
        - **Low** (0.0 - 0.3): Geen significante rode vlaggen
        - **Medium** (0.3 - 0.6): Enkele zorgen, manual review aanbevolen
        - **High** (0.6 - 1.0): Meerdere rode vlaggen, SIU investigation
        
        OUTPUT FORMAT (JSON):
        
        {{
            "risk_score": 0.25,
            "risk_level": "Low",
            "red_flags": [
                "Geen incident datum vermeld"
            ],
            "suspicious_patterns": [
                "Vage beschrijving zonder details"
            ],
            "recommendation": "Auto-approve mogelijk (bij andere criteria OK)",
            "reasoning": "Gedetailleerde uitleg hoe score is opgebouwd."
        }}
        
        BELANGRIJK:
        - Wees NIET paranoia - normale claims krijgen lage scores
        - Wees WEL alert - echte red flags moet je oppakken
        - risk_level moet exact één van: Low, Medium, High
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        try:
            # Get LLM response
            response = self.client.responses.create(
                model=self.model,
                reasoning={"effort": "medium"},  # Fraud needs more thinking
                input=prompt
            )
            
            # Extract text from response
            output_text = response.output_text
            
            # Clean and parse JSON
            output_text = output_text.strip()
            if output_text.startswith('```json'):
                output_text = output_text[7:]
            if output_text.startswith('```'):
                output_text = output_text[3:]
            if output_text.endswith('```'):
                output_text = output_text[:-3]
            output_text = output_text.strip()
            
            # Parse JSON
            result_dict = json.loads(output_text)
            
            # Validate with Pydantic
            validated = FraudRiskOutput(**result_dict)
            
            # Return as dict (backward compatible)
            return validated.model_dump()
            
        except ValidationError as e:
            print(f"⚠️ Agent 3 Validation Error: {e}")
            # Return safe fallback
            return FraudRiskOutput(
                risk_score=0.5,
                risk_level="Medium",
                red_flags=[],
                suspicious_patterns=[],
                recommendation="Manual review aanbevolen",
                reasoning=f"Validation error: {str(e)}"
            ).model_dump()
            
        except Exception as e:
            print(f"⚠️ Agent 3 Error: {e}")
            # Return safe fallback
            return FraudRiskOutput(
                risk_score=0.5,
                risk_level="Medium",
                red_flags=[],
                suspicious_patterns=[],
                recommendation="Manual review aanbevolen",
                reasoning=f"Error: {str(e)}"
            ).model_dump()
