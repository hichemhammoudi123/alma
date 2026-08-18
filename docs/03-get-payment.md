# Récupérer un Paiement

**`GET /v1/payments/{payment_id}`**

Retourne l'objet [`Payment`](objects/payment.md) complet à partir de son identifiant.

> Essentiel pour le Customer Panel : **ne considérez jamais** *« client revenu sur le site ⇒ paiement réussi »*. Vérifiez toujours l'état réel via cet endpoint.

## Requête

```shell
curl "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
```

## Path parameters

| Paramètre | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `payment_id` | string | ✅ | ID du paiement Alma |

## Réponse — 200

Objet `Payment` (identique à la réponse de [Créer un Paiement](02-create-payment.md)).

### Contrôles recommandés (checkout + IPN)

| Champ | Valeurs | À vérifier |
| :--- | :--- | :--- |
| `processing_status` | `awaiting_authorization` / `authorized` / `captured` / `canceled` | ✅ = `authorized` ou `captured` |
| `purchase_amount` | integer | ✅ == montant du panier |
| `cancelation_reason` | `requested_by_merchant` / `requested_by_customer` / `authorization_expired` / `expired` | contexte annulation |
| `state` (déprécié) | `not_ready` / `not_started` / `scored_no` / `scored_yes` / `scored_maybe` / `in_progress` / `paid` | préférer `processing_status` |
| `refunds` / `amount_already_refunded` / `is_completely_refunded` | — | suivi remboursement |

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Paramètre invalide |
| `404` | Payment introuvable |