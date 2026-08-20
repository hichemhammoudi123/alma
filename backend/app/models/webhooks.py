"""Modèles des notifications webhooks (IPN + webhooks bêta)."""

from pydantic import BaseModel, Field


class IpnParams(BaseModel):
    """Paramètres query de l'IPN : GET /api/alma/ipn?pid=payment_xxx."""

    pid: str = Field(..., description="Identifiant du payment Alma concerné")


class WebhookEnvelope(BaseModel):
    """Enveloppe du nouveau système de webhooks (bêta) : POST /api/alma/webhooks."""

    type: str | None = Field(
        None,
        description="Code de l'événement : payment.created / payment.authorized / "
        "payment.captured / payment.canceled",
    )
    data: dict | None = Field(
        None, description="Données de l'événement (le payment Alma complet en général)"
    )
