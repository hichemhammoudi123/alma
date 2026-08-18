# Capture Différée

**`POST /v1/payments/{payment_id}/captures`**

Déclenche le premier prélèvement (ou le prélèvement total en 1x) pour un paiement créé avec `capture_method: "manual"`.

> Utilisée pour le **paiement à l'expédition** : on collecte les fonds uniquement lorsque la commande est prête à être expédiée.

- **Capture partielle** supportée (`amount` < échéance prévue). Sans `amount` → capture complète de la première échéance.
- Captures multiples **non** supportées.
- Capture à déclencher dans les **7 jours** après autorisation, sinon l'autorisation expire et le paiement est annulé.
- Le virement marchand n'est émis qu'**après capture réussie**.

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/captures" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 10000,
    "merchant_reference": "CAP-001"
  }'
```

## Path parameters

| Paramètre | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `payment_id` | string | ✅ | ID du paiement Alma |

## Payload

| Champ | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `amount` | integer | ✅* | Montant à capturer, en centimes (*absent → capture complète de l'échéance) |
| `merchant_reference` | string | ❌ | Référence interne marchand |

## Réponse — 200

```json
{
  "amount": 10000,
  "id": "b0f5ba04-f0b3-4eb8-b292-0b58bc77e16c"
}
```

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Paiement non capturable (déjà capturé, période expirée, etc.) |

## Notes Customer Panel

- Réservé aux paiements créés avec `capture_method: "manual"` (`is_deferred_capture: true` sur le payment).
- Pour un MVP, commencer par la capture automatique (`automatic`).