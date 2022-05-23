import asyncio
from collections import deque

from userbot.plugins import catub, edit_or_reply

plugin_category = "fun"


@catub.cat_cmd(
    pattern="think$",
    command=("think", plugin_category),
    info={
        "header": "Думающая анимация",
        "usage": "{tr}think",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "think")
    deq = deque(list("🤔🧐🤔🧐🤔🧐"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="lmao$",
    command=("lmao", plugin_category),
    info={
        "header": "Смешная анимация",
        "usage": "{tr}lmao",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "lmao")
    deq = deque(list("😂🤣😂🤣😂🤣"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="nothappy$",
    command=("nothappy", plugin_category),
    info={
        "header": "Не смешная анимация",
        "usage": "{tr}nothappy",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "nathappy")
    deq = deque(list("😁☹️😁☹️😁☹️😁"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="clock$",
    command=("clock", plugin_category),
    info={
        "header": "Анимация часов",
        "usage": "{tr}clock",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "clock")
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="muah$",
    command=("muah", plugin_category),
    info={
        "header": "Анимация свиста",
        "usage": "{tr}muah",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "muah")
    deq = deque(list("😗😙😚😚😘"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="heart$",
    command=("heart", plugin_category),
    info={
        "header": "Анимация сердца",
        "usage": "{tr}heart",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "heart")
    deq = deque(list("❤️🧡💛💚💙💜🖤"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="gym$",
    command=("gym", plugin_category),
    info={
        "header": "Анимация зала",
        "usage": "{tr}gym",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "gym")
    deq = deque(list("🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="earth$",
    command=("earth", plugin_category),
    info={
        "header": "Анимация земли",
        "usage": "{tr}earth",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "earth")
    deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="moon$",
    command=("moon", plugin_category),
    info={
        "header": "Анимация луны",
        "usage": "{tr}moon",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "moon")
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    for _ in range(48):
        await asyncio.sleep(0.2)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="smoon$",
    command=("smoon", plugin_category),
    info={
        "header": "Анимация луны х2",
        "usage": "{tr}smoon",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "smoon")
    animation_interval = 0.2
    animation_ttl = range(101)
    await event.edit("smoon..")
    animation_chars = [
        "🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗",
        "🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘",
        "🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑",
        "🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒",
        "🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓\n🌗🌗🌗🌗🌗\n🌓🌓🌓🌓🌓",
        "🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔\n🌘🌘🌘🌘🌘\n🌔🌔🌔🌔🌔",
        "🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕\n🌑🌑🌑🌑🌑\n🌕🌕🌕🌕🌕",
        "🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖\n🌒🌒🌒🌒🌒\n🌖🌖🌖🌖🌖",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 8])


@catub.cat_cmd(
    pattern="tmoon$",
    command=("tmoon", plugin_category),
    info={
        "header": "Анимация луны х3",
        "usage": "{tr}tmoon",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "tmoon")
    animation_interval = 0.2
    animation_ttl = range(96)
    await event.edit("tmoon..")
    animation_chars = [
        "🌗",
        "🌘",
        "🌑",
        "🌒",
        "🌓",
        "🌔",
        "🌕",
        "🌖",
        "🌗",
        "🌘",
        "🌑",
        "🌒",
        "🌓",
        "🌔",
        "🌕",
        "🌖",
        "🌗",
        "🌘",
        "🌑",
        "🌒",
        "🌓",
        "🌔",
        "🌕",
        "🌖",
        "🌗",
        "🌘",
        "🌑",
        "🌒",
        "🌓",
        "🌔",
        "🌕",
        "🌖",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 32])
