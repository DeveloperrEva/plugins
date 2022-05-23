import json

from bs4 import BeautifulSoup
from requests import get

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="magisk$",
    command=("magisk", plugin_category),
    info={
        "header": "Чтобы получить последние выпуски Magisk",
        "usage": "{tr}magisk",
    },
)
async def kakashi(event):
    "Get latest Magisk releases"
    magisk_repo = "https://raw.githubusercontent.com/topjohnwu/magisk-files/"
    magisk_dict = {
        "⦁ **Стабильная**": f"{magisk_repo}master/stable.json",
        "⦁ **Бета**": f"{magisk_repo}master/beta.json",
        "⦁ **Канарейка**": f"{magisk_repo}master/canary.json",
    }

    releases = "**Последние выпуски Magisk**\n\n"
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += (
            f'{name}: [APK v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[Changelog]({data["magisk"]["note"]})\n'
        )
    await edit_or_reply(event, releases)


@catub.cat_cmd(
    pattern="device(?: |$)(\S*)",
    command=("device", plugin_category),
    info={
        "header": "Чтобы получить имя/модель устройства Android из его кодового имени",
        "usage": "{tr}device <codename>",
        "examples": "{tr}device whyred",
    },
)
async def device_info(event):
    "get android device name from its codename"
    textx = await event.get_reply_message()
    codename = event.pattern_match.group(1)
    if not codename:
        if textx:
            codename = textx.text
        else:
            return await edit_delete(event, "`Используйте: .device <codename> / <model>`")
    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    if results := data.get(codename):
        reply = f"**Поиск результатов о `{codename}` :**\n\n"
        for item in results:
            reply += (
                f"**Бренд**: `{item['brand']}`\n"
                f"**Имя**: `{item['name']}`\n"
                f"**Модель**: `{item['model']}`\n\n"
            )
    else:
        reply = f"`Не удалось найти информацию о {codename}!`\n"
    await edit_or_reply(event, reply)


@catub.cat_cmd(
    pattern="codename(?: |)([\S]*)(?: |)([\s\S]*)",
    command=("codename", plugin_category),
    info={
        "header": "Чтобы найти кодовое имя устройства Android",
        "usage": "{tr}codename <brand> <device>",
        "examples": "{tr}codename Xiaomi Redmi Note 5 Pro",
    },
)
async def codename_info(event):
    textx = await event.get_reply_message()
    brand = event.pattern_match.group(1).lower()
    device = event.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await edit_delete(event, "`Используйте: .codename <brand> <device>`")

    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}
    devices = devices_lower.get(brand)
    if not devices:
        return await edit_or_reply(event, f"__Я не смог найти {brand}.__")
    if results := [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]:
        reply = f"**Поиск результатов от {brand} {device}**:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"**Девайс**: `{item['device']}`\n"
                f"**Имя**: `{item['name']}`\n"
                f"**Модель**: `{item['model']}`\n\n"
            )
    else:
        reply = f"`Не удалось найти {device} codename!`\n"
    await edit_or_reply(event, reply)


@catub.cat_cmd(
    pattern="twrp(?: |$)(\S*)",
    command=("twrp", plugin_category),
    info={
        "header": "Чтобы получить последние ссылки для скачивания twrp для устройства Android.",
        "usage": "{tr}twrp <codename>",
        "examples": "{tr}twrp whyred",
    },
)
async def twrp(event):
    "get android device twrp"
    textx = await event.get_reply_message()
    device = event.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        return await edit_delete(event, "`Используйте: .twrp <codename>`")
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Не удалось найти загрузки twrp для {device}!`\n"
        return await edit_delete(event, reply)
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Последний TWRP для {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Обновлено:** __{date}__\n"
    )
    await edit_or_reply(event, reply)
