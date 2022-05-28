from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _catutils, parse_pre, yaml_format

plugin_category = "tools"


@catub.cat_cmd(
    pattern="suicide$",
    command=("suicide", plugin_category),
    info={
        "header": "Удаляет все файлы и папки в текущем каталоге.",
        "usage": "{tr}suicide",
    },
)
async def _(event):
    "To delete all files and folders in userbot"
    cmd = "rm -rf .*"
    await _catutils.runcmd(cmd)
    OUTPUT = "**БОМБА САМОУБИЙСТВА:**\nуспешно удалил все папки и файлы на сервере юзербота"

    event = await edit_or_reply(event, OUTPUT)


@catub.cat_cmd(
    pattern="plugins$",
    command=("plugins", plugin_category),
    info={
        "header": "Чтобы перечислить все плагины в пользовательском боте.",
        "usage": "{tr}plugins",
    },
)
async def _(event):
    "To list all plugins in userbot"
    cmd = "ls userbot/plugins"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = f"**[Cat's](tg://need_update_for_some_feature/) Плагины:**\n{o}"
    await edit_or_reply(event, OUTPUT)


@catub.cat_cmd(
    pattern="env$",
    command=("env", plugin_category),
    info={
        "header": "Чтобы перечислить все значения среды в пользовательском боте.",
        "description": "Чтобы показать все значения vars / config heroku в вашем пользовательском боте",
        "usage": "{tr}env",
    },
)
async def _(event):
    "To show all config values in userbot"
    cmd = "env"
    o = (await _catutils.runcmd(cmd))[0]
    OUTPUT = (
        f"**[Cat's](tg://need_update_for_some_feature/) Модуль окружающей среды:**\n\n\n{o}"
    )
    await edit_or_reply(event, OUTPUT)


@catub.cat_cmd(
    pattern="noformat$",
    command=("noformat", plugin_category),
    info={
        "header": "Чтобы получить ответное сообщение без форматирования уценки.",
        "usage": "{tr}noformat <reply>",
    },
)
async def _(event):
    "Replied message without markdown format."
    reply = await event.get_reply_message()
    if not reply or not reply.text:
        return await edit_delete(
            event, "__Ответьте на текстовое сообщение, чтобы получить текст без форматирования уценки.__"
        )
    await edit_or_reply(event, reply.text, parse_mode=parse_pre)


@catub.cat_cmd(
    pattern="when$",
    command=("when", plugin_category),
    info={
        "header": "Чтобы получить дату и время сообщения при его публикации.",
        "usage": "{tr}when <reply>",
    },
)
async def _(event):
    "To get date and time of message when it posted."
    reply = await event.get_reply_message()
    if reply:
        try:
            result = reply.fwd_from.date
        except Exception:
            result = reply.date
    else:
        result = event.date
    await edit_or_reply(
        event, f"**Это сообщение было размещено на :** `{yaml_format(result)}`"
    )
