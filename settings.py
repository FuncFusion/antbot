import discord
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv


load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

GUILD = 1097272592676700250

DMS_LOGS_GUILD_ID = 1204336106896752650

BOT_COMMANDS_CHANNEL_ID = 1125102361942183987
CREATIONS_FROUM_ID = 1169322456125800498
HELP_FORUM_ID = 1169322456125800498
GIVEAWAYS_CHANNEL_ID = 1125102361942183987
GIVEAWAYS_REQUESTS_CHANNEL_ID = 1125102361942183987
IDEAS_CHANNEL_ID = 1125102361942183987
JOINS_CHANNEL_ID = 1125102361942183987
LEAVES_CHANNEL_ID = 1125102361942183987
LOGS_CHANNEL_ID = 1247124509513879626
LOOK_FOR_CHANNEL_ID = 1125102361942183987
SNAPSHOTS_CHANNEL_ID = 1125102361942183987

VCS_CATEGORY_ID = 1097272593356165234
CREATE_VC_CHANNEL_ID = 1097272593838514352

SNAPSHOT_PING_ROLE = 1262328810779443270

SOLVED_TAG = discord.ForumTag(name="решен")
SOLVED_TAG.id=1269643259609612319

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