import asyncio
from random import choice, randint

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import get_user_from_event
from . import ALIVE_NAME

plugin_category = "fun"


@catub.cat_cmd(
    pattern="scam(?:\s|$)([\s\S]*)",
    command=("scam", plugin_category),
    info={
        "header": "Чтобы показать поддельные действия за определенный период времени",
        "description": "Если время не указано, то он может выбрать случайное время 5 или 6 минут для упоминания использования времени в секундах.",
        "usage": [
            "{tr}scam <action> <time(in seconds)>",
            "{tr}scam <action>",
            "{tr}scam",
        ],
        "examples": "{tr}scam photo 300",
        "actions": [
            "typing",
            "contact",
            "game",
            "location",
            "voice",
            "round",
            "video",
            "photo",
            "document",
        ],
    },
)
async def _(event):
    options = [
        "typing",
        "contact",
        "game",
        "location",
        "voice",
        "round",
        "video",
        "photo",
        "document",
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:
        scam_action = choice(options)
        scam_time = randint(300, 360)
    elif len(args) == 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(300, 360)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:
        try:
            scam_action = str(args[0]).lower()
            scam_time = int(args[1])
        except ValueError:
            return await edit_delete(event, "`Invalid Syntax !!`")
    else:
        return await edit_delete(event, "`Invalid Syntax !!`")
    try:
        if scam_time > 0:
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await asyncio.sleep(scam_time)
    except BaseException:
        return


@catub.cat_cmd(
    pattern="prankpromote(?:\s|$)([\s\S]*)",
    command=("prankpromote", plugin_category),
    info={
        "header": "Продвигать человека без прав администратора",
        "note": "Вам нужны соответствующие права для этого",
        "usage": [
            "{tr}prankpromote <userid/username/reply>",
            "{tr}prankpromote <userid/username/reply> <custom title>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _(event):
    "To promote a person without admin rights"
    new_rights = ChatAdminRights(post_messages=True)
    catevent = await edit_or_reply(event, "`Продвижение...`")
    user, rank = await get_user_from_event(event, catevent)
    if not rank:
        rank = "Admin"
    if not user:
        return
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit("__Я думаю, у вас нет разрешения на рекламу__")
    except Exception as e:
        return await edit_delete(catevent, f"__{e}__", time=10)
    await catevent.edit("`Promoted Successfully! Now gib Party`")


@catub.cat_cmd(
    pattern="padmin$",
    command=("padmin", plugin_category),
    info={
        "header": "Забавная анимация для имитации продвижения пользователя",
        "description": "Анимация, показывающая включение всех разрешений для него, что он является администратором (поддельное продвижение)",
        "usage": "{tr}padmin",
    },
    groups_only=True,
)
async def _(event):
    "Fun animation for faking user promotion."
    animation_interval = 1
    animation_ttl = range(20)
    event = await edit_or_reply(event, "`Продвижение.......`")
    animation_chars = [
        "**Продвижение пользователя в качестве администратора...**",
        "**Включение всех разрешений для пользователя...**",
        "**(1) Отправить сообщения: ☑️**",
        "**(1) Отправить сообщения: ✅**",
        "**(2) Отправить медиа: ☑️**",
        "**(2) Отправить медиа: ✅**",
        "**(3) Отправить стикеры и GIF-файлы: ☑️**",
        "**(3) Отправить стикеры и GIF-файлы: ✅**",
        "**(4) Отправить опросы: ☑️**",
        "**(4) Отправить опросы: ✅**",
        "**(5) Вставить ссылки: ☑️**",
        "**(5) Вставить ссылки: ✅**",
        "**(6) Добавить пользователей: ☑️**",
        "**(6) Добавить пользователей: ✅**",
        "**(7) Закрепить сообщения: ☑️**",
        "**(7) Закрепить сообщения: ✅**",
        "**(8) Изменить информацию о чате: ☑️**",
        "**(8) Изменить информацию о чате: ✅**",
        "**Разрешение предоставлено успешно**",
        f"**УСПЕШНО ПРОДВИГАЕТСЯ: {ALIVE_NAME}**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 20])
