from telegraph import upload_file
from telethon.tl.functions.users import GetFullUserRequest
from urlextract import URLExtract
from validators.url import url

from userbot import BOTLOG_CHATID, catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "tools"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER

extractor = URLExtract()
vlist = [
    "ALIVE_PIC",
    "ALIVE_EMOJI",
    "ALIVE_TEMPLATE",
    "ALIVE_TEXT",
    "ALLOW_NSFW",
    "CHANGE_TIME",
    "DEFAULT_BIO",
    "DEFAULT_NAME",
    "DEFAULT_PIC",
    "DEFAULT_USER",
    "DIGITAL_PIC",
    "FIRST_NAME",
    "HELP_EMOJI",
    "HELP_TEXT",
    "IALIVE_PIC",
    "LAST_NAME",
    "PING_PIC",
    "PING_TEMPLATE",
    "PM_PIC",
    "PM_TEXT",
    "PM_BLOCK",
    "MAX_FLOOD_IN_PMS",
    "START_TEXT",
    "BOT_START_PIC",
    "NO_OF_ROWS_IN_HELP",
    "NO_OF_COLUMNS_IN_HELP",
    "CUSTOM_STICKER_PACKNAME",
]

oldvars = {
    "PM_PIC": "pmpermit_pic",
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",
}


@catub.cat_cmd(
    pattern="(set|get|del)dv(?: |$)([\s\S]*)",
    command=("dv", plugin_category),
    info={
        "header": "Установить переменные в базе данных или проверить или удалить",
        "description": "Установка, выборка или удаление значений или переменных непосредственно в базе данных без перезапуска или переменных героку.\n\nВы можете установить несколько картинок, указав пробел после ссылок в live, ialive, pm..",
        "flags": {
            "set": "Чтобы установить новую переменную в базе данных или изменить старую переменную",
            "get": "Чтобы показать уже существующее значение var.",
            "del": "Чтобы удалить существующее значение",
        },
        "var name": "**[Список переменных]**(https://catuserbot.gitbook.io/catuserbot/data-vars-setup)",
        "usage": [
            "{tr}setdv <var name> <var value>",
            "{tr}getdv <var name>",
            "{tr}deldv <var name>",
        ],
        "examples": [
            "{tr}setdv ALIVE_PIC <pic link>",
            "{tr}setdv ALIVE_PIC <pic link 1> <pic link 2>",
            "{tr}getdv ALIVE_PIC",
            "{tr}deldv ALIVE_PIC",
        ],
    },
)
async def bad(event):  # sourcery no-metrics
    "To manage vars in database"
    cmd = event.pattern_match.group(1).lower()
    vname = event.pattern_match.group(2)
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(vlist, start=1))
    if not vname:
        return await edit_delete(
            event, f"**📑 Дайте правильное имя var из списка :\n\n**{vnlist}", time=60
        )
    vinfo = None
    if " " in vname:
        vname, vinfo = vname.split(" ", 1)
    reply = await event.get_reply_message()
    if not vinfo and reply:
        vinfo = reply.text
    if vname in vlist:
        if vname in oldvars:
            vname = oldvars[vname]
        if cmd == "set":
            if vname == "DEFAULT_USER":
                if not vinfo or vinfo != "Me":
                    return await edit_delete(
                        event,
                        "**Чтобы сохранить информацию о текущем профиле Установите значение:**\\n `.setdv DEFAULT_USER Me`",
                    )

                USERINFO = await catub.get_entity(catub.uid)
                FULL_USERINFO = (await catub(GetFullUserRequest(catub.uid))).full_user
                addgvar("FIRST_NAME", USERINFO.first_name)
                addgvar("DEFAULT_NAME", USERINFO.first_name)
                if USERINFO.last_name:
                    addgvar(
                        "DEFAULT_NAME",
                        f"{USERINFO.first_name}  {USERINFO.first_name}",
                    )
                    addgvar("LAST_NAME", USERINFO.last_name)
                elif gvarstatus("LAST_NAME"):
                    delgvar("LAST_NAME")
                if FULL_USERINFO.about:
                    addgvar("DEFAULT_BIO", FULL_USERINFO.about)
                elif gvarstatus("DEFAULT_BIO"):
                    delgvar("DEFAULT_BIO")
                try:
                    photos = await catub.get_profile_photos(catub.uid)
                    myphoto = await catub.download_media(photos[0])
                    myphoto_urls = upload_file(myphoto)
                    addgvar("DEFAULT_PIC", f"https://telegra.ph{myphoto_urls[0]}")
                except IndexError:
                    if gvarstatus("DEFAULT_PIC"):
                        delgvar("DEFAULT_PIC")
                usrln = gvarstatus("LAST_NAME") or None
                usrbio = gvarstatus("DEFAULT_BIO") or None
                usrphoto = gvarstatus("DEFAULT_PIC") or None
                vinfo = f'**Никнейм:** `{gvarstatus("DEFAULT_NAME")}`\n**Имя:** `{gvarstatus("FIRST_NAME")}`\n**Фамилия:** `{usrln}`\n**Био:** `{usrbio}`\n**Фото:** `{usrphoto}`'
            else:
                if not vinfo and vname in ["ALIVE_TEMPLATE", "PING_TEMPLATE"]:
                    return await edit_delete(event, "Check @cat_alive")
                if not vinfo:
                    return await edit_delete(
                        event,
                        f"Дайте несколько значений, которые вы хотите сохранить для **{vname}**",
                    )
                check = vinfo.split(" ")
                for i in check:
                    if vname == "DEFAULT_PIC" and not url(i):
                        return await edit_delete(event, "**Дай правильную ссылку...**")
                    elif vname == "DIGITAL_PIC" and not url(i):
                        return await edit_delete(event, "**Дай правильную ссылку...**")
                    elif (("PIC" in vname) or ("pic" in vname)) and not url(i):
                        return await edit_delete(event, "**Дай правильную ссылку...**")
                    elif (
                        vname == "DIGITAL_PIC"
                        or vname == "DEFAULT_PIC"
                        or vname == "BOT_START_PIC"
                    ) and url(i):
                        vinfo = i
                        break
                    elif not "PIC" in vname:
                        break
                if vname == "DEFAULT_BIO" and len(vinfo) > 70:
                    return await edit_or_reply(
                        event,
                        f"Количество символов в вашей биографии не должно превышать 70, поэтому сожмите его и установите снова.\n`{vinfo}`",
                    )
                addgvar(vname, vinfo)
            if BOTLOG_CHATID:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#SET_DATAVAR\
                    \n**{vname}** обновляется новым в базе данных, как показано ниже",
                )
                await event.client.send_message(BOTLOG_CHATID, vinfo, silent=True)
            await edit_delete(
                event, f"📑 Ценность **{vname}** меняется на :- `{vinfo}`", time=20
            )
        if cmd == "get":
            var_data = gvarstatus(vname)
            await edit_delete(
                event, f"📑 Ценность **{vname}** это  ```{var_data}```", time=20
            )
        elif cmd == "del":
            if vname == "DEFAULT_USER":
                delgvar("FIRST_NAME")
                delgvar("DEFAULT_NAME")
                if gvarstatus("LAST_NAME"):
                    delgvar("LAST_NAME")
                if gvarstatus("DEFAULT_BIO"):
                    delgvar("DEFAULT_BIO")
                if gvarstatus("DEFAULT_PIC"):
                    delgvar("DEFAULT_PIC")
            delgvar(vname)
            if BOTLOG_CHATID:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#DEL_DATAVAR\
                    \n**{vname}** удаляется из базы данных",
                )
            await edit_delete(
                event,
                f"📑 Ценность **{vname}** теперь удален и установлен по умолчанию.",
                time=20,
            )
    else:
        await edit_delete(
            event, f"**📑 Дайте правильное имя var из списка :\n\n**{vnlist}", time=60
        )


@catub.cat_cmd(
    pattern="custom (pmpermit|pmpic|pmblock|startmsg)$",
    command=("custom", plugin_category),
    info={
        "header": "Чтобы настроить своего Userbot.",
        "options": {
            "pmpermit": "Чтобы настроить текст pmpermit. ",
            "pmblock": "Чтобы настроить сообщение блокировки pmpermit.",
            "startmsg": "Чтобы настроить стартовое сообщение бота, когда кто-то его запустил.",
            "pmpic": "Чтобы настроить pmpermit pic. Ответить на URL-адрес медиа или текст, содержащий медиа.",
        },
        "custom": {
            "{mention}": "Упомянуть пользователя",
            "{first}": "Имя пользователя",
            "{last}": "Фамилия пользователя",
            "{fullname}": "Полное имя пользователя",
            "{username}": "Имя пользователя",
            "{userid}": "Userid пользователя",
            "{my_first}": "Твое имя",
            "{my_last}": "Твоя фамилия ",
            "{my_fullname}": "Ваше полное имя",
            "{my_username}": "Ваш логин",
            "{my_mention}": "Ваше упоминание",
            "{totalwarns}": "Всего предупреждений",
            "{warns}": "Предупреждения",
            "{remwarns}": "Остальные предупреждения",
        },
        "usage": [
            "{tr}custom <option> reply",
        ],
        "NOTE": "Вы можете установить, получить или удалить их, `{tr}setdv` , `{tr}getdv` & `{tr}deldv` также.",
    },
)
async def custom_catuserbot(event):
    "To customize your CatUserbot."
    reply = await event.get_reply_message()
    text = None
    if reply:
        text = reply.text
    if text is None:
        return await edit_delete(event, "Ответ на пользовательский текст или URL")
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        addgvar("pmpermit_txt", text)
    if input_str == "pmblock":
        addgvar("pmblock", text)
    if input_str == "startmsg":
        addgvar("START_TEXT", text)
    if input_str == "pmpic":
        urls = extractor.find_urls(reply.text)
        if not urls:
            return await edit_delete(event, "`данная ссылка не поддерживается`", 5)
        text = " ".join(urls)
        addgvar("pmpermit_pic", text)
    await edit_or_reply(event, f"__Ваш кастом {input_str} был обновлен")
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#SET_DATAVAR\
                    \n**{input_str}** обновляется новым в базе данных, как показано ниже",
        )
        await event.client.send_message(BOTLOG_CHATID, text, silent=True)


@catub.cat_cmd(
    pattern="delcustom (pmpermit|pmpic|pmblock|startmsg)$",
    command=("delcustom", plugin_category),
    info={
        "header": "Чтобы удалить настройку вашего Userbot.",
        "options": {
            "pmpermit": "Чтобы удалить пользовательский текст pmpermit",
            "pmblock": "Чтобы удалить пользовательское сообщение о блокировке разрешений",
            "pmpic": "Чтобы удалить изображение пользовательского разрешения.",
            "startmsg": "Чтобы удалить пользовательское стартовое сообщение бота, когда кто-то его запустил.",
        },
        "usage": [
            "{tr}delcustom <option>",
        ],
        "NOTE": "Вы можете установить, получить или удалить их, `{tr}setdv` , `{tr}getdv` & `{tr}deldv` также.",
    },
)
async def custom_catuserbot(event):
    "To delete costomization of your CatUserbot."
    input_str = event.pattern_match.group(1)
    if input_str == "pmpermit":
        if gvarstatus("pmpermit_txt") is None:
            return await edit_delete(event, "__Вы не настроили свой pmpermit.__")
        delgvar("pmpermit_txt")
    if input_str == "pmblock":
        if gvarstatus("pmblock") is None:
            return await edit_delete(event, "__Вы не настроили свой pmblock.__")
        delgvar("pmblock")
    if input_str == "pmpic":
        if gvarstatus("pmpermit_pic") is None:
            return await edit_delete(event, "__Вы не настроили свой pmpic.__")
        delgvar("pmpermit_pic")
    if input_str == "startmsg":
        if gvarstatus("START_TEXT") is None:
            return await edit_delete(
                event, "__Вы не настроили свой старт сообщение в боте.__"
            )
        delgvar("START_TEXT")
    await edit_or_reply(
        event, f"__успешно удалил вашу настройку {input_str}.__"
    )
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#DEL_DATAVAR\
                    \n**{input_str}** удаляется из базы данных",
        )
