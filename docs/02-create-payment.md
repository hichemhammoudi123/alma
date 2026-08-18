# Créer un Paiement

**`POST /v1/payments`**

Créé un paiement Alma et retourne l'objet [`Payment`](objects/payment.md). Champ obligatoire : `payment.purchase_amount`.

C'est la ressource centrale du checkout : le client choisit son échéancier, vous créez le paiement, puis vous redirigez le client vers `payment.url`.

> Lors de la création, vous pouvez inclure l'adresse de livraison/facturation, le client, une commande (`order`) et du `custom_data` (indispensable pour lier le paiement Alma à vos IDs internes).

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P" \
  -H "Content-Type: application/json" \
  -d '{
    "payment": {
      "purchase_amount": 20000,
      "installments_count": 4,
      "return_url": "https://customer-panel.com/alma/return",
      "customer_cancel_url": "https://customer-panel.com/checkout",
      "failure_return_url": "https://customer-panel.com/checkout/error",
      "ipn_callback_url": "https://api.customer-panel.com/alma/ipn",
      "custom_data": {
        "order_id": "CP-10001",
        "customer_id": "CUS-458",
        "cart_id": "CART-987"
      },
      "locale": "fr",
      "shipping_address": {
        "first_name": "Jean",
        "last_name": "Dupont",
        "line1": "1 rue de Rivoli",
        "city": "Paris",
        "postal_code": "75004",
        "country": "France",
        "phone": "+330612345678",
        "email": "jean@example.com"
      },
      "cart": {
        "items": [
          { "title": "Produit A", "quantity": 1, "line_price": 20000, "picture_url": "https://cdn.example.com/a.jpg" }
        ]
      }
    },
    "customer": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "email": "jean@example.com",
      "phone": "+330612345678",
      "birth_date": "1990-01-01",
      "account_id": "CUS-458",
      "account_created": "2024-01-01T00:00:00Z",
      "previous_orders_count": 3,
      "is_business": false
    },
    "order": {
      "merchant_reference": "CP-10001",
      "merchant_url": "https://customer-panel.com/admin/orders/10001",
      "customer_url": "https://customer-panel.com/orders/10001",
      "data": {},
      "comment": "Panier standard"
    }
  }'
```

## Payload — `payment`

| Champ | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `purchase_amount` | integer | ✅ | Montant du panier, en centimes |
| `installments_count` | integer | ❌ | Nombre d'échéances (défaut 3) |
| `return_url` | string | ❌ | URL de retour après paiement effectué |
| `customer_cancel_url` | string | ❌ | URL si le client annule (reçoit `?pid=`) |
| `failure_return_url` | string | ❌ | URL si le paiement est refusé |
| `ipn_callback_url` | string | ❌ | URL appelée en async une fois le paiement effectué (reçoit `?pid=`) |
| `custom_data` | json | ❌ | Données libres pour lier le payment à vos IDs internes |
| `deferred_months` / `deferred_days` | integer | ❌ | Report du premier prélèvement |
| `locale` | string | ❌ | `fr`, `en`, `it`, `es`, `de`, `nl`, `nl_BE` (défaut `fr`) |
| `expires_after` | integer | ❌ | Durée de validité du lien (minutes), défaut 2880 |
| `capture_method` | string | ❌ | `automatic` (défaut) ou `manual` (capture différée) |
| `shipping_address` / `billing_address` | object | ❌ | Voir [Address](objects/address.md) |
| `cart.items[]` | array | ❌ | Contenu du panier (voir [cart-items](https://docs.almapay.com/reference/cart-items)) |
| `merchant_covers_all_fees` | boolean | ❌ | `true` si le marchand prend les frais à sa charge |
| `origin` | string | ❌ | Origine du paiement (ex. `online`, `pos_sms`) |

### `cart.items[]`

| Champ | Type | Requis |
| :--- | :--- | :--- |
| `title` | string | ✅ |
| `quantity` | integer | ✅ |
| `line_price` | integer | ✅ prix de la ligne en centimes |
| `picture_url` | string | ✅ |

## Payload — `customer`

| Champ | Type | Description |
| :--- | :--- | :--- |
| `first_name` / `last_name` | string | Prénom / nom |
| `email` | string | Email du client |
| `phone` | string | Téléphone |
| `birth_date` | string | `yyyy-mm-dd` |
| `addresses[]` | array | Liste d'adresses |
| `is_business` | boolean | `true` si entreprise (non modifiable ensuite) |
| `business_id_number` | string | SIREN par défaut |
| `business_name` | string | Nom de l'entreprise |
| `account_id` | string | ID client dans **votre** système |
| `account_created` | datetime | Date de création du compte chez vous |
| `previous_orders_count` | integer | Nombre de commandes passées par le client |
| `id` / `created` | string | Lecture seule (Alma) |

## Payload — `order`

| Champ | Type | Description |
| :--- | :--- | :--- |
| `merchant_reference` | string | Référence de commande (le lien entre votre système et Alma) |
| `merchant_url` | string | URL backoffice marchand |
| `customer_url` | string | URL de suivi client |
| `data` | object | Données arbitraires |
| `comment` | string | Commentaire |

## Réponse — 200

```json
{
  "id": "payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "merchant_id": "merchant_123hXXYeg8C4Hbdap7tO06zNzgAx4uKXvg",
  "merchant_name": "blackbear",
  "state": "not_started",
  "processing_status": "awaiting_authorization",
  "cancelation_reason": null,
  "created": 1787048072,
  "updated": 1787048073,
  "expired_at": null,
  "url": "https://checkout.sandbox.getalma.eu/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "return_url": "https://customer-panel.com/alma/return?pid=payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "customer_cancel_url": "https://customer-panel.com/checkout?pid=payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "failure_return_url": null,
  "purchase_amount": 20000,
  "installments_count": 4,
  "kind": "P4X",
  "payment_plan": [
    { "state": "pending", "is_check": false, "original_purchase_amount": 5000, "purchase_amount": 5000, "customer_fee": 0, "customer_interest": 0, "due_date": 1787048072, "date_paid": null },
    { "state": "pending", "is_check": false, "original_purchase_amount": 5000, "purchase_amount": 5000, "customer_fee": 0, "customer_interest": 0, "due_date": 1789726472, "date_paid": null }
  ],
  "customer": {
    "id": "customer_123hrPE1JrciF5U1sDj2QWqRu0cVoxOzG5",
    "created": 1787048072,
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean@example.com",
    "phone": null,
    "is_business": false,
    "business_id_number": null,
    "business_name": null
  },
  "shipping_address": null,
  "billing_address": null,
  "custom_data": { "order_id": "CP-10001", "customer_id": "CUS-458" },
  "orders": [
    { "id": "order_123hrPE6kWYYlvvtzLGxuj8ecBYrn4PmNy", "created": 1787048072, "merchant_reference": "CP-10001", "merchant_url": null, "customer_url": null, "comment": null, "data": {}, "payment": "" }
  ],
  "origin": "online",
  "deferred_months": 0,
  "deferred_days": 0,
  "is_deferred_capture": false,
  "locale": "fr",
  "transaction_country": "FR",
  "country_of_service": "FR",
  "ipn_callback_url": "https://api.customer-panel.com/alma/ipn?pid=payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "refunds": [],
  "is_completely_refunded": false,
  "amount_already_refunded": 0,
  "fees": { "merchant": { "total": 1152, "total_excluding_tax": 960, "tax": 192 } },
  "customer_fee": 0
}
```

> Champs-clés pour le Customer Panel : **`id`** (payment ID), **`url`** (lien de redirection client), **`custom_data`**, **`orders[].merchant_reference`**, **`processing_status`**, **`refunds`**.

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Données de paiement invalides (validation) |

## Notes Customer Panel

- Rediriger le client vers `payment.url` après création.
- Conserver `payment.id` + `custom_data` pour faire le lien avec votre commande.
- Ne **jamais** valider la commande sur la seule interrogation du `return_url` : toujours re-vérifier le paiement ([GET Payment](03-get-payment.md)) et attendre l'[IPN/Webhook](14-webhooks.md).