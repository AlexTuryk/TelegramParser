import configparser
import logging
import time

from telethon import TelegramClient, errors

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
channels_list = [
    'https://t.me/ukraine_digital',
    'https://t.me/smmbunker',
    'https://t.me/growyourupwork_chat',
    'https://t.me/it_job_ua',
    'https://t.me/doubletop_chat'
]
own_private_channel = 'https://t.me/+0zCVd4XC_XFmMGNi'
keywords = "Шукаємо"


async def search_text(client: TelegramClient, channels_list: list, keywords: str, output_channel: str):
    """
    Search text in channels list by keywords and send to the private channel

    :param client:          Telegram client instance
    :param channels_list    List with link to channels for search
    :param keywords:        List with keywords
    :param output_channel   Link to the Telegram channel to publish results

    :return:                None
    """
    output_entity = await client.get_entity(output_channel)
    for channel in channels_list:
        channel_entity = await client.get_entity(channel)
        async for message in client.iter_messages(channel_entity, search=keywords):
            # TODO Telegram throws FloodWaitError which gets ~270 seconds to send 25-40 messages
            #  in order to speed up message parsing the process should be optimized
            try:
                await client.send_message(
                    entity=output_entity, message=f"{message.message}\n\nКонтакт: @{(await message.get_sender()).username}")
            except errors.FloodWaitError as e:
                print('Have to sleep', e.seconds, 'seconds')
                time.sleep(e.seconds)

# Reading Configs
config = configparser.ConfigParser()
config.read("config/config.ini")

# Setting configuration values
api_id = int(config['Telegram']['api_id'])
api_hash = str(config['Telegram']['api_hash'])
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
with client:
    client.loop.run_until_complete(search_text(client, channels_list, keywords, own_private_channel))
