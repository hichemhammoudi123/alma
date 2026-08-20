"""Modèles Pydantic des endpoints de paiement : éligibilité + création de Payment."""

from pydantic import BaseModel, Field, Json

from app.models.common import Address, Cart, Customer, Order


class EligibilityRequest(BaseModel):
    """Payload de POST /api/alma/eligibility (proxy de POST /payments/eligibility)."""

    payment: "EligibilityPayment" = Field(..., description="Données de l'achat à tester")


class EligibilityPayment(BaseModel):
    """Objet Payment partiel — seul `purchase_amount` est requis."""

    purchase_amount: int = Field(..., description="Montant du panier en centimes (20000 = 200,00 €)")
    installments_count: int | list[int] | None = Field(
        None,
        description="Nombre d'échéances à tester (3 par défaut). "
        "Passer un tableau [3, 4] pour vérifier plusieurs échéanciers d'un coup.",
    )


class EligibilityResponse(BaseModel):
    """Objet retourné par Alma pour chaque échéancier testé."""

    eligible: bool = Field(..., description="true si l'achat est éligible à cet échéancier")
    installments_count: int = Field(..., description="Nombre d'échéances de cet échéancier")
    deferred_days: int = Field(0, description="Jours de décalage (paiement différé)")
    deferred_months: int = Field(0, description="Mois de décalage (paiement différé)")
    customer_total_cost_amount: int | None = Field(
        None, description="Frais + intérêts totaux payés par le client (centimes)"
    )
    customer_total_cost_bps: int | None = Field(
        None, description="Part de frais client en points de base"
    )
    payment_plan: list[dict] | None = Field(
        None,
        description="Échéancier détaillé : purchase_amount, customer_fee, "
        "customer_interest, due_date, total_amount",
    )
    reasons: dict | None = Field(
        None, description="Si non éligible : attributs en cause + raison du rejet"
    )
    constraints: dict | None = Field(
        None,
        description="Si non éligible : contraintes à respecter "
        "(ex. purchase_amount.minimum / maximum)",
    )


class PaymentCreateRequest(BaseModel):
    """Payload de POST /api/alma/payments (proxy de POST /payments)."""

    payment: "PaymentCreate" = Field(..., description="Données du paiement (obligatoire)")
    customer: Customer | None = Field(None, description="Données du client")
    order: Order | None = Field(None, description="Commande associée au paiement")


class PaymentCreate(BaseModel):
    """Données du paiement à créer."""

    purchase_amount: int = Field(
        ..., description="Montant du panier en centimes, sans les frais Alma (obligatoire)"
    )
    installments_count: int | None = Field(
        3, description="Nombre de prélèvements (défaut 3)"
    )
    return_url: str | None = Field(
        None,
        description="URL vers laquelle le client sera redirigé une fois le paiement effectué "
        "(Alma ajoute ?pid=<payment_id>)",
    )
    customer_cancel_url: str | None = Field(
        None,
        description="URL de retour si le client annule sans finaliser (Alma ajoute ?pid=)",
    )
    failure_return_url: str | None = Field(
        None, description="URL de retour en cas d'échec de paiement (refus Alma)"
    )
    ipn_callback_url: str | None = Field(
        None,
        description="URL appelée de façon asynchrone par Alma quand le paiement est effectué "
        "(Alma ajoute ?pid=). Obligatoire pour valider la commande côté serveur.",
    )
    custom_data: Json | dict | None = Field(
        None,
        description="Objet JSON libre pour lier le paiement à vos IDs internes "
        "(ex. { \"order_id\": \"CP-10001\", \"customer_id\": \"CUS-458\" })",
    )
    deferred_months: int | None = Field(
        0, description="Nombre de mois précédant la première échéance"
    )
    deferred_days: int | None = Field(
        0, description="Nombre de jours précédant la première échéance"
    )
    locale: str | None = Field(
        "fr",
        description="Langue de communication avec le client : fr, en, it, es, de, nl, nl_BE",
    )
    expires_after: int | None = Field(
        2880,
        description="Durée de validité du lien de paiement en minutes (défaut 2880). "
        "Si expiré, le payment porte l'attribut expired_at.",
    )
    capture_method: str | None = Field(
        "automatic",
        description="\"automatic\" (défaut) ou \"manual\" pour la capture différée",
    )
    shipping_address: Address | None = Field(None, description="Adresse de livraison")
    billing_address: Address | None = Field(None, description="Adresse de facturation")
    cart: Cart | None = Field(None, description="Contenu du panier (contexte de la transaction)")
    merchant_covers_all_fees: bool | None = Field(
        False,
        description="true pour désactiver le partage des frais : le client ne paie pas de frais, "
        "ils sont à la charge du marchand",
    )
    origin: str | None = Field(
        None, description="Origine du paiement (ex. online, pos_sms)"
    )
