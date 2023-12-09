import configparser
import logging
import time
from datetime import datetime, timedelta
from typing import List

import pandas as pd

from telethon import TelegramClient, errors, functions, types

channels_list = [
    "https://t.me/joinchat/RYlASrK1ZBj3CJVr",
    "https://t.me/smmbunker",
    "https://t.me/MarketingClubLviv",
    "https://t.me/ukraine_digital",
    "https://t.me/internationalrecruiting",
    "https://t.me/growyourupwork_chat",
    "https://t.me/targetologkontekstolog",
    "https://t.me/design_ukraine_chat",
    "https://t.me/Kukuruza_blog",
    "https://t.me/webdesign_ukraine",
    "https://t.me/real_targetolog",
    "https://t.me/graphic_designerisss_chat",
    "https://t.me/+jAP_w5E2PvI0NmRi",
    "https://t.me/flschat",
    "https://t.me/webflowuachat",
    "https://t.me/webflowcommunity",
    "https://t.me/marketing_job_ua",
    "https://t.me/design_ukraine_chat",
    "https://t.me/webdesign_ukraine",
    "https://t.me/target_pane",
    "https://t.me/chat_ppc_analytics"

]
own_private_channel = 'https://t.me/+0zCVd4XC_XFmMGNi'

keywords_list = [
    # Target keywords
    "шукаю таргетолога",
    "необхідний таргетолог",
    "таргетолог знайдись",
    "пошуках таргетолога",
    "вакансія таретолога",
    "налаштувати таргет",
    "налаштувати рекламу фейсбук",
    "налаштувати рекламу інстаграм",
    "налаштувати таргетовану рекламу",
    "налаштувати facebook ads",
    "налаштувати instagram ads",
    "налаштувати рекламу facebook",
    "налаштувати рекламу instagram",
    "спеціаліст таргетолог",
    "потрібен таргетолог",
    "потрібно налаштувати рекламу",
    "просування сторінки",
    "просування постів",
    "реклама постів",
    "порадьте таргетолога",
    "порекомендуйте таргетолога",
    # Google keywords
    "шукаю google",
    "шукаю гугл",
    "шукаю контекстолога",
    "необхідно налаштувати контекстну рекламу",
    "гугл спеціаліст знайдись",
    "google спеціаліст знайдись",
    "контекстолог знайдись",
    "пошуках контекстолога",
    "пошуках google спеціаліста",
    "налаштувати пошукову рекламу",
    "налаштувати КМС",
    "вакансія контекстолога"
    "вакансія google ads",
    "налаштувати google ads",
    "налаштувати гугл",
    "налаштувати рекламу гугл",
    "налаштувати рекламу google",
    "налаштувати контекстну рекламу",
    "спеціаліст з реклами",
    "спеціаліст google ads",
    "спеціаліст гугл",
    "потрібен контекстолог",
    "порадьте google",
    "порадьте контекстолога",
    # Designer keywords
    "шукаю дизайнера",
    "шукаю хто створить лого",
    "створити лого",
    "розробити лого",
    "розробити банер",
    "створити банер",
    "потрібен дизайнер",
    "дизайнер знайдись",
    "пошуках дизайнера",
    "вакансія дизайнера",
    "спеціаліст з дизайну",
    "банер для товарки",
    "банер для реклами",
    "потрібен банер",
    "потрібен креатив",
    "креатив для реклами",
    "креатив для товарки",
    "дизайнер відгукнися",
    "робота для дизайнера",
    "шукаю ux/ui",
    "моушн дизайнер",
    "3д дизайнер",
    "створити анімацію",
    "Motion дизайнер",
    "шукаю аніматора",
    "потрібен бренд бук",
    "потрібна айдентика",
    "шукаю айдентика",
    "необхідний айдентика",
    "айдентика знайдись",
    "пошуках айдентика",
    "вакансія айдентика",
    "спеціаліст з айдентика",
    "спеціаліст айдентика",
    "потрібен айдентика",
    "шукаю брендбук",
    "необхідний брендбук",
    "брендбук знайдись",
    "пошуках брендбук",
    "вакансія брендбук",
    "спеціаліст з брендбук",
    "спеціаліст брендбук",
    "потрібен брендбук",
    "порадьте дизайнера",
    "порадьте брендбук",
    # Copywriter
    "шукаю копірайтера",
    "шукаю пише тексти",
    "створити текст",
    "розробити текст",
    "потрібен копірайтер",
    "копірайтер знайдись",
    "пошуках копірайтера",
    "вакансія копірайтера",
    "спеціаліст з копірайту",
    "копірайт для товарки",
    "копірайт для реклами",
    "рекламний текст",
    "копірайтер відгукнися",
    "робота для копірайтера",
    # SMM keywords
    "шукаю смм",
    "шукаю SMM",
    "шукаю контент мейкера",
    "створення рілс",
    "створення reels",
    "потрібно створити контент",
    "контент стратегія",
    "контент для копанії",
    "відео для компанії",
    "потрібне відео",
    "створити смм",
    "розробити смм",
    "сторити smm",
    "розробити smm",
    "створити smm",
    "дизайнер smm",
    "пошуках smm",
    "вакансія smm",
    "спеціаліст smm",
    "smm для товарки",
    "потрібен smm",
    "smm знайдись",
    "smm відгукнися",
    "робота для smm",
    "дизайнер смм",
    "пошуках смм",
    "вакансія смм",
    "спеціаліст смм",
    "смм для товарки",
    "потрібен смм",
    "смм знайдись",
    "смм відгукнися",
    "робота для смм",
    "смм стратегія",
    "smm стратегія",
    "порадьте смм",
    "порадьте smm",
    # SEO keywords
    "шукаю seo",
    "шукаю сео",
    "необхідно налаштувати seo",
    "необхідно налаштувати сео",
    "сео спеціаліст знайдись",
    "seo спеціаліст знайдись",
    "сео знайдись",
    "seo знайдись",
    "пошуках seo",
    "пошук сео",
    "налаштувати сео",
    "налаштувати seo",
    "вакансія seo",
    "вакансія сео",
    "спеціаліст з сео",
    "спеціаліст з seo",
    "спеціаліст seo",
    "спеціаліст сео",
    "потрібен seo",
    "потрібно сео",
    "порадьте seo",
    "порадьте сео",
    # Marketing keywords
    "шукаю маркетолога",
    "необхідний маркетолог",
    "маркетолог знайдись",
    "пошуках маркетолога",
    "вакансія маркетолога",
    "спеціаліст з маркетингу",
    "спеціаліст маркетолог",
    "потрібен маркетолог",
    "спеціаліст маркетингу",
    "шукаю pr",
    "необхідний pr",
    "pr знайдись",
    "пошуках pr",
    "вакансія pr",
    "спеціаліст pr",
    "потрібен pr",
    "порадьте пр",
    "порадьте pr",
    "порадьте маркетолога",
    # Site keywords
    "шукаю дизайнера сайту",
    "необхідний дизайн сайт",
    "потрібно створити сайт",
    "необхідний створити сайт",
    "необхідно розробити сайт",
    "потрібно розробити сайт",
    "сайт знайдись",
    "пошуках сайт",
    "вакансія створення сайту",
    "налаштувати сайту",
    "спеціаліст з сайту",
    "потрібен сайт",
    "спеціаліст створення сайту",
    "шукаю wordpress",
    "необхідний wordpress",
    "wordpress знайдись",
    "пошуках wordpress",
    "вакансія wordpress",
    "спеціаліст з wordpress",
    "порадьте сайт",
    "порадьте wordpress",
    "порадьте вордпрес",
    "спеціаліст wordpress",
    "потрібен wordpress",
    "шукаю вордпрес",
    "необхідний вордпрес",
    "вордпрес знайдись",
    "пошуках вордпрес",
    "вакансія вордпрес",
    "спеціаліст вордпрес",
    "потрібен вордпрес",
    "необхідний webflow",
    "webflow знайдись",
    "пошуках webflow",
    "вакансія webflow",
    "спеціаліст з webflow",
    "спеціаліст webflow",
    "потрібен webflow",
    "шукаю веб",
    "необхідний веб",
    "пошуках веб",
    "вакансія веб",
    "спеціаліст веб",
    "потрібен веб",
    "порадьте webflow",
    # Arbitration keywords
    "шукаю арбітраж",
    "необхідний арбітраж",
    "арбітраж знайдись",
    "пошуках арбітраж",
    "вакансія арбітраж",
    "спеціаліст з арбітраж",
    "спеціаліст арбітраж",
    "потрібен арбітраж",
    # TikTok/chat bot keywords
    "шукаю TikTok",
    "необхідний TikTok",
    "TikTok знайдись",
    "пошуках TikTok",
    "вакансія TikTok",
    "спеціаліст з TikTok",
    "спеціаліст TikTok",
    "потрібен TikTok",
    "шукаю ТікТок",
    "необхідний ТікТок",
    "ТікТок знайдись",
    "пошуках ТікТок",
    "вакансія ТікТок",
    "порадьте ТікТок",
    "порадьте чат бот",
    "спеціаліст з ТікТок",
    "спеціаліст ТікТок",
    "потрібен ТікТок",
    "шукаю чат бот",
    "необхідний чат бот",
    "чат бот знайдись",
    "пошуках чат бот",
    "вакансія чат бот",
    "спеціаліст з чат бот",
    "спеціаліст чат бот",
    "потрібен чат бот",
]

MESSAGES_PER_REQUEST = 3000


async def search_text(client: TelegramClient, channels_list: list, keywords: List, output_channel: str):
    """
    Search text in channels list by keywords and send to the private channel

    :param client:          Telegram client instance
    :param channels_list    List with link to channels for search
    :param keywords:        List with keywords
    :param output_channel   Link to the Telegram channel to publish results

    :return:                None
    """
    message_data = []
    start_time = time.time()
    threshold_date = datetime.now() - timedelta(days=5)
    output_entity = await client.get_entity(output_channel)

    for channel in channels_list:
        try:
            channel_entity = await client.get_entity(channel)
        except ValueError as e:
            logging.error(f"Creating entity for {channel} caused an error: {e}")
            continue
        logging.info(f"Processing channel with username: {channel_entity.username}")
        input_channel_info = channel if channel_entity.username else channel_entity.id
        input_channel_name = channel_entity.title if not channel_entity.username else channel_entity.username
        logging.info(f"Retrieving input entity by data: {input_channel_info}")

        for keyword in keywords:
            try:
                input_entity = await client.get_input_entity(input_channel_info)
            except errors.FloodWaitError as e:
                logging.warning(f"FloodWaitError when parsing entity. Have to sleep {e.seconds} seconds")
                time.sleep(e.seconds)

            result = await client(functions.messages.SearchRequest(
                peer=input_entity,
                q=keyword,
                min_date=threshold_date,
                max_date=datetime.now(),
                filter=types.InputMessagesFilterEmpty(),
                offset_id=0,
                add_offset=0,
                limit=MESSAGES_PER_REQUEST,
                max_id=0,
                min_id=0,
                hash=0
            ))
            for message in result.messages:
                # Verify if found message is unique among all stored messages
                duplicated_message = any(viewed_message[-1] == message.message for viewed_message in message_data)
                if duplicated_message:
                    logging.debug(f"Skipped message with duplicated content {message.id}")
                    continue
                try:
                    sender = (await client.get_entity(message.from_id.user_id)).username
                except AttributeError as e:
                    logging.warning(f"Retrieving of sender caused an error {e}. "
                                    f"Chat = {input_channel_name} Key = {keyword} Date = {message.date}")
                    sender = None

                logging.info(f"Appending message from the chat: {input_channel_name} found by key: {keyword} "
                             f"with id {message.id}, date {message.date} and sender {sender}")
                message_data.append(
                    [message.id, input_channel_name, keyword, sender, message.date, message.message]
                )
                if not sender:
                    await client.forward_messages(output_entity, message)
                else:
                    await client.send_message(
                        entity=output_entity, message=f"{message.message}\n\nКонтакт @{sender}"
                    )
                time.sleep(20)

    df = pd.DataFrame(message_data, columns=['ID', 'Channel name', 'Keyword', 'Contact', 'Date', 'Text'])
    df['Date'] = df['Date'].apply(lambda a: pd.to_datetime(a).date())
    df.to_excel("results/data.xlsx")
    with open("results/data.xlsx", 'rb') as file:
        await client.send_file(output_entity, file)

    await client.send_message(
        output_entity, f"Overall time to collect all data in excel = {time.time()-start_time} seconds"
    )


# Reading Configs
config = configparser.ConfigParser()
config.read("config/config.ini")

# Setting configuration values
api_id = int(config['Telegram']['api_id'])
api_hash = str(config['Telegram']['api_hash'])
username = config['Telegram']['username']

logging.basicConfig(
    format='%(asctime)s %(levelname)s - %(name)s: %(filename)s: %(message)s',
    filename="results/logs.txt",
    level=logging.INFO
)

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
with client:
    client.loop.run_until_complete(search_text(client, channels_list, keywords_list, own_private_channel))
