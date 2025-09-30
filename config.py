"""
Configuration file voor Email Handler Multi-Agent System
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model settings
MODEL_NAME = "gpt-4o-mini"  # Cost-effective model
TEMPERATURE = 0.7

# Email categories
CATEGORIES = [
    "Spam",
    "Klacht",
    "Verzoek",
    "Informatieaanvraag",
    "Feedback",
    "Overig"
]

# Sentiment types
SENTIMENTS = [
    "Positive",
    "Neutral", 
    "Negative"
]

# Agent configurations
AGENT_CONFIG = {
    "classifier": {
        "role": "Email Classifier",
        "goal": "Accurate email classification into predefined categories",
        "backstory": """Je bent een expert in email triage met jaren ervaring.
        Je herkent snel het type en doel van een email en kunt deze classificeren."""
    },
    "sentiment": {
        "role": "Sentiment Analyzer",
        "goal": "Analyze emotional tone and urgency of emails",
        "backstory": """Je bent een expert in emotionele intelligentie en communicatie.
        Je begrijpt de nuances in taalgebruik en kunt sentiment nauwkeurig bepalen."""
    },
    "responder": {
        "role": "Response Generator",
        "goal": "Generate appropriate and professional email responses",
        "backstory": """Je bent een ervaren klantenservice professional.
        Je schrijft heldere, professionele en empathische antwoorden op emails."""
    }
}

# Response templates (voor consistency)
RESPONSE_TEMPLATES = {
    "Klacht": """Beste [naam],

Hartelijk dank voor uw bericht. Het spijt ons te horen dat u niet tevreden bent.

[specifieke response]

Wij doen er alles aan om dit op te lossen. Mocht u nog vragen hebben, aarzel dan niet om contact op te nemen.

Met vriendelijke groet,
Customer Service Team""",
    
    "Verzoek": """Beste [naam],

Hartelijk dank voor uw aanvraag.

[specifieke response]

Mocht u nog vragen hebben, laat het ons gerust weten.

Met vriendelijke groet,
Support Team""",
    
    "Informatieaanvraag": """Beste [naam],

Bedankt voor uw vraag.

[specifieke response]

Hopelijk beantwoordt dit uw vraag. Voor meer informatie kunt u altijd contact met ons opnemen.

Met vriendelijke groet,
Info Team"""
}
