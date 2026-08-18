# Créer un Remboursement

**`POST /v1/payments/{payment_id}/refunds`**

Rembourse un client sur un payment. Alma gère l'allocation entre les échéances : le marchand peut rembourser jusqu'au montant d'achat (`purchase_amount`) sans se soucier de ce que le client a déjà payé.

- Sans champ `amount` → **remboursement intégral**.
- Avec `amount` → **remboursement partiel** (illimité tant que la somme ne dépasse pas `purchase_amount`).
- Le remboursement des frais / intérêts consommateur est géré par Alma.

> 📘 Reversement par carte virtuelle : le remboursement doit être fait depuis le **partenaire**, cet endpoint est désactivé.

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/refunds" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000,
    "merchant_reference": "RMB-987"
  }'
```

## Path parameters

| Paramètre | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `payment_id` | string | ✅ | ID du paiement Alma |

## Payload

| Champ | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `amount` | integer | ❌* | Montant à rembourser, en centimes (*absent → remboursement intégral) |
| `merchant_reference` | string | ❌ | Référence interne marchand, utile pour le rapprochement avec votre base |

## Réponse — 200

```json
{
  "id": "refund_11h3jIO3ysBniMdtgC2AyEW4skyEG43P7H",
  "created": 1552404383,
  "amount": 17000,
  "merchant_reference": "981201927"
}
```

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Montant invalide ou somme des refunds > `purchase_amount` |

## Notes Customer Panel

- Conserver l'historique des remboursements dans votre panel.
- Suivre l'état via [GET Payment](03-get-payment.md) : `refunds`, `amount_already_refunded`, `is_completely_refunded`.