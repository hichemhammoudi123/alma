# Vérifier l'éligibilité d'un achat

**`POST /v1/payments/eligibility`**

Répond à la question : *« Pour ce panier, quels échéanciers Alma puis-je proposer au client ? »*

> ℹ️ Documentation : l'ancienne page (`verifier-leligibilite-dun-achat`) est obsolète, la référence valide est [Vérifier l'éligibilité d'un achat](https://docs.almapay.com/reference/verifier-eligibilite-achat). L'endpoint, lui, reste le même.

> Important : l'éligibilité ne crée **aucun** paiement. Elle doit être appelée avant d'afficher Alma dans le checkout.

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/eligibility" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P" \
  -H "Content-Type: application/json" \
  -d '{
    "payment": {
      "purchase_amount": 20000,
      "installments_count": [3, 4]
    }
  }'
```

## Payload

| Champ | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `payment.purchase_amount` | integer | ✅ | Montant du panier, en centimes |
| `payment.installments_count` | integer \| integer[] | ❌ | Nombre d'échéances (3 par défaut). Tableau pour tester plusieurs échéanciers d'un coup |

## Réponse (achat éligible) — 200

Si `installments_count` est un tableau, la réponse est aussi un tableau (un objet par échéancier, dans le même ordre).

```json
[
  {
    "eligible": true,
    "installments_count": 3,
    "deferred_days": 0,
    "deferred_months": 0,
    "customer_total_cost_amount": 310,
    "customer_total_cost_bps": 155,
    "payment_plan": [
      { "customer_fee": 310, "customer_interest": 0, "due_date": 1636386621, "purchase_amount": 6668, "total_amount": 6978 },
      { "customer_fee": 0,   "customer_interest": 0, "due_date": 1638978621, "purchase_amount": 6666, "total_amount": 6666 },
      { "customer_fee": 0,   "customer_interest": 0, "due_date": 1641657021, "purchase_amount": 6666, "total_amount": 6666 }
    ]
  },
  {
    "eligible": true,
    "installments_count": 4,
    "deferred_days": 0,
    "deferred_months": 0,
    "customer_total_cost_amount": 360,
    "customer_total_cost_bps": 180,
    "payment_plan": [
      { "customer_fee": 360, "customer_interest": 0, "due_date": 1636386621, "purchase_amount": 5000, "total_amount": 5360 },
      { "customer_fee": 0,   "customer_interest": 0, "due_date": 1638978621, "purchase_amount": 5000, "total_amount": 5000 },
      { "customer_fee": 0,   "customer_interest": 0, "due_date": 1641657021, "purchase_amount": 5000, "total_amount": 5000 },
      { "customer_fee": 0,   "customer_interest": 0, "due_date": 1644335421, "purchase_amount": 5000, "total_amount": 5000 }
    ]
  }
]
```

### Champs de la réponse

| Champ | Type | Description |
| :--- | :--- | :--- |
| `eligible` | boolean | `true` si éligible |
| `deferred_days` | integer | Jours de décalage pour du paiement différé |
| `deferred_months` | integer | Mois de décalage pour du paiement différé |
| `installments_count` | integer | Nombre d'échéances |
| `customer_total_cost_amount` | integer | Frais et intérêts totaux payés par le client (centimes) |
| `customer_total_cost_bps` | integer | Part des frais en bps. Non contractuel pour le crédit (>4x) |
| `payment_plan` | array | Détail de chaque échéance |
| `payment_plan[].purchase_amount` | integer | Capital remboursé (centimes) |
| `payment_plan[].customer_fee` | integer | Frais payés par le client sur cette échéance |
| `payment_plan[].customer_interest` | integer | Intérêts sur cette échéance |
| `payment_plan[].due_date` | timestamp | Date d'échéance |
| `payment_plan[].total_amount` | integer | Total de l'échéance (capital + frais + intérêts) |

## Réponse (achat non éligible) — 200

```json
{
  "eligible": false,
  "installments_count": 3,
  "deferred_days": 0,
  "deferred_months": 0,
  "reasons": { "purchase_amount": "invalid_value" },
  "constraints": { "purchase_amount": { "minimum": 100, "maximum": 1000000 } }
}
```

| Champ | Type | Description |
| :--- | :--- | :--- |
| `reasons` | object | Attibuts en cause de l'échec (clé = attribut, valeur = raison) |
| `constraints` | object | Contraintes à respecter (`minimum` / `maximum` en centimes) |

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Compte marchand non activé |

## Notes Customer Panel

- Toujours vérifier `eligible` pour **chaque** échéancier avant de l'afficher.
- Ne présenter à l'utilisateur que les échéanciers éligibles.
- Mapper `payment_plan` pour afficher le détail (ex. `66,68 € + 66,66 € + 66,66 €`).