import configparser
from telethon import TelegramClient

channels_list = [
    'https://t.me/ukraine_digital',
    'https://t.me/smmbunker',
    'https://t.me/growyourupwork_chat',
    'https://t.me/it_job_ua',
    'https://t.me/doubletop_chat'
]
own_private_channel = 'https://t.me/+0zCVd4XC_XFmMGNi'
keywords = "Україна"


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
            await client.send_message(
                entity=output_entity, message=f"{message}\nКонтакт: {(await message.get_sender()).username}")


async def main():
    # Reading Configs
    config = configparser.ConfigParser()
    config.read("config/config.ini")

    # Setting configuration values
    api_id = int(config['Telegram']['api_id'])
    api_hash = str(config['Telegram']['api_hash'])
    username = config['Telegram']['username']

    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash)
    await client.connect()

    await search_text(client, channels_list, keywords, own_private_channel)

    client.disconnect()

# TODO fix calling of the main event loop
if __name__ == '__main__':
    main()
