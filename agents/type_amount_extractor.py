"""
Agent 1: Type & Amount Extractor

Extracts claim type AND damage amount from text.
Pure factual extraction - no sentiment, no urgency.

Uses OpenAI GPT-5 via official SDK with Pydantic validation.
"""

from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from pydantic import ValidationError
from models import ClaimTypeOutput

# Load environment variables from .env file
load_dotenv()


class TypeAmountExtractorAgent:
    """
    Agent 1: Extracts type and amount
    
    Specialization: Factual data extraction
    Output: ClaimTypeOutput (Pydantic validated)
    """
    
    def __init__(self):
        """Initialize with OpenAI client"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
    
    def analyze(self, claim_text: str) -> dict:
        """
        Extract type and amount from claim
        
        Args:
            claim_text: The insurance claim text
            
        Returns:
            dict: Validated {type, amount, confidence, ...}
        """
        
        prompt = f"""
        TAAK: Extraheer TYPE en BEDRAG uit deze verzekeringsclaim.
        
        CLAIM TEKST:
        ---
        {claim_text}
        ---
        
        DEEL 1: TYPE CLASSIFICATIE
        
        Categorieën: Auto, Woning, Inboedel, Aansprakelijkheid
        
        **Auto:**
        Keywords: aanrijding, autoschade, bumper, kenteken, parkeerplaats, WA
        
        **Woning:**
        Keywords: brand, waterschade, lekkage, storm, dak, gevel, huis
        
        **Inboedel:**
        Keywords: inbraak, diefstal, gestolen, laptop, meubels, spullen
        
        **Aansprakelijkheid:**
        Keywords: schade veroorzaakt, aansprakelijk, derde partij, WA schade
        
        DEEL 2: BEDRAG EXTRACTIE
        
        Zoek naar bedragen in verschillende formaten:
        - Direct: "€500", "€1.500", "1000 euro"
        - Schatting: "ongeveer €2000", "schatting 1500"
        - Range: "tussen €500-1000" → neem midpoint (€750)
        - Woorden: "vijfhonderd euro" → €500
        
        Confidence voor bedrag:
        - 0.9-1.0: Exact bedrag ("€500")
        - 0.7-0.9: Schatting ("ongeveer €500")
        - 0.5-0.7: Range of vaag ("een paar honderd")
        - 0.0-0.5: Geen bedrag genoemd
        
        DEEL 3: EXTRA DATA
        
        - Polisnummer: "AUTO-2024-12345", "POL12345"
        - Datum: "30 september 2025", "gisteren" → YYYY-MM-DD
        - Total loss: keywords "total loss", "totaal verloren", "naar sloop"
        
        OUTPUT FORMAT (JSON):
        
        {{
            "type": "Auto",
            "confidence": 0.95,
            "amount_euros": 500.00,
            "amount_confidence": 0.90,
            "keywords": ["autoschade", "bumper"],
            "policy_number": "AUTO-2024-12345" of null,
            "incident_date": "2025-09-30" of null,
            "is_total_loss": false,
            "reasoning": "Type bepaald door keywords X, Y. Bedrag €500 expliciet genoemd."
        }}
        
        BELANGRIJK:
        - Type moet exact één van: Auto, Woning, Inboedel, Aansprakelijkheid
        - amount_euros is float of null
        - amount_confidence tussen 0.0-1.0
        - is_total_loss alleen true bij keywords: "total loss", "totaal verloren", "naar sloop"
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        try:
            # Get LLM response
            response = self.client.responses.create(
                model=self.model,
                reasoning={"effort": "low"},
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
            validated = ClaimTypeOutput(**result_dict)
            
            # Return as dict (backward compatible)
            return validated.model_dump()
            
        except ValidationError as e:
            print(f"⚠️ Agent 1 Validation Error: {e}")
            # Return safe fallback
            return ClaimTypeOutput(
                type="Unknown",
                confidence=0.0,
                amount_euros=None,
                amount_confidence=0.0,
                keywords=[],
                policy_number=None,
                incident_date=None,
                is_total_loss=False,
                reasoning=f"Validation error: {str(e)}"
            ).model_dump()
            
        except Exception as e:
            print(f"⚠️ Agent 1 Error: {e}")
            # Return safe fallback
            return ClaimTypeOutput(
                type="Unknown",
                confidence=0.0,
                amount_euros=None,
                amount_confidence=0.0,
                keywords=[],
                policy_number=None,
                incident_date=None,
                is_total_loss=False,
                reasoning=f"Error: {str(e)}"
            ).model_dump()
