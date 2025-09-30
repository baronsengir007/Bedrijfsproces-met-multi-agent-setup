# 📧 Email Handler Multi-Agent System

Een intelligente email verwerkings-applicatie die gebruik maakt van meerdere gespecialiseerde AI agents om emails te classificeren, sentiment te analyseren en automatisch passende antwoorden te genereren.

## 🎯 Doel

Dit project automatiseert een belangrijk bedrijfsproces: het verwerken van inkomende emails. Door gebruik te maken van een multi-agent architectuur kunnen emails efficiënt worden geclassificeerd en van een passend antwoord worden voorzien.

## 🏗️ Architectuur

### Multi-Agent Workflow

```
Email Input
    ↓
┌─────────────────────────────────┐
│  Agent 1: Email Classifier      │
│  - Classificeert email type     │
│  - Output: Categorie            │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Agent 2: Sentiment Analyzer    │
│  - Analyseert emotionele toon   │
│  - Output: Sentiment            │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Agent 3: Response Generator    │
│  - Genereert passend antwoord   │
│  - Output: Draft email          │
└─────────────────────────────────┘
    ↓
Final Result
```

### Technologie Stack

- **Frontend**: Streamlit (Python web framework)
- **Agent Framework**: CrewAI (multi-agent orchestration)
- **LLM**: OpenAI GPT-4o-mini
- **Containerization**: Docker + Docker Compose

## 🚀 Quick Start

### Vereisten

- Python 3.11+
- OpenAI API key
- Docker (optioneel, voor containerized deployment)

### 1. Setup

```bash
# Clone de repository
git clone <your-repo-url>
cd Bedrijfsproces_multi_agent

# Maak virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Installeer dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Voeg je OPENAI_API_KEY toe in .env
```

### 2. Run Lokaal

```bash
# Start de Streamlit app
streamlit run app.py
```

Open browser op `http://localhost:8501`

### 3. Run met Docker

```bash
# Build en start container
docker-compose up --build

# Of in detached mode
docker-compose up -d

# Stop container
docker-compose down
```

## 📁 Project Structuur

```
Bedrijfsproces_multi_agent/
├── app.py                      # Streamlit frontend
├── crew_setup.py               # CrewAI orchestratie
├── config.py                   # Configuratie en settings
├── agents/                     # Agent modules
│   ├── __init__.py
│   ├── classifier.py           # Agent 1: Email Classifier
│   ├── sentiment.py            # Agent 2: Sentiment Analyzer
│   └── responder.py            # Agent 3: Response Generator
├── test_emails.txt             # Test voorbeelden
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuratie
├── docker-compose.yml          # Docker Compose setup
├── .env.example                # Environment variables template
└── README.md                   # Dit bestand
```

## 🧪 Testen

### Via Streamlit Interface

1. Start de applicatie
2. Kopieer een test email uit `test_emails.txt`
3. Plak in de interface
4. Klik op "Analyseer Email"
5. Bekijk de resultaten

### Via Command Line

```bash
# Test de crew setup direct
python crew_setup.py
```

## 🎯 Email Categorieën

Het systeem classificeert emails in de volgende categorieën:

- **Spam**: Ongewenste marketing, phishing
- **Klacht**: Uitingen van ontevredenheid
- **Verzoek**: Vragen om actie of hulp
- **Informatieaanvraag**: Vragen om informatie
- **Feedback**: Positieve of constructieve terugkoppeling
- **Overig**: Andere types

## 💭 Sentiment Types

- **Positive**: Vriendelijk, positief, opbouwend
- **Neutral**: Zakelijk, neutraal
- **Negative**: Boos, gefrustreerd, ontevreden

## 🔧 Configuratie

Pas `config.py` aan voor:

- Model selectie (GPT-4, GPT-3.5, etc)
- Temperature settings
- Custom categorieën
- Response templates
- Agent configuraties

## 📊 Design Decisions

### Waarom Multi-Agent?

1. **Specialisatie**: Elke agent focust op één specifieke taak
2. **Modulariteit**: Agents kunnen onafhankelijk worden aangepast
3. **Schaalbaarheid**: Nieuwe agents kunnen eenvoudig worden toegevoegd
4. **Testbaarheid**: Elke agent is in isolatie testbaar

### Waarom CrewAI?

- Simpele maar krachtige agent orchestratie
- Sequential processing (agents werken in volgorde)
- Goede integratie met LangChain en OpenAI
- Task context sharing tussen agents

### Waarom Streamlit?

- Snelle prototyping
- Python-native (geen JavaScript nodig)
- Makkelijk te deployen
- Goed voor data/AI applicaties

## 🚧 Toekomstige Verbeteringen

- [ ] Database voor email historie
- [ ] User authentication
- [ ] Email sending functionaliteit
- [ ] Batch processing
- [ ] Analytics dashboard
- [ ] Multiple language support
- [ ] Custom model fine-tuning

## 📝 License

MIT License

## 👤 Auteur

Gebouwd voor Datalumina sollicitatie casus

---

**Note**: Dit is een demonstratie project. Voor productie gebruik zou je extra features nodig hebben zoals error handling, logging, security, en monitoring.
