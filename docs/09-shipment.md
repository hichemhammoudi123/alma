# Envoyer les informations d'expédition

**`POST /v2/orders/{order_id}/shipment`**

Envoie les données de livraison / suivi d'une commande.

> ⚠️ Endpoint **v2** : base URL `https://api.sandbox.getalma.eu/v2/` — et réservé aux **marchands français** (`403` sinon).

## Requête

```shell
curl -X POST "https://api.sandbox.getalma.eu/v2/orders/order_11u6ZY7Bjhh50ew29rpZyUI32InCs5pSxF/shipment" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P" \
  -H "Content-Type: application/json" \
  -d '{
    "carrier": "Colissimo",
    "tracking_number": "8X12345678901",
    "tracking_url": "https://suivi.laposte.fr/8X12345678901"
  }'
```

## Path parameters

| Paramètre | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | string | ✅ | ID Alma de la commande |

## Payload

| Champ | Type | Requis | Description |
| :--- | :--- | :--- | :--- |
| `carrier` | string | ✅ | Transporteur |
| `tracking_number` | string | ✅ | Numéro de suivi |
| `tracking_url` | string | ❌ | URL de suivi |

## Réponse — 204

Succès sans contenu.

## Erreurs

| Code | Meaning |
| :--- | :--- |
| `400` | Requête invalide |
| `401` | Non authentifié |
| `403` | Réservé aux marchands français |
| `404` | Order introuvable |
| `422` | `carrier` / `tracking_number` manquants |