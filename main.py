import asyncio
from app.bot import bot
from app.player import player
from app import config  # load settings

# Register handlers
import app.handlers.basic  # noqa
import app.handlers.play   # noqa

async def run():
    await player.start()
    await bot.start()
    print("Prenses Music Bot started.")
    await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        pass
