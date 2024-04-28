import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv


load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

HELP_FORUM_ID = 1169322456125800498
CREATIONS_FROUM_ID = 1169322456125800498
IDEAS_CHANNEL_ID = 1125102361942183987
LOGS_CHANNEL_ID = 1125102361942183987
DMS_LOGS_GUILD_ID = 1204336106896752650
LOOK_FOR_ID = 1125102361942183987

VCS_CATEGORY_ID = 1097272593356165234
CREATE_VC_CHANNEL_ID = 1097272593838514352

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)