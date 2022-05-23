from telethon import functions

from userbot import catub

from ..Config import Config
from ..core import CMD_INFO, GRP_INFO, PLG_INFO
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

cmdprefix = Config.COMMAND_HAND_LER
BADCAT = Config.BADCAT

plugin_category = "tools"

hemojis = {
    "admin": "👮‍♂️",
    "bot": "🤖",
    "fun": "🎨",
    "misc": "🧩",
    "tools": "🧰",
    "utils": "🗂",
    "extra": "➕",
    "useless": "⚰️",
}


def get_key(val):
    for key, value in PLG_INFO.items():
        for cmd in value:
            if val == cmd:
                return key
    return None


def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None


async def cmdinfo(input_str, event, plugin=False):
    if input_str[0] == cmdprefix:
        input_str = input_str[1:]
    try:
        about = CMD_INFO[input_str]
    except KeyError:
        if plugin:
            await edit_delete(
                event,
                f"**Нет плагина или команды, как **`{input_str}`** в моем боте.**",
            )
            return None
        await edit_delete(
            event, f"**Нет плагина или команды, как **`{input_str}`** в моем боте.**"
        )
        return None
    except Exception as e:
        await edit_delete(event, f"**Ошибка**\n`{e}`")
        return None
    outstr = f"**Команда :** `{cmdprefix}{input_str}`\n"
    plugin = get_key(input_str)
    if plugin is not None:
        outstr += f"**Плагин :** `{plugin}`\n"
        category = getkey(plugin)
        if category is not None:
            outstr += f"**Категория :** `{category}`\n\n"
    outstr += f"**✘  Вступление :**\n{about[0]}"
    return outstr


async def plugininfo(input_str, event, flag):
    try:
        cmds = PLG_INFO[input_str]
    except KeyError:
        outstr = await cmdinfo(input_str, event, plugin=True)
        return outstr
    except Exception as e:
        await edit_delete(event, f"**Ошибка**\n`{e}`")
        return None
    if len(cmds) == 1 and (flag is None or (flag and flag != "-p")):
        outstr = await cmdinfo(cmds[0], event, plugin=False)
        return outstr
    outstr = f"**Плагин : **`{input_str}`\n"
    outstr += f"**Доступные команды :** `{len(cmds)}`\n"
    category = getkey(input_str)
    if category is not None:
        outstr += f"**Категория :** `{category}`\n\n"
    for cmd in sorted(cmds):
        outstr += f"•  **cmd :** `{cmdprefix}{cmd}`\n"
        try:
            outstr += f"•  **Инфо :** `{CMD_INFO[cmd][1]}`\n\n"
        except IndexError:
            outstr += "•  **Инфо :** `None`\n\n"
    outstr += f"**👩‍💻 Использовать : ** `{cmdprefix}help <command name>`\
        \n**Note : **Если имя команды совпадает с именем плагина, используйте это `{cmdprefix}help -c <command name>`."
    return outstr


async def grpinfo():
    outstr = "**Плагины:**\n\n"
    outstr += f"**👩‍💻 Использовать : ** `{cmdprefix}help <plugin name>`\n\n"
    category = ["admin", "bot", "fun", "misc", "tools", "utils", "extra"]
    if BADCAT:
        category.append("useless")
    for cat in category:
        plugins = GRP_INFO[cat]
        outstr += f"**{hemojis[cat]} {cat.title()} **({len(plugins)})\n"
        for plugin in plugins:
            outstr += f"`{plugin}`  "
        outstr += "\n\n"
    return outstr


async def cmdlist():
    outstr = "**Общий список команд: :**\n\n"
    category = ["admin", "bot", "fun", "misc", "tools", "utils", "extra"]
    if BADCAT:
        category.append("useless")
    for cat in category:
        plugins = GRP_INFO[cat]
        outstr += f"**{hemojis[cat]} {cat.title()} ** - {len(plugins)}\n\n"
        for plugin in plugins:
            cmds = PLG_INFO[plugin]
            outstr += f"• **{plugin.title()} has {len(cmds)} commands**\n"
            for cmd in sorted(cmds):
                outstr += f"  - `{cmdprefix}{cmd}`\n"
            outstr += "\n"
    outstr += f"**👩‍💻 Использовать : ** `{cmdprefix}help -c <command name>`"
    return outstr


@catub.cat_cmd(
    pattern="help ?(-c|-p|-t)? ?([\s\S]*)?",
    command=("help", plugin_category),
    info={
        "header": "Чтобы получить руководство.",
        "description": "Чтобы получить информацию или руководство по команде или плагину",
        "note": "Если имя команды и имя плагина совпадают, вы получите руководство для плагина. Итак, используя этот флаг, вы получаете руководство по командам",
        "flags": {
            "c": "Чтобы получить информацию о команде.",
            "p": "Чтобы получить информацию о плагине.",
            "t": "Чтобы получить все плагины в текстовом формате.",
        },
        "usage": [
            "{tr}help (plugin/command name)",
            "{tr}help -c (command name)",
        ],
        "examples": ["{tr}help help", "{tr}help -c help"],
    },
)
async def _(event):
    "To get guide for catuserbot."
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if flag and flag == "-c" and input_str:
        outstr = await cmdinfo(input_str, event)
        if outstr is None:
            return
    elif input_str:
        outstr = await plugininfo(input_str, event, flag)
        if outstr is None:
            return
    elif flag == "-t":
        outstr = await grpinfo()
    else:
        results = await event.client.inline_query(Config.TG_BOT_USERNAME, "help")
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()
        return
    await edit_or_reply(event, outstr)


@catub.cat_cmd(
    pattern="cmds(?:\s|$)([\s\S]*)",
    command=("cmds", plugin_category),
    info={
        "header": "Показать список команд.",
        "description": "Если вход не указан, будет показан список всех команд.",
        "usage": [
            "{tr}cmds для всех команд",
            "{tr}cmds <plugin name> для конкретного плагина",
        ],
    },
)
async def _(event):
    "To get list of commands."
    if input_str := event.pattern_match.group(1):
        try:
            cmds = PLG_INFO[input_str]
        except KeyError:
            return await edit_delete(event, "Неверное имя плагина, проверьте его.__")
        except Exception as e:
            return await edit_delete(event, f"**Ошибка**\n`{e}`")
        outstr = f"• **{input_str.title()} has {len(cmds)} commands**\n"
        for cmd in cmds:
            outstr += f"  - `{cmdprefix}{cmd}`\n"
        outstr += f"**👩‍💻 Использовать : ** `{cmdprefix}help -c <command name>`"
    else:
        outstr = await cmdlist()
    await edit_or_reply(
        event, outstr, aslink=True, linktext="Всего команд: :"
    )


@catub.cat_cmd(
    pattern="s ([\s\S]*)",
    command=("s", plugin_category),
    info={
        "header": "Поиск команд.",
        "examples": "{tr}s song",
    },
)
async def _(event):
    "To search commands."
    cmd = event.pattern_match.group(1)
    if found := [i for i in sorted(list(CMD_INFO)) if cmd in i]:
        out_str = "".join(f"`{i}`    " for i in found)
        out = f"**Я нашел {len(found)} команды для: **`{cmd}`\n\n{out_str}"
        out += f"\n\n__Для получения дополнительной информации проверьте {cmdprefix}help -c <command>__"
    else:
        out = f"Я не могу найти такую ​​команду `{cmd}`"
    await edit_or_reply(event, out)


@catub.cat_cmd(
    pattern="dc$",
    command=("dc", plugin_category),
    info={
        "header": "Чтобы показать DC вашей учетной записи.",
        "description": "DC вашей учетной записи и список DC будут показаны",
        "usage": "{tr}dc",
    },
)
async def _(event):
    "To get dc of your bot"
    result = await event.client(functions.help.GetNearestDcRequest())
    result = f"**Dc детали вашей учетной записи:**\
              \n**Страна :** {result.country}\
              \n**Текущий Dc :** {result.this_dc}\
              \n**Ближайший Dc :** {result.nearest_dc}\
              \n\n**Список центров обработки данных Telegram:**\
              \n**DC1 : **Miami FL, USA\
              \n**DC2 :** Amsterdam, NL\
              \n**DC3 :** Miami FL, USA\
              \n**DC4 :** Amsterdam, NL\
              \n**DC5 : **Singapore, SG\
                "
    await edit_or_reply(event, result)
