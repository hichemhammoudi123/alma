# Récupérer une liste de Payments

**`GET /v1/payments`**

Retourne une liste de payments avec un sous-ensemble des champs du [`Payment`](objects/payment.md).

## Requête

```shell
curl "https://api.sandbox.getalma.eu/v1/payments?limit=20&state=paid&customer_email=jean%40example.com" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
```

## Query parameters

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `created_after` | integer | Timestamp (s). Paiements créés après ou à cette date |
| `created_before` | integer | Timestamp (s). Paiements créés avant ou à cette date |
| `customer_email` | string | Filtre partiel sur l'email du client (contient) |
| `state` | string | `not_started`, `scored_no`, `scored_yes`, `scored_maybe`, `paid` |
| `limit` | integer | Nombre max de résultats (défaut 20) |
| `starting_after` | string | ID du payment pour pagination (trié du plus récent au plus ancien) |

## Réponse — 200

```json
{
  "has_more": false,
  "data": [
    {
      "id": "payment_123hpWi69Ob5uYhmoMctuAkAMYwyF7WP9N",
      "merchant_name": "blackbear",
      "state": "not_started",
      "processing_status": "awaiting_authorization",
      "cancelation_reason": null,
      "created": 1787040848,
      "updated": 1787046785,
      "purchase_amount": 20000,
      "kind": "P4X",
      "payment_plan": [ { "state": "pending", "purchase_amount": 5000, "due_date": 1787040848 } ],
      "customer": { "id": "customer_...", "first_name": "Jean", "last_name": "Dupont", "email": "jean@example.com" },
      "orders": [ { "id": "order_...", "merchant_reference": "CP-10001" } ],
      "origin": "online",
      "deferred_months": 0,
      "deferred_days": 0,
      "transaction_country": "FR",
      "refunds": []
    }
  ]
}
```

### Format de liste

| Champ | Type | Description |
| :--- | :--- | :--- |
| `data` | array | Les objets retournés (triés du plus récent au plus ancien) |
| `has_more` | boolean | `true` s'il existe d'autres résultats (utiliser `starting_after`) |

### Champs des objets (liste)

`id`, `merchant_name`, `state`, `created`, `updated`, `purchase_amount`, `kind`, `payment_plan`, `customer`, `orders`, `origin`, `deferred_months`, `deferred_days`, `transaction_country`, `refunds`.

> ⚠️ La forme exacte de l'enveloppe (`data` + `has_more`) peut varier selon les environnements : vérifier la réponse réelle de la sandbox. Certains environnements retournent un tableau brut.

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Paramètre de filtrage invalide |

## Notes Customer Panel

- Préférer le filtrage serveur (`customer_email`, `state`, dates) plutôt que de tout rapatrier et filtrer côté client.
- Paginer avec `starting_after` tant que `has_more` est `true`.