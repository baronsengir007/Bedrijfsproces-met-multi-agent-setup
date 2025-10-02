# 🚀 Deployment Instructies

## Lokaal Testen (Streamlit)

### 1. Installeer dependencies
```bash
pip install -r requirements.txt
```

### 2. Zet OpenAI API key in .env
```bash
OPENAI_API_KEY=sk-proj-...
```

### 3. Start Streamlit app
```bash
streamlit run app.py
```

De app opent automatisch in je browser op `http://localhost:8501`

---

## Docker Deployment

### Optie 1: Docker Compose (Aanbevolen)

```bash
# Build en start container
docker-compose up --build

# Of in detached mode
docker-compose up -d --build

# Stop container
docker-compose down
```

### Optie 2: Pure Docker

```bash
# Build image
docker build -t insurance-claims-app .

# Run container
docker run -p 8501:8501 --env-file .env insurance-claims-app

# Stop container
docker stop <container_id>
```

### Container toegang
- **URL:** http://localhost:8501
- **Health check:** http://localhost:8501/_stcore/health

---

## Environment Variables

Zorg dat `.env` bestand bestaat met:

```
OPENAI_API_KEY=sk-proj-...
```

---

## Testen

### Command-line test (zonder UI)
```bash
python crew_setup_openai.py
```

Dit draait 5 test cases door en toont alle resultaten.

### Streamlit UI test
1. Start app: `streamlit run app.py`
2. Voer een test claim in
3. Klik "Claim Verwerken"
4. Bekijk alle 3 fases

---

## Troubleshooting

### "Module not found"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
Check `.env` bestand en zorg dat `OPENAI_API_KEY` correct is.

### Docker health check fails
Wacht 40 seconden na container start - OpenAI initialisatie duurt even.

### Port 8501 already in use
Stop andere Streamlit apps:
```bash
docker-compose down
# Of kill process op port 8501
```

---

## Production Checklist

- ✅ `.env` bestand met API key
- ✅ `requirements.txt` compleet
- ✅ Docker image gebuild
- ✅ Health check werkt
- ✅ Alle 5 test cases slagen
- ✅ Streamlit UI werkt
- ✅ Code gepusht naar GitHub

---

## Performance

- **Verwerkingstijd:** 30-50 seconden per claim
- **LLM Calls:** 4 per claim (Agents 1, 2, 3, 5)
- **Router:** Pure Python (instant, geen LLM)

---

## Support

Bij vragen of problemen, check de logs:

```bash
# Docker logs
docker-compose logs -f

# Of voor specifieke container
docker logs <container_name>
```
