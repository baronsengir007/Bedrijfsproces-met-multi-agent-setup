"""
Agent 5: Response Generator

Generates professional customer communication based on routing decision.
Selects and fills appropriate template (A, B, C, or D).
"""

from crewai import Agent, Task
from config import AGENT_CONFIG, AGENT_SETTINGS
from models import ClaimResponse
from datetime import datetime


class ResponseGeneratorAgent:
    """
    Agent 5: Generates customer email responses
    
    Specialization: Professional, context-appropriate communication
    Output: ClaimResponse (Pydantic model)
    """
    
    def __init__(self):
        """Initialize the response generator agent"""
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent with configuration"""
        config = AGENT_CONFIG["response_generator"]
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=AGENT_SETTINGS["verbose"],
            allow_delegation=AGENT_SETTINGS["allow_delegation"],
            llm=AGENT_SETTINGS["llm"]
        )
    
    def create_task(
        self,
        claim_text: str,
        claim_type: str,
        routing_decision_result: str
    ) -> Task:
        """
        Create a response generation task
        
        Args:
            claim_text: Original claim text
            claim_type: Claim type from Agent 1
            routing_decision_result: JSON output from Agent 4
            
        Returns:
            Task: CrewAI task object
        """
        
        # Generate claim reference number
        claim_ref = f"CLM-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        description = f"""
        TAAK: Genereer een professionele email response voor de klant op basis van de routing beslissing.
        
        ═══════════════════════════════════════════════════════════════
        ORIGINELE CLAIM
        ═══════════════════════════════════════════════════════════════
        {claim_text}
        
        ═══════════════════════════════════════════════════════════════
        ROUTING BESLISSING (van Agent 4)
        ═══════════════════════════════════════════════════════════════
        {routing_decision_result}
        
        CLAIM TYPE: {claim_type}
        CLAIM REFERENCE: {claim_ref}
        
        ═══════════════════════════════════════════════════════════════
        TEMPLATE SELECTIE
        ═══════════════════════════════════════════════════════════════
        
        Kies het juiste template op basis van response_template_type in de routing decision:
        
        **TEMPLATE A: Auto-Approve** (response_template_type = "A")
        Wanneer: Claim is automatisch goedgekeurd
        Tone: Positief, Efficient, Enthousiast
        Structuur:
        ```
        Beste [Naam],
        
        ✅ GOEDGEKEURD: Uw claim is automatisch goedgekeurd!
        
        WIJ HEBBEN ONTVANGEN:
        • Type claim: [claim_type]
        • Bedrag: €[amount]
        • Incident datum: [datum of "Niet vermeld"]
        • Polisnummer: [nummer of "Wordt verwerkt"]
        
        BETALING:
        Het bedrag van €[amount] wordt binnen 2 werkdagen overgemaakt naar 
        uw rekeningnummer.
        
        U ontvangt een aparte bevestiging zodra de betaling is verwerkt.
        
        CLAIMNUMMER: {claim_ref}
        
        Heeft u nog vragen? Neem gerust contact op via 020-1234567.
        
        Met vriendelijke groet,
        Claims Team
        Verzekeringen NL
        ```
        
        **TEMPLATE B: Standard Processing** (response_template_type = "B")
        Wanneer: Standaard handmatige verwerking
        Tone: Professioneel, Reassuring
        Structuur:
        ```
        Beste [Naam],
        
        Hartelijk dank voor het indienen van uw claim.
        
        WIJ HEBBEN ONTVANGEN:
        • Type claim: [claim_type]
        • Geschatte schade: €[amount of "Nader te bepalen"]
        • Incident datum: [datum of "Niet vermeld"]
        • Polisnummer: [nummer of "Wordt verwerkt"]
        
        IN BEHANDELING:
        Een van onze claims behandelaars gaat uw claim beoordelen.
        
        VERWACHTE DOORLOOPTIJD:
        U ontvangt binnen [X werkdagen] bericht over de afhandeling van uw claim.
        
        WAT GEBEURT ER NU?
        • We beoordelen de schade aan de hand van uw opgave
        • Indien nodig nemen we contact op voor aanvullende informatie
        • U ontvangt een definitieve beslissing binnen de gestelde termijn
        
        CLAIMNUMMER: {claim_ref}
        
        Mocht u eerder vragen hebben, neem dan contact op via 020-1234567.
        
        Met vriendelijke groet,
        Claims Team
        Verzekeringen NL
        ```
        
        **TEMPLATE C: Manual Review** (response_template_type = "C")
        Wanneer: Senior review, complexe zaken, hoge bedragen
        Tone: Thoughtful, Transparant, Professioneel
        Structuur:
        ```
        Beste [Naam],
        
        Hartelijk dank voor het indienen van uw claim.
        
        WIJ HEBBEN ONTVANGEN:
        • Type claim: [claim_type]
        • Geschatte schade: €[amount of "Nader te bepalen"]
        • Incident datum: [datum of "Niet vermeld"]
        • Polisnummer: [nummer of "Wordt verwerkt"]
        
        EXTRA BEOORDELING NODIG:
        Uw claim wordt zorgvuldig beoordeeld door een van onze gespecialiseerde behandelaars.
        
        WAT BETEKENT DIT?
        [Reden: "Vanwege het bedrag" of "Vanwege de complexiteit" of 
         "Voor een zorgvuldige beoordeling"]
        
        VERWACHTE DOORLOOPTIJD:
        Een behandelaar neemt binnen [X werkdagen] persoonlijk contact met u op.
        
        WAT KAN U VERWACHTEN?
        • Een persoonlijke behandelaar wordt toegewezen aan uw claim
        • Deze neemt telefonisch contact met u op voor eventuele vragen
        [IF requires_inspection: "• Mogelijk is een schade-inspectie nodig"]
        • U wordt op de hoogte gehouden van de voortgang
        
        CLAIMNUMMER: {claim_ref}
        
        Voor directe vragen kunt u contact opnemen via 020-1234567.
        
        Met vriendelijke groet,
        Senior Claims Team
        Verzekeringen NL
        ```
        
        **TEMPLATE D: High Priority / Escalation** (response_template_type = "D")
        Wanneer: Critical urgency, SIU investigation, hoge prioriteit
        Tone: Empathetic, Urgent (maar niet alarmerend)
        Structuur:
        ```
        Beste [Naam],
        
        Hartelijk dank voor het indienen van uw claim.
        
        WIJ HEBBEN ONTVANGEN:
        • Type claim: [claim_type]
        • Geschatte schade: €[amount of "Nader te bepalen"]
        • Incident datum: [datum of "Niet vermeld"]
        • Polisnummer: [nummer of "Wordt verwerkt"]
        
        HOOGSTE PRIORITEIT:
        Uw claim krijgt onze speciale aandacht.
        
        [Pas aan op situatie:
         IF critical_urgency: "We begrijpen dat dit een urgente situatie betreft."
         IF high_amount: "Vanwege het aanzienlijke bedrag wordt uw claim door 
                         senior specialisten behandeld."
         IF fraud_risk: "Voor een zorgvuldige beoordeling hebben we mogelijk 
                        aanvullende informatie nodig."]
        
        VOLGENDE STAPPEN:
        Een senior behandelaar neemt [vandaag nog / binnen 24 uur] telefonisch 
        contact met u op om de situatie te bespreken.
        
        VERWACHTE REACTIETIJD: [2-4 uur / binnen 24 uur]
        
        CLAIMNUMMER: {claim_ref}
        
        Voor directe vragen kunt u bellen naar 020-1234567.
        
        Met vriendelijke groet,
        Senior Claims Team
        Verzekeringen NL
        ```
        
        ═══════════════════════════════════════════════════════════════
        INFORMATIE EXTRACTIE & VULLING
        ═══════════════════════════════════════════════════════════════
        
        Haal uit de originele claim:
        - Klantnaam (als vermeld, anders "klant")
        - Bedrag (uit routing decision)
        - Incident datum (als vermeld, anders "Niet vermeld")
        - Polisnummer (als vermeld, anders "Wordt verwerkt")
        
        Bereken processing tijd:
        - SLA 2h → "2 werkdagen" (voor auto-approve betaling)
        - SLA 8h → "1 werkdag"
        - SLA 24h → "1-2 werkdagen"
        - SLA 48-72h → "3 werkdagen"
        - SLA 120h+ → "5 werkdagen"
        
        ═══════════════════════════════════════════════════════════════
        OUTPUT FORMAT (JSON)
        ═══════════════════════════════════════════════════════════════
        
        Geef ALLEEN een JSON object terug in dit exacte format:
        
        {{
            "response_text": "Beste klant,\n\n[Complete email text hier]\n\nMet vriendelijke groet,\nClaims Team",
            "template_used": "A" | "B" | "C" | "D",
            "tone": "Professional-Positive" | "Professional" | "Thoughtful" | "Empathetic-Urgent",
            "includes_approval": true/false,
            "includes_next_steps": true,
            "estimated_processing_time": "2 werkdagen",
            "claim_reference_number": "{claim_ref}"
        }}
        
        TONE MAPPING:
        - Template A → "Professional-Positive"
        - Template B → "Professional"
        - Template C → "Thoughtful"
        - Template D → "Empathetic-Urgent"
        
        INCLUDES_APPROVAL:
        - true alleen voor Template A (auto-approve)
        - false voor alle andere templates
        
        KRITIEKE VEREISTEN:
        1. Email moet compleet zijn - niet alleen een snippet
        2. Gebruik correcte claim reference: {claim_ref}
        3. Tone moet passen bij situatie
        4. Geen jargon - heldere, begrijpelijke taal
        5. Concrete timelines - geen vage "zo snel mogelijk"
        6. Response moet VOLLEDIG IN HET NEDERLANDS zijn
        7. Gebruik correct Nederlands email format
        
        Geef ALLEEN het JSON object terug, geen extra tekst.
        """
        
        return Task(
            description=description,
            agent=self.agent,
            expected_output="JSON object met email response volgens ClaimResponse model"
        )
