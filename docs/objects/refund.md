# Objet Refund

Représente un remboursement opéré sur un [`Payment`](payment.md). Alma gère toute la complexité du remboursement en plusieurs fois : le marchand n'a pas à se soucier de ce que le client a déjà payé ou doit encore payer.

- Le marchand peut rembourser à hauteur du montant d'achat (`payment.purchase_amount`).
- Autant de remboursements que souhaité, tant que la somme ≤ `purchase_amount`.
- Le remboursement des frais / intérêts consommateur est entièrement géré par Alma.

## Champs

| Champ | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Identifiant du remboursement |
| `created` | timestamp | Date de création |
| `amount` | integer | Montant du remboursement (centimes) |
| `amount_customer_fees` | integer | ⚠️ **Déprécié**. Frais client remboursés (net) |
| `amount_customer_fees_with_vat` | integer | ⚠️ **Déprécié** |
| `amount_customer_fees_vat` | integer | ⚠️ **Déprécié** |
| `merchant_reference` | string | Référence interne marchand (rapprochement avec votre base) |

## Exemple

```json
{
  "id": "refund_11h3jIO3ysBniMdtgC2AyEW4skyEG43P7H",
  "created": 1552404383,
  "amount": 17000,
  "merchant_reference": "981201927"
}
```

## Suivi côté Payment

| Champ | Description |
| :--- | :--- |
| `refunds` | Liste des remboursements opérés |
| `amount_already_refunded` | Montant total déjà remboursé |
| `is_completely_refunded` | `true` si remboursement intégral |

## Création

[Créer un Remboursement](../10-refund.md) — `POST /v1/payments/{payment_id}/refunds`