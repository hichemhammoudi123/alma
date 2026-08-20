"""Point d'entrée du backend FastAPI — Intégration Alma (Customer Panel).

Lancement :
    uvicorn app.main:app --reload --port 8000

Docs auto : http://localhost:8000/docs
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import (
    balance,
    captures,
    eligibility,
    orders,
    pay_by_link,
    payments,
    refunds,
    shipment,
    webhooks,
)
from app.services.alma_client import AlmaAPIError

app = FastAPI(
    title="Alma API — Customer Panel Backend",
    description=(
        "Backend proxy vers l'API Alma (sandbox). La clé API Alma reste "
        "côté serveur uniquement. Voir endpoint.md pour la doc globale."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------- CORS
# Autorise le frontend React (http://localhost:3000 par défaut) à appeler le backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------- Gestion des erreurs Alma
@app.exception_handler(AlmaAPIError)
async def alma_error_handler(_: Request, exc: AlmaAPIError) -> JSONResponse:
    """Transforme une erreur Alma en réponse HTTP propre, lisible par le frontend."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": exc.error_code},
    )


# ------------------------------------------------------- Routes de base
@app.get("/", include_in_schema=False)
async def root() -> dict:
    return {
        "service": "Alma API — Customer Panel Backend",
        "docs": "/docs",
        "endpoint_md": "../endpoint.md",
    }


# ------------------------------------------------------- Routers
app.include_router(eligibility.router, prefix="/api/alma")
app.include_router(payments.router, prefix="/api/alma")
app.include_router(orders.router, prefix="/api/alma")
app.include_router(shipment.router, prefix="/api/alma")
app.include_router(refunds.router, prefix="/api/alma")
app.include_router(captures.router, prefix="/api/alma")
app.include_router(pay_by_link.router, prefix="/api/alma")
app.include_router(balance.router, prefix="/api/alma")
app.include_router(webhooks.router)
