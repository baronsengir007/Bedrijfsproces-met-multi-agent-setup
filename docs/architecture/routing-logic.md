# Routing Decision Logic - Complete Decision Tree

## 🎯 Purpose

This document defines the **complete routing logic** for Agent 4 (Smart Router). All routing decisions follow this decision tree.

---

## 📊 Input Data

Agent 4 receives structured data from Agents 1, 2, and 3:

```python
# From Agent 1: Claim Type
type: str                    # "Auto", "Woning", "Inboedel", "Aansprakelijkheid"
type_confidence: float       # 0.0 - 1.0

# From Agent 2: Urgency & Amount
urgency_level: str          # "Critical", "High", "Medium", "Low"
amount_euros: float         # €0 - €1,000,000+
is_total_loss: bool
has_immediate_danger: bool

# From Agent 3: Fraud Risk
risk_score: float           # 0.0 - 1.0
risk_level: str             # "Low", "Medium", "High"
red_flags: List[str]
```

---

## 🚦 Configuration Thresholds

```python
# Defined in config/routing_rules.py

AUTO_APPROVE_THRESHOLD_EUROS = 750
AUTO_APPROVE_MAX_FRAUD_RISK = 0.3
AUTO_APPROVE_MIN_TYPE_CONFIDENCE = 0.8

HIGH_VALUE_THRESHOLD = 25000
MEDIUM_VALUE_THRESHOLD = 10000

FRAUD_INVESTIGATION_THRESHOLD = 0.6
FRAUD_MANUAL_REVIEW_THRESHOLD = 0.3
```

---

## 🌳 Complete Decision Tree

### LEVEL 1: Critical Conditions (Immediate Routing)

These conditions override everything else:

```
┌─────────────────────────────────────────────────────────┐
│ CONDITION 1A: High Fraud Risk                           │
├─────────────────────────────────────────────────────────┤
│ IF fraud_risk_score >= 0.6:                             │
│    → route_path = "SIU-Investigation"                   │
│    → route_to_team = "Special Investigations Unit"      │
│    → priority = 1                                        │
│    → sla_hours = 24                                      │
│    → response_template = "D"                            │
│    → requires_manager_approval = TRUE                   │
│    → escalation_flags = ["high_fraud_risk"]             │
│    → reasoning = "Frauderisico boven 0.6 - SIU onderzoek│
│                   vereist. Red flags: [lijst]"          │
│    STOP - No further checks needed                      │
└─────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────┐
│ CONDITION 1B: Critical Urgency with Immediate Danger    │
├─────────────────────────────────────────────────────────┤
│ IF urgency_level == "Critical" AND                      │
│    has_immediate_danger == TRUE:                        │
│    → route_path = "Senior-Adjuster-Emergency"           │
│    → route_to_team = "Senior Claims Team"               │
│    → priority = 1                                        │
│    → sla_hours = 2                                       │
│    → response_template = "D"                            │
│    → requires_immediate_contact = TRUE                  │
│    → escalation_flags = ["critical_urgency",            │
│                          "immediate_danger"]            │
│    → reasoning = "Kritieke urgentie met acuut gevaar - │
│                   onmiddellijke actie vereist"          │
│    STOP - No further checks needed                      │
└─────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────┐
│ CONDITION 1C: Extreme High Value                        │
├─────────────────────────────────────────────────────────┤
│ IF amount_euros > 100000:                               │
│    → route_path = "Senior-Adjuster-High-Value"          │
│    → route_to_team = "Senior Claims Team"               │
│    → priority = 1                                        │
│    → sla_hours = 8                                       │
│    → response_template = "C"                            │
│    → requires_manager_approval = TRUE                   │
│    → requires_inspection = TRUE                         │
│    → escalation_flags = ["extreme_high_value"]          │
│    → reasoning = "Bedrag boven €100k - senior specialist│
│                   en manager goedkeuring vereist"       │
│    STOP - No further checks needed                      │
└─────────────────────────────────────────────────────────┘
```

---

### LEVEL 2: Auto-Approve Check (Straight-Through Processing)

If none of the critical conditions apply, check for auto-approve eligibility:

```
┌─────────────────────────────────────────────────────────┐
│ AUTO-APPROVE CRITERIA (ALL must be TRUE)                │
├─────────────────────────────────────────────────────────┤
│ 1. amount_euros < 750                                   │
│ 2. fraud_risk_score < 0.3                               │
│ 3. type_confidence > 0.8                                │
│ 4. is_total_loss == FALSE                               │
│ 5. urgency_level != "Critical"                          │
│ 6. len(red_flags) == 0                                  │
├─────────────────────────────────────────────────────────┤
│ IF ALL criteria met:                                    │
│    → route_path = "Auto-Approve"                        │
│    → route_to_team = "Automated Processing"            │
│    → priority = 3                                        │
│    → sla_hours = 2                                       │
│    → response_template = "A"                            │
│    → requires_manager_approval = FALSE                  │
│    → escalation_flags = []                              │
│    → reasoning = "Voldoet aan alle auto-approve         │
│                   criteria: laag bedrag, laag risico,   │
│                   hoge confidence"                      │
│    STOP - Auto-approved!                                │
│                                                          │
│ ELSE:                                                    │
│    → Continue to LEVEL 3                                │
└─────────────────────────────────────────────────────────┘
```

---

### LEVEL 3: Standard Routing (Amount & Fraud Based)

If auto-approve fails, route based on amount and fraud risk:

```
┌─────────────────────────────────────────────────────────┐
│ ROUTE 3A: High Value + Medium-High Fraud Risk           │
├─────────────────────────────────────────────────────────┤
│ IF amount_euros > 10000 AND                             │
│    fraud_risk_score >= 0.3:                             │
│    → route_path = "Senior-Adjuster"                     │
│    → route_to_team = "Senior Claims Team"               │
│    → priority = 2                                        │
│    → sla_hours = 48                                      │
│    → response_template = "C"                            │
│    → requires_inspection = TRUE                         │
│    → escalation_flags = ["high_value_with_risk"]        │
│    → reasoning = "Hoog bedrag (>€10k) gecombineerd met │
│                   verhoogd frauderisico - senior review"│
│    STOP                                                  │
└─────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────┐
│ ROUTE 3B: High Value + Low Fraud Risk                   │
├─────────────────────────────────────────────────────────┤
│ IF amount_euros > 10000 AND                             │
│    fraud_risk_score < 0.3:                              │
│    → route_path = "Senior-Adjuster"                     │
│    → route_to_team = "Senior Claims Team"               │
│    → priority = 2                                        │
│    → sla_hours = 48                                      │
│    → response_template = "C"                            │
│    → requires_inspection = TRUE                         │
│    → escalation_flags = []                              │
│    → reasoning = "Hoog bedrag (>€10k) vereist senior   │
│                   beoordeling ondanks laag risico"      │
│    STOP                                                  │
└─────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────┐
│ ROUTE 3C: Medium Value + Medium Fraud Risk              │
├─────────────────────────────────────────────────────────┤
│ IF 750 <= amount_euros <= 10000 AND                     │
│    0.3 <= fraud_risk_score < 0.6:                       │
│    → route_path = "Standard-Adjuster"                   │
│    → route_to_team = "Claims Adjusters"                 │
│    → priority = 3                                        │
│    → sla_hours = 72                                      │
│    → response_template = "B"                            │
│    → escalation_flags = ["manual_review_needed"]        │
│    → reasoning = "Medium bedrag + medium risico -       │
│                   standaard handmatige review"          │
│    STOP                                                  │
└─────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────┐
│ ROUTE 3D: Medium Value + Low Fraud Risk                 │
├─────────────────────────────────────────────────────────┤
│ IF 750 <= amount_euros <= 10000 AND                     │
│    fraud_risk_score < 0.3:                              │
│    → route_path = "Junior-Adjuster"                     │
│    → route_to_team = "Junior Claims Team"               │
│    → priority = 3                                        │
│    → sla_hours = 72                                      │
│    → response_template = "B"                            │
│    → escalation_flags = []                              │
│    → reasoning = "Medium bedrag maar laag risico -      │
│                   geschikt voor junior behandelaar"     │
│    STOP                                                  │
└─────────────────────────────────────────────────────────┘
```

---

### LEVEL 4: Urgency Override

Urgency can override standard routing:

```
┌─────────────────────────────────────────────────────────┐
│ URGENCY OVERRIDE 4A: Critical + Not Yet Routed          │
├─────────────────────────────────────────────────────────┤
│ IF urgency_level == "Critical" AND                      │
│    NOT routed_in_previous_levels:                       │
│    → route_path = "Senior-Adjuster-Urgent"              │
│    → route_to_team = "Senior Claims Team"               │
│    → priority = 1                                        │
│    → sla_hours = 8                                       │
│    → response_template = "D"                            │
│    → escalation_flags = ["critical_urgency"]            │
│    → reasoning = "Kritieke urgentie vereist snelle     │
│                   senior review"                        │
│    STOP                                                  │
└─────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────┐
│ URGENCY OVERRIDE 4B: High + Not Yet Routed              │
├─────────────────────────────────────────────────────────┤
│ IF urgency_level == "High" AND                          │
│    NOT routed_in_previous_levels:                       │
│    → Upgrade priority by 1 level                        │
│    → Reduce SLA by 50%                                  │
│    → Add escalation_flag = ["high_urgency"]             │
│    → Otherwise use standard routing                     │
└─────────────────────────────────────────────────────────┘
```

---

### LEVEL 5: Type Confidence Check

Handle low confidence in claim type:

```
┌─────────────────────────────────────────────────────────┐
│ LOW CONFIDENCE HANDLING                                  │
├─────────────────────────────────────────────────────────┤
│ IF type_confidence < 0.5:                               │
│    → route_path = "Manual-Classification"               │
│    → route_to_team = "Claims Triage Team"               │
│    → priority = 3                                        │
│    → sla_hours = 48                                      │
│    → response_template = "B"                            │
│    → escalation_flags = ["type_unclear"]                │
│    → reasoning = "Type onzeker (confidence < 0.5) -    │
│                   handmatige classificatie vereist"     │
│    STOP                                                  │
└─────────────────────────────────────────────────────────┘
```

---

### LEVEL 6: Total Loss Handling

```
┌─────────────────────────────────────────────────────────┐
│ TOTAL LOSS DETECTION                                     │
├─────────────────────────────────────────────────────────┤
│ IF is_total_loss == TRUE:                               │
│    → Upgrade to Senior-Adjuster (minimum)               │
│    → priority = min(current_priority, 2)                │
│    → requires_inspection = TRUE                         │
│    → Add escalation_flag = ["total_loss"]               │
│    → response_template = "C"                            │
│    → reasoning += " - Total loss gedetecteerd"          │
└─────────────────────────────────────────────────────────┘
```

---

### LEVEL 7: Default Fallback

If somehow none of the above applied (edge case):

```
┌─────────────────────────────────────────────────────────┐
│ DEFAULT FALLBACK                                         │
├─────────────────────────────────────────────────────────┤
│ IF not routed yet:                                       │
│    → route_path = "Standard-Adjuster"                   │
│    → route_to_team = "Claims Adjusters"                 │
│    → priority = 3                                        │
│    → sla_hours = 72                                      │
│    → response_template = "B"                            │
│    → escalation_flags = ["default_routing"]             │
│    → reasoning = "Standaard routing - geen specifieke  │
│                   criteria getriggerd"                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Priority Assignment Logic

Priority is set based on multiple factors:

```python
def calculate_priority(urgency, amount, fraud_risk, is_total_loss):
    """
    Priority scale: 1 (highest) - 5 (lowest)
    """
    
    # Start with base priority from urgency
    if urgency == "Critical":
        priority = 1
    elif urgency == "High":
        priority = 2
    elif urgency == "Medium":
        priority = 3
    else:  # Low
        priority = 4
    
    # Adjust for high amount
    if amount > 25000:
        priority = min(priority, 1)  # Upgrade to P1
    elif amount > 10000:
        priority = min(priority, 2)  # Upgrade to P2
    
    # Adjust for fraud risk
    if fraud_risk >= 0.6:
        priority = 1  # High fraud = always P1
    elif fraud_risk >= 0.3:
        priority = min(priority, 2)  # Medium fraud = at least P2
    
    # Adjust for total loss
    if is_total_loss:
        priority = min(priority, 2)  # Total loss = at least P2
    
    return priority
```

---

## ⏱️ SLA Calculation Logic

```python
def calculate_sla(priority, urgency, is_auto_approve):
    """
    SLA in hours based on priority and special conditions
    """
    
    if is_auto_approve:
        return 2  # Auto-approve = 2 hours
    
    if urgency == "Critical" and has_immediate_danger:
        return 2  # Emergency = 2 hours
    
    # Standard SLA by priority
    sla_map = {
        1: 8,    # P1: 8 hours
        2: 24,   # P2: 24 hours  
        3: 72,   # P3: 72 hours
        4: 120,  # P4: 120 hours
        5: 168   # P5: 168 hours (7 days)
    }
    
    return sla_map.get(priority, 72)
```

---

## 🚩 Escalation Flags

Possible escalation flags that can be set:

| Flag | Meaning | Trigger Condition |
|------|---------|-------------------|
| `high_fraud_risk` | High fraud score detected | fraud_risk >= 0.6 |
| `critical_urgency` | Critical urgency level | urgency == "Critical" |
| `immediate_danger` | Immediate danger mentioned | has_immediate_danger == True |
| `extreme_high_value` | Very high claim amount | amount > €100k |
| `high_value_with_risk` | High amount + medium fraud | amount > €10k AND fraud > 0.3 |
| `total_loss` | Total loss detected | is_total_loss == True |
| `type_unclear` | Low type confidence | type_confidence < 0.5 |
| `manual_review_needed` | Standard manual review | Medium risk/amount |
| `multiple_red_flags` | Multiple fraud red flags | len(red_flags) >= 3 |

---

## 📋 Response Template Selection

```python
def select_template(route_path, priority, fraud_risk):
    """
    A: Auto-Approve (positive, quick)
    B: Standard Processing (professional, standard)
    C: Manual Review (thoughtful, detailed)
    D: Escalation/Investigation (empathetic, urgent)
    """
    
    if route_path == "Auto-Approve":
        return "A"
    
    if fraud_risk >= 0.6:
        return "D"  # Investigation
    
    if priority == 1:
        return "D"  # High priority = escalation template
    
    if route_path in ["Senior-Adjuster", "Senior-Adjuster-High-Value"]:
        return "C"  # Senior review
    
    # Default: standard template
    return "B"
```

---

## 🧪 Example Routing Decisions

### Example 1: Simple Auto-Approve
```
Input:
- type: "Auto", confidence: 0.95
- urgency: "Low"
- amount: €600
- fraud_risk: 0.15

Decision Tree Path:
LEVEL 1: No critical conditions → Continue
LEVEL 2: Auto-approve check
  ✅ amount < €750
  ✅ fraud_risk < 0.3
  ✅ type_confidence > 0.8
  ✅ NOT total_loss
  ✅ urgency != Critical
  ✅ no red_flags
  → AUTO-APPROVE!

Output:
- route_path: "Auto-Approve"
- priority: 3
- sla_hours: 2
- template: "A"
```

### Example 2: High Fraud Risk
```
Input:
- type: "Inboedel", confidence: 0.80
- urgency: "Medium"
- amount: €2000
- fraud_risk: 0.75
- red_flags: ["recent_policy", "vague_description"]

Decision Tree Path:
LEVEL 1: CONDITION 1A triggered
  ✅ fraud_risk >= 0.6
  → SIU INVESTIGATION!

Output:
- route_path: "SIU-Investigation"
- priority: 1
- sla_hours: 24
- template: "D"
- escalation_flags: ["high_fraud_risk"]
```

### Example 3: High Value
```
Input:
- type: "Auto", confidence: 0.90
- urgency: "High"
- amount: €35000
- fraud_risk: 0.20
- is_total_loss: True

Decision Tree Path:
LEVEL 1: No immediate critical condition
LEVEL 2: Auto-approve fails (amount > €750)
LEVEL 3: ROUTE 3B triggered
  ✅ amount > €10000
  ✅ fraud_risk < 0.3
  → SENIOR-ADJUSTER
LEVEL 6: Total loss upgrade
  ✅ is_total_loss
  → Requires inspection

Output:
- route_path: "Senior-Adjuster"
- priority: 2 (upgraded due to total loss)
- sla_hours: 48
- template: "C"
- requires_inspection: True
- escalation_flags: ["total_loss"]
```

---

## 🔄 Decision Tree Flowchart (Text Format)

```
START
  │
  ├─→ Fraud Risk >= 0.6? ──YES──→ SIU Investigation [P1, 24h, Template D]
  │        │
  │        NO
  │        ↓
  ├─→ Critical + Danger? ──YES──→ Senior Emergency [P1, 2h, Template D]
  │        │
  │        NO
  │        ↓
  ├─→ Amount > €100k? ──YES──→ Senior High-Value [P1, 8h, Template C]
  │        │
  │        NO
  │        ↓
  ├─→ Auto-Approve Criteria Met? ──YES──→ Auto-Approve [P3, 2h, Template A]
  │        │
  │        NO
  │        ↓
  ├─→ Amount > €10k? ──YES──→ Senior Adjuster [P2, 48h, Template C]
  │        │
  │        NO
  │        ↓
  ├─→ Fraud Risk >= 0.3? ──YES──→ Standard Adjuster [P3, 72h, Template B]
  │        │
  │        NO
  │        ↓
  ├─→ Amount > €750? ──YES──→ Junior Adjuster [P3, 72h, Template B]
  │        │
  │        NO
  │        ↓
  └─→ Type Confidence < 0.5? ──YES──→ Manual Triage [P3, 48h, Template B]
           │
           NO
           ↓
        DEFAULT ROUTE → Standard Adjuster [P3, 72h, Template B]
```

---

## 📊 Routing Statistics (Expected Distribution)

Based on 1000 claims:

| Route Path | Expected % | Priority | Avg SLA |
|------------|-----------|----------|---------|
| Auto-Approve | 60-70% | P3 | 2h |
| Junior Adjuster | 10-15% | P3-P4 | 72h |
| Standard Adjuster | 10-15% | P3 | 72h |
| Senior Adjuster | 5-10% | P2 | 48h |
| SIU Investigation | 2-5% | P1 | 24h |
| Emergency | <1% | P1 | 2h |

**Target: 60-70% auto-approval rate**

---

**Version:** 1.0  
**Last Updated:** 2025-10-01  
**Maintained By:** Datalumnia Automation Team
