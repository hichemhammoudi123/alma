# Introduction

## URLs de base

| Environnement | URL |
| :--- | :--- |
| Production | `https://api.getalma.eu/v1/` |
| Sandbox | `https://api.sandbox.getalma.eu/v1/` |

Endpoint Shipment (v2) : `https://api.sandbox.getalma.eu/v2/`

## Authentification

Pour toute requête authentifiée, ajouter le header :

| Header | Valeur |
| :--- | :--- |
| `Authorization` | `Alma-Auth <API key>` |

```shell
curl "https://api.sandbox.getalma.eu/v1/payments?limit=2" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
```

- Clé de test : `sk_test_...` (sandbox)
- Clé de production : `sk_live_...` (live)
- En cas d'échec d'authentification : erreur `401` avec les raisons de l'échec.

> ❗️ La clé d'API est **secrète**. Tous les appels authentifiés doivent être effectués depuis vos serveurs (backend), jamais depuis un frontend (React).

## Format des données

- Corps des requêtes et réponses : **JSON**
- `Content-Type: application/json`
- **Montants en centimes** (entiers) : `20000` = `200,00 €`
- **Dates / timestamps** : en secondes (epoch)
- Identifiants : préfixés (`payment_...`, `order_...`, `refund_...`, `customer_...`)

## Structure générale d'un appel

| Méthode | URL | Body |
| :--- | :--- | :--- |
| `GET` | `/v1/resource/{id}` | — |
| `POST` | `/v1/resource` | JSON |
| `POST` | `/v1/resource/{id}/action` | JSON si besoin |

## Codes de retour courants

| Code | Signification |
| :--- | :--- |
| `200` | Succès |
| `204` | Succès sans contenu |
| `400` | Requête invalide (validation) |
| `401` | Authentification invalide |
| `404` | Ressource introuvable |
| `422` | Erreur de validation de champs |
| `403` | Opération non autorisée (ex. marchand hors France) |