import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default=None, required: bool = False):
    value = os.getenv(key, default)

    if required and not value:
        raise ValueError(
            f"Missing required environment variable: {key}"
        )

    return value


API_KEY = get_env("OPENCODE_API_KEY", required=True)
BASE_URL = get_env("BASE_URL", required=True)
MODEL = get_env("MODEL", required=True)

WORKSPACE = get_env(
    "WORKSPACE",
    default="workspace",
)