# Envoyer un lien de paiement (SMS / Email)

Envoyez un lien de paiement au client par SMS ou par email. Deux alternatives :

1. Utiliser votre propre infrastructure d'envoi : récupérez simplement l'attribut `url` du payment créé ([Create Payment](02-create-payment.md)).
2. Utiliser les endpoints ci-dessous pour déclencher l'envoi par Alma.

> 🚫 Fonctionnalités **non activées par défaut** : contacter le support Alma pour les activer.

## Envoyer par SMS

**`POST /v1/payments/{payment_id}/send-sms`**

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/send-sms" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
```

Necessite un `customer[phone]` lors de la création du payment. Recommandé : `origin: "pos_sms"` à la création (cas caisse).

Réponse — 200 : `{ "success": true }`

Erreurs :

| Code | Meaning |
| :--- | :--- |
| `400` | `customer[phone]` manquant |
| `403` | Fonctionnalité non activée pour le compte |

## Envoyer par Email

**`POST /v1/payments/{payment_id}/send-email`**

```shell
curl -X POST "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/send-email" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
```

Réponse — 200 : `{ "success": true }`

Erreurs :

| Code | Meaning |
| :--- | :--- |
| `400` | Requête invalide (ex. email manquant) |
| `401` | Credentials invalides |

## Notes Customer Panel

- Cas d'usage typique : paiement en boutique / relance d'une commande abandonnée via lien unique.
- Préférer l'option 1 (votre propre envoi + `payment.url`) pour contrôler le contenu du message.