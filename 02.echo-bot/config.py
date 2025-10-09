import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978

    # Azure Language Service credentials (from .env)
    AZURE_LANGUAGE_KEY = os.environ.get("AZURE_LANGUAGE_KEY", "")
    AZURE_LANGUAGE_ENDPOINT = os.environ.get("AZURE_LANGUAGE_ENDPOINT", "")

