from telethon.tl import functions

from .. import catub
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..utils.tools import create_supergroup

plugin_category = "tools"


@catub.cat_cmd(
    pattern="create (b|g|c) ([\s\S]*)",
    command=("create", plugin_category),
    info={
        "header": "Чтобы создать частную группу/канал с юзерботом.",
        "description": "Используйте эту команду для создания супергруппы, формальной группы или канала..",
        "flags": {
            "b": "создать частную супергруппу",
            "g": "Чтобы создать частную базовую группу.",
            "c": "создать приватный канал",
        },
        "usage": "{tr}create (b|g|c) <name of group/channel>",
        "examples": "{tr}create b userbot",
    },
)
async def _(event):
    "To create a private group/channel with userbot"
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    if type_of_group == "c":
        descript = "Это тестовый канал, созданный с помощью userbot."
    else:
        descript = "Это тестовая группа, созданная с помощью userbot."
    if type_of_group == "g":
        try:
            result = await event.client(
                functions.messages.CreateChatRequest(
                    users=[Config.TG_BOT_USERNAME],
                    # Not enough users (to create a chat, for example)
                    # Telegram, no longer allows creating a chat with ourselves
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event, f"Группа `{group_name}` успешно создана. Зайти {result.link}"
            )
        except Exception as e:
            await edit_delete(event, f"**Ошибка:**\n{str(e)}")
    elif type_of_group == "c":
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about=descript,
                    megagroup=False,
                )
            )
            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await edit_or_reply(
                event,
                f"Канал `{group_name}` успешно создан. Зайти {result.link}",
            )
        except Exception as e:
            await edit_delete(event, f"**Ошибка:**\n{e}")
    elif type_of_group == "b":
        answer = await create_supergroup(
            group_name, event.client, Config.TG_BOT_USERNAME, descript
        )
        if answer[0] != "error":
            await edit_or_reply(
                event,
                f"Мегагруппа `{group_name}` успешно создана. ЗАйти {answer[0].link}",
            )
        else:
            await edit_delete(event, f"**Ошибка:**\n{answer[1]}")
    else:
        await edit_delete(event, "Прочиатй `.help create` чтобы понять, как использовать меня")
