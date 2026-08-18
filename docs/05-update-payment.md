# Modifier un Paiement

**`POST /v1/payments/{payment_id}`**

Met à jour l'objet [`Payment`](objects/payment.md) ou [`Customer`](objects/customer.md).

> Un paiement ne peut être modifié que s'il n'a pas encore commencé (premier prélèvement non effectué). Un champ client renseigné ne peut plus être modifié ensuite.

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "email": "jean@example.com",
      "phone": "+330612345678",
      "birth_date": "1990-01-01",
      "is_business": false,
      "addresses": [
        {
          "first_name": "Jean",
          "last_name": "Dupont",
          "line1": "1 rue de Rivoli",
          "city": "Paris",
          "postal_code": "75004",
          "country": "France"
        }
      ]
    },
    "locale": "fr"
  }'
```

## Payload

| Champ | Type | Description |
| :--- | :--- | :--- |
| `customer` | object | Données du client à mettre à jour (voir [Customer](objects/customer.md)) |
| `customer.addresses[]` | array | Adresses liées au client (voir [Address](objects/address.md)) |
| `locale` | string | Langue de communication avec le client |

## Réponse — 200

Objet `Payment` mis à jour.

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Paiement déjà commencé ou champ non modifiable |