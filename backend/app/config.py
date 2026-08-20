"""Configuration du backend : lecture des variables d'environnement (fichier .env)."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Toutes les valeurs configurables du backend.

    Champs chargés depuis le fichier `.env` (voir `.env.example`).
    """

    # Clé API Alma : secrète, reste uniquement côté serveur.
    ALMA_API_KEY: str = "sk_test_3RG9iMTw2oearUHkNCBUUZ3P"
    # URL de base de l'API Alma (v1).
    ALMA_API_BASE: str = "https://api.sandbox.getalma.eu/v1"
    # URL de base de l'API Alma (v2) — utilisée uniquement pour le shipment.
    ALMA_API_BASE_V2: str = "https://api.sandbox.getalma.eu/v2"
    # Origines autorisées pour le CORS (séparées par des virgules).
    CORS_ORIGINS: str = "http://localhost:3000"
    # Timeout des appels HTTP vers Alma (secondes).
    ALMA_TIMEOUT: int = 30
    # Vérification du certificat TLS (mettre à false si un proxy d'entreprise
    # intercepte les flux HTTPS avec un certificat auto-signé).
    ALMA_SSL_VERIFY: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origins_list(self) -> list[str]:
        """Transforme la chaîne CORS_ORIGINS en liste d'origines."""
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


# Instance unique de la configuration, importable partout :
#   from app.config import settings
settings = Settings()
