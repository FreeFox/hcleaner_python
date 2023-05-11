from datetime import datetime
from telethon import TelegramClient, events
from config import api_hash, api_id
import argparse
import asyncio
from periodic import Periodic


parser = argparse.ArgumentParser()
parser.add_argument("--api_id", required=False, help="user api ID", type=str, default=api_id)
parser.add_argument("--api_hash", required=False, help="user api Hash", type=str, default=api_hash)

args = parser.parse_args()
messages_to_delete = []


async def periodically():
    if len(messages_to_delete):
        not_old_enough = []
        print("queue size: ", str(len(messages_to_delete)), " item(s)")
        utcnow = datetime.utcnow()
        for msg in messages_to_delete:
            chat_id = msg['chat']
            message_id = msg['message']
            delta = utcnow - datetime.strptime(msg['date'], "%Y-%m-%d %H:%M:%S")
            if delta.seconds > 30:
                await client.delete_messages(chat_id, message_id)
                print(datetime.now(), 'Done!')
            else:
                not_old_enough.append(msg)
        messages_to_delete.clear()
        messages_to_delete.extend(not_old_enough)


async def main():
    p = Periodic(10, periodically)
    await p.start()


loop = asyncio.new_event_loop()
loop.create_task(main())
asyncio.set_event_loop(loop)
client = TelegramClient("Cleaner", args.api_id, args.api_hash, loop=loop)


@client.on(events.NewMessage(pattern=r'(?i)^\/(achievements|drochnut|topd|topdall|topdd|help|dice|craft|case|use|keys|shop|trade|me|bonuscode|inventory|newcase|rr|give|donate|dick|top)'))
async def user_command_handler(event):
    messages_to_delete.append({
        "message": event.message.id,
        "chat": event.chat.id,
        "date": event.message.date.strftime("%Y-%m-%d %H:%M:%S")
    })
    print("[New event] Queue size: ", str(len(messages_to_delete)), " item(s)")


@client.on(events.NewMessage(from_users=[1303228016,539991741]))
async def bot_message_handler(event):
    messages_to_delete.append({
        "message": event.message.id,
        "chat": event.chat.id,
        "date": event.message.date.strftime("%Y-%m-%d %H:%M:%S")
    })
    print("[New event] Queue size: ", str(len(messages_to_delete)), " item(s)")


def test():
    try:
        client.start()
        client.run_until_disconnected()
    except ConnectionError: #catches the ConnectionError and starts the connections process again
        print('ConnectionError. ХУЙ pУСНІ!')
        test()

test()
