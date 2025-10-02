"""
Agent 2: Urgency Analyzer

Determines urgency level based on TIMING keywords only.
No sentiment analysis - pure time pressure assessment.

Uses OpenAI GPT-5 via official SDK with Pydantic validation.
"""

from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from pydantic import ValidationError
from models import UrgencyOutput

# Load environment variables from .env file
load_dotenv()


class UrgencyAnalyzerAgent:
    """
    Agent 2: Analyzes urgency (timing only)
    
    Specialization: Time pressure and SLA determination
    Output: UrgencyOutput (Pydantic validated)
    """
    
    def __init__(self):
        """Initialize with OpenAI client"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
    
    def analyze(self, claim_text: str) -> dict:
        """
        Analyze urgency from claim
        
        Args:
            claim_text: The insurance claim text
            
        Returns:
            dict: Validated {urgency_level, sla_hours, ...}
        """
        
        prompt = f"""
        TAAK: Bepaal ALLEEN de urgentie (tijdsdruk) van deze claim.
        NIET sentiment, NIET emotie - alleen WANNEER dit moet worden afgehandeld.
        
        CLAIM TEKST:
        ---
        {claim_text}
        ---
        
        URGENTIE LEVELS:
        
        **Critical** (SLA: 2-8 uur)
        Keywords: "SPOED", "URGENT", "NOODGEVAL", "onmiddellijk", "acuut gevaar"
        Situaties: Veiligheidsrisico, acute noodsituatie, systeem down
        
        **High** (SLA: 8-24 uur)
        Keywords: "zo snel mogelijk", "ASAP", "vandaag nog", "binnen 24 uur"
        Situaties: Expliciete deadline vandaag/morgen
        
        **Medium** (SLA: 72 uur)
        Keywords: "deze week", "binnen 2-3 dagen"
        Situaties: Normale verwachting, geen extreme haast
        
        **Low** (SLA: 120 uur)
        Keywords: geen urgentie keywords, "wanneer het uitkomt"
        Situaties: Informatief, geen tijdsdruk
        
        LET OP:
        - "ONACCEPTABEL" is GEEN urgentie keyword (dat is emotie)
        - "Ik ben boos" is GEEN urgentie keyword (dat is sentiment)
        - Alleen TIMING keywords tellen: "vandaag", "urgent", "spoed", "nu"
        
        DEADLINE DETECTIE:
        
        Zoek expliciete deadlines:
        - "voor 17:00" → deadline_time
        - "vandaag voor 12:00" → deadline_date + time
        - "binnen 3 dagen" → bereken deadline_date
        
        IMMEDIATE DANGER:
        
        Is er acuut fysiek gevaar?
        - "brand", "instortingsgevaar", "gaslek"
        - "gevaar voor personen"
        
        OUTPUT FORMAT (JSON):
        
        {{
            "urgency_level": "High",
            "sla_hours": 24,
            "has_explicit_deadline": true,
            "deadline_date": "2025-10-03" of null,
            "deadline_time": "17:00" of null,
            "time_keywords": ["zo snel mogelijk", "vandaag"],
            "has_immediate_danger": false,
            "reasoning": "Urgency High vanwege 'zo snel mogelijk' en 'vandaag' keywords. 
                         Geen immediate danger. SLA 24 uur passend."
        }}
        
        BELANGRIJK:
        - urgency_level moet exact één van: Critical, High, Medium, Low
        - sla_hours is integer (2, 8, 24, 72, 120)
        - has_immediate_danger alleen true bij fysiek gevaar/risico
        - time_keywords zijn ALLEEN timing words, geen emotie words
        
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
            validated = UrgencyOutput(**result_dict)
            
            # Return as dict (backward compatible)
            return validated.model_dump()
            
        except ValidationError as e:
            print(f"⚠️ Agent 2 Validation Error: {e}")
            # Return safe fallback
            return UrgencyOutput(
                urgency_level="Medium",
                sla_hours=72,
                has_explicit_deadline=False,
                deadline_date=None,
                deadline_time=None,
                time_keywords=[],
                has_immediate_danger=False,
                reasoning=f"Validation error: {str(e)}"
            ).model_dump()
            
        except Exception as e:
            print(f"⚠️ Agent 2 Error: {e}")
            # Return safe fallback
            return UrgencyOutput(
                urgency_level="Medium",
                sla_hours=72,
                has_explicit_deadline=False,
                deadline_date=None,
                deadline_time=None,
                time_keywords=[],
                has_immediate_danger=False,
                reasoning=f"Error: {str(e)}"
            ).model_dump()
