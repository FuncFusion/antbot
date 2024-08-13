import discord
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv


load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

GUILD = 1270326885544493076

DMS_LOGS_GUILD_ID = 1204336106896752650

BOT_COMMANDS_CHANNEL_ID = 1270326886203133967
CREATIONS_FORUM_ID = 1270351447116218408
HELP_FORUM_ID = 1270351345714597888
GIVEAWAYS_CHANNEL_ID = 1270326886391746572
GIVEAWAYS_REQUESTS_CHANNEL_ID = 1270326887066898514
IDEAS_CHANNEL_ID = 1270326886203133968
JOINS_CHANNEL_ID = 1270326886022643719
LEAVES_CHANNEL_ID = 1270326886022643720
LOGS_CHANNEL_ID = 1270326887066898515
LOOK_FOR_CHANNEL_ID = 1270326886391746573
SNAPSHOTS_CHANNEL_ID = 1270326886203133966

VCS_CATEGORY_ID = 1270326886890868742
CREATE_VC_CHANNEL_ID = 1270326886890868744

SNAPSHOT_PING_ROLE = 1270326885544493084
DATAPACK_MASTER_ROLE = 1270326885686968324
RESOURCEPACK_MASTER_ROLE = 1270326885686968323

SOLVED_TAG = discord.ForumTag(name="Решено")
SOLVED_TAG.id=1270400825096929301
DATAPACKS_TAG = discord.ForumTag(name="datapack")
DATAPACKS_TAG.id = 1272928452164587562
RESOURCEPACKS_TAG = discord.ForumTag(name="resourcepacks")
RESOURCEPACKS_TAG.id = 1272928530962841671
BLOCKBENCH_TAG = discord.ForumTag(name="blockbench")
BLOCKBENCH_TAG.id = 1272928803252867153
OPTIFINE_TAG = discord.ForumTag(name="optifine")
OPTIFINE_TAG.id = 1272935395465756799
RESOURCEPACKS_TAGS = (RESOURCEPACKS_TAG, BLOCKBENCH_TAG, OPTIFINE_TAG)

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