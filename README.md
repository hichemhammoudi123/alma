# Alma — Intégration Customer Panel

Documentation technique complète de l'API Alma (sandbox) pour le projet **Customer Panel**.

Base de référence : [docs.almapay.com/reference](https://docs.almapay.com/reference)

## Environnements

| Environnement | URL de base |
| :--- | :--- |
| Sandbox (test) | `https://api.sandbox.getalma.eu/v1/` |
| Production (live) | `https://api.getalma.eu/v1/` |

> ⚠️ Endpoint `shipment` seul est en **v2** : `https://api.sandbox.getalma.eu/v2/`.

## Clé d'API

- Header requis : `Authorization: Alma-Auth <API key>` (géré côté backend, pas besoin de la mettre dans Postman).
- Clé de test : `sk_test_3RG9iMTw2oearUHkNCBUUZ3P` (sandbox)
- La clé est **secrète** : elle ne doit être utilisée que côté serveur (backend), jamais dans React.

## Liste des endpoints

| Méthode | Endpoint | Description | Doc |
| :--- | :--- | :--- | :--- |
| `POST` | `/v1/payments/eligibility` | Vérifier l'éligibilité d'un achat | [#1](#1-éligibilité) |
| `POST` | `/v1/payments` | Créer un paiement | [#2](#2-créer-un-paiement) |
| `GET` | `/v1/payments/{payment_id}` | Récupérer un paiement | [#4](#4-récupérer-un-paiement) |
| `GET` | `/v1/payments` | Lister les paiements | [#3](#3-lister-les-paiements) |
| `POST` | `/v1/payments/{payment_id}` | Modifier un paiement | [#5](#5-modifier-un-paiement) |
| `POST` | `/v1/payments/{payment_id}/cancel` | Annuler un paiement | [#6](#6-annuler-un-paiement) |
| `POST` | `/v1/payments/{payment_id}/orders` | Créer une Order pour un Payment | [#7](#7-créer-une-order-pour-un-payment-existant) |
| `POST` | `/v1/payments/{payment_ext_id}/orders/{merchant_ref}/status` | Envoyer le statut d'une commande | [#8](#8-envoyer-le-statut-dune-commande) |
| `POST` | `/v2/orders/{order_id}/shipment` | Envoyer les infos d'expédition | [#9](#9-envoyer-les-informations-dexpédition) |
| `POST` | `/v1/payments/{payment_id}/refunds` | Créer un remboursement | [#10](#10-créer-un-remboursement) |
| `POST` | `/v1/payments/{payment_id}/captures` | Capture différée | [#11](#11-capture-différée) |
| `POST` | `/v1/payments/{payment_id}/send-sms` | Envoyer un lien par SMS | [#12--13](#12--13-envoyer-un-lien-de-paiement-par-sms--email) |
| `POST` | `/v1/payments/{payment_id}/send-email` | Envoyer un lien par email | [#12--13](#12--13-envoyer-un-lien-de-paiement-par-sms--email) |
| `GET` | `/v1/balance-transactions` | Balance transactions (compta) | [#14](#14-balance-transactions-back-office--compta) |

## Webhooks

| Type | Méthode | Description | Doc |
| :--- | :--- | :--- | :--- |
| IPN | `GET` sur `ipn_callback_url?pid={payment_id}` | Notification serveur à serveur | [#15](#15-ipn--notification-serveur-à-serveur) |
| Webhooks (bêta) | `POST` | `payment.created` / `authorized` / `captured` / `canceled` | [#16](#16-webhooks-bêta-post) |

## Objets

- [Payment](docs/objects/payment.md)
- [Customer](docs/objects/customer.md)
- [Address](docs/objects/address.md)
- [Order](docs/objects/order.md)
- [Refund](docs/objects/refund.md)

## Convention

Tous les montants sont exprimés en **centimes** :

```text
purchase_amount = 20000  ⇔  200,00 €
```

---

# Référence détaillée — Payloads et Réponses

**Comment lire ?** Chaque endpoint présente :
1. **Le JSON « Postman »** : bloc `json` → copier/coller tel quel (c'est du JSON valide, sans commentaire).
2. **Le tableau des champs** : explique chaque champ du payload (l'équivalent d'un commentaire par champ).

Le backend local expose ces endpoints via `http://localhost:8000/api/alma/*`.

**⚠️ Postman — règle d'or (cause n°1 d'erreur `Input should be a valid dictionary`)** :
1. Onglet **Body** → bouton radio **raw**.
2. Tout à droite du dropdown (à côté de &lt;TEXT&gt;) : cliquer et sélectionner **JSON** (postman envoie alors `Content-Type: application/json`).
3. Coller le JSON.
   Si vous laissez « Text », le body est envoyé comme chaîne → FastAPI refuse avec `Input should be a valid dictionary or object`.

---

## 1. Éligibilité

> Vérifie quels échéanciers Alma peut proposer pour un panier. Ne crée aucun paiement. À appeler avant d'afficher Alma.

**Endpoint :** `POST /api/alma/eligibility`

**JSON Postman**

```json
{
  "payment": {
    "purchase_amount": 20000,
    "installments_count": [3, 4]
  }
}
```

**Champs du payload**

| Champ | Type | Obligatoire | Explication |
| :--- | :--- | :--- | :--- |
| `payment.purchase_amount` | int | ✅ | Montant du panier en centimes (`20000` = `200 €`) |
| `payment.installments_count` | int ou `[int,...]` | non | NB d'échéances : entier → réponse objet unique ; tableau `[3,4]` → réponse en tableau ; absent → `3` par défaut |

**Réponse (200)**

```json
[
  {
    "eligible": true,
    "installments_count": 3,
    "deferred_days": 0,
    "deferred_months": 0,
    "customer_total_cost_amount": 0,
    "customer_total_cost_bps": 0,
    "payment_plan": [
      { "due_date": 1787216267, "purchase_amount": 6668, "customer_fee": 0, "customer_interest": 0, "total_amount": 6668 },
      { "due_date": 1789894667, "purchase_amount": 6666, "customer_fee": 0, "customer_interest": 0, "total_amount": 6666 }
    ]
  },
  {
    "eligible": true,
    "installments_count": 4,
    "deferred_days": 0,
    "deferred_months": 0,
    "customer_total_cost_amount": 0,
    "customer_total_cost_bps": 0,
    "payment_plan": [
      { "due_date": 1787216267, "purchase_amount": 5000, "customer_fee": 0, "customer_interest": 0, "total_amount": 5000 }
    ]
  }
]
```

**Champs de la réponse**

| Champ | Explication |
| :--- | :--- |
| `eligible` | `true` → échéancier proposable au client |
| `installments_count` | NB d'échéances de cet échéancier |
| `deferred_days` / `deferred_months` | Décalage de la 1ère échéance (paiement différé) |
| `customer_total_cost_amount` | Frais + intérêts client en centimes |
| `customer_total_cost_bps` | Frais client en points de base (non contractuel pour le crédit) |
| `payment_plan[]` | Une ligne par échéance : `due_date` (timestamp s), `purchase_amount`, `customer_fee`, `customer_interest`, `total_amount` |

> Si non éligible : `{ "eligible": false, "reasons": { "purchase_amount": "invalid_value" }, "constraints": { "purchase_amount": { "minimum": 100, "maximum": 1000000 } } }`

---

## 2. Créer un paiement

> Appel le plus important : crée le paiement → Alma fournit une URL de checkout à laquelle rediriger le client.

**Endpoint :** `POST /api/alma/payments` — seul `payment.purchase_amount` est obligatoire.

**JSON Postman**

```json
{
  "payment": {
    "purchase_amount": 20000,
    "installments_count": 4,
    "return_url": "https://cp.fr/alma/return",
    "customer_cancel_url": "https://cp.fr/checkout",
    "failure_return_url": "https://cp.fr/checkout/error",
    "ipn_callback_url": "https://cp.fr/alma/ipn",
    "custom_data": {
      "order_id": "CP-10001",
      "customer_id": "CUS-458"
    },
    "deferred_months": 0,
    "deferred_days": 0,
    "locale": "fr",
    "expires_after": 2880,
    "capture_method": "automatic",
    "shipping_address": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "line1": "1 rue de Rivoli",
      "city": "Paris",
      "postal_code": "75004",
      "country": "France",
      "phone": "+330612345678",
      "email": "jean@example.com"
    },
    "billing_address": {
      "first_name": "Jean",
      "last_name": "Dupont",
      "line1": "1 rue de Rivoli",
      "city": "Paris",
      "postal_code": "75004",
      "country": "France",
      "phone": "+330612345678",
      "email": "jean@example.com"
    },
    "cart": {
      "items": [
        { "title": "Produit A", "quantity": 1, "line_price": 20000, "picture_url": "https://cdn.ex/a.jpg" }
      ]
    },
    "merchant_covers_all_fees": false,
    "origin": "online"
  },
  "customer": {
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean@example.com",
    "phone": "+330612345678",
    "birth_date": "1990-01-01",
    "is_business": false,
    "business_id_number": null,
    "business_name": null,
    "account_id": "CUS-458",
    "account_created": "2024-01-01T00:00:00Z",
    "previous_orders_count": 3
  },
  "order": {
    "merchant_reference": "CP-10001",
    "merchant_url": "https://cp.fr/admin/orders/10001",
    "customer_url": "https://cp.fr/orders/10001",
    "data": { "campaign": "ete" },
    "comment": "Panier standard"
  }
}
```

**Champs du payload — `payment`**

| Champ | Type | Obligatoire | Explication |
| :--- | :--- | :--- | :--- |
| `purchase_amount` | int | ✅ | Montant du panier **sans** frais Alma (centimes) |
| `installments_count` | int | non | NB de prélèvements (défaut 3) |
| `return_url` | string | ✅ | URL de retour APRÈS paiement (Alma ajoute `?pid=`) |
| `customer_cancel_url` | string | non | URL si le client annule (Alma ajoute `?pid=`) |
| `failure_return_url` | string | non | URL si le paiement est refusé |
| `ipn_callback_url` | string | non | URL notifiée en async quand le paiement est effectué (recommandé) |
| `custom_data` | objet | non | JSON libre → lie le payment à VOS IDs internes (`order_id`, `customer_id`) |
| `deferred_months` / `deferred_days` | int | non | Report de la 1ère échéance en mois / jours |
| `locale` | string | non | Langue client : `fr`, `en`, `it`, `es`, `de`, `nl`, `nl_BE` |
| `expires_after` | int | non | Validité du lien en minutes (défaut 2880) |
| `capture_method` | string | non | `automatic` (défaut) ou `manual` (capture différée) |
| `shipping_address` / `billing_address` | objet | non | Voir champ `line1` etc. — adresse de livraison/facturation |
| `cart.items[]` | tableau | non | Contenu du panier : `title`, `quantity`, `line_price`, `picture_url` |
| `merchant_covers_all_fees` | bool | non | `true` → le marchand prend les frais à sa charge |
| `origin` | string | non | Origine du paiement (`online`, `pos_sms`, ...) |

**Champs du payload — `customer`**

| Champ | Type | Obligatoire | Explication |
| :--- | :--- | :--- | :--- |
| `first_name` / `last_name` | string | non | Prénom / nom de famille |
| `email` | string | non | Email |
| `phone` | string | non | Téléphone (ex. `+33...`) |
| `birth_date` | string | non | Date de naissance `YYYY-MM-DD` |
| `is_business` | bool | non | `true` si entreprise (non modifiable ensuite) |
| `business_id_number` / `business_name` | string | non | Identifiant (SIREN par défaut) / nom de l'entreprise |
| `account_id` | string | non | ID client dans VOTRE système |
| `account_created` | string | non | Date de création du compte chez vous (ISO 8601) |
| `previous_orders_count` | int | non | NB de commandes passées chez vous |

**Champs du payload — `order` (facultatif)**

| Champ | Type | Explication |
| :--- | :--- | :--- |
| `merchant_reference` | string | Référence marchand → le lien entre votre commande et Alma |
| `merchant_url` | string | URL backoffice marchand |
| `customer_url` | string | URL de suivi visible par le client |
| `data` | objet | Données arbitraires |
| `comment` | string | Commentaire marchand |

**Réponse (200)**

```json
{
  "id": "payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "url": "https://checkout.sandbox.getalma.eu/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8",
  "processing_status": "awaiting_authorization",
  "state": "not_started",
  "cancelation_reason": null,
  "purchase_amount": 20000,
  "installments_count": 4,
  "kind": "P4X",
  "payment_plan": [
    { "state": "pending", "due_date": 1787048072, "purchase_amount": 5000, "customer_fee": 0 }
  ],
  "customer": { "id": "customer_...", "first_name": "Jean", "email": "jean@example.com" },
  "custom_data": { "order_id": "CP-10001", "customer_id": "CUS-458" },
  "orders": [ { "id": "order_...", "merchant_reference": "CP-10001" } ],
  "is_deferred_capture": false,
  "refunds": [],
  "is_completely_refunded": false,
  "amount_already_refunded": 0,
  "fees": { "merchant": { "total": 1152, "total_excluding_tax": 960, "tax": 192 } }
}
```

**Champs de la réponse**

| Champ | Explication |
| :--- | :--- |
| `id` | ID Alma du payment → à conserver |
| `url` | **À ne surtout pas confondre** : page checkout → **rediriger le client ici** |
| `processing_status` | `awaiting_authorization` → `authorized` → `captured` / `canceled` |
| `state` | (déprécié) `not_started`, `paid`, ... |
| `cancelation_reason` | Si annulé : `requested_by_merchant`, `requested_by_customer`, `authorization_expired`, `expired` |
| `kind` | Type de paiement (`P3X`, `P4X`, `P10X`...) |
| `payment_plan[]` | Une ligne par échéance (`state`, `due_date`, `purchase_amount`, `customer_fee`) |
| `customer` | Client lié |
| `custom_data` | Vos données internes (retournées telles quelles) |
| `orders` | Orders liées au payment |
| `is_deferred_capture` | `true` si capture différée |
| `refunds` / `is_completely_refunded` / `amount_already_refunded` | État des remboursements |
| `fees` | Frais marchand (`total`, `total_excluding_tax`, `tax`) |

> ⚠️ Ne **jamais** valider la commande sur le simple `return_url` : toujours re-vérifier via l'endpoint [#4](#4-récupérer-un-paiement) + IPN [#15](#15-ipn--notification-serveur-à-serveur).

---

## 3. Lister les paiements

**Endpoint :** `GET /api/alma/payments`

**Query params**

| Param | Exemple | Explication |
| :--- | :--- | :--- |
| `created_after` / `created_before` | `1787040000` | Filtrer par date de création (timestamp s) |
| `customer_email` | `jean@example.com` | Recherche par email (contient) |
| `state` | `paid` | `not_started` / `scored_no` / `scored_yes` / `scored_maybe` / `paid` |
| `limit` | `20` | Nombre de résultats (défaut 20) |
| `starting_after` | `payment_...` | Pagination : ID du dernier payment de la page précédente |

**Exemple d'URL**

```
GET /api/alma/payments?limit=20&state=paid&customer_email=jean@example.com
```

**Réponse (200)**

```json
{
  "has_more": false,
  "data": [
    {
      "id": "payment_...",
      "merchant_name": "blackbear",
      "state": "not_started",
      "processing_status": "...",
      "created": 1787040848,
      "updated": 1787046785,
      "purchase_amount": 20000,
      "kind": "P4X",
      "customer": { "first_name": "Jean", "last_name": "Dupont", "email": "jean@example.com" },
      "orders": [ { "id": "order_...", "merchant_reference": "CP-10001" } ],
      "origin": "online",
      "refunds": []
    }
  ]
}
```

**Champs de la réponse**

| Champ | Explication |
| :--- | :--- |
| `has_more` | `true` → il existe d'autres pages |
| `data[]` | Liste des payments, du plus récent au plus ancien (id, créé, updated, montant, type, client, orders, refunds) |

---

## 4. Récupérer un paiement

> Endpoint de contrôle le plus important : après le retour client, un IPN ou un webhook, vérifiez TOUJOURS ici avant de valider la commande.

**Endpoint :** `GET /api/alma/payments/{payment_id}`

**Exemple d'URL**

```
GET /api/alma/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8
```

**Réponse (200)** — même objet que la réponse de l'endpoint [#2](#2-créer-un-paiement).

**Contrôles à faire**

| Champ | Valeur attendue | Explication |
| :--- | :--- | :--- |
| `processing_status` | `authorized` ou `captured` | paiement réussi |
| `purchase_amount` | == montant du panier | aucun écart de montant |
| `custom_data.order_id` | == votre référence de commande | bonne commande |
| `cancelation_reason` | `requested_by_merchant` / `requested_by_customer` / `authorization_expired` / `expired` | contexte si annulé |

---

## 5. Modifier un paiement

> Uniquement si le **1er prélèvement n'a pas eu lieu**. Un champ client déjà renseigné ne peut plus être modifié.

**Endpoint :** `POST /api/alma/payments/{payment_id}`

**JSON Postman**

```json
{
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
        "line1": "1 rue de Rivoli",
        "city": "Paris",
        "postal_code": "75004",
        "country": "France"
      }
    ]
  },
  "locale": "fr"
}
```

**Champs du payload**

| Champ | Type | Explication |
| :--- | :--- | :--- |
| `customer` | objet | Données du client à mettre à jour (mêmes champs que l'endpoint 2) |
| `customer.addresses[]` | tableau | Adresses liées au client (`first_name`, `line1`, `city`, `postal_code`, `country`) |
| `locale` | string | Langue de communication avec le client |

---

## 6. Annuler un paiement

**Endpoint :** `POST /api/alma/payments/{payment_id}/cancel` — aucun body.

**Exemple d'URL**

```
POST /api/alma/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/cancel
```

| Réponse | Signification |
| :--- | :--- |
| `204` | Annulé ✅ |
| `400` | Non annulable → `{ "message": "Le statut de ce paiement ne permet pas de l'annuler" }` |

---

## 7. Créer une Order pour un Payment existant

> Quand la référence de commande n'était pas connue à la création du payment.

**Endpoint :** `POST /api/alma/payments/{payment_id}/orders`

**JSON Postman**

```json
{
  "order": {
    "merchant_reference": "CP-10001",
    "merchant_url": "https://cp.fr/admin/orders/10001",
    "customer_url": "https://cp.fr/orders/10001",
    "data": { "campaign": "ete" },
    "comment": null
  }
}
```

**Champs du payload**

| Champ | Type | Explication |
| :--- | :--- | :--- |
| `merchant_reference` | string | Référence marchand → le lien entre vos 2 systèmes |
| `merchant_url` | string | URL backoffice marchand |
| `customer_url` | string | URL de suivi client |
| `data` | objet | Données arbitraires |
| `comment` | string/null | Commentaire marchand |

**Réponse (200)**

```json
[
  {
    "id": "order_...",
    "created": 1787215054,
    "updated": 1787215054,
    "merchant_reference": "CP-10001",
    "merchant_url": null,
    "customer_url": null,
    "payment": "payment_...",
    "comment": null,
    "data": {}
  }
]
```

**Champs de la réponse**

| Champ | Explication |
| :--- | :--- |
| `id` | Identifiant Alma de l'order |
| `merchant_reference` | Référence marchand |
| `payment` | ID du payment associé |

---

## 8. Envoyer le statut d'une commande

**Endpoint :** `POST /api/alma/payments/{payment_external_id}/orders/{merchant_order_reference}/status`

**Exemple d'URL**

```
POST /api/alma/payments/payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8/orders/CP-10001/status
```

**JSON Postman**

```json
{
  "status": "shipped",
  "is_shipped": true
}
```

**Champs du payload**

| Champ | Type | Explication |
| :--- | :--- | :--- |
| `status` | string | REQUIS · nouveau statut à enregistrer (`shipped`, ...) |
| `is_shipped` | bool | `true` si la commande est expédiée (en route vers le client) |

→ `204` en cas de succès. Erreur `422` si `is_shipped` n'est pas un booléen.

---

## 9. Envoyer les informations d'expédition

> ⚠️ Endpoint Alma en **v2**, réservé aux **marchands français**.

**Endpoint :** `POST /api/alma/orders/{order_id}/shipment`

**Exemple d'URL**

```
POST /api/alma/orders/order_11u6ZY7Bjhh50ew29rpZyUI32InCs5pSxF/shipment
```

**JSON Postman**

```json
{
  "carrier": "Colissimo",
  "tracking_number": "8X12345678901",
  "tracking_url": "https://suivi.laposte.fr/8X12345678901"
}
```

**Champs du payload**

| Champ | Type | Obligatoire | Explication |
| :--- | :--- | :--- | :--- |
| `carrier` | string | ✅ | Transporteur (`Colissimo`, `DPD`, ...) |
| `tracking_number` | string | ✅ | Numéro de suivi |
| `tracking_url` | string | non | URL de suivi |

| Réponse | Signification |
| :--- | :--- |
| `204` | Succès ✅ |
| `403` | Marchand hors France |
| `404` | Order introuvable |
| `422` | Champ obligatoire manquant |

---

## 10. Créer un remboursement

**Endpoint :** `POST /api/alma/payments/{payment_id}/refunds`

**JSON Postman**

```json
{
  "amount": 5000,
  "merchant_reference": "RMB-987"
}
```

Pour un remboursement **intégral** : `{ "merchant_reference": "RMB-987" }` (sans `amount`).

**Champs du payload**

| Champ | Type | Explication |
| :--- | :--- | :--- |
| `amount` | int | Montant à rembourser en centimes. **Absent → remboursement intégral.** Partiel autorisé tant que somme des refunds ≤ `purchase_amount` |
| `merchant_reference` | string | Référence interne marchand (rapprochement avec votre base) |

**Réponse (200)**

```json
{
  "id": "refund_...",
  "created": 1787048999,
  "amount": 5000,
  "merchant_reference": "RMB-987"
}
```

> ❌ `400` si le payment n'a pas encore « débuté » (`not_started`) : impossible de rembourser.

---

## 11. Capture différée

> Pour un payment créé avec `capture_method: "manual"`.

**Endpoint :** `POST /api/alma/payments/{payment_id}/captures`

**JSON Postman**

```json
{
  "amount": 10000,
  "merchant_reference": "CAP-001"
}
```

**Champs du payload**

| Champ | Type | Explication |
| :--- | :--- | :--- |
| `amount` | int | Montant à capturer en centimes. **Absent → 1ère échéance complète** |
| `merchant_reference` | string | Référence interne de la capture |

**Réponse (200)**

```json
{
  "amount": 10000,
  "id": "b0f5ba04-f0b3-4eb8-b292-0b58bc77e16c"
}
```

> ⚠️ Capturer dans les **7 jours** après autorisation (sinon expiration + annulation). Captures multiples non supportées.

---

## 12 & 13. Envoyer un lien de paiement par SMS / Email

- `POST /api/alma/payments/{payment_id}/send-sms` — requiert `customer.phone` à la création du payment.
- `POST /api/alma/payments/{payment_id}/send-email`

Aucun body. ⚠️ Fonctionnalités **non activées par défaut** (contact support Alma).

**Réponse**

```json
{
  "success": true
}
```

Erreurs : `400` (champ manquant), `403` (non activé). Alternative : envoyer vous-même `payment.url` (endpoint [#2](#2-créer-un-paiement)).

---

## 14. Balance transactions (back-office / compta)

**Endpoint :** `GET /api/alma/balance-transactions`

**Query params**

| Param | Exemple | Explication |
| :--- | :--- | :--- |
| `merchant` | `all` | Défaut = marchand authentifié ; `all` = comptes enfants |
| `kind` | `from_payout` | `from_transaction` / `from_adjustment` / `from_payout` / `from_refund` / `from_fee_waiver` / `from_merchant_default_coverage` |
| `limit` | `20` | **Minimum 20** |
| `starting_after` | `balance_txn_...` | Pagination |

**Exemple d'URL**

```
GET /api/alma/balance-transactions?limit=20&merchant=all
```

**Réponse (200)**

```json
{
  "id": "balance_txn_...",
  "merchant_id": "merchant_...",
  "amount": -283462,
  "net_amount": -283462,
  "merchant_fee": 0,
  "payment_id": null,
  "refund_id": null,
  "payout_id": "payout_...",
  "included_in_payout_id": null,
  "kind": "from_payout",
  "comment": null,
  "available_on": 1590592915,
  "created": 1590592915,
  "updated": 1590592915
}
```

**Champs de la réponse**

| Champ | Explication |
| :--- | :--- |
| `id` | Identifiant de la transaction |
| `merchant_id` | Marchand concerné |
| `amount` / `net_amount` | Montant signé / net en centimes (négatif = débit) |
| `merchant_fee` | Frais marchand |
| `payment_id` / `refund_id` / `payout_id` | Élément lié selon le type de transaction |
| `included_in_payout_id` | Payout dans lequel la transaction est incluse |
| `kind` | Type de transaction |
| `available_on` | Date de disponibilité (timestamp s) |
| `created` / `updated` | Date de création / dernière modification |

---

## 15. IPN — notification serveur à serveur

> Appelé **par Alma** : `GET {ipn_callback_url}?pid={payment_id}` (async, ~60 s après paiement, rejoué ×10 si réponse ≠ 200). **Non signé.**

**Exemple d'URL (simulation test)**

```
GET /api/alma/ipn?pid=payment_123hrPE19ndy31CuIuidKXYtGUBGV9mtS8
```

**Traitement côté backend**

1. Alma appelle `GET {ipn_callback_url}?pid=payment_xxx`.
2. Le backend **rappelle** `GET /api/alma/payments/{pid}` (avec la clé privée) pour vérifier :
   - `processing_status` ∈ `authorized` / `captured`
   - `purchase_amount` == montant du panier
   - `custom_data.order_id` == votre référence
3. Si conforme → marquer la commande **PAID** (traitement idempotent). Répondre `200`.

**Réponse backend (200)**

```json
{
  "received": true,
  "payment_id": "payment_...",
  "payment": {}
}
```

**Champs de la réponse**

| Champ | Explication |
| :--- | :--- |
| `received` | Accusé de réception |
| `payment_id` | Payment concerné |
| `payment` | Payment complet récupéré pour vérification |

---

## 16. Webhooks bêta (POST)

> Notifiés **par Alma** (à activer : squad-integrations@getalma.eu). Notifications **POST** structurées.

**Endpoint :** `POST /api/alma/webhooks`

**Enveloppe reçue**

```json
{
  "type": "payment.captured",
  "data": {
    "id": "payment_...",
    "processing_status": "captured",
    "purchase_amount": 20000,
    "custom_data": { "order_id": "CP-10001" }
  }
}
```

**Champs de l'enveloppe**

| Champ | Explication |
| :--- | :--- |
| `type` | Code événement : `payment.created` / `payment.authorized` / `payment.captured` / `payment.canceled` |
| `data` | Payment Alma complet |

**Réponse backend (200)**

```json
{
  "received": true,
  "event": "payment.captured",
  "payment_id": "payment_..."
}
```

> Toujours re-vérifier l'état réel via l'endpoint [#4](#4-récupérer-un-paiement) (webhook non signé, réjouable).

---

## Codes d'erreur (toutes les routes)

Le backend propage les erreurs Alma :

```json
{
  "detail": "message d'erreur Alma (ou validation FastAPI)",
  "error_code": "validation_error"
}
```

| Code HTTP | Signification |
| :--- | :--- |
| `200` | Succès |
| `204` | Succès sans contenu |
| `400` | Requête invalide / paiement non annulable / non remboursable |
| `401` | Clé API invalide ou manquante |
| `403` | Opération non autorisée (ex. shipment hors France) |
| `404` | Ressource introuvable |
| `422` | Erreur de validation d'un champ |

---

## Flow de référence (Customer Panel)

```
Checkout → 1. Eligibility → client choisit l'échéancier
        → 2. Create Payment (+ custom_data + ipn_callback_url)
        → redirection vers payment.url
        → 15/16. IPN ou Webhook  (ou 3/4. GET Payment)
        → vérifier processing_status + montant
        → ORDER = PAID
        → (plus tard) 10. Refund / 14. Balance transactions
```