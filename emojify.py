"""
Created by @Jisan7509
modified by  @mrconfused
Userbot plugin for CatUserbot
"""

from userbot import catub

from userbot.core.managers import edit_or_reply
from userbot.helpers import fonts as emojify

plugin_category = "fun"


@catub.cat_cmd(
    pattern="emoji(?:\s|$)([\s\S]*)",
    command=("emoji", plugin_category),
    info={
        "header": "Преобразует ваш текст в большой текст эмодзи с некоторыми эмодзи по умолчанию..",
        "usage": "{tr}emoji <text>",
        "examples": ["{tr}emoji userbot"],
    },
)
async def itachi(event):
    "To get emoji art text."
    args = event.pattern_match.group(1)
    get = await event.get_reply_message()
    if not args and get:
        args = get.text
    if not args:
        await edit_or_reply(
            event, "Что мне делать с этим идиотом, дай мне текст.__"
        )
        return
    result = ""
    for a in args:
        a = a.lower()
        if a in emojify.kakashitext:
            char = emojify.kakashiemoji[emojify.kakashitext.index(a)]
            result += char
        else:
            result += a
    await edit_or_reply(event, result)


@catub.cat_cmd(
    pattern="cmoji(?:\s|$)([\s\S]*)",
    command=("cmoji", plugin_category),
    info={
        "header": "Преобразует ваш текст в большой текст смайликов с вашими собственными смайликами..",
        "usage": "{tr}cmoji <emoji> <text>",
        "examples": ["{tr}cmoji 😺 userbot"],
    },
)
async def itachi(event):
    "To get custom emoji art text."
    args = event.pattern_match.group(1)
    get = await event.get_reply_message()
    if not args and get:
        args = get.text
    if not args:
        return await edit_or_reply(
            event, "__Что мне делать с этим идиотом, дай мне текст.__"
        )
    try:
        emoji, arg = args.split(" ", 1)
    except Exception:
        arg = args
        emoji = "😺"
    result = ""
    for a in arg:
        a = a.lower()
        if a in emojify.kakashitext:
            char = emojify.itachiemoji[emojify.kakashitext.index(a)].format(cj=emoji)
            result += char
        else:
            result += a
    await edit_or_reply(event, result)
