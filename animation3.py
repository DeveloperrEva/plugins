import asyncio
from collections import deque

from userbot.plugins import catub, edit_delete, edit_or_reply, mention

plugin_category = "fun"


@catub.cat_cmd(
    pattern="star$",
    command=("star", plugin_category),
    info={
        "header": "Анимация звезд",
        "usage": "{tr}star",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "`Звездочки.....`")
    deq = deque(list("🦋✨🦋✨🦋✨🦋✨"))
    for _ in range(48):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="boxs$",
    command=("boxs", plugin_category),
    info={
        "header": "Анимация коробок",
        "usage": "{tr}boxs",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "`Коробки...`")
    deq = deque(list("🟥🟧🟨🟩🟦🟪🟫⬛⬜"))
    for _ in range(999):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="rain$",
    command=("rain", plugin_category),
    info={
        "header": "Анимация дождя",
        "usage": "{tr}rain",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "`Дождь.......`")
    deq = deque(list("🌬☁️🌩🌨🌧🌦🌥⛅🌤"))
    for _ in range(48):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)


@catub.cat_cmd(
    pattern="deploy$",
    command=("deploy", plugin_category),
    info={
        "header": "Анимация деплоя",
        "usage": "{tr}deploy",
    },
)
async def _(event):
    "animation command"
    animation_interval = 3
    animation_ttl = range(12)
    event = await edit_or_reply(event, "`Deploying...`")
    animation_chars = [
        "**Heroku подключается к последней сборке Github **",
        f"**Сборка запущена пользователем** {mention}",
        f"**Деплой** `535a74f0` **пользователем** {mention}",
        "**Перезапуск сервера Heroku...**",
        "**Состояние изменено с до на начальное**",
        "**Остановка всех процессов с помощью SIGTERM**",
        "**Процесс завершен с** `status 143`",
        "**Запуск процесса командой** `python3 -m userbot`",
        "**Состояние изменено с запуска на вверх**",
        "__INFO:Userbot:Logged in as 557667062__",
        "__INFO:Userbot:Successfully loaded all plugins__",
        "**Сборка выполнена успешно**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 12])


@catub.cat_cmd(
    pattern="dump(?:\s|$)([\s\S]*)",
    command=("dump", plugin_category),
    info={
        "header": "Анимация дампа",
        "usage": "{tr}dump <any three emoji's(optional)>",
        "examples": ["{tr}dump", "{tr}dump 🍰🍎🐓"],
    },
)
async def _(event):
    "Animation Command"
    try:
        obj = event.pattern_match.group(1)
        if len(obj) != 3:
            return await edit_delete(event, "`Длина ввода должна быть 3 или пуста.`")
        inp = " ".join(obj)
    except IndexError:
        inp = "🥞 🎂 🍫"
    event = await edit_or_reply(event, "`Сброс....`")
    u, t, g, o, s, n = inp.split(), "🗑", "<(^_^ <)", "(> ^_^)>", "⠀ ", "\n"
    h = [(u[0], u[1], u[2]), (u[0], u[1], ""), (u[0], "", "")]
    for something in reversed(
        [
            [
                "".join(x)
                for x in (
                    f + (s, g, s + s * f.count(""), t),
                    f + (g, s * 2 + s * f.count(""), t),
                    f[:i] + (o, f[i], s * 2 + s * f.count(""), t),
                    f[:i] + (s + s * f.count(""), o, f[i], s, t),
                    f[:i] + (s * 2 + s * f.count(""), o, f[i], t),
                    f[:i] + (s * 3 + s * f.count(""), o, t),
                    f[:i] + (s * 3 + s * f.count(""), g, t),
                )
            ]
            for i, f in enumerate(reversed(h))
        ]
    ):
        for something_else in something:
            await asyncio.sleep(0.3)
            await event.edit(something_else)


@catub.cat_cmd(
    pattern="fleaveme$",
    command=("fleaveme", plugin_category),
    info={
        "header": "Анимация расставания",
        "usage": "{tr}fleaveme",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(10)
    animation_chars = [
        "⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛",
        "⬛⬛⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬇️↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n↙️⬇️↘️",
        "⬛⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
        "↖️⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
    ]
    event = await edit_or_reply(event, "Брось меня....")
    await asyncio.sleep(2)
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 10])


@catub.cat_cmd(
    pattern="loveu$",
    command=("loveu", plugin_category),
    info={
        "header": "Анимация любви",
        "usage": "{tr}loveu",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.5
    animation_ttl = range(70)
    event = await edit_or_reply(event, "loveu")
    animation_chars = [
        "😀",
        "👩‍🎨",
        "😁",
        "😂",
        "🤣",
        "😃",
        "😄",
        "😅",
        "😊",
        "☺",
        "🙂",
        "🤔",
        "🤨",
        "😐",
        "😑",
        "😶",
        "😣",
        "😥",
        "😮",
        "🤐",
        "😯",
        "😴",
        "😔",
        "😕",
        "☹",
        "🙁",
        "😖",
        "😞",
        "😟",
        "😢",
        "😭",
        "🤯",
        "💔",
        "❤",
        "Я люблю тебя❤",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 35])


@catub.cat_cmd(
    pattern="plane$",
    command=("plane", plugin_category),
    info={
        "header": "Анимация самолета",
        "usage": "{tr}plane",
    },
)
async def _(event):
    "animation command"
    event = await edit_or_reply(event, "Ожидайте самолет...")
    await event.edit("✈-------------")
    await event.edit("-✈------------")
    await event.edit("--✈-----------")
    await event.edit("---✈----------")
    await event.edit("----✈---------")
    await event.edit("-----✈--------")
    await event.edit("------✈-------")
    await event.edit("-------✈------")
    await event.edit("--------✈-----")
    await event.edit("---------✈----")
    await event.edit("----------✈---")
    await event.edit("-----------✈--")
    await event.edit("------------✈-")
    await event.edit("-------------✈")
    await asyncio.sleep(3)


@catub.cat_cmd(
    pattern="police$",
    command=("police", plugin_category),
    info={
        "header": "Анимация полиции",
        "usage": "{tr}police",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.3
    animation_ttl = range(12)
    event = await edit_or_reply(event, "Police")
    animation_chars = [
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        "🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴\n🔵🔵🔵⬜⬜⬜🔴🔴🔴",
        "🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵\n🔴🔴🔴⬜⬜⬜🔵🔵🔵",
        f"{mention} **Полиция здесь**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 12])


@catub.cat_cmd(
    pattern="jio$",
    command=("jio", plugin_category),
    info={
        "header": "Анимация JIO",
        "usage": "{tr}jio",
    },
)
async def _(event):
    "animation command"
    animation_interval = 1
    animation_ttl = range(19)
    event = await edit_or_reply(event, "jio сеть буститься...")
    animation_chars = [
        "`Подключение к JIO сети ....`",
        "`█ ▇ ▆ ▅ ▄ ▂ ▁`",
        "`▒ ▇ ▆ ▅ ▄ ▂ ▁`",
        "`▒ ▒ ▆ ▅ ▄ ▂ ▁`",
        "`▒ ▒ ▒ ▅ ▄ ▂ ▁`",
        "`▒ ▒ ▒ ▒ ▄ ▂ ▁`",
        "`▒ ▒ ▒ ▒ ▒ ▂ ▁`",
        "`▒ ▒ ▒ ▒ ▒ ▒ ▁`",
        "`▒ ▒ ▒ ▒ ▒ ▒ ▒`",
        "*Оптимизация JIO Сети...*",
        "`▒ ▒ ▒ ▒ ▒ ▒ ▒`",
        "`▁ ▒ ▒ ▒ ▒ ▒ ▒`",
        "`▁ ▂ ▒ ▒ ▒ ▒ ▒`",
        "`▁ ▂ ▄ ▒ ▒ ▒ ▒`",
        "`▁ ▂ ▄ ▅ ▒ ▒ ▒`",
        "`▁ ▂ ▄ ▅ ▆ ▒ ▒`",
        "`▁ ▂ ▄ ▅ ▆ ▇ ▒`",
        "`▁ ▂ ▄ ▅ ▆ ▇ █`",
        "**JIO сеть забущена....**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 19])


@catub.cat_cmd(
    pattern="solarsystem$",
    command=("solarsystem", plugin_category),
    info={
        "header": "Анимация вращение солнца",
        "usage": "{tr}solarsystem",
    },
)
async def _(event):
    "animation command"
    animation_interval = 0.1
    animation_ttl = range(80)
    event = await edit_or_reply(event, "solarsystem")
    animation_chars = [
        "`◼️◼️◼️◼️◼️\n◼️◼️◼️◼️☀\n◼️◼️🌎◼️◼️\n🌕◼️◼️◼️◼️\n◼️◼️◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n🌕◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️☀\n◼️◼️◼️◼️◼️`",
        "`◼️🌕◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️☀◼️`",
        "`◼️◼️◼️🌕◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️☀◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n◼️◼️◼️◼️🌕\n◼️◼️🌎◼️◼️\n☀◼️◼️◼️◼️\n◼️◼️◼️◼️◼️`",
        "`◼️◼️◼️◼️◼️\n☀◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️🌕\n◼️◼️◼️◼️◼️`",
        "`◼️☀◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️🌕◼️`",
        "`◼️◼️◼️☀◼️\n◼️◼️◼️◼️◼️\n◼️◼️🌎◼️◼️\n◼️◼️◼️◼️◼️\n◼️🌕◼️◼️◼️`",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 8])
