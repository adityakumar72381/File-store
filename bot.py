import sys
import glob
import importlib
from pathlib import Path
import logging
import logging.config
import asyncio
from datetime import date, datetime
import pytz

from pyrogram import idle
from config import LOG_CHANNEL, CLONE_MODE
from Script import script
from plugins.clone import restart_bots
from TechVJ.bot import StreamBot
from TechVJ.bot.clients import initialize_clients

# Logging configuration
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# Load all plugins
ppath = "plugins/*.py"
files = glob.glob(ppath)

# Start main bot client
StreamBot.start()
loop = asyncio.get_event_loop()


async def start():
    print("\nInitializing Bot...")

    # Basic bot info
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username

    # Initialize multi-clients if enabled
    await initialize_clients()

    # Load plugins dynamically
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = f"plugins.{plugin_name}"

            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            sys.modules[import_path] = module
            print(f"Imported plugin => {plugin_name}")

    # Send restart message to log channel
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")

    await StreamBot.send_message(
        chat_id=LOG_CHANNEL,
        text=script.RESTART_TXT.format(today, time)
    )

    # Clone mode support
    if CLONE_MODE is True:
        await restart_bots()

    print("Bot Started Successfully on VPS!")
    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info("Service Stopped Bye 👋")
