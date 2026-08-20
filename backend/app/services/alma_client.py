"""Client HTTP minimaliste vers l'API Alma.

Tous les appels vers Alma sont centralisés ici :
- la clé d'API est injectée automatiquement via le header Authorization
- les erreurs Alma (400/401/403/404/422...) sont propagées au frontend
  en conservant le message et le code d'erreur d'Alma.
"""
import httpx

from app.config import settings


class AlmaAPIError(Exception):
    """Erreur renvoyée par l'API Alma (code HTTP != 2xx)."""

    def __init__(self, status_code: int, detail: str, error_code: str | None = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        super().__init__(detail)


class AlmaClient:
    """Wrapper autour des endpoints de l'API Alma.

    Chaque méthode correspond à un endpoint Alma. Elles ne connaissent que
    l'URL Alma : les payloads sont des dict Python passés par les routers.
    """

    def __init__(self) -> None:
        # Headers communs à tous les appels authentifiés.
        self._headers = {
            "Authorization": f"Alma-Auth {settings.ALMA_API_KEY}",
            "Content-Type": "application/json",
        }
        self._timeout = settings.ALMA_TIMEOUT
        self._verify = settings.ALMA_SSL_VERIFY

    # ------------------------------------------------------------------
    # Helper de requête
    # ------------------------------------------------------------------
    def _request(self, method: str, path: str, base: str | None = None, **kwargs):
        """Exécute une requête HTTP vers Alma et normalise le résultat/les erreurs."""
        url = f"{(base or settings.ALMA_API_BASE).rstrip('/')}/{path.lstrip('/')}"
        with httpx.Client(timeout=self._timeout, verify=self._verify) as client:
            response = client.request(method, url, headers=self._headers, **kwargs)

        if response.status_code >= 400:
            # Tente d'extraire le message d'erreur JSON d'Alma.
            try:
                payload = response.json()
            except Exception:
                payload = {}
            message = (
                payload.get("message")
                or payload.get("error")
                or response.text
                or "Erreur Alma inconnue"
            )
            raise AlmaAPIError(response.status_code, message, payload.get("error_code"))

        # 204 = succès sans contenu.
        if response.status_code == 204 or not response.text:
            return {}

        return response.json()

    # ------------------------------------------------------------------
    # Éligibilité
    # ------------------------------------------------------------------
    def eligibility(self, payload: dict) -> dict:
        """POST /payments/eligibility — vérifie l'éligibilité d'un achat."""
        return self._request("POST", "/payments/eligibility", json=payload)

    # ------------------------------------------------------------------
    # Payments
    # ------------------------------------------------------------------
    def create_payment(self, payload: dict) -> dict:
        """POST /payments — crée un paiement et retourne le Payment (avec `url`)."""
        return self._request("POST", "/payments", json=payload)

    def get_payment(self, payment_id: str) -> dict:
        """GET /payments/{id} — récupère un paiement complet."""
        return self._request("GET", f"/payments/{payment_id}")

    def list_payments(self, params: dict | None = None) -> dict:
        """GET /payments — liste les paiements avec filtres."""
        return self._request("GET", "/payments", params=params)

    def update_payment(self, payment_id: str, payload: dict) -> dict:
        """POST /payments/{id} — modifie un paiement (client, locale...)."""
        return self._request("POST", f"/payments/{payment_id}", json=payload)

    def cancel_payment(self, payment_id: str) -> dict:
        """POST /payments/{id}/cancel — annule un paiement (204)."""
        return self._request("POST", f"/payments/{payment_id}/cancel")

    # ------------------------------------------------------------------
    # Orders
    # ------------------------------------------------------------------
    def create_order(self, payment_id: str, payload: dict) -> dict:
        """POST /payments/{id}/orders — attache une Order à un Payment existant."""
        return self._request("POST", f"/payments/{payment_id}/orders", json=payload)

    def send_order_status(
        self, payment_external_id: str, merchant_order_reference: str, payload: dict
    ) -> dict:
        """POST /payments/{ext_id}/orders/{ref}/status — envoie le statut d'une commande."""
        return self._request(
            "POST",
            f"/payments/{payment_external_id}/orders/{merchant_order_reference}/status",
            json=payload,
        )

    def send_shipment(self, order_id: str, payload: dict) -> dict:
        """POST /v2/orders/{id}/shipment — envoie les infos d'expédition (base v2)."""
        return self._request(
            "POST", f"/orders/{order_id}/shipment", base=settings.ALMA_API_BASE_V2, json=payload
        )

    # ------------------------------------------------------------------
    # Refunds
    # ------------------------------------------------------------------
    def create_refund(self, payment_id: str, payload: dict) -> dict:
        """POST /payments/{id}/refunds — crée un remboursement (partiel ou total)."""
        return self._request("POST", f"/payments/{payment_id}/refunds", json=payload)

    # ------------------------------------------------------------------
    # Capture différée
    # ------------------------------------------------------------------
    def capture_payment(self, payment_id: str, payload: dict) -> dict:
        """POST /payments/{id}/captures — déclenche le premier prélèvement (capture manuelle)."""
        return self._request("POST", f"/payments/{payment_id}/captures", json=payload)

    # ------------------------------------------------------------------
    # Pay-by-link (SMS / Email)
    # ------------------------------------------------------------------
    def send_payment_link_sms(self, payment_id: str) -> dict:
        """POST /payments/{id}/send-sms — envoie le lien de paiement par SMS."""
        return self._request("POST", f"/payments/{payment_id}/send-sms")

    def send_payment_link_email(self, payment_id: str) -> dict:
        """POST /payments/{id}/send-email — envoie le lien de paiement par email."""
        return self._request("POST", f"/payments/{payment_id}/send-email")

    # ------------------------------------------------------------------
    # Balance transactions
    # ------------------------------------------------------------------
    def list_balance_transactions(self, params: dict | None = None) -> dict:
        """GET /balance-transactions — transactions comptables du compte marchand."""
        return self._request("GET", "/balance-transactions", params=params)


# Instance unique réutilisée par tous les routers.
alma_client = AlmaClient()
