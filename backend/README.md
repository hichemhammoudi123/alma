# Backend FastAPI — Intégration Alma (Customer Panel)

Backend proxy qui expose les endpoints Alma via `/api/alma/*`.
La clé d'API Alma est utilisée uniquement côté serveur (jamais exposée au frontend).

## Installation

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # Windows
```

La clé API est déjà renseignée dans `.env` (sandbox). Lancez :

```bash
uvicorn app.main:app --reload --port 8010
```

- Docs Swagger : http://localhost:8010/docs
- Docs ReDoc : http://localhost:8010/redoc

## Tests rapides

```bash
curl http://localhost:8000/api/alma/eligibility \
  -H "Content-Type: application/json" \
  -d "{\"payment\":{\"purchase_amount\":20000,\"installments_count\":[3,4]}}"
```

> ⚠️ En environnement professionnel, si un proxy intercepte le HTTPS avec un
> certificat auto-signé, mettre `ALMA_SSL_VERIFY=false` dans `.env`.

## Architecture

```
backend/
├── app/
│   ├── main.py                 # App FastAPI + CORS + routers
│   ├── config.py               # Settings (.env)
│   ├── models/                 # Schémas Pydantic (payloads + descriptions)
│   ├── routers/                # Routes /api/alma/*
│   └── services/
│       └── alma_client.py      # Client HTTP vers l'API Alma
```

Documentation globale de tous les endpoints (URL, payloads, réponses avec explication de chaque champ) :
[`README.md`](../README.md) à la racine du projet.
