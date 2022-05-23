"""command: .hack & .thack """
# thx to @r4v4n4
import asyncio

from userbot import catub

from userbot.core.managers import edit_or_reply
from userbot.helpers.utils import _format
from userbot.plugins import ALIVE_NAME

plugin_category = "fun"


@catub.cat_cmd(
    pattern="hack$",
    command=("hack", plugin_category),
    info={
        "header": "Анимация Взлома.",
        "description": "Ответить на сообщение пользователя для анимации",
        "note": "Это просто анимация. Не взлом!.",
        "usage": "{tr}hack",
    },
)
async def _(event):
    "Fun hack animation."
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        idd = reply_message.sender_id
        if idd == 1035034432:
            await edit_or_reply(
                event, "Это мой владелец\nЯ не могу взломать своего владельца"
            )
        else:
            event = await edit_or_reply(event, "Взлом..")
            animation_chars = [
                "`Подключение к взломанному частному серверу...`",
                "`Цель выбрана.`",
                "`Взлом... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Взлом... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Взлом... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Взлом... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Взлом... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Взлом... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
                "`Взлом... 84%\n█████████████████████▒▒▒▒ `",
                "`Взлом... 100%\n█████████ВЗЛОМАНО███████████ `",
                f"`Целевая учетная запись взломана...\n\nОплатите 69$ ` {ALIVE_NAME} . ` чтобы удалить взлом..`",
            ]
            animation_interval = 3
            animation_ttl = range(11)
            for i in animation_ttl:
                await asyncio.sleep(animation_interval)
                await event.edit(animation_chars[i % 11])
    else:
        await edit_or_reply(
            event,
            "Юзер не найдем\n Не могу взломать",
            parse_mode=_format.parse_pre,
        )


@catub.cat_cmd(
    pattern="thack$",
    command=("thack", plugin_category),
    info={
        "header": "Анимация телеграм взлома.",
        "description": "Ответить на сообщение пользователя для анимации",
        "note": "Это просто анимация. Не взлом!",
        "usage": "{tr}thack",
    },
)
async def _(event):
    "Fun Telegram hack animation."
    animation_interval = 2
    animation_ttl = range(12)
    event = await edit_or_reply(event, "thack")
    animation_chars = [
        "**Подключение к центру обработки данных Telegram**",
        f"Цель выбрана хакером: {ALIVE_NAME}",
        "`Взлом... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)",
        "`Взлом... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package",
        "`Взлом... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)",
        "`Взлом... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'",
        "`Взлом... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e",
        "`Взлом... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b",
        "`Взлом... 84%\n█████████████████████▒▒▒▒ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b\n\n **Успешно взломана база данных сервера Telegram**",
        "`Взлом... 100%\n█████████ВЗЛОМАНО███████████ `\n\n\n  TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: /app/.cache/pip/wheels/a2/9f/b5/650dd4d533f0a17ca30cc11120b176643d27e0e1f5c9876b5b\n\n **Успешно взломана база данных сервера Telegram**\n\n\n🔹Вывод: Генерируется.....",
        f"`Целевая учетная запись взломана...\n\nОплатите 699$ ` {ALIVE_NAME} .`чтобы удалить взлом`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@catub.cat_cmd(
    pattern="wahack$",
    command=("wahack", plugin_category),
    info={
        "header": "Анимация ватсап взлома.",
        "description": "Ответить на сообщение пользователя для анимации",
        "note": "Это просто анимация. Не взлом.",
        "usage": "{tr}wahack",
    },
)
async def _(event):
    "Fun Whatsapp hack animation."
    animation_interval = 2
    animation_ttl = range(15)
    event = await edit_or_reply(event, "Взлом..")
    animation_chars = [
        "Ищем базы данных WhatsApp у целевого человека...",
        "Пользователь онлайн: True\nДоступ к телеграмму: True\nЧтение хранилища: True ",
        "Взлом... 0%\n[░░░░░░░░░░░░░░░░░░░░]\n`Ищу WhatsApp...`\nETA: 0m, 30s",
        "Взлом... 11.07%\n[██░░░░░░░░░░░░░░░░░░]\n`Ищу WhatsApp...`\nETA: 0m, 27s",
        "Взлом... 20.63%\n[███░░░░░░░░░░░░░░░░░]\n`Найдена папка C:/WhatsApp`\nETA: 0m, 24s",
        "Взлом... 34.42%\n[█████░░░░░░░░░░░░░░░]\n`Найдена папка C:/WhatsApp`\nETA: 0m, 21s",
        "Взлом... 42.17%\n[███████░░░░░░░░░░░░░]\n`Поиск баз данных`\nETA: 0m, 18s",
        "Взлом... 55.30%\n[█████████░░░░░░░░░░░]\n`Поиск msgstore.db.crypt12`\nETA: 0m, 15s",
        "Взлом... 64.86%\n[███████████░░░░░░░░░]\n`Поиск msgstore.db.crypt12`\nETA: 0m, 12s",
        "Взлом... 74.02%\n[█████████████░░░░░░░]\n`Попытка расшифровать...`\nETA: 0m, 09s",
        "Взлом... 86.21%\n[███████████████░░░░░]\n`Попытка расшифровать...`\nETA: 0m, 06s",
        "Взлом... 93.50%\n[█████████████████░░░]\n`Расшифровка прошла успешно!`\nETA: 0m, 03s",
        "Взлом... 100%\n[████████████████████]\n`Сканирование файла...`\nETA: 0m, 00s",
        "Взлом завершен!\nЗагрузка файла...",
        "Целевая учетная запись взломана...!\n\n ✅ Файл успешно загружен на мой сервер.\nБаза данных WhatsApp:\n`./DOWNLOADS/msgstore.db.crypt12`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 15])
