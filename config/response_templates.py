"""
Response Templates for Customer Communication

Defines the 4 email response templates (A, B, C, D) used by Agent 5.
Templates use placeholders that are filled in dynamically.
"""

# ==========================================
# TEMPLATE A: AUTO-APPROVE
# ==========================================

TEMPLATE_A_AUTO_APPROVE = """Beste {customer_name},

✅ GOEDGEKEURD: Uw claim is automatisch goedgekeurd!

WIJ HEBBEN ONTVANGEN:
• Type claim: {claim_type}
• Bedrag: €{amount}
• Incident datum: {incident_date}
• Polisnummer: {policy_number}

BETALING:
Het bedrag van €{amount} wordt binnen 2 werkdagen overgemaakt naar rekeningnummer eindigend op {account_last_digits}.

U ontvangt een aparte bevestiging zodra de betaling is verwerkt.

CLAIMNUMMER: {claim_reference}

Heeft u nog vragen? Neem gerust contact op via {contact_phone} of {contact_email}.

Met vriendelijke groet,
Claims Team
{company_name}
"""


# ==========================================
# TEMPLATE B: STANDARD PROCESSING
# ==========================================

TEMPLATE_B_STANDARD = """Beste {customer_name},

Hartelijk dank voor het indienen van uw claim.

WIJ HEBBEN ONTVANGEN:
• Type claim: {claim_type}
• Geschatte schade: €{amount}
• Incident datum: {incident_date}
• Polisnummer: {policy_number}

IN BEHANDELING:
Een van onze claims behandelaars gaat uw claim beoordelen.

VERWACHTE DOORLOOPTIJD:
U ontvangt binnen {processing_days} werkdagen bericht over de afhandeling van uw claim.

WAT GEBEURT ER NU?
• We beoordelen de schade aan de hand van uw opgave
• Indien nodig nemen we contact op voor aanvullende informatie
• U ontvangt een definitieve beslissing binnen de gestelde termijn

CLAIMNUMMER: {claim_reference}

Mocht u eerder vragen hebben, dan kunt u contact opnemen via {contact_phone} of {contact_email} onder vermelding van uw claimnummer.

Met vriendelijke groet,
Claims Team
{company_name}
"""


# ==========================================
# TEMPLATE C: MANUAL REVIEW NEEDED
# ==========================================

TEMPLATE_C_MANUAL_REVIEW = """Beste {customer_name},

Hartelijk dank voor het indienen van uw claim.

WIJ HEBBEN ONTVANGEN:
• Type claim: {claim_type}
• Geschatte schade: €{amount}
• Incident datum: {incident_date}
• Polisnummer: {policy_number}

EXTRA BEOORDELING NODIG:
Uw claim wordt zorgvuldig beoordeeld door een van onze gespecialiseerde behandelaars.

WAT BETEKENT DIT?
{review_reason}

Vanwege de aard van uw claim hebben we wat extra tijd en mogelijk aanvullende informatie nodig om alles goed te beoordelen.

VERWACHTE DOORLOOPTIJD:
Een behandelaar neemt binnen {processing_days} werkdagen persoonlijk contact met u op.

WAT KAN U VERWACHTEN?
• Een persoonlijke behandelaar wordt toegewezen aan uw claim
• Deze neemt telefonisch contact met u op voor eventuele vragen
{inspection_note}
• U wordt op de hoogte gehouden van de voortgang

CLAIMNUMMER: {claim_reference}

Voor directe vragen kunt u contact opnemen via {contact_phone} of {contact_email}.

Met vriendelijke groet,
Senior Claims Team
{company_name}
"""


# ==========================================
# TEMPLATE D: HIGH PRIORITY / ESCALATION
# ==========================================

TEMPLATE_D_ESCALATION = """Beste {customer_name},

Hartelijk dank voor het indienen van uw claim.

WIJ HEBBEN ONTVANGEN:
• Type claim: {claim_type}
• Geschatte schade: €{amount}
• Incident datum: {incident_date}
• Polisnummer: {policy_number}

HOOGSTE PRIORITEIT:
Uw claim krijgt onze speciale aandacht.

{priority_reason}

UW CLAIM:
• Prioriteit: Hoogste
• Toegewezen aan: Senior Claims Specialist

VOLGENDE STAPPEN:
Een senior behandelaar neemt {contact_timeframe} telefonisch contact met u op om de situatie te bespreken en de vervolgstappen door te nemen.

VERWACHTE REACTIETIJD: {response_time}

CLAIMNUMMER: {claim_reference}

Voor directe vragen kunt u bellen naar {priority_phone}.

Met vriendelijke groet,
Senior Claims Team
{company_name}
"""


# ==========================================
# TEMPLATE PLACEHOLDERS
# ==========================================

REQUIRED_PLACEHOLDERS = {
    "A": [
        "customer_name",
        "claim_type",
        "amount",
        "incident_date",
        "policy_number",
        "account_last_digits",
        "claim_reference",
        "contact_phone",
        "contact_email",
        "company_name"
    ],
    "B": [
        "customer_name",
        "claim_type",
        "amount",
        "incident_date",
        "policy_number",
        "processing_days",
        "claim_reference",
        "contact_phone",
        "contact_email",
        "company_name"
    ],
    "C": [
        "customer_name",
        "claim_type",
        "amount",
        "incident_date",
        "policy_number",
        "review_reason",
        "processing_days",
        "inspection_note",
        "claim_reference",
        "contact_phone",
        "contact_email",
        "company_name"
    ],
    "D": [
        "customer_name",
        "claim_type",
        "amount",
        "incident_date",
        "policy_number",
        "priority_reason",
        "contact_timeframe",
        "response_time",
        "claim_reference",
        "priority_phone",
        "company_name"
    ]
}


# ==========================================
# DEFAULT VALUES
# ==========================================

DEFAULT_VALUES = {
    "company_name": "Verzekeringen NL",
    "contact_phone": "020-1234567",
    "contact_email": "claims@verzekering.nl",
    "priority_phone": "020-1234567 (prioriteit lijn)",
    "account_last_digits": "1234",
    "customer_name": "klant"
}


# ==========================================
# REVIEW REASON TEMPLATES
# ==========================================

REVIEW_REASONS = {
    "high_amount": "Omdat uw claim een hoger bedrag betreft, willen we extra zorgvuldig zijn in onze beoordeling.",
    "complex_situation": "De situatie die u beschrijft vraagt om een gedetailleerde beoordeling door een specialist.",
    "additional_info_needed": "We hebben mogelijk aanvullende informatie nodig om een goede beslissing te kunnen nemen.",
    "requires_inspection": "Voor een accurate beoordeling is een inspectie ter plaatse nodig.",
    "fraud_concern": "Voor een zorgvuldige beoordeling van uw claim hebben we mogelijk aanvullende documentatie nodig.",
    "total_loss": "Omdat het om een totale schade gaat, wordt uw claim behandeld door onze gespecialiseerde afdeling."
}


# ==========================================
# PRIORITY REASON TEMPLATES
# ==========================================

PRIORITY_REASONS = {
    "critical_urgency": "We begrijpen dat dit een urgente situatie betreft en gaan hier met prioriteit mee aan de slag.",
    "immediate_danger": "Uw veiligheid staat voorop. We nemen direct contact met u op om de situatie te bespreken.",
    "high_value": "Vanwege het aanzienlijke schadebedrag wordt uw claim behandeld door onze senior specialisten.",
    "complex_case": "De complexiteit van uw claim vraagt om directe aandacht van een ervaren specialist.",
    "investigation_needed": "Voor een zorgvuldige afhandeling van uw claim is nader onderzoek vereist."
}


# ==========================================
# CONTACT TIMEFRAMES
# ==========================================

CONTACT_TIMEFRAMES = {
    "same_day": "vandaag nog",
    "within_hours": "binnen 4 uur",
    "within_24h": "binnen 24 uur",
    "within_48h": "binnen 2 werkdagen"
}


# ==========================================
# RESPONSE TIME PHRASES
# ==========================================

RESPONSE_TIME_PHRASES = {
    "2h": "Binnen 2-4 uur",
    "8h": "Binnen 8 uur",
    "24h": "Binnen 24 uur",
    "48h": "Binnen 2 werkdagen"
}


# ==========================================
# PROCESSING DAYS CALCULATION
# ==========================================

def sla_hours_to_days(sla_hours: int) -> str:
    """
    Convert SLA hours to readable processing days
    
    Args:
        sla_hours: SLA in hours
        
    Returns:
        Human-readable string (e.g., "3 werkdagen")
    """
    if sla_hours <= 8:
        return "1 werkdag"
    elif sla_hours <= 24:
        return "1-2 werkdagen"
    elif sla_hours <= 72:
        return "3 werkdagen"
    elif sla_hours <= 120:
        return "5 werkdagen"
    else:
        return "7 werkdagen"


# ==========================================
# INSPECTION NOTE GENERATION
# ==========================================

def generate_inspection_note(requires_inspection: bool) -> str:
    """
    Generate inspection note if inspection is required
    
    Args:
        requires_inspection: Whether inspection is needed
        
    Returns:
        Inspection note text or empty string
    """
    if requires_inspection:
        return "• Mogelijk is een schade-inspectie ter plaatse nodig (wordt ingepland)"
    return ""


# ==========================================
# TEMPLATE SELECTION HELPER
# ==========================================

TEMPLATE_MAP = {
    "A": TEMPLATE_A_AUTO_APPROVE,
    "B": TEMPLATE_B_STANDARD,
    "C": TEMPLATE_C_MANUAL_REVIEW,
    "D": TEMPLATE_D_ESCALATION
}


def get_template(template_type: str) -> str:
    """
    Get template by type
    
    Args:
        template_type: A, B, C, or D
        
    Returns:
        Template string
        
    Raises:
        ValueError: If template_type is invalid
    """
    if template_type not in TEMPLATE_MAP:
        raise ValueError(f"Invalid template type: {template_type}. Must be A, B, C, or D.")
    
    return TEMPLATE_MAP[template_type]


def fill_template(template_type: str, values: dict) -> str:
    """
    Fill template with provided values
    
    Args:
        template_type: A, B, C, or D
        values: Dictionary with placeholder values
        
    Returns:
        Filled template string
    """
    template = get_template(template_type)
    
    # Merge with default values
    final_values = {**DEFAULT_VALUES, **values}
    
    try:
        return template.format(**final_values)
    except KeyError as e:
        raise ValueError(f"Missing required placeholder: {e}")
