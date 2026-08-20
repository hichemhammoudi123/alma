"""Routes d'éligibilité : POST /api/alma/eligibility."""

from fastapi import APIRouter

from app.models.payments import EligibilityRequest
from app.services.alma_client import alma_client

router = APIRouter(prefix="/eligibility", tags=["Eligibility"])


@router.post("", summary="Vérifier l'éligibilité d'un achat")
async def check_eligibility(payload: EligibilityRequest) -> list[dict] | dict:
    """Vérifie quels échéanciers Alma peuvent être proposés pour un panier.

    N'appelle pas de créer un paiement. À appeler AVANT d'afficher Alma
    dans le checkout, puis ne montrer au client que les échéanciers
    `eligible: true`.
    """
    return alma_client.eligibility(payload.model_dump(exclude_none=True))
