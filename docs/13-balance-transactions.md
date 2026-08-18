# Récupérer une liste de Balance Transactions

**`GET /v1/balance-transactions`**

Ressource **back-office** (comptabilité / réconciliation), pas un endpoint de checkout.

Retourne les transactions liées aux mouvements du compte marchand (paiements, remboursements, virements — payouts —, ajustements...).

## Requête

```shell
curl "https://api.sandbox.getalma.eu/v1/balance-transactions?limit=50&merchant=all&kind=from_payout" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
```

## Query parameters

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `merchant` | string | ID du marchand. Défaut = marchand authentifié. `all` = tous les comptes enfants accessibles |
| `kind` | string | `from_transaction`, `from_adjustment`, `from_payout`, `from_refund`, `from_fee_waiver`, `from_merchant_default_coverage` |
| `limit` | integer | Limite de résultats |
| `starting_after` | string | ID de transaction (pagination) |

## Réponse — 200

```json
{
  "id": "balance_txn_11jdy0c34dqAkKfXsqUy042CAqaq577qFN",
  "merchant_id": "merchant_11iTSik4Ej76KAEMyo8cEK42wUeSd69hbo",
  "amount": -283462,
  "net_amount": -283462,
  "merchant_fee": 0,
  "payment_id": null,
  "refund_id": null,
  "payout_id": "payout_11jdxsj3doAjuaugq864kukq4WMYM2kPl1",
  "included_in_payout_id": null,
  "kind": "from_payout",
  "comment": null,
  "updated": 1590592915,
  "available_on": 1590592915,
  "created": 1590592915
}
```

### Champs principaux

| Champ | Type | Description |
| :--- | :--- | :--- |
| `id` | string | ID de la transaction |
| `merchant_id` | string | ID du marchand |
| `amount` | integer | Montant (centimes, signé) |
| `net_amount` | integer | Montant net |
| `merchant_fee` | integer | Frais marchand |
| `payment_id` / `refund_id` / `payout_id` | string \| null | Objets liés |
| `kind` | string | Type de transaction |
| `comment` | string \| null | Commentaire |
| `available_on` / `created` / `updated` | timestamp | Dates |

> ⚠️ La forme exacte de l'enveloppe (liste directe vs `data` + `has_more`) peut varier selon l'environnement : vérifier la réponse réelle.

## Notes Customer Panel

- Utiliser les `custom_data` des paiements : ils remontent dans les exports comptables, ce qui facilite le rapprochement avec vos IDs internes (`order_id`, `customer_id`).