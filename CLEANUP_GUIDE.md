# File Cleanup & Migration Guide

## 📋 FILES TO REPLACE

### ✅ REPLACE THESE FILES:

1. **crew_setup.py** → **crew_setup_new.py**
   - Old: Email handler workflow
   - New: Insurance claims workflow
   - Action: Delete old, rename new

2. **app.py** → **app_new.py**
   - Old: Email processing UI
   - New: Insurance claims UI
   - Action: Delete old, rename new

3. **README.md** → **README_NEW.md**
   - Old: Email handler documentation
   - New: Insurance claims documentation
   - Action: Delete old, rename new

### ❌ DELETE THESE FILES (no longer needed):

4. **models.py** (old root file)
   - Replaced by: `/models/claim_models.py`
   - Action: Delete

5. **config.py** (old root file)
   - Replaced by: `/config/agent_config.py`, `/config/routing_rules.py`, etc.
   - Action: Delete

6. **test_emails.txt** (old test data)
   - Replaced by: `/tests/test_claims/*.txt` (25 test claims)
   - Action: Delete

### 🔄 DELETE OLD AGENTS (in /agents folder):

7. `/agents/categorizer.py` → Replaced by `claim_type_classifier.py`
8. `/agents/classifier.py` → Replaced by `claim_type_classifier.py`
9. `/agents/sentiment.py` → Replaced by `fraud_risk_detector.py`
10. `/agents/urgency.py` → Replaced by `urgency_amount_analyzer.py`
11. `/agents/router.py` → Replaced by `smart_router.py`
12. `/agents/responder.py` → Replaced by `response_generator.py`

---

## 🎯 FINAL PROJECT STRUCTURE (after cleanup):

```
Bedrijfsproces_multi_agent/
│
├── docs/                          # ✅ NEW - Complete documentation
│   ├── use-cases/
│   │   ├── UC-001-smart-triage.md
│   │   └── UC-002-automated-communication.md
│   ├── architecture/
│   │   ├── architecture-overview.md
│   │   └── routing-logic.md
│   └── testing/
│
├── agents/                         # ✅ UPDATED - New claim agents
│   ├── __init__.py
│   ├── claim_type_classifier.py
│   ├── urgency_amount_analyzer.py
│   ├── fraud_risk_detector.py
│   ├── smart_router.py
│   └── response_generator.py
│
├── models/                         # ✅ NEW - Structured models
│   ├── __init__.py
│   └── claim_models.py
│
├── config/                         # ✅ NEW - Configuration files
│   ├── __init__.py
│   ├── agent_config.py
│   ├── routing_rules.py
│   └── response_templates.py
│
├── tests/                          # ✅ NEW - 25 test claims
│   └── test_claims/
│       ├── auto_claims.txt
│       ├── property_inboedel_claims.txt
│       ├── fraud_scenarios.txt
│       ├── edge_cases.txt
│       └── auto_approve_cases.txt
│
├── crew_setup.py                  # ✅ UPDATED - Rename from crew_setup_new.py
├── app.py                          # ✅ UPDATED - Rename from app_new.py
├── README.md                       # ✅ UPDATED - Rename from README_NEW.md
│
├── requirements.txt               # ✅ KEEP - Dependencies
├── Dockerfile                     # ✅ KEEP - Docker setup
├── docker-compose.yml             # ✅ KEEP - Docker Compose
├── .env.example                   # ✅ KEEP - Environment template
├── .gitignore                     # ✅ KEEP - Git ignore
│
└── .git/                          # ✅ KEEP - Git repository
```

---

## 🔧 MANUAL CLEANUP STEPS:

### Step 1: Backup (optional but recommended)
```bash
# Create backup of current state
git add .
git commit -m "Backup before cleanup"
```

### Step 2: Delete old files
```bash
# Delete old root files
rm models.py
rm config.py
rm test_emails.txt

# Delete old agent files
rm agents/categorizer.py
rm agents/classifier.py
rm agents/sentiment.py
rm agents/urgency.py
rm agents/router.py
rm agents/responder.py
```

### Step 3: Rename new files to main names
```bash
# Rename new files
mv crew_setup_new.py crew_setup.py
mv app_new.py app.py
mv README_NEW.md README.md
```

### Step 4: Test
```bash
# Test command line
python crew_setup.py

# Test Streamlit
streamlit run app.py
```

### Step 5: Commit
```bash
git add .
git commit -m "Migrated to insurance claims multi-agent system"
```

---

## ✅ VERIFICATION CHECKLIST:

After cleanup, verify:

- [ ] `crew_setup.py` exists and runs without errors
- [ ] `app.py` exists and Streamlit starts
- [ ] `README.md` shows insurance claims documentation
- [ ] `/agents/` folder contains only 5 new agents + `__init__.py`
- [ ] `/models/` folder exists with claim_models.py
- [ ] `/config/` folder exists with 3 config files
- [ ] `/tests/test_claims/` contains 5 text files with 25 test scenarios
- [ ] `/docs/` contains complete documentation
- [ ] Old files (models.py, config.py, test_emails.txt) are deleted
- [ ] Old agents (categorizer.py, etc.) are deleted

---

## 🚀 READY TO USE:

After cleanup and verification:

1. **Update .env file:**
   ```
   OPENAI_API_KEY=your-key-here
   ```

2. **Run tests:**
   ```bash
   python crew_setup.py
   ```

3. **Start UI:**
   ```bash
   streamlit run app.py
   ```

4. **Deploy (optional):**
   ```bash
   docker-compose up --build
   ```

---

**Status: All new files created, ready for manual cleanup!**
