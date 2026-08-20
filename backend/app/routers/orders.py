"""Routes des orders : création sur payment existant, statut, expédition."""

from fastapi import APIRouter

from app.models.orders_refunds_captures import OrderCreateRequest, OrderStatusRequest, ShipmentRequest
from app.services.alma_client import alma_client

router = APIRouter(prefix="/payments", tags=["Orders"])


@router.post("/{payment_id}/orders", summary="Créer une Order pour un Payment existant")
async def create_order(payment_id: str, payload: OrderCreateRequest) -> list[dict] | dict:
    """Associe une Order à un Payment existant.

    Utilisé quand la référence de commande n'était pas disponible à la
    création du Payment (workflow : checkout → payment → commande → attach).
    `merchant_reference` fait le lien entre votre commande et Alma.
    """
    return alma_client.create_order(payment_id, payload.model_dump(exclude_none=True))


@router.post("/{payment_external_id}/orders/{merchant_order_reference}/status",
             summary="Envoyer le statut d'une commande")
async def send_order_status(
    payment_external_id: str, merchant_order_reference: str, payload: OrderStatusRequest
) -> dict:
    """Enregistre le statut d'une commande (ex. shipped / is_shipped=true).

    `payment_external_id` = ID Alma du payment.
    `merchant_order_reference` = la référence marchand de la commande.
    """
    return alma_client.send_order_status(
        payment_external_id, merchant_order_reference, payload.model_dump(exclude_none=True)
    )
