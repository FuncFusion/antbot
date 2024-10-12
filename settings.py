import discord
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv


load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
GITHUB_HEADERS = {"Authorization": os.getenv("GITHUB_PAT")}

GUILD = 914772142300749854

DMS_LOGS_GUILD_ID = 1204336106896752650 
BOT_COMMANDS_CHANNEL_ID = 916788471480348743
CREATIONS_FORUM_ID = 1119942140705898667
HELP_FORUM_ID = 1020948396636389376
GIVEAWAYS_CHANNEL_ID = 923945448786501675
GIVEAWAYS_REQUESTS_CHANNEL_ID = 916725389458550805
IDEAS_CHANNEL_ID = 1276169141572730880
MEDIA_CHANNEL_ID = 1259458225997090910
FB_IDEAS_CHANNEL_ID = 1078066910933037106
JOINS_CHANNEL_ID = 916731552031969370
LEAVES_CHANNEL_ID = 916751412271153182
LOGS_CHANNEL_ID = 916753359304790066
LOOK_FOR_CHANNEL_ID = 941590548039483422
SNAPSHOTS_CHANNEL_ID = 1245321212582957160

VCS_CATEGORY_ID = 1284883106293223567
CREATE_VC_CHANNEL_ID = 1284883998711091271

SNAPSHOT_PING_ROLE = 1245322215428329503
DATAPACK_MASTER_ROLE = 924185371225497600
RESOURCEPACK_MASTER_ROLE = 940944701895356468

SOLVED_TAG = discord.ForumTag(name="solved")
SOLVED_TAG.id=1284875549247799328
DATAPACKS_TAG = discord.ForumTag(name="datapack")
DATAPACKS_TAG.id = 1026759908214968360
RESOURCEPACKS_TAG = discord.ForumTag(name="resourcepacks")
RESOURCEPACKS_TAG.id = 1026759958294954014
BLOCKBENCH_TAG = discord.ForumTag(name="blockbench")
BLOCKBENCH_TAG.id = 1026760450815295528
OPTIFINE_TAG = discord.ForumTag(name="optifine")
OPTIFINE_TAG.id = 1026760514895892580
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