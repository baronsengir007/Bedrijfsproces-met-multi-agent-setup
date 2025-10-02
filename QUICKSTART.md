# ⚡ Quick Start Guide

## Streamlit UI Starten (Lokaal)

```bash
# Stap 1: Installeer dependencies
pip install -r requirements.txt

# Stap 2: Start Streamlit
streamlit run app.py
```

Browser opent automatisch op: **http://localhost:8501**

---

## Docker Deployment

```bash
# Start alles met één commando
docker-compose up --build
```

Wacht 30 seconden, ga naar: **http://localhost:8501**

---

## Testen

### Test 1: Command Line
```bash
python crew_setup_openai.py
```
Dit draait 5 test cases door (~3-4 minuten).

### Test 2: Streamlit UI
1. Open http://localhost:8501
2. Voer testclaim in:
```
Kleine kras op bumper door winkelwagentje.
Schade: €400
Polisnummer: AUTO-2024-12345
```
3. Klik "Claim Verwerken"
4. Wacht ~30-40 seconden
5. Bekijk resultaten

---

## Verwachte Output

**Fase 1:** Type (Auto), Urgentie (Low), Fraud (Low)  
**Fase 2:** Route (Auto-Goedkeuring), Team (Geautomatiseerde Verwerking)  
**Fase 3:** Email met empathische opening + goedkeuring

---

## Problemen?

**"OpenAI API key not found"**
- Check `.env` bestand
- Zorg dat `OPENAI_API_KEY=sk-proj-...` erin staat

**"Module not found"**
- Run: `pip install -r requirements.txt`

**Docker werkt niet**
- Check: `docker --version`
- Install Docker Desktop als nodig

---

## Klaar voor Inlevering? ✅

- [ ] Command line test werkt (5 tests slagen)
- [ ] Streamlit UI werkt (kan claim verwerken)
- [ ] Docker image build succesvol
- [ ] Docker container draait op port 8501
- [ ] Alle code gepusht naar GitHub
- [ ] README.md up-to-date

Succes! 🚀
