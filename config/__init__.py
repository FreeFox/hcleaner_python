import os

try:
    from .config import (
        api_id, api_hash,
        BOT_IDS, COMMAND_PATTERN,
        DELETE_DELAY_SECONDS, CHECK_INTERVAL_SECONDS,
    )
except ImportError:
    api_id = os.environ.get("API_ID", "")
    api_hash = os.environ.get("API_HASH", "")
    BOT_IDS = [1303228016, 539991741]
    COMMAND_PATTERN = r'(?i)^\/(achievements|drochnut|topd|topdall|topdd|help|dice|craft|case|use|keys|shop|trade|me|bonuscode|inventory|newcase|rr|give|donate|dick|top)'
    DELETE_DELAY_SECONDS = 30
    CHECK_INTERVAL_SECONDS = 10

__all__ = ['api_id', 'api_hash', 'BOT_IDS', 'COMMAND_PATTERN', 'DELETE_DELAY_SECONDS', 'CHECK_INTERVAL_SECONDS']
