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

# Urgency levels
URGENCY_LEVELS = [
    "Critical",  # Moet binnen 1-2 uur
    "High",      # Moet vandaag
    "Medium",    # Moet binnen 48 uur
    "Low"        # Kan wachten
]

# Sentiment types
SENTIMENTS = [
    "Positive",
    "Neutral",
    "Negative",
    "Very_Negative"
]

# Routing teams
ROUTING_TEAMS = [
    "Senior_Customer_Service",
    "Junior_Customer_Service",
    "Technical_Support",
    "Sales",
    "Management"
]

# Agent configurations
AGENT_CONFIG = {
    "categorizer": {
        "role": "Email Categorizer",
        "goal": "Accurately classify emails into predefined categories",
        "backstory": """Je bent een expert in email classificatie met 10+ jaar ervaring.
        Je herkent snel patronen en categorieën, zelfs in vage of ambigue emails.
        Je let op keywords, context en intentie van de afzender."""
    },
    
    "urgency": {
        "role": "Urgency Analyzer",
        "goal": "Determine urgency level and time sensitivity of emails",
        "backstory": """Je bent gespecialiseerd in het beoordelen van urgentie en deadlines.
        Je let op expliciete tijdsaanduidingen maar ook impliciete signalen zoals toon,
        context en business impact. Je begrijpt wanneer iets echt urgent is versus
        wanneer iemand alleen maar denkt dat het urgent is."""
    },
    
    "sentiment": {
        "role": "Sentiment & Emotion Analyzer",
        "goal": "Analyze emotional tone and identify escalation risks",
        "backstory": """Je bent een expert in emotionele intelligentie en communicatie.
        Je detecteert nuances in sentiment, van subtiele frustratie tot openlijke woede.
        Je kunt inschatten wanneer een klant op het punt staat te churnen of te escaleren.
        Je let op toon, woordkeuze, leestekens en emotionele signalen."""
    },
    
    "router": {
        "role": "Routing Decision Orchestrator",
        "goal": "Make optimal routing decisions based on all available analysis",
        "backstory": """Je bent een senior operations manager met 15+ jaar ervaring in
        customer service management. Je begrijpt perfect welke emails naar welk team moeten,
        welke prioriteit ze verdienen, en welke risico's ze met zich meebrengen.
        Je maakt data-driven beslissingen en balanceert klanttevredenheid met efficiency.
        Je weet wanneer escalatie nodig is en wanneer een junior team member het kan oppakken."""
    },
    
    "responder": {
        "role": "Professional Email Response Generator",
        "goal": "Generate contextually appropriate and professional email responses",
        "backstory": """Je bent een senior customer service professional en communication expert.
        Je schrijft empathische, heldere en effectieve email responses. Je past je tone aan
        op basis van de situatie: formeel bij klachten, vriendelijk bij vragen, oplossingsgericht
        bij problemen. Je vermijdt jargon en schrijft altijd in begrijpelijke taal.
        Je weet wanneer je je moet excuseren, wanneer je oplossingen moet bieden, en wanneer
        je om meer informatie moet vragen."""
    }
}

# SLA Settings (in hours)
SLA_BY_PRIORITY = {
    1: 2,   # Critical: 2 hours
    2: 8,   # High: 8 hours (same day)
    3: 24,  # Medium: 24 hours
    4: 48,  # Normal: 48 hours
    5: 72   # Low: 72 hours
}

# Response templates per category
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
Info Team""",
    
    "Feedback": """Beste [naam],

Hartelijk dank voor uw feedback!

[specifieke response]

We waarderen uw input enorm en zullen hiermee aan de slag gaan.

Met vriendelijke groet,
Team"""
}
