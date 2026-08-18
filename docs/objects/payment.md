# Objet Payment

L'objet `Payment` décrit un achat en plusieurs fois dans sa totalité : montant et date de l'achat, informations client et échéancier.

La plupart des attributs sont **en lecture seule** : seuls ceux décrits dans [Créer un Paiement](../02-create-payment.md) peuvent être renseignés.

## Champs

| Champ | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Identifiant du Payment |
| `merchant_id` | string | ID du marchand attaché au Payment |
| `merchant_name` | string | Nom du marchand |
| `state` | string | ⚠️ **Obsolète**, utiliser `processing_status`. `not_ready` / `not_started` / `scored_no` / `scored_yes` / `scored_maybe` / `in_progress` / `paid` |
| `processing_status` | string | `awaiting_authorization` (attente infos client), `authorized` (autorisé, en attente de capture), `captured` (capturé), `canceled` (annulé) |
| `cancelation_reason` | string \| null | `requested_by_merchant` / `requested_by_customer` / `authorization_expired` / `expired` |
| `created` / `updated` | timestamp | Dates de création / dernière modification |
| `expired_at` | timestamp \| null | Date d'expiration du Payment, si expiré |
| `url` | string | URL de la page Alma (redirection client). Devenue résumé client si `paid` |
| `return_url` | string \| null | Redirection après paiement effectué |
| `customer_cancel_url` | string \| null | Redirection si paiement annulé (client ou marchand) |
| `failure_return_url` | string \| null | Redirection si paiement refusé |
| `purchase_amount` | integer | Montant du panier, **sans** frais Alma (centimes) |
| `installments_count` | integer | Nombre d'échéances |
| `kind` | string \| null | Type : `P1X`, `P1X_D+30`, `P3X`, `P10X`, etc. |
| `payment_plan` | array | Liste des échéances (voir ci-dessous) |
| `customer` | [Customer](customer.md) | Client |
| `shipping_address` / `billing_address` | [Address](address.md) \| null | Adresses |
| `custom_data` | json | Données libres (liens vers vos IDs internes) |
| `orders` | list of [Order](order.md) | Commandes payées avec ce payment |
| `origin` | string \| null | Origine du paiement |
| `integration_origin` | string \| null | ID de l'intégration d'origine |
| `seller` | object \| null | Vendeur (id, name, display_name, email) |
| `deferred_months` / `deferred_days` | integer | Report de la première échéance |
| `is_deferred_capture` | boolean | `true` si capture différée |
| `capture_method` | string | `automatic` ou `manual` |
| `authorization_expires_at` | datetime \| null | Expiration de l'autorisation |
| `locale` | string | `fr`, `en`, `it`, `es`, `de`, `nl`, `nl_BE` |
| `transaction_country` | string \| null | Pays de la vente |
| `country_of_service` | string \| null | Pays des CGV applicables |
| `ipn_callback_url` | string \| null | URL IPN (notifications async) |
| `cart` | object \| null | Contenu du panier à la création |
| `payout` | object \| null | Transaction (intégration indirecte) : `status` (`pending`/`completed`/`failed`), `merchant_psp`, `merchant_psp_id`, `merchant_psp_metadata`, `processed_at` |
| `refunds` | list of [Refund](refund.md) | Remboursements opérés |
| `is_completely_refunded` | boolean | `true` si remboursé intégralement |
| `amount_already_refunded` | integer | Montant total remboursé |
| `fees` | object | Détail des frais : `merchant.total`, `merchant.total_excluding_tax`, `merchant.tax` |
| `customer_fee` | integer | Frais bruts client |
| `customer_interest` | integer | Intérêts client (crédit) |
| `annual_interest_rate` | integer | TAEG (crédit) |
| `merchant_target_fee` | integer | Frais bruts marchand |

## `payment_plan[]`

| Champ | Type | Description |
| :--- | :--- | :--- |
| `state` | string | `pending` (pas encore prélevé), `paid` (prélevé), `covered` (incident couvert par Alma). ⚠️ Ne renseigne pas sur l'existence d'un remboursement : voir `refunds` |
| `is_check` | boolean | `true` si vérification de la carte par Alma |
| `original_purchase_amount` | integer | Montant originel de l'échéance |
| `purchase_amount` | integer | Montant de l'échéance sans frais |
| `customer_fee` | integer | Frais client de l'échéance |
| `customer_interest` | integer | Intérêts de l'échéance |
| `due_date` | timestamp | Date d'échéance |
| `date_paid` | timestamp \| null | Date de paiement de l'échéance |

## Exemple

```json
{
  "id": "payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "merchant_name": "blackbear",
  "processing_status": "awaiting_authorization",
  "state": "not_started",
  "purchase_amount": 20000,
  "installments_count": 4,
  "kind": "P4X",
  "url": "https://checkout.sandbox.getalma.eu/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "custom_data": { "order_id": "CP-10001" },
  "refunds": [],
  "is_completely_refunded": false
}
```