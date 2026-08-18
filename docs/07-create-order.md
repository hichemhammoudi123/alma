# Créer une Order pour un Payment existant

**`POST /v1/payments/{payment_id}/orders`**

Associe une [`Order`](objects/order.md) à un paiement existant, notamment lorsque la référence de commande n'était pas disponible lors de la création du Payment.

> Contexte Customer Panel : votre workflow est *checkout → Create Payment → Alma → commande créée dans votre système → Attach Order to Payment*.

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/orders" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P" \
  -H "Content-Type: application/json" \
  -d '{
    "order": {
      "merchant_reference": "CP-10001",
      "merchant_url": "https://customer-panel.com/admin/orders/10001",
      "customer_url": "https://customer-panel.com/orders/10001",
      "data": { "campaign": "ete-2026" },
      "comment": "Commande crée après paiement"
    }
  }'
```

## Path parameters

| Paramètre | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `payment_id` | string | ✅ | ID du payment sur lequel créer l'order |

## Payload — `order`

| Champ | Type | Description |
| :--- | :--- | :--- |
| `merchant_reference` | string | Référence marchand, présentée au client (le lien entre vos 2 systèmes) |
| `merchant_url` | string | URL de la page backoffice marchand |
| `customer_url` | string | URL de détails de commande visible par le client |
| `data` | object | Données arbitraires du marchand |
| `comment` | string | Commentaire du marchand |

## Réponse — 200

```json
[
  {
    "id": "order_11u6ZY7Bjhh50ew29rpZyUI32InCs5pSxF",
    "created": 1645059062,
    "updated": 1645059062,
    "merchant_reference": "CP-10001",
    "merchant_url": "https://customer-panel.com/admin/orders/10001",
    "customer_url": "https://customer-panel.com/orders/10001",
    "payment": "payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
    "data": {},
    "comment": null
  }
]
```

## Notes Customer Panel

- `merchant_reference` permet de faire le lien entre votre commande et Alma.
- Lier aussi le payment via `custom_data` dès la création ([voir Create Payment](02-create-payment.md)).