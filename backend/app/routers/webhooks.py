"""Routes des notifications Alma : IPN (GET) et webhooks bêta (POST)."""

from fastapi import APIRouter, HTTPException, Query

from app.models.webhooks import WebhookEnvelope
from app.services.alma_client import AlmaAPIError, alma_client

router = APIRouter(tags=["Webhooks / IPN"])


@router.get("/api/alma/ipn", summary="IPN : notification asynchrone de paiement réussi")
async def ipn(pid: str = Query(..., description="Identifiant du payment Alma concerné")) -> dict:
    """Endpoint appelé par Alma (GET ipn_callback_url?pid=payment_xxx).

    Alma rejoue jusqu'à 10 fois si la réponse n'est pas 200.
    IMPORTANT — sécurité : le GET n'est pas signé. Vérifier l'authenticité
    en rappelant GET /payments/{pid} avec la clé privée, puis :
      - processing_status ∈ {authorized, captured} → succès
      - purchase_amount == montant du panier
      - custom_data.order_id == votre référence de commande
    Ensuite marquer la commande PAID (traitement idempotent).
    """
    payment_id = pid
    try:
        payment = alma_client.get_payment(payment_id)
    except AlmaAPIError as exc:
        # Répondre 200 quand même ? Non : une erreur 4xx/5xx fait retenter Alma.
        # On renvoie une erreur HTTP pour que Alma rejoue l'IPN.
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    return {"received": True, "payment_id": payment_id, "payment": payment}


@router.post("/api/alma/webhooks", summary="Webhooks bêta : événements de paiement (POST)")
async def webhook(notification: WebhookEnvelope) -> dict:
    """Nouveau système de webhooks (bêta) : payment.created / authorized / captured / canceled.

    Notification en POST avec une enveloppe structurée (event code + data).
    Toujours re-vérifier l'état réel via GET /payments/{id} avant d'agir.
    Répondre 200 rapidement, traiter en tâche de fond si nécessaire.
    """
    event_type = notification.type
    payment_id = (notification.data or {}).get("id") if notification.data else None

    if event_type == "payment.canceled":
        # Exemple : libération de stock / annulation de commande.
        pass
    elif event_type in ("payment.authorized", "payment.captured"):
        # Exemple : marquer la commande PAID (après vérification du montant).
        pass
    # payment.created → exemple : journaliser le paiement.

    return {"received": True, "event": event_type, "payment_id": payment_id}
