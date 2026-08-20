"""Route des remboursements : POST /api/alma/payments/{id}/refunds."""

from fastapi import APIRouter

from app.models.orders_refunds_captures import RefundCreateRequest
from app.services.alma_client import alma_client

router = APIRouter(prefix="/payments", tags=["Refunds"])


@router.post("/{payment_id}/refunds", summary="Créer un remboursement")
async def create_refund(payment_id: str, payload: RefundCreateRequest) -> dict:
    """Rembourse le client sur un payment.

    - Sans `amount` → remboursement intégral.
    - Avec `amount` → remboursement partiel (somme totale <= purchase_amount).
    - Alma gère l'allocation entre les échéances et le remboursement des frais.
    """
    return alma_client.create_refund(payment_id, payload.model_dump(exclude_none=True))
