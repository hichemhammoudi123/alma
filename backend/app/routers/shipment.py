"""Route d'expédition (endpoint Alma v2)."""

from fastapi import APIRouter

from app.models.orders_refunds_captures import ShipmentRequest
from app.services.alma_client import alma_client

router = APIRouter(prefix="/orders", tags=["Shipment"])


@router.post("/{order_id}/shipment", summary="Envoyer les informations d'expédition")
async def send_shipment(order_id: str, payload: ShipmentRequest) -> dict:
    """Envoie les données de suivi d'une commande.

    ⚠️ Endpoint Alma en **v2** et réservé aux marchands français.
    `order_id` = ID Alma de la commande (order_...).
    """
    return alma_client.send_shipment(order_id, payload.model_dump(exclude_none=True))
