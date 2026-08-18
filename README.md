# Alma — Intégration Customer Panel

Documentation technique complète de l'API Alma (sandbox) pour le projet **Customer Panel**.

Base de référence : [docs.almapay.com/reference](https://docs.almapay.com/reference)

## Environnements

| Environnement | URL de base |
| :--- | :--- |
| Sandbox (test) | `https://api.sandbox.getalma.eu/v1/` |
| Production (live) | `https://api.getalma.eu/v1/` |

> ⚠️ Endpoint `shipment` un seul est en **v2** : `https://api.sandbox.getalma.eu/v2/`.

## Clé d'API

- Header requis : `Authorization: Alma-Auth <API key>`
- Clé de test : `sk_test_3RG9iMTw2oearUHkNCBUUZ3P` (sandbox)
- La clé est **secrète** : elle ne doit être utilisée que côté serveur (backend), jamais dans React.

## Liste des endpoints

| Méthode | Endpoint | Description | Doc |
| :--- | :--- | :--- | :--- |
| `POST` | `/v1/payments/eligibility` | Vérifier l'éligibilité d'un achat | [doc](docs/01-eligibility.md) |
| `POST` | `/v1/payments` | Créer un paiement | [doc](docs/02-create-payment.md) |
| `GET` | `/v1/payments/{payment_id}` | Récupérer un paiement | [doc](docs/03-get-payment.md) |
| `GET` | `/v1/payments` | Lister les paiements | [doc](docs/04-list-payments.md) |
| `POST` | `/v1/payments/{payment_id}` | Modifier un paiement | [doc](docs/05-update-payment.md) |
| `POST` | `/v1/payments/{payment_id}/cancel` | Annuler un paiement | [doc](docs/06-cancel-payment.md) |
| `POST` | `/v1/payments/{payment_id}/orders` | Créer une Order pour un Payment | [doc](docs/07-create-order.md) |
| `POST` | `/v1/payments/{payment_ext_id}/orders/{merchant_ref}/status` | Envoyer le statut d'une commande | [doc](docs/08-order-status.md) |
| `POST` | `/v2/orders/{order_id}/shipment` | Envoyer les infos d'expédition | [doc](docs/09-shipment.md) |
| `POST` | `/v1/payments/{payment_id}/refunds` | Créer un remboursement | [doc](docs/10-refund.md) |
| `POST` | `/v1/payments/{payment_id}/captures` | Capture différée | [doc](docs/11-capture.md) |
| `POST` | `/v1/payments/{payment_id}/send-sms` | Envoyer un lien par SMS | [doc](docs/12-pay-by-link.md) |
| `POST` | `/v1/payments/{payment_id}/send-email` | Envoyer un lien par email | [doc](docs/12-pay-by-link.md) |
| `GET` | `/v1/balance-transactions` | Balance transactions (compta) | [doc](docs/13-balance-transactions.md) |

## Webhooks

| Type | Méthode | Description | Doc |
| :--- | :--- | :--- | :--- |
| IPN | `GET` sur `ipn_callback_url?pid={payment_id}` | Notification serveur à serveur | [doc](docs/14-webhooks.md) |
| Webhooks (bêta) | `POST` | `payment.created` / `authorized` / `captured` / `canceled` | [doc](docs/14-webhooks.md) |

## Objets

- [Payment](docs/objects/payment.md)
- [Customer](docs/objects/customer.md)
- [Address](docs/objects/address.md)
- [Order](docs/objects/order.md)
- [Refund](docs/objects/refund.md)

## Convention

Tous les montants sont exprimés en **centimes** :

```text
purchase_amount = 20000  ⇔  200,00 €
```