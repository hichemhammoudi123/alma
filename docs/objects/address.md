# Objet Address

Objet décrivant une adresse (livraison ou facturation). Il ne peut être créé ou récupéré **directement**, seulement via l'objet [`Payment`](payment.md).

## Champs

| Champ | Type | Description |
| :--- | :--- | :--- |
| `created` | timestamp | Date de création |
| `title` | string \| null | Titre |
| `first_name` | string \| null | Prénom |
| `last_name` | string \| null | Nom |
| `company` | string \| null | Entreprise |
| `line1` | string \| null | Ligne principale (ex. "1 rue de Rivoli") |
| `line2` | string \| null | Complément d'adresse |
| `city` | string \| null | Ville |
| `postal_code` | string \| null | Code postal |
| `county_sublocality` | string \| null | Département |
| `state_province` | string \| null | Région |
| `country` | string \| null | Pays |
| `email` | string \| null | Email associé |
| `phone` | string \| null | Téléphone (ex. contact qui reçoit la livraison) |

## Exemple

```json
{
  "created": 1552378923,
  "title": null,
  "first_name": null,
  "last_name": null,
  "company": null,
  "line1": "1 rue de Rivoli",
  "line2": null,
  "city": "Paris",
  "postal_code": "75004",
  "country": "France",
  "county_sublocality": null,
  "province": null,
  "email": null,
  "phone": "+330612345678"
}
```

## Utilisation

- Dans [Create Payment](../02-create-payment.md) : `payment.shipping_address` / `payment.billing_address`.
- Dans [Update Payment](../05-update-payment.md) : `customer.addresses[]`.