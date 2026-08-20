"""Route de capture différée : POST /api/alma/payments/{id}/captures."""

from fastapi import APIRouter

from app.models.orders_refunds_captures import CaptureCreateRequest
from app.services.alma_client import alma_client

router = APIRouter(prefix="/payments", tags=["Capture"])


@router.post("/{payment_id}/captures", summary="Capture différée (paiement à l'expédition)")
async def capture_payment(payment_id: str, payload: CaptureCreateRequest) -> dict:
    """Déclenche le premier prélèvement d'un payment créé avec `capture_method: "manual"`.

    - Sans `amount` → capture complète de la première échéance.
    - À déclencher dans les 7 jours après l'autorisation, sinon expiration.
    - Captures multiples non supportées.
    """
    return alma_client.capture_payment(payment_id, payload.model_dump(exclude_none=True))
