"""Route balance transactions : GET /api/alma/balance-transactions (back-office/compta)."""

from typing import Optional

from fastapi import APIRouter, Query

from app.services.alma_client import alma_client

router = APIRouter(prefix="/balance-transactions", tags=["Balance transactions"])


@router.get("", summary="Récupérer une liste de Balance Transactions")
async def list_balance_transactions(
    merchant: Optional[str] = Query(
        None,
        description="ID du marchand. Défaut = marchand authentifié. "
        "'all' = tous les comptes enfants accessibles",
    ),
    kind: Optional[str] = Query(
        None,
        description="Type : from_transaction, from_adjustment, from_payout, "
        "from_refund, from_fee_waiver, from_merchant_default_coverage",
    ),
    limit: int = Query(
        50, ge=20, description="Limite de résultats (minimum 20 imposé par Alma)"
    ),
    starting_after: Optional[str] = Query(None, description="ID de transaction (pagination)"),
) -> dict:
    """Transactions comptables du compte marchand (rapprochement, reporting).

    Ressource back-office, pas un endpoint du parcours client.
    """
    params = {"merchant": merchant, "kind": kind, "limit": limit, "starting_after": starting_after}
    return alma_client.list_balance_transactions({k: v for k, v in params.items() if v is not None})
