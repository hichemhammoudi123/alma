# Objet Customer

Informations personnelles d'un client. Il ne peut être créé ou récupéré **directement** : seulement via l'objet [`Payment`](payment.md) (créé/modifié lors des endpoints Payment).

## Champs

| Champ | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Identifiant Alma du client |
| `created` | timestamp | Date de création (Alma) |
| `first_name` | string \| null | Prénom |
| `last_name` | string \| null | Nom de famille |
| `email` | string \| null | Email |
| `phone` | string \| null | Téléphone |
| `is_business` | boolean | `true` si entreprise |
| `business_id_number` | string \| null | ID de l'entreprise (ex. SIREN) |
| `business_name` | string \| null | Nom de l'entreprise |
| `account_id` | string | ID du client dans **votre** système (marchand) |
| `account_created` | timestamp | Date de création du compte chez vous |
| `previous_orders_count` | integer | Nombre de commandes passées (votre historique) |

## Exemple

```json
{
  "id": "customer_11h3ch7UDyyCiuHCKy02y4EeWkwd3JuHUb",
  "created": 1552378923,
  "first_name": "Martin",
  "last_name": "Dupont",
  "email": "martin.dupont@gmail.com",
  "phone": "+330612345678",
  "is_business": false,
  "business_id_number": null,
  "business_name": null,
  "account_id": "45rfT6lo_908",
  "account_created": 1780500147,
  "previous_orders_count": 42
}
```

## Champs modifiables

✅ À la création ([Create Payment](../02-create-payment.md)) : `first_name`, `last_name`, `email`, `phone`, `birth_date`, `addresses[]`, `is_business`, `business_id_number`, `business_name`, `account_id`, `account_created`, `previous_orders_count`.

⚠️ Via [Update Payment](../05-update-payment.md) : un champ déjà renseigné ne peut **plus être modifié** ensuite.