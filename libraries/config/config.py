import os


class CONFIG:
    DiscordToken = os.getenv("DISCORD_TOKEN")
    BodlanServerID = os.getenv("BodlanServerID")
    TestChannelID = os.getenv("TestChannelID")
    filename = os.path.join("logs", "discord.log")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if not os.path.isfile(os.path.join("logs", "discord.log")):
        try:
            open(filename, "a").close()
        except OSError:
            print("Failed create a discord logs")
        else:
            print("Logs created!")
    DiscordLogs = os.path.join("logs", "discord.log")

    class Emoji:
        TrollDespair = "<:TrollDespair:919338162331992174>"
        ThumbUp = "👍"
        One = "1️⃣"
        Two = "2️⃣"
        Three = "3️⃣"
        Four = "4️⃣"
        Five = "5️⃣"
        bet_list = [One, Two, Three, Four, Five]
        Based = "<:BASED:919339730863280188>"
        Okayge = "<:Okayge:919334781240623106>"

    class Database:
        Password = os.getenv("db_password")
        Login = os.getenv("db_login")
