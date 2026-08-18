# Annuler un Paiement

**`POST /v1/payments/{payment_id}/cancel`**

Annule un paiement, tant que le premier prélèvement n'a pas été exécuté. Si le statut ne le permet pas, une erreur `400` est renvoyée.

> Contexte Customer Panel : annulation administrative côté back-office, ou à la suite du retour client sur `customer_cancel_url`.

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/cancel" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
```

## Path parameters

| Paramètre | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `payment_id` | string | ✅ | ID du paiement Alma |

## Corps

Aucun.

## Réponse — 204

Succès sans contenu.

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Le statut de ce paiement ne permet pas de l'annuler |

```json
{ "message": "Le statut de ce paiement ne permet pas de l'annuler" }
```