# UC-001: Smart Claim Triage

## 📋 Use Case Overview

**Use Case ID:** UC-001  
**Use Case Name:** Smart Claim Triage  
**Actor:** Claims Manager / Automated System  
**Goal:** Automatically classify, analyze, and route incoming insurance claims to the appropriate handling path

---

## 🎯 Business Value

**Problem:**
- Manual claim triage is time-consuming (5-10 minutes per claim)
- Inconsistent routing decisions between different claims handlers
- High-value or high-risk claims sometimes missed in initial assessment
- No standardized fraud risk screening at intake

**Solution:**
- Automated multi-agent system analyzes claims in <30 seconds
- Consistent routing based on objective criteria
- Automatic fraud risk scoring on every claim
- 60-70% of simple claims can be auto-approved (straight-through processing)

**Expected Impact:**
- ⏱️ **Time Savings:** 80% reduction in triage time
- 💰 **Cost Savings:** €50-100 per claim in handling costs
- 📊 **Consistency:** 100% standardized initial assessment
- 🚨 **Risk Reduction:** Early fraud detection prevents €100k+ annual losses

---

## 👥 Actors

**Primary Actor:**
- Claims Manager (oversees automated triage)
- Automated Triage System (performs classification)

**Secondary Actors:**
- Claims Adjusters (receive routed claims)
- SIU Team (Special Investigations Unit - receives high-risk claims)
- Customer (submits claim, receives acknowledgement)

---

## 📋 Preconditions

1. Customer has submitted a claim via email/web form/app
2. Claim contains minimum required information:
   - Customer identification (name/email)
   - Policy number
   - Basic incident description
3. System has access to:
   - OpenAI API (for LLM processing)
   - Routing rules configuration
   - Response templates

---

## 📤 Input

**Claim Submission Text** containing:
- Customer details (name, contact info)
- Policy number
- Incident description
- Estimated damage amount (optional)
- Incident date/time (optional)
- Supporting details (location, circumstances, etc.)

**Example Input:**
```
Beste verzekering,

Gisteren ben ik aangereden door een andere auto op de parkeerplaats 
van de supermarkt. De andere bestuurder heeft mijn achterbumper geraakt.

Schade schatting: ongeveer €600
Datum incident: 30 september 2025
Polisnummer: AUTO-2024-12345
Kenteken: AA-123-BB

De andere partij heeft zijn gegevens achtergelaten.

Met vriendelijke groet,
Jan Janssen
```

---

## 🔄 Process Flow

### **PHASE 1: Parallel Analysis** (Agents 1, 2, 3)

#### **Agent 1: Claim Type Classification**
**Input:** Full claim text  
**Processing:**
- Identifies claim category (Auto, Woning, Inboedel, Aansprakelijkheid)
- Extracts policy number
- Detects incident date
- Calculates confidence score

**Output:**
```json
{
  "type": "Auto",
  "confidence": 0.95,
  "keywords": ["aangereden", "bumper", "parkeerplaats", "kenteken"],
  "policy_number": "AUTO-2024-12345",
  "incident_date": "2025-09-30"
}
```

---

#### **Agent 2: Urgency & Amount Analysis**
**Input:** Full claim text  
**Processing:**
- Determines urgency level (Critical/High/Medium/Low)
- Extracts damage amount
- Detects time-sensitive keywords
- Checks for total loss indicators
- Calculates recommended SLA

**Output:**
```json
{
  "urgency_level": "Low",
  "amount_euros": 600.00,
  "amount_confidence": 0.85,
  "is_total_loss": false,
  "has_immediate_danger": false,
  "sla_hours": 72,
  "deadline_detected": null,
  "time_sensitive_keywords": []
}
```

---

#### **Agent 3: Fraud Risk Detection**
**Input:** Full claim text  
**Processing:**
- Checks for completeness (date, location, details)
- Detects suspicious patterns (vague descriptions, inconsistencies)
- Identifies strategic amount positioning (just under threshold)
- Analyzes language vs. amount consistency
- Detects recent policy mentions
- Scores overall fraud risk (0.0 - 1.0)

**Output:**
```json
{
  "risk_score": 0.15,
  "risk_level": "Low",
  "red_flags": [],
  "suspicious_patterns": [],
  "recommendation": "Auto-approve mogelijk (bij andere criteria OK)",
  "reasoning": "Claim bevat alle relevante details, geen verdachte patronen gedetecteerd"
}
```

---

### **PHASE 2: Routing Decision** (Agent 4: Orchestrator)

**Input:** Combined outputs from Agents 1, 2, 3  
**Processing:**
- Evaluates type confidence (>0.8 required for auto-approve)
- Checks amount against threshold (€750)
- Validates fraud risk score (<0.3 for auto-approve)
- Applies routing rules based on all criteria
- Determines team assignment
- Sets priority level (1-5)
- Calculates SLA hours

**Decision Tree:**
```
IF (amount < €750 AND fraud_risk < 0.3 AND type_confidence > 0.8):
    → Route: "Auto-Approve"
    → Team: "Automated Processing"
    → Priority: 3
    → SLA: 2 hours
    → Template: A

ELIF (fraud_risk >= 0.6):
    → Route: "SIU Investigation"
    → Team: "Special Investigations Unit"
    → Priority: 1
    → SLA: 24 hours
    → Template: D
    → Escalation: TRUE

ELIF (amount > €25000 OR urgency == "Critical"):
    → Route: "Senior Adjuster"
    → Team: "Senior Claims Team"
    → Priority: 1
    → SLA: 8 hours
    → Template: C
    → Requires inspection: TRUE

ELIF (amount > €750 OR fraud_risk >= 0.3):
    → Route: "Standard Adjuster"
    → Team: "Claims Adjusters"
    → Priority: 3
    → SLA: 72 hours
    → Template: B

ELSE:
    → Route: "Junior Adjuster"
    → Team: "Junior Claims Team"
    → Priority: 4
    → SLA: 120 hours
    → Template: B
```

**Output:**
```json
{
  "route_path": "Auto-Approve",
  "route_to_team": "Automated Processing",
  "priority": 3,
  "sla_hours": 2,
  "requires_manager_approval": false,
  "requires_inspection": false,
  "response_template_type": "A",
  "escalation_flags": [],
  "reasoning": "Claim voldoet aan alle auto-approve criteria: bedrag onder €750, laag frauderisico, hoge type confidence."
}
```

---

### **PHASE 3: Response Generation** (Agent 5)

**Input:** Routing decision + Original claim  
**Processing:**
- Selects appropriate response template (A/B/C/D)
- Fills in claim-specific details
- Adjusts tone based on routing decision
- Includes SLA commitment
- Adds claim reference number

**Output:**
```json
{
  "response_text": "Beste Jan Janssen,\n\nGoedgekeurd! Uw claim van €600 wordt binnen 2 werkdagen uitbetaald naar rekening NL...\n\nClaimnummer: CLM-20251001-001\n\nMet vriendelijke groet,\nClaims Team",
  "template_used": "A",
  "tone": "Professional-Positive",
  "includes_approval": true,
  "includes_next_steps": true,
  "estimated_processing_time": "2 werkdagen",
  "claim_reference_number": "CLM-20251001-001"
}
```

---

## 📤 Output

**For Customer:**
- Automated email acknowledgement
- Claim reference number
- Expected processing timeline
- Next steps (if any)

**For System:**
- Complete triage analysis (logged)
- Routing decision (stored)
- Fraud risk score (flagged if high)
- Auto-approval or assignment to claims team

---

## ✅ Success Criteria

**Functional:**
- ✅ Claim is classified into correct category (>90% accuracy)
- ✅ Amount is extracted correctly (>85% accuracy)
- ✅ Fraud risk is assessed and scored (0.0-1.0)
- ✅ Routing decision follows configured rules
- ✅ Customer receives acknowledgement within 2 minutes

**Non-Functional:**
- ✅ Total processing time <30 seconds
- ✅ System availability >99.5%
- ✅ All decisions are logged and auditable
- ✅ No personal data leakage

---

## 🚫 Failure Scenarios

**Scenario 1: Ambiguous Claim Type**
- **Trigger:** Type confidence <0.5
- **Handling:** Route to "Manual Review" with flag "Type unclear"
- **Response:** Template C (Manual Review)

**Scenario 2: Amount Cannot Be Extracted**
- **Trigger:** No amount mentioned or highly ambiguous
- **Handling:** Route to "Standard Adjuster" with flag "Amount missing"
- **Response:** Template B requesting more information

**Scenario 3: High Fraud Risk**
- **Trigger:** Risk score >0.6
- **Handling:** Route to "SIU Team" with all red flags
- **Response:** Template D (Investigation)

**Scenario 4: System Error**
- **Trigger:** LLM API failure, timeout, or parsing error
- **Handling:** Fallback to "Manual Review" queue
- **Response:** Generic acknowledgement with "We'll contact you within 24 hours"

---

## 📊 Key Performance Indicators

**Operational Metrics:**
- Average triage time per claim
- Auto-approval rate (target: 60-70%)
- Manual review rate (target: 20-30%)
- SIU escalation rate (target: 5-10%)

**Accuracy Metrics:**
- Type classification accuracy (target: >90%)
- Amount extraction accuracy (target: >85%)
- Fraud detection precision (target: >70%)
- Fraud detection recall (target: >80%)

**Customer Experience:**
- Time to first response (target: <2 minutes)
- Customer satisfaction with initial response (target: >4.0/5.0)

---

## 🔄 Post-Conditions

1. Claim is assigned to appropriate team/path
2. Customer has received acknowledgement
3. Claim is logged in system with full triage data
4. SLA timer has started
5. If auto-approved, payment process is initiated
6. If escalated, manager/SIU is notified

---

## 📝 Notes & Assumptions

**Assumptions:**
- Customers provide claims in Dutch language
- Basic claim info is always present (name, contact)
- Policy numbers follow standard format
- System has 24/7 access to OpenAI API

**Future Enhancements:**
- Integration with policy database for validation
- Historical claim lookup for repeat claimer detection
- Image analysis for damage assessment
- Multi-language support
- Real-time payment integration

---

## 🔗 Related Use Cases

- **UC-002:** Automated Customer Communication
- **UC-003:** Claims Dashboard & Analytics (future)
- **UC-004:** SIU Investigation Workflow (future)

---

**Version:** 1.0  
**Last Updated:** 2025-10-01  
**Owner:** Datalumnia Automation Team
