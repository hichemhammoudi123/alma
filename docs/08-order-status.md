# Envoyer le statut d'une commande

**`POST /v1/payments/{payment_external_id}/orders/{merchant_order_reference}/status`**

Envoie le statut d'une commande liée à un payment.

> L'endpoint historique (`send-order-status`) est **déprécié** : utiliser cette version.

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/orders/CP-10001/status" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shipped",
    "is_shipped": true
  }'
```

## Path parameters

| Paramètre | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `payment_external_id` | string | ✅ | ID Alma du payment lié à la commande |
| `merchant_order_reference` | string | ✅ | Référence marchand de la commande |

## Payload

| Champ | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `status` | string | ✅ | Nouveau statut à enregistrer |
| `is_shipped` | boolean | ❌ | `true` si la commande est partie (en route vers le client) |

## Réponse — 204

Succès sans contenu.

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `404` | Payment ou commande introuvable |
| `422` | Erreur de validation (ex. `is_shipped` doit être un booléen) |

```json
{
  "message": "Input should be a valid boolean, unable to interpret input",
  "error_code": "validation_error",
  "detail": [{ "type": "bool_parsing", "loc": ["body", "is_shipped"], "msg": "...", "input": "string" }]
}
```