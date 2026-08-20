"""Modèles Pydantic des endpoints Orders, Refunds, Captures, Shipment."""

from pydantic import BaseModel, Field

from app.models.common import Order


class OrderCreateRequest(BaseModel):
    """Payload de POST /api/alma/payments/{id}/orders."""

    order: Order = Field(..., description="Détails de l'Order à créer sur le payment existant")


class OrderStatusRequest(BaseModel):
    """Payload de POST /api/alma/payments/{ext_id}/orders/{ref}/status."""

    status: str = Field(..., description="Nouveau statut à enregistrer")
    is_shipped: bool | None = Field(
        None, description="true si la commande est expédiée (en route vers le client)"
    )


class ShipmentRequest(BaseModel):
    """Payload de POST /api/alma/orders/{order_id}/shipment (endpoint v2)."""

    carrier: str = Field(..., description="Transporteur (ex. Colissimo)")
    tracking_number: str = Field(..., description="Numéro de suivi")
    tracking_url: str | None = Field(None, description="URL de suivi du colis")


class RefundCreateRequest(BaseModel):
    """Payload de POST /api/alma/payments/{id}/refunds."""

    amount: int | None = Field(
        None,
        description="Montant à rembourser en centimes. Absent = remboursement intégral. "
        "Partiel autorisé tant que la somme des refunds <= purchase_amount.",
    )
    merchant_reference: str | None = Field(
        None,
        description="Référence interne marchand, utile pour rapprocher avec votre base de données",
    )


class CaptureCreateRequest(BaseModel):
    """Payload de POST /api/alma/payments/{id}/captures (capture différée)."""

    amount: int | None = Field(
        None,
        description="Montant à capturer en centimes. Absent = capture de la première échéance "
        "complète. Capture partielle supportée, captures multiples non.",
    )
    merchant_reference: str | None = Field(
        None, description="Référence interne marchand de la capture"
    )
