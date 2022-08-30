import logging
from libraries import bot
from libraries import CONFIG
from libraries import log_handler


def main():
    with open("VERSION", "r") as version_file:
        print("Version:", version_file.readlines()[0])
    bot.run(CONFIG.DiscordToken, log_handler=log_handler, log_level=logging.DEBUG)


if __name__ == "__main__":
    main()
