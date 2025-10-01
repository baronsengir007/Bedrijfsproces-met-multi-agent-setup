"""
Config package initialization
"""

from config.agent_config import (
    AGENT_CONFIG,
    AGENT_SETTINGS,
    OPENAI_API_KEY,
    MODEL_NAME,
    TEMPERATURE
)

from config.routing_rules import (
    AUTO_APPROVE_THRESHOLD_EUROS,
    AUTO_APPROVE_MAX_FRAUD_RISK,
    AUTO_APPROVE_MIN_TYPE_CONFIDENCE,
    HIGH_VALUE_THRESHOLD,
    MEDIUM_VALUE_THRESHOLD,
    FRAUD_INVESTIGATION_THRESHOLD,
    FRAUD_MANUAL_REVIEW_THRESHOLD,
    CLAIM_TYPES,
    URGENCY_LEVELS,
    ROUTE_PATHS,
    TEAMS,
    SLA_BY_PRIORITY,
    calculate_priority,
    calculate_sla,
    should_auto_approve,
    select_response_template
)

from config.response_templates import (
    TEMPLATE_A_AUTO_APPROVE,
    TEMPLATE_B_STANDARD,
    TEMPLATE_C_MANUAL_REVIEW,
    TEMPLATE_D_ESCALATION,
    get_template,
    fill_template,
    sla_hours_to_days,
    generate_inspection_note,
    REVIEW_REASONS,
    PRIORITY_REASONS,
    CONTACT_TIMEFRAMES,
    RESPONSE_TIME_PHRASES
)

__all__ = [
    # Agent config
    "AGENT_CONFIG",
    "AGENT_SETTINGS",
    "OPENAI_API_KEY",
    "MODEL_NAME",
    "TEMPERATURE",
    
    # Routing rules
    "AUTO_APPROVE_THRESHOLD_EUROS",
    "AUTO_APPROVE_MAX_FRAUD_RISK",
    "AUTO_APPROVE_MIN_TYPE_CONFIDENCE",
    "HIGH_VALUE_THRESHOLD",
    "MEDIUM_VALUE_THRESHOLD",
    "FRAUD_INVESTIGATION_THRESHOLD",
    "FRAUD_MANUAL_REVIEW_THRESHOLD",
    "CLAIM_TYPES",
    "URGENCY_LEVELS",
    "ROUTE_PATHS",
    "TEAMS",
    "SLA_BY_PRIORITY",
    "calculate_priority",
    "calculate_sla",
    "should_auto_approve",
    "select_response_template",
    
    # Templates
    "get_template",
    "fill_template",
    "sla_hours_to_days",
    "generate_inspection_note",
    "REVIEW_REASONS",
    "PRIORITY_REASONS",
    "CONTACT_TIMEFRAMES",
    "RESPONSE_TIME_PHRASES"
]
