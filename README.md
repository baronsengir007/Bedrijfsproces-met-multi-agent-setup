# Schadeclaim Verwerkingssysteem

Multi-agent AI systeem voor geautomatiseerde verwerking van verzekeringsclaims.

## Overzicht

Dit systeem gebruikt 5 gespecialiseerde AI agents om schadeclaims te analyseren en gepaste responses te genereren:

- **Agent 1-3:** Parallelle analyse (Type/Bedrag, Urgentie, Fraude)
- **Agent 4:** Pure Python router (geen LLM, instant routing)
- **Agent 5:** Response generator met empathische opening

**Performance:** ~30-50 seconden per claim | 4 LLM calls

---

## Waarom Custom Multi-Agent Architecture i.p.v. CrewAI?

Deze implementatie gebruikt een **custom multi-agent architectuur** in plaats van frameworks zoals CrewAI of OpenAI Agents om de volgende redenen:

### Performance & Efficiency
1. **Echte parallelle executie**: Agents 1-3 draaien simultaan via `asyncio.gather()`, waardoor de verwerkingstijd met 66% vermindert vergeleken met sequentiële executie
2. **Geen LLM voor routing**: Agent 4 gebruikt pure Python logica in plaats van een LLM call, wat €0.02 per claim bespaart en instant routing mogelijk maakt
3. **Minimale overhead**: Geen framework abstractions die performance beïnvloeden

### Controle & Transparantie  
4. **Expliciete flow control**: De verwerkingsstappen zijn direct zichtbaar in code (`crew_setup_openai.py`), wat debugging en onderhoud vergemakkelijkt
5. **Voorspelbaar gedrag**: Geen "black box" orchestratie door een framework
6. **Pydantic validation**: Strenge type-checking op alle agent outputs

### Use Case Specifiek
Deze use case vereist **onafhankelijke parallelle analyse** zonder inter-agent communicatie:
- Agent 1 classificeert alleen claim type & bedrag
- Agent 2 analyseert alleen urgentie  
- Agent 3 detecteert alleen fraude
- Geen collaboration tussen agents nodig

**Wanneer WEL CrewAI/OpenAI Agents gebruiken:**
- Agents moeten met elkaar communiceren ("collaborative reasoning")
- Dynamische task allocation is vereist
- Built-in memory tussen agents nodig is

Voor productie-ready insurance claim processing met strikte SLA's en kostencontrole is deze custom architectuur de optimale keuze.

---

## Vereisten

- **Docker Desktop** (voor containerized deployment)
  - Download: https://www.docker.com/products/docker-desktop
- **OpenAI API Key** 
  - Verkrijg via: https://platform.openai.com/api-keys

---

## Installatie & Gebruik

### Optie 1: Docker (Aanbevolen)

#### Stap 1: Clone repository
```bash
git clone https://github.com/baronsengir007/Bedrijfsproces-met-multi-agent-setup.git
cd Bedrijfsproces-met-multi-agent-setup
```

#### Stap 2: Maak .env bestand
Maak een bestand genaamd `.env` in de root directory met:
```
OPENAI_API_KEY=sk-proj-your-key-here
```

**Let op:** Vervang `sk-proj-your-key-here` met je echte OpenAI API key.

#### Stap 3: Start applicatie met Docker
```bash
docker-compose up --build
```

De eerste keer duurt dit 2-3 minuten (download Python, installeer packages).

#### Stap 4: Open in browser
Ga naar: **http://localhost:8501**

#### Stoppen
Druk `Ctrl+C` in de terminal, of run:
```bash
docker-compose down
```

---

### Optie 2: Lokaal (zonder Docker)

Als Docker niet beschikbaar is:

#### Stap 1: Installeer Python 3.11 of hoger
Download van: https://www.python.org/downloads/

#### Stap 2: Installeer dependencies
```bash
pip install -r requirements.txt
```

#### Stap 3: Maak .env bestand
Zelfde als bij Docker - maak `.env` met je API key.

#### Stap 4: Start applicatie
```bash
streamlit run app.py
```

#### Stap 5: Open in browser
Ga naar: **http://localhost:8501**

---

## Gebruik

1. **Voer schadeclaim in** (links)
2. **Klik "Verwerk Claim"**
3. **Bekijk resultaten:**
   - Respons van verzekeraar (rechts)
   - Multi-agent workflow visualisatie (onder)

### Voorbeeld Claims

**Auto - Auto-goedkeuring (<€750):**
```
Kleine kras op bumper door winkelwagentje.
Schade: €400
Polisnummer: AUTO-2024-12345
```

**Hoge waarde - Senior review:**
```
Ernstige aanrijding, total loss.
Cataloguswaarde: €28.000
Polisnummer: AUTO-2024-67890
```

**Verdacht - Fraudeonderzoek:**
```
Laptop gestolen uit auto.
Schatting: €2.200
Polis vorige week afgesloten.
```

---

## Technische Details

### Architectuur
- **Frontend:** Streamlit (Python)
- **Backend:** OpenAI GPT-4o-mini via API
- **Validation:** Pydantic v2
- **Deployment:** Docker + Docker Compose

### Multi-Agent Pipeline
1. **Fase 1:** 3 agents draaien parallel (Type/Bedrag, Urgentie, Fraude)
2. **Fase 2:** Pure Python router combineert analyses → routeringsbeslissing
3. **Fase 3:** Response generator maakt empathische klantcommunicatie

### LLM Gebruik
- **4 LLM calls per claim** (agents 1, 2, 3, 5)
- **0 LLM calls voor routing** (pure Python logica in agent 4)

### Performance
- Verwerkingstijd: 30-50 seconden per claim
- Target: 60-70% auto-approval rate
- Accuracy: >95% voor claim type classificatie

---

## Project Structuur

```
Bedrijfsproces_multi_agent/
├── app.py                          # Streamlit UI
├── crew_setup_openai.py            # Multi-agent pipeline
├── agents/
│   ├── type_amount_extractor.py    # Agent 1: Type & Bedrag
│   ├── urgency_analyzer.py         # Agent 2: Urgentie
│   ├── fraud_detector.py           # Agent 3: Fraude
│   ├── router.py                   # Agent 4: Router (Python)
│   └── response_generator_hybrid.py # Agent 5: Response
├── models/
│   └── pydantic_models.py          # Data validation
├── config/
│   └── prompts/                    # LLM prompts per agent
├── Dockerfile                      # Docker image definitie
├── docker-compose.yml              # Docker orchestratie
├── requirements.txt                # Python dependencies
└── .env                           # API keys (niet in Git!)
```

---

## Troubleshooting

### "OpenAI API key not found"
- Check of `.env` bestand bestaat
- Check of `OPENAI_API_KEY=sk-proj-...` correct is

### "Module not found"
```bash
pip install -r requirements.txt
```

### Docker build fails
- Zorg dat Docker Desktop draait
- Probeer: `docker-compose down` → `docker-compose up --build`

### Port 8501 already in use
- Stop andere Streamlit apps
- Of gebruik andere port in `docker-compose.yml`: `"8502:8501"`

---

## Output

Het systeem genereert:
- **Visuele analyse:** Claim type, urgentie, frauderisico
- **Routing beslissing:** Welk team + prioriteit + SLA
- **Klant response:** Empathische e-mail (Template A/B/C/D)
- **JSON export:** Volledige analyse downloadbaar

---

## Contact & Support

- **GitHub:** https://github.com/baronsengir007/Bedrijfsproces-met-multi-agent-setup
- **Issues:** Gebruik GitHub Issues voor bugs/vragen

---

## Licentie

Dit project is ontwikkeld voor educatieve doeleinden.
