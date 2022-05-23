import os
from pathlib import Path

from ..Config import Config
from ..core import CMD_INFO, PLG_INFO
from ..utils import load_module, remove_plugin
from . import CMD_HELP, CMD_LIST, SUDO_LIST, catub, edit_delete, edit_or_reply, reply_id

plugin_category = "tools"

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


def plug_checker(plugin):
    plug_path = f"./userbot/plugins/{plugin}.py"
    if not os.path.exists(plug_path):
        plug_path = f"./xtraplugins/{plugin}.py"
    if not os.path.exists(plug_path):
        plug_path = f"./badcatext/{plugin}.py"
    return plug_path


@catub.cat_cmd(
    pattern="install$",
    command=("install", plugin_category),
    info={
        "header": "Чтобы установить внешний плагин.",
        "description": "Ответьте на любой внешний плагин, чтобы установить его в свой бот..",
        "usage": "{tr}install",
    },
)
async def install(event):
    "To install an external plugin."
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "userbot/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edit_delete(
                    event,
                    f"Установленный плагин `{os.path.basename(downloaded_file_name)}`",
                    10,
                )
            else:
                os.remove(downloaded_file_name)
                await edit_delete(
                    event, "Ошибки! Этот плагин уже installed/pre-installed.", 10
                )
        except Exception as e:
            await edit_delete(event, f"**Error:**\n`{e}`", 10)
            os.remove(downloaded_file_name)


@catub.cat_cmd(
    pattern="load ([\s\S]*)",
    command=("load", plugin_category),
    info={
        "header": "Чтобы снова загрузить плагин. если ты его разгрузил",
        "description": "Чтобы снова загрузить плагин, который вы выгрузили с помощью {tr}unload",
        "usage": "{tr}load <plugin name>",
        "examples": "{tr}load markdown",
    },
)
async def load(event):
    "To load a plugin again. if you have unloaded it"
    shortname = event.pattern_match.group(1)
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await edit_delete(event, f"`Успешно загружено {shortname}`", 10)
    except Exception as e:
        await edit_or_reply(
            event,
            f"Не мог загрузить {shortname} из-за следующей ошибки.\n{e}",
        )


@catub.cat_cmd(
    pattern="send ([\s\S]*)",
    command=("send", plugin_category),
    info={
        "header": "Чтобы загрузить файл плагина в телеграмм чат",
        "usage": "{tr}send <plugin name>",
        "examples": "{tr}send markdown",
    },
)
async def send(event):
    "To uplaod a plugin file to telegram chat"
    reply_to_id = await reply_id(event)
    thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
    input_str = event.pattern_match.group(1)
    the_plugin_file = plug_checker(input_str)
    if os.path.exists(the_plugin_file):
        caat = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            thumb=thumb,
            caption=f"**➥ Название плагина:-** `{input_str}`",
        )
        await event.delete()
    else:
        await edit_or_reply(event, "404: File Not Found")


@catub.cat_cmd(
    pattern="unload ([\s\S]*)",
    command=("unload", plugin_category),
    info={
        "header": "Чтобы временно выгрузить плагин.",
        "description": "Вы можете загрузить этот незагруженный плагин, перезапустив его или используя {tr}load cmd. Полезно для таких случаев, как установка заметок в розовом боте ({tr} unload markdown).",
        "usage": "{tr}unload <plugin name>",
        "examples": "{tr}unload markdown",
    },
)
async def unload(event):
    "To unload a plugin temporarily."
    shortname = event.pattern_match.group(1)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"Разгружено {shortname} успешно")
    except Exception as e:
        await edit_or_reply(event, f"Успешно выгружено {shortname}\n{e}")


@catub.cat_cmd(
    pattern="uninstall ([\s\S]*)",
    command=("uninstall", plugin_category),
    info={
        "header": "Чтобы временно удалить плагин.",
        "description": "Чтобы остановить работу этого плагина и удалить этот плагин из бота.",
        "note": "Чтобы навсегда выгрузить плагин из бота, установите NO_LOAD var в хероку с этим именем плагина, дайте пробел между именами плагинов, если их больше 1..",
        "usage": "{tr}uninstall <plugin name>",
        "examples": "{tr}uninstall markdown",
    },
)
async def unload(event):
    "To uninstall a plugin."
    shortname = event.pattern_match.group(1)
    path = plug_checker(shortname)
    if not os.path.exists(path):
        return await edit_delete(
            event, f"Нет плагина с путем {path} чтобы удалить его"
        )
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"{shortname} Удален успешно")
    except Exception as e:
        await edit_or_reply(event, f"Успешно удалено {shortname}\n{e}")
    if shortname in PLG_INFO:
        for cmd in PLG_INFO[shortname]:
            CMD_INFO.pop(cmd)
        PLG_INFO.pop(shortname)
