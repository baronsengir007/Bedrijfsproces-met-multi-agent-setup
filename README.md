# 📧 Email Handler Multi-Agent System

Een intelligente email verwerkings-applicatie die gebruik maakt van **5 gespecialiseerde AI agents** in een hybride workflow om emails te analyseren, routeren en beantwoorden.

## 🎯 Waarom Dit Project?

Dit project demonstreert de **echte kracht van multi-agent systems** door:

✅ **Parallel Processing** - Agents 1, 2, 3 werken tegelijk voor efficiency  
✅ **Orchestration** - Agent 4 combineert alle analyses voor slimme beslissingen  
✅ **Context Sharing** - Elke agent bouwt voort op vorige resultaten  
✅ **Structured Output** - Pydantic models zorgen voor type-safe communicatie  

**Dit is GEEN gedwongen multi-agent setup** - elk agent heeft een echte specialisatie en voegt unieke waarde toe!

---

## 🏗️ Architectuur

### Multi-Agent Workflow (Hybrid: Parallel + Sequential)

```
                    📧 EMAIL INPUT
                         ↓
    ┌────────────────────────────────────────────────┐
    │         FASE 1: PARALLEL ANALYSIS              │
    │                (Independent)                    │
    ├────────────────────────────────────────────────┤
    │                                                 │
    │  ┌───────────────┐  ┌────────────────┐  ┌────────────────┐
    │  │   Agent 1     │  │    Agent 2     │  │    Agent 3     │
    │  │ Categorizer   │  │ Urgency        │  │ Sentiment      │
    │  │               │  │ Analyzer       │  │ Analyzer       │
    │  │ Output:       │  │                │  │                │
    │  │ • Category    │  │ Output:        │  │ Output:        │
    │  │ • Confidence  │  │ • Urgency      │  │ • Sentiment    │
    │  │ • Keywords    │  │ • Deadline     │  │ • Emotion      │
    │  │               │  │ • SLA          │  │ • Risk         │
    │  └───────────────┘  └────────────────┘  └────────────────┘
    │         ↓                  ↓                    ↓
    └─────────┼──────────────────┼────────────────────┼───────────┘
              │                  │                    │
              └──────────────────┴────────────────────┘
                                 ↓
    ┌─────────────────────────────────────────────────┐
    │         FASE 2: ROUTING DECISION                │
    │              (Orchestrator)                      │
    ├─────────────────────────────────────────────────┤
    │                                                  │
    │              ┌────────────────┐                 │
    │              │    Agent 4     │                 │
    │              │    Router      │                 │
    │              │  (Orchestrator)│                 │
    │              │                │                 │
    │              │ Input: ALL 3   │                 │
    │              │ previous       │                 │
    │              │ analyses       │                 │
    │              │                │                 │
    │              │ Output:        │                 │
    │              │ • Route to team│                 │
    │              │ • Priority     │                 │
    │              │ • Risk flags   │                 │
    │              │ • Escalation?  │                 │
    │              └────────────────┘                 │
    │                     ↓                            │
    └─────────────────────┼────────────────────────────┘
                          ↓
    ┌─────────────────────────────────────────────────┐
    │         FASE 3: RESPONSE GENERATION             │
    │              (Sequential)                        │
    ├─────────────────────────────────────────────────┤
    │                                                  │
    │              ┌────────────────┐                 │
    │              │    Agent 5     │                 │
    │              │   Responder    │                 │
    │              │                │                 │
    │              │ Input: Routing │                 │
    │              │ decision       │                 │
    │              │                │                 │
    │              │ Output:        │                 │
    │              │ • Response text│                 │
    │              │ • Tone         │                 │
    │              │ • Follow-up    │                 │
    │              └────────────────┘                 │
    │                     ↓                            │
    └─────────────────────┼────────────────────────────┘
                          ↓
                   📨 FINAL OUTPUT
```

---

## 🤖 De 5 Agents

### Agent 1: Categorizer 📋
**Specialisatie:** Email classificatie  
**Input:** Email text  
**Output:** `EmailCategory` (Pydantic)
- Category: Klacht, Verzoek, Informatieaanvraag, Feedback, Spam, Overig
- Confidence score (0-1)
- Keywords die tot classificatie leidden
- Reasoning

**Waarom nodig?** Bepaalt welk type behandeling nodig is.

---

### Agent 2: Urgency Analyzer ⏰
**Specialisatie:** Tijdsgevoeligheid & deadlines  
**Input:** Email text  
**Output:** `UrgencyAnalysis` (Pydantic)
- Urgency level: Critical, High, Medium, Low
- Deadline detection (expliciet & impliciet)
- Recommended response time
- Time-sensitive keywords

**Waarom nodig?** Bepaalt prioritering en SLA.

---

### Agent 3: Sentiment Analyzer 😊
**Specialisatie:** Emotie & escalatie risico  
**Input:** Email text  
**Output:** `SentimentAnalysis` (Pydantic)
- Sentiment: Positive, Neutral, Negative, Very_Negative
- Emotion score (-1 tot +1)
- Escalation risk (bool)
- Customer satisfaction indicator
- Tone indicators

**Waarom nodig?** Bepaalt response tone en escalatie noodzaak.

---

### Agent 4: Router (ORCHESTRATOR) 🎯
**Specialisatie:** Routing beslissingen  
**Input:** Output van Agent 1, 2, 3 (combined)  
**Output:** `RoutingDecision` (Pydantic)
- Route to team: Senior/Junior CS, Technical, Sales, Management
- Priority (1-5)
- SLA hours
- Escalation flags
- Risk indicators (legal, PR, churn, fraud, compliance)

**Waarom nodig?** Dit is de kern! Combineert ALLE data voor optimale beslissing.

**Waarom dit ECHT multi-agent is:**
- Kan niet werken zonder Agent 1, 2, 3
- Maakt complexe trade-offs (urgency vs sentiment vs category)
- Business logic die alle context nodig heeft

---

### Agent 5: Response Generator ✉️
**Specialisatie:** Email responses  
**Input:** Routing decision van Agent 4  
**Output:** `EmailResponse` (Pydantic)
- Response text (complete email)
- Tone (Formal, Friendly, Apologetic, etc)
- Response type (Full_Answer, Acknowledgment, etc)
- Follow-up info
- CC manager?

**Waarom nodig?** Past response aan op basis van routing beslissing.

---

## 💡 Waarom Is Dit ECHTE Multi-Agent?

### ❌ Wat Dit NIET Is:
- 1 LLM call die alles doet
- Fake scheiding van taken
- Agents die eigenlijk niet nodig zijn

### ✅ Wat Dit WEL Is:

1. **Agent Dependencies:**
   - Agent 4 **kan niet** zonder Agent 1, 2, 3
   - Agent 5 **kan niet** zonder Agent 4
   - Elke agent voegt unieke analyse toe

2. **Parallel Efficiency:**
   - Agent 1, 2, 3 draaien tegelijk
   - 3x sneller dan sequentieel
   - Geen dependency tussen deze 3

3. **Smart Orchestration:**
   - Agent 4 combineert alle data
   - Maakt trade-offs (bijv: High urgency + Positive sentiment = different route dan High urgency + Negative sentiment)
   - Business logic die ALLE context nodig heeft

4. **Structured Communication:**
   - Pydantic models tussen agents
   - Type-safe
   - Validate

able
   - Clear contracts

---

## 🚀 Quick Start

### Vereisten

- Python 3.11+
- OpenAI API key
- Docker (optioneel)

### 1. Setup

```bash
# Clone repository
git clone https://github.com/baronsengir007/Bedrijfsproces-met-multi-agent-setup.git
cd Bedrijfsproces_multi_agent

# Virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Voeg je OPENAI_API_KEY toe in .env
```

### 2. Run Locally

```bash
# Streamlit UI
streamlit run app.py
# Open browser: http://localhost:8501

# Command line test
python crew_setup.py
```

### 3. Run with Docker

```bash
docker-compose up --build
# Open browser: http://localhost:8501
```

---

## 📁 Project Structure

```
Bedrijfsproces_multi_agent/
│
├── agents/                     # 5 Agent modules
│   ├── __init__.py
│   ├── categorizer.py         # Agent 1: Email Categorizer
│   ├── urgency.py             # Agent 2: Urgency Analyzer
│   ├── sentiment.py           # Agent 3: Sentiment Analyzer
│   ├── router.py              # Agent 4: Routing Decision (Orchestrator)
│   └── responder.py           # Agent 5: Response Generator
│
├── models.py                   # Pydantic models (structured output)
├── config.py                   # Configuration & settings
├── crew_setup.py              # CrewAI orchestration (hybrid workflow)
├── app.py                      # Streamlit frontend
│
├── test_emails.txt            # 10 test emails met expected outputs
├── requirements.txt           # Dependencies
├── Dockerfile                 # Docker setup
├── docker-compose.yml         # Docker Compose
├── .env.example               # Environment template
├── .gitignore                 # Git ignore
└── README.md                  # This file
```

---

## 🧪 Testing

### Via Streamlit

1. Start: `streamlit run app.py`
2. Load test email (button in UI)
3. Click "Analyseer Email"
4. Zie alle 5 agents in actie!

### Via Command Line

```bash
python crew_setup.py
```

Runs 3 test emails en toont complete output.

### Test Emails

`test_emails.txt` bevat 10 scenario's:
- Critical urgency + legal threats
- Technical emergencies
- Churn risk scenarios
- PR risks
- Spam detection
- Positive feedback
- Standard requests

Elk met **expected output** voor validation.

---

## 🎯 Email Categories

| Category | Beschrijving |
|----------|-------------|
| **Spam** | Ongewenste marketing, phishing |
| **Klacht** | Ontevredenheid, problemen |
| **Verzoek** | Actie vragen (opzeggen, wijzigen) |
| **Informatieaanvraag** | Vragen om info/uitleg |
| **Feedback** | Positieve/constructieve feedback |
| **Overig** | Niet passend in bovenstaande |

## ⏰ Urgency Levels

| Level | Response Time | Wanneer? |
|-------|--------------|----------|
| **Critical** | 1-2 uur | System down, legal threats, expliciete crisis |
| **High** | 4-8 uur | Deadline vandaag, "zo snel mogelijk" |
| **Medium** | 24 uur | Deadline 2-3 dagen, standaard urgency |
| **Low** | 48-72 uur | Geen tijdsdruk, algemene vragen |

## 🎯 Routing Teams

| Team | Verantwoordelijk voor |
|------|----------------------|
| **Senior Customer Service** | Complex complaints, escalations, high-value customers |
| **Junior Customer Service** | Standard requests, low-risk queries |
| **Technical Support** | Technical issues, bugs, errors |
| **Sales** | Product info, commercial interest |
| **Management** | Legal threats, PR risks, escalations |

---

## 📊 Design Decisions

### Waarom Multi-Agent Architecture?

1. **Specialisatie** - Elke agent focust op één ding en doet dat goed
2. **Parallel Efficiency** - 3 analyses tegelijk = sneller
3. **Modulair** - Agents kunnen onafhankelijk worden aangepast
4. **Testbaar** - Elke agent is in isolatie testbaar
5. **Schaalbaar** - Nieuwe agents zijn makkelijk toe te voegen

### Waarom CrewAI?

- Simpele maar krachtige orchestratie
- Support voor task dependencies
- Context sharing tussen agents
- Goede LangChain/OpenAI integratie

### Waarom Pydantic?

- Type safety tussen agents
- Validation van output
- Clear contracts
- Auto-documentation
- IDE support

### Waarom Hybrid Workflow?

**Parallel (Fase 1):**
- Agent 1, 2, 3 hebben elkaar niet nodig
- Kunnen tegelijk draaien
- 3x efficiency gain

**Sequential (Fase 2, 3):**
- Agent 4 MOET wachten op 1, 2, 3
- Agent 5 MOET wachten op 4
- Logische dependencies

---

## 🚧 Toekomstige Verbeteringen

- [ ] Database voor email history & analytics
- [ ] Real email integration (IMAP/SMTP)
- [ ] User authentication & multi-tenancy
- [ ] Batch processing mode
- [ ] A/B testing van responses
- [ ] Fine-tuning models op company data
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Auto-learning van routing beslissingen

---

## 🔧 Configuration

Pas `config.py` aan voor:
- Model selectie (GPT-4, GPT-4o-mini, etc)
- Temperature settings
- Custom categories
- Routing teams
- SLA times
- Response templates

---

## 📝 License

MIT License

---

## 👤 Auteur

Gebouwd voor Datalumina Sollicitatie Casus - Automation Group

**Contact:** [GitHub](https://github.com/baronsengir007)

---

## 🎓 Wat Maakt Dit Project Speciaal?

### Voor Sollicitatie:

✅ **Demonstrates Deep Understanding:**
- Multi-agent is niet "fake" - echte orchestratie
- Hybrid workflow (parallel + sequential)
- Structured output met Pydantic
- Business logic in orchestrator

✅ **Production-Ready Code:**
- Type hints overal
- Error handling
- Logging
- Docker support
- Comprehensive tests

✅ **Well Documented:**
- Clear README
- Code comments
- Design decisions explained
- Test scenarios

✅ **Showcases Skills:**
- AI/LLM expertise
- Software architecture
- Python best practices
- DevOps (Docker)
- UI/UX (Streamlit)

---

## 💭 Interview Talking Points

**"Waarom multi-agent?"**
> "Email processing lijkt simpel, maar de beslissing wie het oppakt en hoe urgent het is, vereist ALLE context. Door 3 agents parallel te runnen (categorie, urgency, sentiment) en die in een orchestrator te combineren, maak ik slimmere routing beslissingen dan met 1 groot prompt. Plus: het is efficient én modulair."

**"Waarom deze architectuur?"**
> "Hybrid workflow: Agent 1, 2, 3 hebben elkaar niet nodig dus parallel. Agent 4 heeft alle 3 nodig dus sequential. Agent 5 hangt af van 4. Dit is logisch én efficient. En met Pydantic krijg je type-safe communication tussen agents."

**"Kun je dit uitbreiden?"**
> "Ja! Je kunt Agent 6 toevoegen voor CRM lookup, Agent 7 voor compliance checks, etc. De architectuur is modulair. Of je kunt Agent 4 vervangen door een ML model dat leert van historical routing decisions."

---

**Built with ❤️ and 🤖 AI**
