"""
Routing Rules Configuration

Defines all thresholds and decision criteria for Agent 4 (Smart Router).
These values can be easily adjusted without changing agent code.
"""

# ==========================================
# AUTO-APPROVE THRESHOLDS
# ==========================================

# Maximum amount (in euros) eligible for auto-approval
AUTO_APPROVE_THRESHOLD_EUROS = 750

# Maximum fraud risk score for auto-approval (0.0 - 1.0)
AUTO_APPROVE_MAX_FRAUD_RISK = 0.3

# Minimum type confidence required for auto-approval (0.0 - 1.0)
AUTO_APPROVE_MIN_TYPE_CONFIDENCE = 0.8


# ==========================================
# AMOUNT THRESHOLDS
# ==========================================

# High value threshold requiring senior adjuster
HIGH_VALUE_THRESHOLD = 25000

# Medium value threshold
MEDIUM_VALUE_THRESHOLD = 10000

# Extreme high value requiring immediate escalation
EXTREME_HIGH_VALUE_THRESHOLD = 100000


# ==========================================
# FRAUD RISK THRESHOLDS
# ==========================================

# Threshold for SIU investigation (0.0 - 1.0)
FRAUD_INVESTIGATION_THRESHOLD = 0.6

# Threshold for manual review due to fraud concerns (0.0 - 1.0)
FRAUD_MANUAL_REVIEW_THRESHOLD = 0.3


# ==========================================
# TYPE CONFIDENCE THRESHOLDS
# ==========================================

# Minimum confidence to proceed with routing
MIN_TYPE_CONFIDENCE = 0.5

# High confidence threshold
HIGH_TYPE_CONFIDENCE = 0.8


# ==========================================
# CLAIM TYPES
# ==========================================

CLAIM_TYPES = [
    "Auto",
    "Woning",
    "Inboedel",
    "Aansprakelijkheid"
]


# ==========================================
# URGENCY LEVELS
# ==========================================

URGENCY_LEVELS = [
    "Critical",  # Immediate action required (2h SLA)
    "High",      # Same day response required (8h SLA)
    "Medium",    # 2-3 day response (72h SLA)
    "Low"        # Standard processing (120h SLA)
]


# ==========================================
# ROUTE PATHS
# ==========================================

ROUTE_PATHS = {
    "auto_approve": "Auto-Approve",
    "junior_adjuster": "Junior-Adjuster",
    "standard_adjuster": "Standard-Adjuster",
    "senior_adjuster": "Senior-Adjuster",
    "senior_high_value": "Senior-Adjuster-High-Value",
    "senior_urgent": "Senior-Adjuster-Urgent",
    "senior_emergency": "Senior-Adjuster-Emergency",
    "siu_investigation": "SIU-Investigation",
    "manual_classification": "Manual-Classification"
}


# ==========================================
# TEAMS
# ==========================================

TEAMS = {
    "auto_approve": "Automated Processing",
    "junior_adjuster": "Junior Claims Team",
    "standard_adjuster": "Claims Adjusters",
    "senior_adjuster": "Senior Claims Team",
    "siu": "Special Investigations Unit",
    "triage": "Claims Triage Team"
}


# ==========================================
# PRIORITY LEVELS & SLA MAPPING
# ==========================================

# Priority levels: 1 (highest) to 5 (lowest)
PRIORITY_LEVELS = [1, 2, 3, 4, 5]

# SLA hours by priority level
SLA_BY_PRIORITY = {
    1: 8,    # P1: 8 hours (same day)
    2: 24,   # P2: 24 hours (next day)
    3: 72,   # P3: 72 hours (3 days)
    4: 120,  # P4: 120 hours (5 days)
    5: 168   # P5: 168 hours (7 days)
}

# Special SLA overrides
SLA_AUTO_APPROVE = 2  # Auto-approve = 2 hours
SLA_EMERGENCY = 2     # Emergency = 2 hours
SLA_SIU = 24          # SIU investigation = 24 hours


# ==========================================
# ESCALATION FLAGS
# ==========================================

ESCALATION_FLAGS = {
    "high_fraud_risk": "High fraud risk score detected (>=0.6)",
    "critical_urgency": "Critical urgency level",
    "immediate_danger": "Immediate danger or emergency situation",
    "extreme_high_value": "Claim amount exceeds €100,000",
    "high_value_with_risk": "High amount combined with elevated fraud risk",
    "total_loss": "Total loss detected",
    "type_unclear": "Low type confidence (<0.5)",
    "manual_review_needed": "Standard manual review required",
    "multiple_red_flags": "Multiple fraud red flags detected",
    "default_routing": "Routed via default fallback"
}


# ==========================================
# RESPONSE TEMPLATES
# ==========================================

RESPONSE_TEMPLATE_TYPES = {
    "A": "Auto-Approve (Positive, Quick)",
    "B": "Standard Processing (Professional, Standard)",
    "C": "Manual Review (Thoughtful, Detailed)",
    "D": "Escalation/Investigation (Empathetic, Urgent)"
}


# ==========================================
# ROUTING DECISION LOGIC
# ==========================================

def get_priority_by_urgency(urgency_level: str) -> int:
    """
    Get base priority from urgency level
    
    Args:
        urgency_level: Critical, High, Medium, or Low
        
    Returns:
        Priority level (1-5)
    """
    urgency_map = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }
    return urgency_map.get(urgency_level, 3)


def calculate_priority(
    urgency: str,
    amount: float,
    fraud_risk: float,
    is_total_loss: bool
) -> int:
    """
    Calculate final priority based on multiple factors
    
    Args:
        urgency: Urgency level
        amount: Claim amount in euros
        fraud_risk: Fraud risk score (0.0 - 1.0)
        is_total_loss: Whether claim is total loss
        
    Returns:
        Final priority (1-5)
    """
    # Start with urgency-based priority
    priority = get_priority_by_urgency(urgency)
    
    # Upgrade for high fraud risk
    if fraud_risk >= FRAUD_INVESTIGATION_THRESHOLD:
        priority = 1
    elif fraud_risk >= FRAUD_MANUAL_REVIEW_THRESHOLD:
        priority = min(priority, 2)
    
    # Upgrade for high amounts
    if amount > EXTREME_HIGH_VALUE_THRESHOLD:
        priority = 1
    elif amount > HIGH_VALUE_THRESHOLD:
        priority = min(priority, 1)
    elif amount > MEDIUM_VALUE_THRESHOLD:
        priority = min(priority, 2)
    
    # Upgrade for total loss
    if is_total_loss:
        priority = min(priority, 2)
    
    return priority


def calculate_sla(priority: int, is_auto_approve: bool, has_immediate_danger: bool) -> int:
    """
    Calculate SLA hours based on priority and special conditions
    
    Args:
        priority: Priority level (1-5)
        is_auto_approve: Whether this is auto-approved
        has_immediate_danger: Whether there's immediate danger
        
    Returns:
        SLA in hours
    """
    if is_auto_approve:
        return SLA_AUTO_APPROVE
    
    if has_immediate_danger:
        return SLA_EMERGENCY
    
    return SLA_BY_PRIORITY.get(priority, 72)


def should_auto_approve(
    amount: float,
    fraud_risk: float,
    type_confidence: float,
    is_total_loss: bool,
    urgency: str,
    red_flags_count: int
) -> bool:
    """
    Determine if claim should be auto-approved
    
    All conditions must be met for auto-approval.
    
    Args:
        amount: Claim amount in euros
        fraud_risk: Fraud risk score (0.0 - 1.0)
        type_confidence: Type classification confidence (0.0 - 1.0)
        is_total_loss: Whether claim is total loss
        urgency: Urgency level
        red_flags_count: Number of fraud red flags
        
    Returns:
        True if all auto-approve criteria are met
    """
    return (
        amount < AUTO_APPROVE_THRESHOLD_EUROS and
        fraud_risk < AUTO_APPROVE_MAX_FRAUD_RISK and
        type_confidence > AUTO_APPROVE_MIN_TYPE_CONFIDENCE and
        not is_total_loss and
        urgency != "Critical" and
        red_flags_count == 0
    )


def select_response_template(route_path: str, priority: int, fraud_risk: float) -> str:
    """
    Select appropriate response template
    
    Args:
        route_path: The route path chosen
        priority: Priority level
        fraud_risk: Fraud risk score
        
    Returns:
        Template type: A, B, C, or D
    """
    # Auto-approve always gets template A
    if route_path == ROUTE_PATHS["auto_approve"]:
        return "A"
    
    # High fraud risk gets investigation template
    if fraud_risk >= FRAUD_INVESTIGATION_THRESHOLD:
        return "D"
    
    # P1 priority gets escalation template
    if priority == 1:
        return "D"
    
    # Senior adjuster routes get manual review template
    if "Senior" in route_path:
        return "C"
    
    # Default: standard processing template
    return "B"


# ==========================================
# VALIDATION FUNCTIONS
# ==========================================

def validate_amount(amount: float) -> bool:
    """Validate that amount is within reasonable range"""
    return 0 <= amount <= 10_000_000  # Max 10 million euros


def validate_fraud_score(score: float) -> bool:
    """Validate fraud risk score is in valid range"""
    return 0.0 <= score <= 1.0


def validate_confidence(confidence: float) -> bool:
    """Validate confidence score is in valid range"""
    return 0.0 <= confidence <= 1.0


def validate_priority(priority: int) -> bool:
    """Validate priority is in valid range"""
    return priority in PRIORITY_LEVELS
