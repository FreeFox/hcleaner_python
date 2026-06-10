import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from config import api_hash, api_id, BOT_IDS, COMMAND_PATTERN, DELETE_DELAY_SECONDS, CHECK_INTERVAL_SECONDS
import argparse
import asyncio
from periodic import Periodic
import db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--api_id", required=False, help="user api ID", type=str, default=api_id)
parser.add_argument("--api_hash", required=False, help="user api Hash", type=str, default=api_hash)

args = parser.parse_args()

db.init()
messages_to_delete = db.load_all()
log.info("Loaded %d pending message(s) from persistent queue", len(messages_to_delete))


async def periodically():
    if len(messages_to_delete):
        not_old_enough = []
        log.info("Queue size: %d item(s)", len(messages_to_delete))
        utcnow = datetime.utcnow()
        for msg in messages_to_delete:
            chat_id = msg['chat']
            message_id = msg['message']
            delta = utcnow - datetime.strptime(msg['date'], "%Y-%m-%d %H:%M:%S")
            if delta.total_seconds() > DELETE_DELAY_SECONDS:
                try:
                    await client.delete_messages(chat_id, message_id)
                    db.remove(message_id, chat_id)
                    log.info("Deleted message %d from chat %d", message_id, chat_id)
                except FloodWaitError as e:
                    log.warning("FloodWait: retrying in %ds, message %d requeued", e.seconds, message_id)
                    not_old_enough.append(msg)
                    await asyncio.sleep(e.seconds)
            else:
                not_old_enough.append(msg)
        messages_to_delete[:] = not_old_enough


async def main():
    p = Periodic(CHECK_INTERVAL_SECONDS, periodically)
    await p.start()


loop = asyncio.new_event_loop()
loop.create_task(main())
asyncio.set_event_loop(loop)
client = TelegramClient("sessions/Cleaner", args.api_id, args.api_hash, loop=loop)


@client.on(events.NewMessage(pattern=COMMAND_PATTERN))
async def user_command_handler(event):
    msg = {
        "message": event.message.id,
        "chat": event.chat_id,
        "date": event.message.date.strftime("%Y-%m-%d %H:%M:%S"),
    }
    db.add(msg["message"], msg["chat"], msg["date"])
    messages_to_delete.append(msg)
    log.info("[user command] Queue size: %d item(s)", len(messages_to_delete))


@client.on(events.NewMessage(from_users=BOT_IDS))
async def bot_message_handler(event):
    msg = {
        "message": event.message.id,
        "chat": event.chat_id,
        "date": event.message.date.strftime("%Y-%m-%d %H:%M:%S"),
    }
    db.add(msg["message"], msg["chat"], msg["date"])
    messages_to_delete.append(msg)
    log.info("[bot message] Queue size: %d item(s)", len(messages_to_delete))


# @client.on(events.NewMessage(pattern=r'(?si).*голос.*'))
# async def golos_handler(event):
#     await asyncio.sleep(1)
#     await event.reply("гав")
#     log.info("[golos] replied in chat %d", event.chat_id)


def run():
    while True:
        try:
            client.start()
            client.run_until_disconnected()
        except ConnectionError: #catches the ConnectionError and starts the connections process again
            log.error('ConnectionError. ХУЙ pУСНІ!')

run()
