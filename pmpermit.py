import random
import re
from datetime import datetime

from telethon import Button, functions
from telethon.events import CallbackQuery
from telethon.utils import get_display_name

from userbot import catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper import pmpermit_sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import mention

plugin_category = "utils"
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER


class PMPERMIT:
    def __init__(self):
        self.TEMPAPPROVED = []


PMPERMIT_ = PMPERMIT()


async def do_pm_permit_action(event, chat):  # sourcery no-metrics
    reply_to_id = await reply_id(event)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    me = await event.client.get_me()
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    if str(chat.id) not in PM_WARNS:
        PM_WARNS[str(chat.id)] = 0
    try:
        MAX_FLOOD_IN_PMS = int(gvarstatus("MAX_FLOOD_IN_PMS") or 6)
    except (ValueError, TypeError):
        MAX_FLOOD_IN_PMS = 6
    totalwarns = MAX_FLOOD_IN_PMS + 1
    warns = PM_WARNS[str(chat.id)] + 1
    remwarns = totalwarns - warns
    if PM_WARNS[str(chat.id)] >= MAX_FLOOD_IN_PMS:
        try:
            if str(chat.id) in PMMESSAGE_CACHE:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
                del PMMESSAGE_CACHE[str(chat.id)]
        except Exception as e:
            LOGS.info(str(e))
        custompmblock = gvarstatus("pmblock") or None
        if custompmblock is not None:
            USER_BOT_WARN_ZERO = custompmblock.format(
                mention=mention,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
                totalwarns=totalwarns,
                warns=warns,
                remwarns=remwarns,
            )
        else:
            USER_BOT_WARN_ZERO = f"**Вы спамите моего хозяина** {my_mention}**, вы заблокированы.**"
        msg = await event.reply(USER_BOT_WARN_ZERO)
        await event.client(functions.contacts.BlockRequest(chat.id))
        the_message = f"#BLOCKED_PM\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) заблокирован\
                            \n**Количество сообщений:** {PM_WARNS[str(chat.id)]}"
        del PM_WARNS[str(chat.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
        try:
            return await event.client.send_message(
                BOTLOG_CHATID,
                the_message,
            )
        except BaseException:
            return
    custompmpermit = gvarstatus("pmpermit_txt") or None
    if custompmpermit is not None:
        USER_BOT_NO_WARN = custompmpermit.format(
            mention=mention,
            first=first,
            last=last,
            fullname=fullname,
            username=username,
            userid=userid,
            my_first=my_first,
            my_last=my_last,
            my_fullname=my_fullname,
            my_username=my_username,
            my_mention=my_mention,
            totalwarns=totalwarns,
            warns=warns,
            remwarns=remwarns,
        )
    elif gvarstatus("pmmenu") is None:
        USER_BOT_NO_WARN = f"""Привет {mention}__, Я еще не разрешил вам отправлять мне личные сообщения. 

У вас {warns}/{totalwarns} бот будет предупреждать вас об этом пока вы не будете заблокированы.

Выберите один из вариантов ниже, чтобы указать причину вашего сообщения, и подождите, пока я ее проверю.. __⬇️"""
    else:
        USER_BOT_NO_WARN = f"""Привет {mention}__, Я еще не разрешил вам отправлять мне личные сообщения.

У вас {warns}/{totalwarns} бот будет предупреждать вас об этом пока вы не будете заблокированы.

Не спамьте мне лс. Скажи причину и дождись моего ответа.__"""
    addgvar("pmpermit_text", USER_BOT_NO_WARN)
    PM_WARNS[str(chat.id)] += 1
    try:
        if gvarstatus("pmmenu") is None:
            results = await event.client.inline_query(
                Config.TG_BOT_USERNAME, "pmpermit"
            )
            msg = await results[0].click(chat.id, reply_to=reply_to_id, hide_via=True)
        else:
            if PM_PIC := gvarstatus("pmpermit_pic"):
                CAT = list(PM_PIC.split())
                PIC = list(CAT)
                CAT_IMG = random.choice(PIC)
            else:
                CAT_IMG = None
            if CAT_IMG is not None:
                msg = await event.client.send_file(
                    chat.id,
                    CAT_IMG,
                    caption=USER_BOT_NO_WARN,
                    reply_to=reply_to_id,
                    force_document=False,
                )
            else:
                msg = await event.client.send_message(
                    chat.id, USER_BOT_NO_WARN, reply_to=reply_to_id
                )
    except Exception as e:
        LOGS.error(e)
        msg = await event.reply(USER_BOT_NO_WARN)
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    PMMESSAGE_CACHE[str(chat.id)] = msg.id
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


async def do_pm_options_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "__Выберите вариант из приведенного выше сообщения и подождите. Не спамьте мне лс, это ваше последнее предупреждение.__"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = "**Если я правильно помню, я упомянул в своем предыдущем сообщении, что это не подходящее место для спама.. \\\x1fХотя вы игнорируете это сообщение. Так что я просто заблокировал вас. \\\x1fТеперь вы ничего не сможете сделать, пока мой мастер не выйдет в сеть и не разблокирует вас.**"

    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) is blocked\
                            \n**Причина:** __Он/она не выбирал ни один из предложенных вариантов и продолжал обмениваться сообщениями.__"
    sqllist.rm_from_list("pmoptions", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_enquire_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """__Привет! Наберитесь терпения. Мой хозяин еще не видел твоего сообщения. \
Мой хозяин обычно отвечает людям, хотя я не знаю некоторых исключительных пользователей.__
__Мой мастер ответит, когда он/она выйдет в сеть, если он/она захочет.__
** Пожалуйста, не рассылайте спам, если вы не хотите, чтобы вас заблокировали и отправили жалобу.**"""
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = "**Если я правильно помню, я упомянул в своем предыдущем сообщении, что это не подходящее место для спама. \\\x1fХотя вы игнорируете это сообщение. Так я тебя просто заблокировал. \\\x1fТеперь вы ничего не сможете сделать, пока мой мастер не выйдет в сеть и не разблокирует вас.**"

    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) заблокирован\
                \n**Причина:** __Он/Она выбрал вариант запроса, но не стал ждать, когда ему также сказали, и продолжал обмениваться сообщениями, поэтому заблокирован.__"
    sqllist.rm_from_list("pmenquire", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_request_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """__Эй, наберись терпения. Мой хозяин еще не видел твоего сообщения. \
Мой хозяин обычно отвечает людям, хотя я не знаю некоторых исключительных пользователей.__
__Мой хозяин ответит, когда вернется в онлайн, если захочет.__
** Пожалуйста, не рассылайте спам, если вы не хотите, чтобы вас заблокировали и отправили жалобу..**"""
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = "**Если я правильно помню, я упомянул в своем предыдущем сообщении, что это не подходящее место для спама.. \\\x1fХотя вы проигнорировали меня и написали мне. Так я тебя просто заблокировал. \\\x1fТеперь вы ничего не сможете сделать, пока мой мастер не выйдет в сеть и не разблокирует вас..**"

    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) заблокирован\
                \n**Причина:** __Он/Она выбрал вариант запроса, но не стал ждать, когда ему также сказали, и продолжал обмениваться сообщениями, поэтому заблокирован.__"
    sqllist.rm_from_list("pmrequest", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_chat_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = """__Привет! Я сейчас занят, я уже попросил вас подождать, знаете. После окончания моей работы. \
Мы можем говорить, но не правильно знаем. Надеюсь ты понимаешь.__
__Мой хозяин ответит, когда вернется в онлайн, если захочет.__
** Пожалуйста, не рассылайте спам, если вы не хотите, чтобы вас заблокировали и отправили жалобу..**"""
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = "**Если я правильно помню, я упоминал в своем предыдущем сообщении, что это не подходящее место для спама.. \\\x1fХотя вы игнорируете это сообщение. Так я тебя просто заблокировал. \\\x1fТеперь вы ничего не сможете сделать, пока мой мастер не выйдет в сеть и не разблокирует вас.**"

    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                \n[{get_display_name(chat)}](tg://user?id={chat.id}) заблокирован\
                \n**Причина:** __Он/она выбрал вариант чата, но не стал ждать после того, как ему сказали, что его также заблокировали.__"
    sqllist.rm_from_list("pmchat", chat.id)
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


async def do_pm_spam_action(event, chat):
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    USER_BOT_WARN_ZERO = "**Если я правильно помню, я упоминал в своем предыдущем сообщении, что это не подходящее место для спама.. \\\x1fХотя вы игнорируете это сообщение. Так я тебя просто заблокировал. \\\x1fТеперь вы ничего не сможете сделать, пока мой мастер не выйдет в сеть и не разблокирует вас..**"

    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"#BLOCKED_PM\
                            \n[{get_display_name(chat)}](tg://user?id={chat.id}) заблокирован\
                            \n**Причина:** Он выбрал вариант спама и снова отправил сообщение."
    sqllist.rm_from_list("pmspam", chat.id)
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    try:
        return await event.client.send_message(
            BOTLOG_CHATID,
            the_message,
        )
    except BaseException:
        return


@catub.cat_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def on_new_private_message(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if pmpermit_sql.is_approved(chat.id):
        return
    if chat.id in PMPERMIT_.TEMPAPPROVED:
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return await do_pm_spam_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return await do_pm_chat_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return await do_pm_request_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return await do_pm_enquire_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return await do_pm_options_action(event, chat)
    await do_pm_permit_action(event, chat)


@catub.cat_cmd(outgoing=True, func=lambda e: e.is_private, edited=False, forword=None)
async def you_dm_other(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return
    if event.text and event.text.startswith(
        (
            f"{cmdhd}block",
            f"{cmdhd}disapprove",
            f"{cmdhd}a",
            f"{cmdhd}da",
            f"{cmdhd}approve",
            f"{cmdhd}tempapprove",
            f"{cmdhd}tempa",
            f"{cmdhd}tapprove",
            f"{cmdhd}ta",
        )
    ):
        return
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    start_date = str(datetime.now().strftime("%B %d, %Y"))
    if not pmpermit_sql.is_approved(chat.id) and str(chat.id) not in PM_WARNS:
        pmpermit_sql.approve(
            chat.id, get_display_name(chat), start_date, chat.username, "For Outgoing"
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(chat.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    chat.id, PMMESSAGE_CACHE[str(chat.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(chat.id)]
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"show_pmpermit_options")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "Идиот, эти опции предназначены для пользователей, которые пишут вам сообщения, а не для вас"
        return await event.answer(text, cache_time=0, alert=True)
    text = f"""Хорошо, теперь вы получаете доступ к доступному меню моего мастера, {mention}.
__Давайте сделаем это гладко и дайте мне знать, почему вы здесь.__

**Выберите одну из следующих причин, почему вы здесь:**"""
    buttons = [
        (Button.inline(text="Чтобы узнать что-то.", data="to_enquire_something"),),
        (Button.inline(text="Запросить что-то.", data="to_request_something"),),
        (Button.inline(text="Поболтать с моим хозяином.", data="to_chat_with_my_master"),),
        (
            Button.inline(
                text="Чтобы спамить лс моего хозяина.",
                data="to_spam_my_master_inbox",
            ),
        ),
    ]
    sqllist.add_to_list("pmoptions", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    await event.edit(text, buttons=buttons)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"to_enquire_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "Идиот, эти опции предназначены для пользователей, которые пишут вам сообщения, а не для вас"
        return await event.answer(text, cache_time=0, alert=True)
    text = """__Хорошо. Ваш запрос зарегистрирован. Не спамить лс моего хозяина сейчас. \
Мой мастер сейчас занят. Когда мой мастер выйдет в сеть, он / она проверит ваше сообщение и пропингует вас. \
Тогда мы сможем продолжить этот разговор, но не сейчас..__"""
    sqllist.add_to_list("pmenquire", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"to_request_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "Идиот, эти опции предназначены для пользователей, которые пишут вам сообщения, а не для вас"
        return await event.answer(text, cache_time=0, alert=True)
    text = """__Хорошо. Я сообщил об этом своему хозяину. Когда он/она появится в сети\ или когда мой мастер будет свободен, он/она заглянет в этот чат и пропингует вас, чтобы мы могли поболтать по-дружески.__\

**Но сейчас, пожалуйста, не спамьте, если не хотите, чтобы вас заблокировали..**"""
    sqllist.add_to_list("pmrequest", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"to_chat_with_my_master")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "Идиот, эти опции предназначены для пользователей, которые пишут вам сообщения, а не для вас"
        return await event.answer(text, cache_time=0, alert=True)
    text = """__Да, конечно, мы можем дружески поболтать, но не сейчас. мы можем сделать это \
в другой раз. Сейчас я немного занят. когда я выхожу в сеть и если я свободен. Я пропингую тебя, это чертовски точно.__"""
    sqllist.add_to_list("pmchat", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@catub.tgbot.on(CallbackQuery(data=re.compile(rb"to_spam_my_master_inbox")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "Идиот, эти опции предназначены для пользователей, которые пишут вам сообщения, а не для вас"
        return await event.answer(text, cache_time=0, alert=True)
    text = "`███████▄▄███████████▄\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\
         \n▓▓▓▓▓▓███░░░░░░░░░░░░█\
         \n██████▀▀▀█░░░░██████▀ \
         \n░░░░░░░░░█░░░░█\
         \n░░░░░░░░░░█░░░█\
         \n░░░░░░░░░░░█░░█\
         \n░░░░░░░░░░░█░░█\
         \n░░░░░░░░░░░░▀▀`\
         \n**Так некруто, это не твой дом. Иди заморачивайся в другом месте.\
         \n\nИ это ваше последнее предупреждение, если вы отправите еще одно сообщение, вы будете автоматически заблокированы..**"
    sqllist.add_to_list("pmspam", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmspam").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    sqllist.rm_from_list("pmoptions", event.query.user_id)
    await event.edit(text)


@catub.cat_cmd(
    pattern="pmguard (on|off)$",
    command=("pmguard", plugin_category),
    info={
        "header": "Чтобы включить или выключить pmpermit.",
        "usage": "{tr}pmguard on/off",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmpermit."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvarstatus("pmpermit") is None:
            addgvar("pmpermit", "true")
            await edit_delete(
                event, "__Pmpermit успешно включен для вашей учетной записи.__"
            )
        else:
            await edit_delete(event, "__Pmpermit уже включен для вашей учетной записи__")
    elif gvarstatus("pmpermit") is not None:
        delgvar("pmpermit")
        await edit_delete(
            event, "__Pmpermit успешно отключен для вашей учетной записи__"
        )
    else:
        await edit_delete(event, "__Pmpermit уже отключен для вашей учетной записи__")


@catub.cat_cmd(
    pattern="pmmenu (on|off)$",
    command=("pmmenu", plugin_category),
    info={
        "header": "Чтобы включить или выключить меню.",
        "usage": "{tr}pmmenu on/off",
    },
)
async def pmpermit_on(event):
    "Turn on/off pmmenu."
    input_str = event.pattern_match.group(1)
    if input_str == "off":
        if gvarstatus("pmmenu") is None:
            addgvar("pmmenu", "false")
            await edit_delete(
                event,
                "__Pmpermit Меню успешно отключено для вашей учетной записи.__",
            )
        else:
            await edit_delete(
                event, "Меню разрешений уже отключено для вашей учетной записи"
            )
    elif gvarstatus("pmmenu") is not None:
        delgvar("pmmenu")
        await edit_delete(
            event, "__Меню Pmpermit успешно включено для вашей учетной записи__"
        )
    else:
        await edit_delete(
            event, "__Меню Pmpermit уже включено для вашей учетной записи__"
        )


@catub.cat_cmd(
    pattern="(a|approve)(?:\s|$)([\s\S]*)",
    command=("approve", plugin_category),
    info={
        "header": "Разрешить пользователю отправлять вам прямые сообщения.",
        "usage": [
            "{tr}a/approve <username/reply reason> в группе",
            "{tr}a/approve <reason> в лс",
        ],
    },
)
async def approve_p_m(event):  # sourcery no-metrics
    "To approve user to pm"
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__Включите pmpermit, выполнив __`{cmdhd}pmguard on` __для работы этого плагина__",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)
    else:
        user, reason = await get_user_from_event(event, secondgroup=True)
        if not user:
            return
    if not reason:
        reason = "Not mentioned"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if not pmpermit_sql.is_approved(user.id):
        if str(user.id) in PM_WARNS:
            del PM_WARNS[str(user.id)]
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        pmpermit_sql.approve(
            user.id, get_display_name(user), start_date, user.username, reason
        )
        chat = user
        if str(chat.id) in sqllist.get_collection_list("pmspam"):
            sqllist.rm_from_list("pmspam", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmchat"):
            sqllist.rm_from_list("pmchat", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmrequest"):
            sqllist.rm_from_list("pmrequest", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmenquire"):
            sqllist.rm_from_list("pmenquire", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmoptions"):
            sqllist.rm_from_list("pmoptions", chat.id)
        await edit_delete(
            event,
            f"__Одобрено в личку__ [{user.first_name}](tg://user?id={user.id})\n**Причина :** __{reason}__",
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(user.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    user.id, PMMESSAGE_CACHE[str(user.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(user.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    else:
        await edit_delete(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __уже в утвержденном списке__",
        )


@catub.cat_cmd(
    pattern="t(emp)?(a|approve)(?:\s|$)([\s\S]*)",
    command=("tapprove", plugin_category),
    info={
        "header": "Разрешить пользователю временно отправлять вам прямые сообщения.",
        "note": "Heroku перезапускается каждые 24 часа, поэтому при каждом перезапуске он отклоняет каждого временного одобренного пользователя.",
        "usage": [
            "{tr}ta/tapprove <username/reply reason> в группе",
            "{tr}ta/tapprove <reason> в лс",
        ],
    },
)
async def tapprove_pm(event):  # sourcery no-metrics
    "Temporarily approve user to pm"
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__Включите pmpermit, выполнив __`{cmdhd}pmguard on` __для работы этого плагина__",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(3)
    else:
        user, reason = await get_user_from_event(event, thirdgroup=True)
        if not user:
            return
    if not reason:
        reason = "Not mentioned"
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if (user.id not in PMPERMIT_.TEMPAPPROVED) and (
        not pmpermit_sql.is_approved(user.id)
    ):
        if str(user.id) in PM_WARNS:
            del PM_WARNS[str(user.id)]
        PMPERMIT_.TEMPAPPROVED.append(user.id)
        chat = user
        if str(chat.id) in sqllist.get_collection_list("pmspam"):
            sqllist.rm_from_list("pmspam", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmchat"):
            sqllist.rm_from_list("pmchat", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmrequest"):
            sqllist.rm_from_list("pmrequest", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmenquire"):
            sqllist.rm_from_list("pmenquire", chat.id)
        if str(chat.id) in sqllist.get_collection_list("pmoptions"):
            sqllist.rm_from_list("pmoptions", chat.id)
        await edit_delete(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) временно утвержден в личке__\n**Причина :** __{reason}__",
        )
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(user.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(
                    user.id, PMMESSAGE_CACHE[str(user.id)]
                )
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(user.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    elif pmpermit_sql.is_approved(user.id):
        await edit_delete(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) находится в утвержденном списке",
        )
    else:
        await edit_delete(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) уже находится во временном утвержденном списке",
        )


@catub.cat_cmd(
    pattern="(da|disapprove)(?:\s|$)([\s\S]*)",
    command=("disapprove", plugin_category),
    info={
        "header": "Чтобы запретить пользователю отправлять вам прямые сообщения.",
        "note": "Эта команда работает только для авторизованных пользователей",
        "options": {"all": "Чтобы отклонить всех одобренных пользователей"},
        "usage": [
            "{tr}da/disapprove <username/reply> в группе",
            "{tr}da/disapprove в лс",
            "{tr}da/disapprove all - отклонить всех.",
        ],
    },
)
async def disapprove_p_m(event):
    "To disapprove user to direct message you."
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__Включите pmpermit, выполнив __`{cmdhd}pmguard on` __для работы этого плагина__",
        )
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(2)

    else:
        reason = event.pattern_match.group(2)
        if reason != "all":
            user, reason = await get_user_from_event(event, secondgroup=True)
            if not user:
                return
    if reason == "all":
        pmpermit_sql.disapprove_all()
        return await edit_delete(
            event, "__В порядке! Я успешно отклонил всех.__"
        )
    if not reason:
        reason = "Not Mentioned."
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
        await edit_or_reply(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __отклонено, напишите мне в личные сообщения.__\n**Причина:**__ {reason}__",
        )
    elif user.id in PMPERMIT_.TEMPAPPROVED:
        PMPERMIT_.TEMPAPPROVED.remove(user.id)
        await edit_or_reply(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __отклонено, напишите мне в личные сообщения.__\n**Причина:**__ {reason}__",
        )
    else:
        await edit_delete(
            event,
            f"[{user.first_name}](tg://user?id={user.id}) __еще не утвержден__",
        )


@catub.cat_cmd(
    pattern="block(?:\s|$)([\s\S]*)",
    command=("block", plugin_category),
    info={
        "header": "Чтобы заблокировать пользователя для прямого сообщения вам.",
        "usage": [
            "{tr}block <username/reply reason> в группе",
            "{tr}block <reason> в лс",
        ],
    },
)
async def block_p_m(event):
    "To block user to direct message you."
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "Not Mentioned."
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(user.id) in PM_WARNS:
        del PM_WARNS[str(user.id)]
    if str(user.id) in PMMESSAGE_CACHE:
        try:
            await event.client.delete_messages(user.id, PMMESSAGE_CACHE[str(user.id)])
        except Exception as e:
            LOGS.info(str(e))
        del PMMESSAGE_CACHE[str(user.id)]
    if pmpermit_sql.is_approved(user.id):
        pmpermit_sql.disapprove(user.id)
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    await event.client(functions.contacts.BlockRequest(user.id))
    await edit_or_reply(
        event,
        f"[{user.first_name}](tg://user?id={user.id}) __заблокирован, он больше не может отправлять вам личные сообщения.__\n**Причина:** __{reason}__",
    )


@catub.cat_cmd(
    pattern="unblock(?:\s|$)([\s\S]*)",
    command=("unblock", plugin_category),
    info={
        "header": "Чтобы разблокировать пользователя.",
        "usage": [
            "{tr}unblock <username/reply reason> в группе",
            "{tr}unblock <reason> в лс",
        ],
    },
)
async def unblock_pm(event):
    "To unblock a user."
    if event.is_private:
        user = await event.get_chat()
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
    if not reason:
        reason = "Not Mentioned."
    await event.client(functions.contacts.UnblockRequest(user.id))
    await edit_or_reply(
        event,
        f"[{user.first_name}](tg://user?id={user.id}) __разблокирован, он/она может теперь отправлять вам личные сообщения.__\n**Причина:** __{reason}__",
    )


@catub.cat_cmd(
    pattern="l(ist)?a(pproved)?$",
    command=("listapproved", plugin_category),
    info={
        "header": "Чтобы увидеть список одобренных пользователей.",
        "usage": [
            "{tr}listapproved",
        ],
    },
)
async def approve_p_m(event):
    "To see list of approved users."
    if gvarstatus("pmpermit") is None:
        return await edit_delete(
            event,
            f"__Включите pmpermit, выполнив __`{cmdhd}pmguard on` __для работы этого плагина__",
        )
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "**Текущие утвержденные**\n\n"
    if len(approved_users) > 0:
        for user in approved_users:
            APPROVED_PMs += f"• 👤 {_format.mentionuser(user.first_name , user.user_id)}\n**ID:** `{user.user_id}`\n**Никнейм:** @{user.username}\n**Дата: **__{user.date}__\n**Причина: **__{user.reason}__\n\n"
    else:
        APPROVED_PMs = "`Вы еще никого не утвердили`"
    await edit_or_reply(
        event,
        APPROVED_PMs,
        file_name="approvedpms.txt",
        caption="`Текущие утвержденные`",
    )
