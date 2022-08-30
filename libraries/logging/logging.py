import logging
from libraries import CONFIG

log_handler = logging.FileHandler(filename=CONFIG.DiscordLogs, encoding="utf-8", mode="w")
