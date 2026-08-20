"""Routes pay-by-link : envoi du lien de paiement par SMS ou email."""

from fastapi import APIRouter

from app.services.alma_client import alma_client

router = APIRouter(prefix="/payments", tags=["Pay by link"])


@router.post("/{payment_id}/send-sms", summary="Envoyer un lien de paiement par SMS")
async def send_sms(payment_id: str) -> dict:
    """Déclenche l'envoi du lien de paiement par SMS (Alma).

    ⚠️ Fonctionnalité non activée par défaut (contact support Alma).
    Requiert `customer.phone` à la création du payment.
    """
    return alma_client.send_payment_link_sms(payment_id)


@router.post("/{payment_id}/send-email", summary="Envoyer un lien de paiement par email")
async def send_email(payment_id: str) -> dict:
    """Déclenche l'envoi du lien de paiement par email (Alma).

    ⚠️ Fonctionnalité non activée par défaut (contact support Alma).
    """
    return alma_client.send_payment_link_email(payment_id)
