"""
Agent 5: Response Generator (Hybrid)

ALWAYS adds empathetic opening via LLM with 2-sentence structure.
KORT EN BONDIG: Max 15 woorden per zin.

Uses OpenAI GPT-5 with Pydantic validation.
"""

from openai import OpenAI
import json
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from pydantic import ValidationError
from models import CustomerResponse

# Load environment variables from .env file
load_dotenv()


class ResponseGeneratorAgent:
    """
    Agent 5: Generates customer responses
    
    Specialization: ALWAYS adds 2-sentence empathetic opening via LLM
    Output: CustomerResponse (Pydantic validated)
    
    2 KORTE zinnen: Context → Ontzorgen
    """
    
    # Response templates (WITHOUT "Beste {name}," - LLM adds that)
    TEMPLATES = {
        "A": """WIJ HEBBEN ONTVANGEN:
• Type claim: {claim_type}
• Bedrag: {amount}
• Polisnummer: {policy_number}

✅ GOEDGEKEURD:
Uw claim is automatisch goedgekeurd!

BETALING:
Het bedrag van {amount} wordt binnen 2 werkdagen overgemaakt.

CLAIMNUMMER: {claim_ref}

Heeft u nog vragen? Bel 020-1234567.

Met vriendelijke groet,
Claims Team
Verzekeringen NL""",
        
        "B": """WIJ HEBBEN ONTVANGEN:
• Type claim: {claim_type}
• Geschatte schade: {amount}
• Polisnummer: {policy_number}

IN BEHANDELING:
Een claims behandelaar gaat uw claim beoordelen.

VERWACHTE DOORLOOPTIJD:
U ontvangt binnen {processing_time} bericht over de afhandeling.

CLAIMNUMMER: {claim_ref}

Voor vragen: 020-1234567.

Met vriendelijke groet,
Claims Team
Verzekeringen NL""",
        
        "C": """WIJ HEBBEN ONTVANGEN:
• Type claim: {claim_type}
• Geschatte schade: {amount}
• Polisnummer: {policy_number}

EXTRA BEOORDELING NODIG:
Uw claim wordt zorgvuldig beoordeeld door een gespecialiseerde behandelaar.

VERWACHTE DOORLOOPTIJD:
Een behandelaar neemt binnen {processing_time} persoonlijk contact met u op.

CLAIMNUMMER: {claim_ref}

Voor directe vragen: 020-1234567.

Met vriendelijke groet,
Senior Claims Team
Verzekeringen NL""",
        
        "D": """WIJ HEBBEN ONTVANGEN:
• Type claim: {claim_type}
• Geschatte schade: {amount}
• Polisnummer: {policy_number}

HOOGSTE PRIORITEIT:
Uw claim krijgt onze speciale aandacht.

VOLGENDE STAPPEN:
Een senior behandelaar neemt {contact_time} telefonisch contact met u op.

CLAIMNUMMER: {claim_ref}

Voor directe vragen: 020-1234567.

Met vriendelijke groet,
Senior Claims Team
Verzekeringen NL"""
    }
    
    def __init__(self):
        """Initialize with OpenAI client"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
    
    def detect_sentiment(self, claim_text: str) -> str:
        """
        Detect sentiment from claim text (NO LLM - pure Python!)
        
        Returns: "angry", "worried", "neutral", "polite"
        """
        text_upper = claim_text.upper()
        
        # Angry indicators
        angry_keywords = [
            "ONACCEPTABEL", "SCHANDELIJK", "ADVOCAAT",
            "KLACHT", "DIT KAN NIET", "WAARDENLOOS", "BELACHELIJK"
        ]
        exclamation_count = claim_text.count('!')
        caps_ratio = sum(1 for c in claim_text if c.isupper()) / max(len(claim_text), 1)
        
        if any(kw in text_upper for kw in angry_keywords) or exclamation_count > 3 or caps_ratio > 0.3:
            return "angry"
        
        # Worried indicators
        worried_keywords = [
            "MAAK ME ZORGEN", "BANG", "WAT MOET IK", "HELP", "BEZORGD"
        ]
        if any(kw in text_upper for kw in worried_keywords):
            return "worried"
        
        # Polite indicators
        polite_keywords = [
            "BEDANKT", "DANK", "GRAAG", "VRIENDELIJKE GROET", "SVP", "ALSTUBLIEFT"
        ]
        if any(kw in text_upper for kw in polite_keywords):
            return "polite"
        
        return "neutral"
    
    def extract_customer_name(self, claim_text: str) -> str:
        """Extract customer name from signature (NO LLM - pure regex!)"""
        # Try to find name after "Met vriendelijke groet," or "Groet,"
        patterns = [
            r'(?:Met vriendelijke groet,|Groet,|Mvg,|Hoogachtend,)\s*\n\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:Met vriendelijke groet,|Groet,|Mvg,|Hoogachtend,)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, claim_text)
            if match:
                return match.group(1)
        
        return "klant"
    
    def generate(
        self,
        routing_decision: dict,
        type_data: dict,
        claim_text: str
    ) -> dict:
        """
        Generate customer response
        
        ALWAYS uses LLM for 2-sentence empathetic opening + template for structure
        
        Returns:
            dict: Validated CustomerResponse
        """
        
        # Generate claim reference
        claim_ref = f"CLM-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Extract data
        template_type = routing_decision.get('response_template_type', 'B')
        claim_type = type_data.get('type', 'Unknown')
        amount = type_data.get('amount_euros')
        policy_number = type_data.get('policy_number', 'Wordt verwerkt')
        priority = routing_decision.get('priority', 3)
        sla_hours = routing_decision.get('sla_hours', 72)
        
        # Detect sentiment (NO LLM - pure Python!)
        sentiment = self.detect_sentiment(claim_text)
        
        # Extract customer name (NO LLM - pure regex!)
        customer_name = self.extract_customer_name(claim_text)
        
        # Format amount
        amount_str = f"€{amount:,.2f}" if amount else "Nader te bepalen"
        
        # Calculate processing time
        if sla_hours <= 8:
            processing_time = "1 werkdag"
        elif sla_hours <= 24:
            processing_time = "1-2 werkdagen"
        elif sla_hours <= 72:
            processing_time = "3 werkdagen"
        else:
            processing_time = "5 werkdagen"
        
        # Contact time for urgent cases
        if priority == 1:
            contact_time = "vandaag nog"
        elif priority == 2:
            contact_time = "binnen 24 uur"
        else:
            contact_time = "binnen enkele dagen"
        
        # Get base template (without opening)
        base_template = self.TEMPLATES.get(template_type, self.TEMPLATES["B"])
        
        # Fill template
        template_body = base_template.format(
            claim_type=claim_type,
            amount=amount_str,
            policy_number=policy_number,
            claim_ref=claim_ref,
            processing_time=processing_time,
            contact_time=contact_time
        )
        
        # ALWAYS use LLM for 2-sentence empathetic opening
        response_text = self._generate_empathetic_response(
            customer_name=customer_name,
            claim_text=claim_text,  # Give FULL claim for context
            template_body=template_body,
            sentiment=sentiment
        )
        
        tone = f"Empathetic-{sentiment.title()}"
        
        try:
            # Validate with Pydantic
            validated = CustomerResponse(
                response_text=response_text,
                template_used=template_type,
                tone=tone,
                includes_approval=(template_type == "A"),
                includes_next_steps=True,
                estimated_processing_time=processing_time,
                claim_reference_number=claim_ref,
                sentiment_detected=sentiment,
                llm_enhanced=True  # Always true now!
            )
            
            return validated.model_dump()
            
        except ValidationError as e:
            print(f"⚠️ Agent 5 Validation Error: {e}")
            # Return fallback
            fallback_text = f"Beste {customer_name},\n\nHartelijk dank voor het indienen van uw claim.\n\n{template_body}"
            return CustomerResponse(
                response_text=fallback_text,
                template_used=template_type,
                tone="Professional-Standard",
                includes_approval=(template_type == "A"),
                includes_next_steps=True,
                estimated_processing_time=processing_time,
                claim_reference_number=claim_ref,
                sentiment_detected=sentiment,
                llm_enhanced=False
            ).model_dump()
    
    def _generate_empathetic_response(
        self,
        customer_name: str,
        claim_text: str,
        template_body: str,
        sentiment: str
    ) -> str:
        """
        ALWAYS use LLM to generate 2-sentence empathetic opening + add template body
        
        KRITIEK: Elke zin MAX 15 woorden. Volg voorbeelden EXACT.
        """
        
        prompt = f"""
        TAAK: Schrijf 2 KORTE empathische zinnen. Elke zin MAX 15 woorden.
        
        KLANT: {customer_name}
        CLAIM: {claim_text[:400]}
        
        FORMAT:
        Beste {customer_name},
        
        [Zin 1: Empathie]. [Zin 2: Ontzorgen].
        
        ---
        [template volgt hier]
        
        VOLG DEZE VOORBEELDEN EXACT (let op de LENGTE!):
        
        1. "Wat vervelend dat uw laptop is gestolen uit uw auto. We helpen u hier snel mee."
        
        2. "Wat vervelend dat dit gebeurde terwijl uw dochter in het ziekenhuis ligt. We zorgen dat dit snel geregeld wordt zodat u zich kunt focussen op wat belangrijk is."
        
        3. "Wat vervelend dat uw auto beschadigd is door een winkelwagentje. We zorgen dat dit snel voor u geregeld wordt."
        
        4. "Wat een schrik moet het ongeluk op de A2 zijn geweest. We helpen u hier zo snel mogelijk doorheen."
        
        5. "Vervelend dat uw bedrijfswagen beschadigd is tijdens de leverrit. We begrijpen dat dit impact heeft op uw bedrijfsvoering."
        
        REGELS:
        - Zin 1: Benoem de SITUATIE in max 15 woorden
        - Zin 2: Ontzorg in max 15 woorden
        - Volg de STIJL van de voorbeelden
        - KORT EN BONDIG
        
        Begin met "Beste {customer_name}," gevolgd door een lege regel.
        Voeg dan de 2 zinnen toe.
        Voeg dan deze template toe:
        
        {template_body}
        """
        
        try:
            response = self.client.responses.create(
                model=self.model,
                reasoning={"effort": "low"},
                input=prompt
            )
            
            # Extract text
            enhanced_text = response.output_text.strip()
            
            # Clean markdown if present
            if enhanced_text.startswith('```'):
                enhanced_text = enhanced_text.split('```')[1].strip()
            
            return enhanced_text
            
        except Exception as e:
            print(f"⚠️ Agent 5 LLM Error: {e}")
            # Fallback: basic 2-sentence opening + template
            return f"Beste {customer_name},\n\nWat vervelend. We helpen u graag.\n\n{template_body}"
