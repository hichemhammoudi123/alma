"""Routes des payments : création, lecture, liste, modification, annulation."""

from typing import Optional

from fastapi import APIRouter, Query

from app.models.payments import PaymentCreateRequest
from app.services.alma_client import alma_client

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("", summary="Créer un paiement")
async def create_payment(payload: PaymentCreateRequest) -> dict:
    """Crée un Payment Alma et retourne l'objet Payment complet.

    Points importants :
    - `payment.url` → URL de la page Alma vers laquelle rediriger le client.
    - Mettre `payment.ipn_callback_url` pour recevoir la notification serveur.
    - Utiliser `payment.custom_data` pour lier le paiement à vos IDs internes.
    """
    return alma_client.create_payment(payload.model_dump(exclude_none=True))


@router.get("", summary="Récupérer une liste de payments")
async def list_payments(
    created_after: Optional[int] = Query(None, description="Timestamp (s) : paiements créés après/à cette date"),
    created_before: Optional[int] = Query(None, description="Timestamp (s) : paiements créés avant/à cette date"),
    customer_email: Optional[str] = Query(None, description="Filtre partiel sur l'email du client (contient)"),
    state: Optional[str] = Query(None, description="État du paiement : not_started, scored_no, scored_yes, scored_maybe, paid"),
    limit: int = Query(20, description="Nombre max de résultats (défaut 20)"),
    starting_after: Optional[str] = Query(None, description="ID du dernier payment de la page précédente (pagination)"),
) -> dict:
    """Liste les paiements du compte marchand, avec filtres et pagination."""
    params = {
        "created_after": created_after,
        "created_before": created_before,
        "customer_email": customer_email,
        "state": state,
        "limit": limit,
        "starting_after": starting_after,
    }
    return alma_client.list_payments({k: v for k, v in params.items() if v is not None})


@router.get("/{payment_id}", summary="Récupérer un paiement")
async def get_payment(payment_id: str) -> dict:
    """Retourne le Payment complet.

    Après le retour client (return_url) ou la réception d'un IPN/webhook,
    TOUJOURS vérifier ici : `processing_status` (authorized/captured) et
    `purchase_amount` (== montant du panier) avant de valider la commande.
    """
    return alma_client.get_payment(payment_id)


@router.post("/{payment_id}", summary="Modifier un paiement")
async def update_payment(payment_id: str, payload: dict) -> dict:
    """Modifie un Payment (données client, locale...).

    Uniquement tant que le premier prélèvement n'a pas été effectué.
    Un champ client déjà renseigné ne peut plus être modifié.
    """
    return alma_client.update_payment(payment_id, payload)


@router.post("/{payment_id}/cancel", summary="Annuler un paiement")
async def cancel_payment(payment_id: str) -> dict:
    """Annule un paiement non commencé (premier prélèvement non effectué).

    Retourne 204 si OK ; 400 si le statut ne permet pas l'annulation.
    """
    return alma_client.cancel_payment(payment_id)
