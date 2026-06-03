import os

try:
    from .config import api_id, api_hash
except ImportError:
    api_id = os.environ.get("API_ID", "")
    api_hash = os.environ.get("API_HASH", "")

__all__ = ['api_id', 'api_hash']
