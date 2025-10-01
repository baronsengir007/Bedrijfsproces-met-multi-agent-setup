# Insurance Claims Multi-Agent System - Architecture Overview

## 🏗️ System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                        CUSTOMER INPUT                            │
│                    (Claim Submission Text)                       │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                           │
│                     (crew_setup.py)                              │
│                                                                   │
│  • Manages agent workflow                                        │
│  • Handles parallel execution                                    │
│  • Coordinates data flow between agents                          │
│  • Error handling & logging                                      │
└────────────────────────────┬────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              PHASE 1: PARALLEL ANALYSIS                          │
│           (3 Independent Agents Run Simultaneously)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌───────────────────┐  ┌────────────────────┐  ┌────────────┐│
│   │    AGENT 1        │  │     AGENT 2        │  │  AGENT 3   ││
│   │  Claim Type       │  │   Urgency &        │  │  Fraud     ││
│   │  Classifier       │  │   Amount Analyzer  │  │  Risk      ││
│   │                   │  │                    │  │  Detector  ││
│   │  Input:           │  │  Input:            │  │  Input:    ││
│   │  • Raw claim text │  │  • Raw claim text  │  │  • Raw     ││
│   │                   │  │                    │  │    claim   ││
│   │  Output:          │  │  Output:           │  │    text    ││
│   │  • ClaimType      │  │  • Urgency-        │  │            ││
│   │    (Pydantic)     │  │    AmountAnalysis  │  │  Output:   ││
│   │  • Type: Auto     │  │    (Pydantic)      │  │  • Fraud-  ││
│   │  • Confidence:    │  │  • Urgency: Low    │  │    Risk-   ││
│   │    0.95           │  │  • Amount: €600    │  │    Analysis││
│   │  • Keywords: []   │  │  • SLA: 72h        │  │    (Pyd.)  ││
│   │  • Policy #       │  │  • Is_total_loss   │  │  • Risk:   ││
│   │  • Incident date  │  │                    │  │    0.15    ││
│   └───────────────────┘  └────────────────────┘  └────────────┘│
│            │                      │                      │       │
└────────────┼──────────────────────┼──────────────────────┼───────┘
             │                      │                      │
             └──────────────────────┴──────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│         PHASE 2: ROUTING DECISION (ORCHESTRATOR)                 │
│                    (Sequential Processing)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                    ┌─────────────────────────┐                   │
│                    │       AGENT 4           │                   │
│                    │    Smart Router         │                   │
│                    │   (Orchestrator)        │                   │
│                    │                         │                   │
│                    │  Input:                 │                   │
│                    │  • Output Agent 1, 2, 3 │                   │
│                    │  • Original claim text  │                   │
│                    │                         │                   │
│                    │  Processing:            │                   │
│                    │  ┌─────────────────┐   │                   │
│                    │  │ Decision Logic  │   │                   │
│                    │  │                 │   │                   │
│                    │  │ • Type check    │   │                   │
│                    │  │ • Amount check  │   │                   │
│                    │  │ • Fraud check   │   │                   │
│                    │  │ • Urgency check │   │                   │
│                    │  │                 │   │                   │
│                    │  │ → Route path    │   │                   │
│                    │  │ → Team assign   │   │                   │
│                    │  │ → Priority set  │   │                   │
│                    │  │ → SLA calc      │   │                   │
│                    │  │ → Template pick │   │                   │
│                    │  └─────────────────┘   │                   │
│                    │                         │                   │
│                    │  Output:                │                   │
│                    │  • RoutingDecision      │                   │
│                    │    (Pydantic)           │                   │
│                    │  • route_path           │                   │
│                    │  • route_to_team        │                   │
│                    │  • priority: 1-5        │                   │
│                    │  • sla_hours            │                   │
│                    │  • template_type        │                   │
│                    │  • escalation_flags     │                   │
│                    └─────────────────────────┘                   │
│                               │                                   │
└───────────────────────────────┼───────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│          PHASE 3: RESPONSE GENERATION                            │
│                 (Sequential Processing)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                    ┌─────────────────────────┐                   │
│                    │       AGENT 5           │                   │
│                    │  Response Generator     │                   │
│                    │                         │                   │
│                    │  Input:                 │                   │
│                    │  • RoutingDecision      │                   │
│                    │  • Original claim       │                   │
│                    │  • Claim details        │                   │
│                    │                         │                   │
│                    │  Processing:            │                   │
│                    │  ┌─────────────────┐   │                   │
│                    │  │ Template Select │   │                   │
│                    │  │                 │   │                   │
│                    │  │ IF template A:  │   │                   │
│                    │  │  → Auto-approve │   │                   │
│                    │  │  → Positive     │   │                   │
│                    │  │                 │   │                   │
│                    │  │ IF template B:  │   │                   │
│                    │  │  → Standard     │   │                   │
│                    │  │  → Professional │   │                   │
│                    │  │                 │   │                   │
│                    │  │ IF template C:  │   │                   │
│                    │  │  → Manual       │   │                   │
│                    │  │  → Thoughtful   │   │                   │
│                    │  │                 │   │                   │
│                    │  │ IF template D:  │   │                   │
│                    │  │  → Escalation   │   │                   │
│                    │  │  → Empathetic   │   │                   │
│                    │  └─────────────────┘   │                   │
│                    │                         │                   │
│                    │  Output:                │                   │
│                    │  • ClaimResponse        │                   │
│                    │    (Pydantic)           │                   │
│                    │  • response_text        │                   │
│                    │  • template_used        │                   │
│                    │  • tone                 │                   │
│                    │  • claim_reference      │                   │
│                    └─────────────────────────┘                   │
│                               │                                   │
└───────────────────────────────┼───────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                        FINAL OUTPUT                              │
│                                                                   │
│  • Complete triage analysis (all 3 agents)                       │
│  • Routing decision (agent 4)                                    │
│  • Customer response (agent 5)                                   │
│  • System logs & audit trail                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Specifications

### Agent 1: Claim Type Classifier

**Responsibility:** Identify the type of insurance claim

**Technology:**
- LLM: GPT-4o-mini (via OpenAI API)
- Framework: CrewAI Agent
- Output: Pydantic model (ClaimType)

**Input:** Raw claim text

**Processing:**
1. Analyzes claim text for keywords and patterns
2. Identifies insurance domain (Auto, Woning, Inboedel, Aansprakelijkheid)
3. Extracts structured data (policy number, incident date)
4. Calculates confidence score

**Output Structure:**
```python
class ClaimType(BaseModel):
    type: str  # "Auto" | "Woning" | "Inboedel" | "Aansprakelijkheid"
    confidence: float  # 0.0 - 1.0
    keywords: List[str]
    policy_number: Optional[str]
    incident_date: Optional[str]
    reasoning: str
```

**Key Patterns Recognized:**
- Auto: "aanrijding", "schade auto", "kenteken", "bumper", "WA verzekering"
- Woning: "brand", "waterschade", "lekkage", "storm", "inbraak woning"
- Inboedel: "gestolen laptop", "inboedel", "diefstal", "inventaris"
- Aansprakelijkheid: "schade veroorzaakt", "aansprakelijk", "WA schade"

---

### Agent 2: Urgency & Amount Analyzer

**Responsibility:** Determine urgency level and extract damage amount

**Technology:**
- LLM: GPT-4o-mini (via OpenAI API)
- Framework: CrewAI Agent
- Output: Pydantic model (UrgencyAmountAnalysis)

**Input:** Raw claim text

**Processing:**
1. Scans for urgency keywords ("urgent", "spoed", "vandaag nog", "acuut")
2. Detects critical situations (total loss, immediate danger)
3. Extracts monetary amounts (€500, 1000 euro, vijfhonderd)
4. Calculates recommended SLA based on urgency

**Output Structure:**
```python
class UrgencyAmountAnalysis(BaseModel):
    urgency_level: str  # "Critical" | "High" | "Medium" | "Low"
    amount_euros: Optional[float]
    amount_confidence: float  # 0.0 - 1.0
    is_total_loss: bool
    has_immediate_danger: bool
    sla_hours: int
    deadline_detected: Optional[str]
    time_sensitive_keywords: List[str]
    reasoning: str
```

**Urgency Mapping:**
- **Critical:** Total loss, immediate danger, explicit emergency
- **High:** "Zo snel mogelijk", deadline today, urgent tone
- **Medium:** Standard timeline (2-3 days mentioned)
- **Low:** No urgency indicators, general inquiry

---

### Agent 3: Fraud Risk Detector

**Responsibility:** Assess fraud risk based on text patterns

**Technology:**
- LLM: GPT-4o-mini (via OpenAI API)
- Framework: CrewAI Agent
- Output: Pydantic model (FraudRiskAnalysis)

**Input:** Raw claim text

**Processing:**
1. Checks claim completeness (date, location, details present?)
2. Detects suspicious patterns (vague description, inconsistencies)
3. Identifies strategic amount positioning (€9,950 near €10k threshold)
4. Analyzes language-amount consistency
5. Detects "recent policy" or "repeat claim" mentions in text
6. Scores overall fraud risk (0.0 - 1.0)

**Output Structure:**
```python
class FraudRiskAnalysis(BaseModel):
    risk_score: float  # 0.0 - 1.0
    risk_level: str  # "Low" | "Medium" | "High"
    red_flags: List[str]
    suspicious_patterns: List[str]
    recommendation: str
    reasoning: str
```

**Risk Scoring Logic:**
```python
risk_score = 0.0

# Completeness penalties (0-0.3)
if no_incident_date: risk_score += 0.15
if no_location: risk_score += 0.10
if vague_description: risk_score += 0.15

# Timing signals (0-0.3)
if mentions_recent_policy: risk_score += 0.25
if mentions_repeat_claims: risk_score += 0.20

# Amount positioning (0-0.2)
if suspicious_amount_positioning: risk_score += 0.20

# Inconsistencies (0-0.3)
if language_vs_amount_mismatch: risk_score += 0.15
if conflicting_statements: risk_score += 0.25

# Cap at 1.0
risk_score = min(risk_score, 1.0)
```

**Risk Level Mapping:**
- **Low:** score < 0.3 → Auto-approve possible
- **Medium:** 0.3 ≤ score < 0.6 → Manual review
- **High:** score ≥ 0.6 → SIU investigation

---

### Agent 4: Smart Router (Orchestrator)

**Responsibility:** Make routing decisions based on all analysis

**Technology:**
- LLM: GPT-4o-mini (via OpenAI API)
- Framework: CrewAI Agent
- Output: Pydantic model (RoutingDecision)

**Input:** 
- Output from Agent 1 (ClaimType)
- Output from Agent 2 (UrgencyAmountAnalysis)
- Output from Agent 3 (FraudRiskAnalysis)
- Original claim text

**Processing:**
1. Evaluates all criteria against configured rules
2. Applies decision tree logic (see routing-logic.md)
3. Determines optimal route path
4. Assigns to appropriate team
5. Sets priority level (1-5)
6. Calculates SLA hours
7. Selects response template type

**Output Structure:**
```python
class RoutingDecision(BaseModel):
    route_path: str  # "Auto-Approve" | "Junior-Adjuster" | "Senior-Adjuster" | "SIU-Team"
    route_to_team: str
    priority: int  # 1-5 (1=highest)
    sla_hours: int
    requires_manager_approval: bool
    requires_inspection: bool
    response_template_type: str  # "A" | "B" | "C" | "D"
    escalation_flags: List[str]
    reasoning: str
```

**This is the CORE of the system** - combines all intelligence for optimal decision.

---

### Agent 5: Response Generator

**Responsibility:** Generate appropriate customer communication

**Technology:**
- LLM: GPT-4o-mini (via OpenAI API)
- Framework: CrewAI Agent
- Output: Pydantic model (ClaimResponse)

**Input:**
- RoutingDecision from Agent 4
- Original claim text
- Claim details (type, amount, customer name)

**Processing:**
1. Selects template based on `response_template_type`
2. Fills placeholders with claim-specific data
3. Adjusts tone based on routing decision
4. Generates claim reference number
5. Includes appropriate SLA commitment

**Output Structure:**
```python
class ClaimResponse(BaseModel):
    response_text: str  # Complete email body
    template_used: str  # "A" | "B" | "C" | "D"
    tone: str  # "Professional-Positive" | "Professional" | "Thoughtful" | "Empathetic-Urgent"
    includes_approval: bool
    includes_next_steps: bool
    estimated_processing_time: str
    claim_reference_number: str
```

**Template Selection:**
- **A (Auto-Approve):** Used when `route_path == "Auto-Approve"`
- **B (Standard):** Used for junior/standard adjuster routing
- **C (Manual Review):** Used for senior adjuster or complex cases
- **D (Escalation):** Used for SIU, high priority, or critical cases

---

## 🔄 Data Flow

### Phase 1: Parallel Analysis (Agents 1, 2, 3)

```
Claim Text → ┬→ Agent 1 → ClaimType
             ├→ Agent 2 → UrgencyAmountAnalysis
             └→ Agent 3 → FraudRiskAnalysis

Duration: ~5-8 seconds (parallel)
```

### Phase 2: Routing Decision (Agent 4)

```
ClaimType + UrgencyAmountAnalysis + FraudRiskAnalysis → Agent 4 → RoutingDecision

Duration: ~3-5 seconds
```

### Phase 3: Response Generation (Agent 5)

```
RoutingDecision + Claim Details → Agent 5 → ClaimResponse

Duration: ~3-5 seconds
```

**Total Processing Time: ~15-20 seconds**

---

## 🛠️ Technology Stack

### Core Technologies
- **Language Model:** GPT-4o-mini (OpenAI API)
- **Agent Framework:** CrewAI
- **Data Validation:** Pydantic v2
- **Programming Language:** Python 3.11+
- **Frontend:** Streamlit
- **Containerization:** Docker + Docker Compose

### Key Libraries
```
crewai==0.70.0
langchain==0.3.0
openai==1.50.0
pydantic==2.9.0
streamlit==1.39.0
python-dotenv==1.0.1
```

### Infrastructure
- **Deployment:** Docker containers
- **Configuration:** Environment variables (.env)
- **Logging:** Python logging module
- **Error Handling:** Try-except with fallbacks

---

## 📊 Performance Characteristics

### Throughput
- **Target:** 100+ claims per hour
- **Actual:** ~200 claims per hour (given 15-20s per claim)

### Latency
- **Parallel Phase:** 5-8 seconds
- **Routing Phase:** 3-5 seconds
- **Response Phase:** 3-5 seconds
- **Total:** 15-20 seconds end-to-end

### Accuracy (Target)
- **Type Classification:** >90%
- **Amount Extraction:** >85%
- **Fraud Detection Precision:** >70%
- **Fraud Detection Recall:** >80%
- **Routing Correctness:** >95%

---

## 🔐 Security & Privacy

### Data Protection
- No claim data stored permanently (unless configured)
- All API calls encrypted (HTTPS)
- Customer PII minimized in logs
- Compliance with GDPR requirements

### API Security
- OpenAI API key stored in environment variables
- No hardcoded credentials
- Rate limiting on API calls
- Error responses sanitized (no sensitive data exposure)

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Docker Container                 │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │     Streamlit Frontend (Port 8501) │ │
│  └──────────────┬─────────────────────┘ │
│                 │                        │
│  ┌──────────────▼─────────────────────┐ │
│  │      crew_setup.py (Orchestrator)  │ │
│  └──────────────┬─────────────────────┘ │
│                 │                        │
│  ┌──────────────▼─────────────────────┐ │
│  │      5 CrewAI Agents               │ │
│  │  (Agent 1, 2, 3, 4, 5)             │ │
│  └──────────────┬─────────────────────┘ │
│                 │                        │
│  ┌──────────────▼─────────────────────┐ │
│  │      Models & Config               │ │
│  │  (Pydantic, routing rules)         │ │
│  └────────────────────────────────────┘ │
│                                          │
└──────────────────┬───────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   OpenAI API        │
         │   (External)        │
         └─────────────────────┘
```

### Docker Compose Setup
```yaml
services:
  claims-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./logs:/app/logs
```

---

## 📝 Configuration Management

### Environment Variables
```
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.7
AUTO_APPROVE_THRESHOLD=750
MAX_FRAUD_RISK_AUTO_APPROVE=0.3
```

### Config Files Structure
```
config/
├── agent_config.py         # Agent roles, goals, backstories
├── routing_rules.py        # Decision thresholds and rules
└── response_templates.py   # Email templates A, B, C, D
```

---

## 🔄 Error Handling & Fallbacks

### Agent Failures
- **Retry logic:** 3 attempts per agent
- **Timeout:** 30 seconds per agent
- **Fallback:** Route to manual review on failure

### API Failures
- **OpenAI API down:** Fallback to "System unavailable" message
- **Network timeout:** Retry with exponential backoff
- **Rate limit:** Queue claims for processing

### Data Validation
- **Pydantic validation:** Ensures structured output
- **Missing data:** Use defaults and flag for review
- **Invalid amounts:** Mark as "Amount unclear"

---

## 📈 Monitoring & Logging

### Metrics Tracked
- Claims processed per hour
- Average processing time
- Agent accuracy rates
- Error rates by type
- Auto-approve rate
- SIU escalation rate

### Logging
```python
logs/
├── claims_processing.log   # Main application log
├── agent_outputs.log       # Individual agent outputs
└── errors.log              # Error tracking
```

---

## 🔮 Future Architecture Enhancements

### Planned Improvements
1. **Database Integration:**
   - Store claim history
   - Enable repeat claimer detection
   - Historical fraud pattern analysis

2. **Real-time Policy Lookup:**
   - Validate policy numbers
   - Check coverage details
   - Verify policy status (active/expired)

3. **Image Analysis:**
   - Agent 6: Damage Photo Analyzer
   - Automated damage assessment
   - Fraud detection from photos

4. **ML Model Integration:**
   - Replace rule-based fraud detection with ML model
   - Train on historical fraud cases
   - Continuous learning from outcomes

5. **Orchestration Optimization:**
   - True parallel execution (currently sequential in CrewAI)
   - Agent result caching
   - Adaptive routing based on workload

---

**Version:** 1.0  
**Last Updated:** 2025-10-01  
**Maintained By:** Datalumnia Automation Team
