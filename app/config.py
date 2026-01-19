import os
from dotenv import load_dotenv

# Load .env if present (safe no-op if missing)
load_dotenv()


def get_env(name, default=None, required=False):
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


class Config:
    # Flask
    FLASK_SECRET_KEY = get_env("FLASK_SECRET_KEY", required=True)

    # SAML / Entra ID
    SAML_IDP_ENTITY_ID = get_env("SAML_IDP_ENTITY_ID", required=True)
    SAML_IDP_SSO_URL = get_env("SAML_IDP_SSO_URL", required=True)
    SAML_IDP_X509CERT = get_env("SAML_IDP_X509CERT", required=True)

    # Feature flags
    SAML_DEBUG = get_env("SAML_DEBUG", "false").lower() == "true"
    SAML_ENABLE_SLO = get_env("SAML_ENABLE_SLO", "false").lower() == "true"
