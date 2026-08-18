# Webhooks / IPN

Deux mécanismes de notification serveur-à-serveur : l'**IPN** (actuel, obligatoire) et le nouveau système de **webhooks** (bêta, plus détaillé).

## 1. IPN — Callback serveur à serveur (obligatoire)

Alma envoie un callback **IPN** (Instant Payment Notification) lorsqu'un paiement a été **accepté** et son premier prélèvement effectué.

- Envoyé de manière **asynchrone** (délai ≈ 60 s) sur l'URL renseignée dans `payment.ipn_callback_url`.
- Renvoyé **jusqu'à 10 fois** en cas de non-réponse (ou réponse ≠ 200).
- Non signé : simple **`GET`** avec paramètre `pid` :

```
GET https://api.customer-panel.com/alma/ipn?pid=payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8
```

### Vérification d'authenticité (indispensable)

Rappeler l'API avec votre clé privée :

```shell
curl "https://api.sandbox.getalma.eu/v1/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8" \
  -H "Authorization: Alma-Auth sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
```

Vérifier dans la réponse :

| Champ | Attendu |
| :--- | :--- |
| `processing_status` | `authorized` ou `captured` |
| `purchase_amount` | == montant de la commande |
| (optionnel) `custom_data.order_id` | == votre référence de commande |

Si tout est conforme → marquer la commande **PAID** dans le Customer Panel. Toujours répondre **`200`** à l'IPN (Alma retente sinon).

> L'IPN garantit que même si le client ferme la page avant le retour sur votre site, la commande est validée.

## 2. Webhooks modernes (bêta — à activer auprès d'Alma)

En lieu et place des IPN :

- 4 événements de paiement : `payment.created` / `payment.authorized` / `payment.captured` / `payment.canceled`
- Notifications en **`POST`** avec enveloppe structurée + code d'événement
- Latence réduite (quasi instantané), abonnement par type d'événement
- Activation : [squad-integrations@getalma.eu](mailto:squad-integrations@getalma.eu)

### Structure type (POST)

```json
{
  "type": "payment.captured",
  "data": {
    "id": "payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
    "processing_status": "captured",
    "purchase_amount": 20000,
    "custom_data": { "order_id": "CP-10001" }
  }
}
```

> Toujours re-vérifier l'état réel via `GET /v1/payments/{id}` (un webhook non signé peut être rejoué).

## Notes Customer Panel

| Point | Recommandation |
| :--- | :--- |
| URL d'écoute | API backend (`/alma/ipn`, `/alma/webhooks`), pas le frontend |
| Réponse requise | `200` le plus vite possible (traitement en tâche de fond) |
| Idempotence | Traitement idempotent (même `pid` plusieurs fois ≠ double commande) |
| Statut | Ne pas se fier à la seule redirection : IPN + GET Payment |
| Webhooks bêta | Prévoir le support dès maintenant (event-driven) pour migrer plus tard |