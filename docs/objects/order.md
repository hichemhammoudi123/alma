# Objet Order

L'objet `Order` représente une commande, généralement liée à un [`Payment`](payment.md).

> Distinction importante pour le Customer Panel : **Payment ≠ Order**. Le payment est le paiement Alma ; l'order est la commande associée.

## Champs

| Champ | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Identifiant Alma de la commande |
| `created` | timestamp | Date de création sur Alma |
| `merchant_reference` | string \| null | Référence marchand — **le lien entre votre système et Alma** |
| `merchant_url` | string \| null | URL page backoffice marchand |
| `customer_url` | string \| null | URL de suivi de commande côté client |
| `payment` | string | ID Alma du payment correspondant (non présent dans la représentation depuis un payment) |
| `data` | object | Données arbitraires entrées par le marchand |
| `comment` | string \| null | Commentaire marchand |

## Exemple

```json
{
  "id": "order_11h4MCc4atnjecmoK6GU6UYGo6qMK6RMLw",
  "created": 1552553941,
  "merchant_reference": "ref-9676683702228572",
  "merchant_url": "https://backoffice.merchant.com/orders/ref-9676683702228572",
  "customer_url": null,
  "payment": "payment_11h4MEW6jokMbn3ya4sI0scgeauAm41CO4",
  "data": {},
  "comment": null
}
```

## Création

- Directement à la création du payment : `order` dans [Create Payment](../02-create-payment.md).
- Après coup : [Créer une Order pour un Payment existant](../07-create-order.md).