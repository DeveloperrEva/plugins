# corona virus stats for catuserbot
from covid import Covid

from userbot.plugins import catub, covidindia, edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="covid(?:\s|$)([\s\S]*)",
    command=("covid", plugin_category),
    info={
        "header": "Чтобы получить последнюю информацию о covid-19.",
        "description": "Получить информацию о данных covid-19 в данной стране/штате (только штаты Индии).",
        "usage": "{tr}covid <state_name/country_name>",
        "examples": ["{tr}covid andhra pradesh", "{tr}covid india", "{tr}covid world"],
    },
)
async def corona(event):
    "To get latest information about covid-19."
    input_str = event.pattern_match.group(1)
    country = (input_str).title() if input_str else "World"
    catevent = await edit_or_reply(event, "`Сбор данных...`")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n⚠️ Подтвержденный   : <code>{hmm1}</code>"
        data += f"\n😔 Активный           : <code>{country_data['active']}</code>"
        data += f"\n⚰️ Смерти         : <code>{hmm2}</code>"
        data += f"\n🤕 Критические          : <code>{country_data['critical']}</code>"
        data += f"\n😊 Выздоровленные   : <code>{country_data['recovered']}</code>"
        data += f"\n💉 Всего тестов    : <code>{country_data['total_tests']}</code>"
        data += f"\n🥺 Новые заболевании   : <code>{country_data['new_cases']}</code>"
        data += f"\n😟 Новые смерти : <code>{country_data['new_deaths']}</code>"
        await catevent.edit(
            "<b>Информация о коронавирусе {}:\n{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            cat1 = int(data["new_positive"]) - int(data["positive"])
            cat2 = int(data["new_death"]) - int(data["death"])
            cat3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Информация о коронавирусе {data['state_name']}\
                \n\n⚠️ Подтвержденный   : <code>{data['new_positive']}</code>\
                \n😔 Активный           : <code>{data['new_active']}</code>\
                \n⚰️ Смерти         : <code>{data['new_death']}</code>\
                \n😊 Выздоровленные   : <code>{data['new_cured']}</code>\
                \n🥺 Новые заболевании    : <code>{cat1}</code>\
                \n😟 Новые смерти : <code>{cat2}</code>\
                \n😃 Новый вылеченный  : <code>{cat3}</code> </b>"
            await catevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                catevent,
                f"`Информация о коронавирусе {country} недоступен или не может получить`",
                5,
            )
