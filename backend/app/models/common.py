"""Objets partagés : Address, Customer, Order — utilisés dans les payloads des paiements."""

from pydantic import BaseModel, Field


class Address(BaseModel):
    """Adresse de livraison ou de facturation."""

    title: str | None = Field(None, description="Titre (ex. M., Mme)")
    first_name: str | None = Field(None, description="Prénom")
    last_name: str | None = Field(None, description="Nom")
    company: str | None = Field(None, description="Entreprise")
    line1: str | None = Field(None, description="Ligne principale, ex. \"1 rue de Rivoli\"")
    line2: str | None = Field(None, description="Complément d'adresse")
    city: str | None = Field(None, description="Ville")
    postal_code: str | None = Field(None, description="Code postal")
    county_sublocality: str | None = Field(None, description="Département")
    state_province: str | None = Field(None, description="Région")
    country: str | None = Field(None, description="Pays (ex. France)")
    email: str | None = Field(None, description="Email associé à l'adresse")
    phone: str | None = Field(None, description="Téléphone (ex. contact livraison)")


class Customer(BaseModel):
    """Informations personnelles du client."""

    id: str | None = Field(None, description="Identifiant Alma du client (lecture seule)")
    created: str | None = Field(None, description="Date de création chez Alma (lecture seule)")
    first_name: str | None = Field(None, description="Prénom")
    last_name: str | None = Field(None, description="Nom de famille")
    email: str | None = Field(None, description="Email du client")
    phone: str | None = Field(None, description="Téléphone du client")
    birth_date: str | None = Field(None, description="Date de naissance (format yyyy-mm-dd)")
    addresses: list[Address] | None = Field(None, description="Adresses liées au client")
    is_business: bool | None = Field(
        False,
        description="true si entreprise. Une fois envoyé, le client ne peut pas modifier cette valeur.",
    )
    business_id_number: str | None = Field(None, description="ID de l'entreprise (SIREN par défaut)")
    business_name: str | None = Field(None, description="Nom de l'entreprise")
    account_id: str | None = Field(
        None, description="Identifiant du client dans VOTRE système (marchand)"
    )
    account_created: str | None = Field(
        None, description="Date de création du compte client dans votre système"
    )
    previous_orders_count: int | None = Field(
        None, description="Nombre de commandes passées par le client (votre historique)"
    )


class Order(BaseModel):
    """Commande associée au paiement (format Order Alma)."""

    merchant_reference: str | None = Field(
        None,
        description="Référence marchand de la commande, présentée au client — "
        "fait le lien entre votre commande et le paiement Alma",
    )
    merchant_url: str | None = Field(
        None, description="URL de la page du backoffice marchand pour cette commande"
    )
    customer_url: str | None = Field(
        None, description="URL de la page de suivi de commande destinée au client"
    )
    data: dict | None = Field(None, description="Données arbitraires entrées par le marchand")
    comment: str | None = Field(None, description="Commentaire marchand sur la commande")


class CartItem(BaseModel):
    """Ligne du panier transmise à Alma (contexte de la transaction)."""

    title: str = Field(..., description="Nom du produit")
    quantity: int = Field(..., description="Quantité")
    line_price: int = Field(..., description="Prix de la ligne en centimes")
    picture_url: str = Field(..., description="URL de l'image du produit")


class Cart(BaseModel):
    """Contenu du panier à la création du Payment."""

    items: list[CartItem] = Field(..., description="Lignes du panier")
