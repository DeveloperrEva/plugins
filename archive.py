import asyncio
import io
import os
import time
import zipfile
from datetime import datetime
from pathlib import Path
from tarfile import is_tarfile
from tarfile import open as tar_open

from telethon import types
from telethon.utils import get_extension

from ..Config import Config
from . import catub, edit_delete, edit_or_reply, progress

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
plugin_category = "misc"


def zipdir(dirName):
    filePaths = []
    for root, directories, files in os.walk(dirName):
        for filename in files:
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
    return filePaths


@catub.cat_cmd(
    pattern="zip(?:\s|$)([\s\S]*)",
    command=("zip", plugin_category),
    info={
        "header": "Чтобы сжать файл/папки",
        "description": "Создаст zip-файл для заданного пути к файлу или пути к папке.",
        "usage": [
            "{tr}zip <file/folder path>",
        ],
        "examples": ["{tr}zip downloads", "{tr}zip sample_config.py"],
    },
)
async def zip_file(event):
    "To create zip file"
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_delete(event, "`Укажите путь к файлу в zip`")
    start = datetime.now()
    if not os.path.exists(Path(input_str)):
        return await edit_or_reply(
            event,
            f"Нет такого каталога или файла с именем `{input_str}` Проверьте еще раз",
        )
    if os.path.isfile(Path(input_str)):
        return await edit_delete(event, "`Сжатие файлов еще не реализовано`")
    mone = await edit_or_reply(event, "`Выполняется сжатие....`")
    filePaths = zipdir(input_str)
    filepath = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY, os.path.basename(Path(input_str))
    )
    zip_file = zipfile.ZipFile(f"{filepath}.zip", "w")
    with zip_file:
        for file in filePaths:
            zip_file.write(file)
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(
        f"Заархивирован путь `{input_str}` в `{filepath}.zip` в __{ms}__ секунд"
    )


@catub.cat_cmd(
    pattern="tar(?:\s|$)([\s\S]*)",
    command=("tar", plugin_category),
    info={
        "header": "Чтобы сжать файл/папки в файл tar",
        "description": "Создаст tar-файл для заданного пути к файлу или папке.",
        "usage": [
            "{tr}tar <file/folder path>",
        ],
        "examples": ["{tr}tar downloads", "{tr}tar sample_config.py"],
    },
)
async def tar_file(event):
    "To create tar file"
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_delete(event, "`Укажите путь к файлу для сжатия`")
    if not os.path.exists(Path(input_str)):
        return await edit_or_reply(
            event,
            f"Нет такого каталога или файла с именем `{input_str}` Проверьте еще раз",
        )
    if os.path.isfile(Path(input_str)):
        return await edit_delete(event, "`Сжатие файлов еще не реализовано`")
    mone = await edit_or_reply(event, "`Выполняется создание Tar....`")
    start = datetime.now()
    filePaths = zipdir(input_str)
    filepath = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY, os.path.basename(Path(input_str))
    )
    destination = f"{filepath}.tar.gz"
    zip_file = tar_open(destination, "w:gz")
    with zip_file:
        for file in filePaths:
            zip_file.add(file)
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(
        f"Создал файл tar для данного пути {input_str} как `{destination}` в __{ms}__ секунд"
    )


@catub.cat_cmd(
    pattern="unzip(?:\s|$)([\s\S]*)",
    command=("unzip", plugin_category),
    info={
        "header": "Чтобы распаковать данный zip-файл",
        "description": "Ответьте на zip-файл или укажите путь к zip-файлу с командой для распаковки данного файла.",
        "usage": [
            "{tr}unzip <reply/file path>",
        ],
    },
)
async def zip_file(event):  # sourcery no-metrics
    "To unpack the zip file"
    if input_str := event.pattern_match.group(1):
        path = Path(input_str)
        if os.path.exists(path):
            start = datetime.now()
            if not zipfile.is_zipfile(path):
                return await edit_delete(
                    event, f"`Данный путь {path} это не zip файл для распаковки`"
                )

            mone = await edit_or_reply(event, "`Распаковка....`")
            destination = os.path.join(
                Config.TMP_DOWNLOAD_DIRECTORY,
                os.path.splitext(os.path.basename(path))[0],
            )
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(destination)
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                f"распаковать и сохранить в `{destination}` \n**Затраченное время :** `{ms} секунд`"
            )
        else:
            await edit_delete(event, f"Я не могу найти этот путь `{input_str}`", 10)
    elif event.reply_to_msg_id:
        start = datetime.now()
        reply = await event.get_reply_message()
        ext = get_extension(reply.document)
        if ext != ".zip":
            return await edit_delete(
                event,
                "`Ответный файл не является zip-файлом, перепроверьте ответное сообщение`",
            )
        mone = await edit_or_reply(event, "`Распаковка....`")
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                filename = attr.file_name
        filename = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, filename)
        c_time = time.time()
        try:
            dl = io.FileIO(filename, "a")
            await event.client.fast_download_file(
                location=reply.document,
                out=dl,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "пытаюсь скачать")
                ),
            )
            dl.close()
        except Exception as e:
            return await edit_delete(mone, f"**Ошибка:**\n__{e}__")
        await mone.edit("`Скачать готовый Распаковать сейчас`")
        destination = os.path.join(
            Config.TMP_DOWNLOAD_DIRECTORY,
            os.path.splitext(os.path.basename(filename))[0],
        )
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(destination)
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
            f"распаковать и сохранить в `{destination}` \n**Затраченное время :** `{ms} секунд`"
        )
        os.remove(filename)
    else:
        await edit_delete(
            mone,
            "`Либо ответьте на zip-файл, либо укажите путь к zip-файлу вместе с командой`",
        )


@catub.cat_cmd(
    pattern="untar(?:\s|$)([\s\S]*)",
    command=("untar", plugin_category),
    info={
        "header": "Чтобы распаковать данный файл tar",
        "description": "Ответьте на файл tar или укажите путь к файлу tar с командой для распаковки данного файла tar.",
        "usage": [
            "{tr}untar <reply/file path>",
        ],
    },
)
async def untar_file(event):  # sourcery no-metrics
    "To unpack the tar file"
    if input_str := event.pattern_match.group(1):
        path = Path(input_str)
        if os.path.exists(path):
            start = datetime.now()
            if not is_tarfile(path):
                return await edit_delete(
                    event, f"`Данный путь {path} это не tar-файл для распаковки`"
                )

            mone = await edit_or_reply(event, "`Распаковка....`")
            destination = os.path.join(
                Config.TMP_DOWNLOAD_DIRECTORY, (os.path.basename(path).split("."))[0]
            )
            if not os.path.exists(destination):
                os.mkdir(destination)
            file = tar_open(path)
            # extracting file
            file.extractall(destination)
            file.close()
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                f"**Затраченное время :** `{ms} секунд`\
                \nРаспаковал входной путь `{input_str}` и хранится в `{destination}`"
            )
        else:
            await edit_delete(event, f"Я не могу найти этот путь `{input_str}`", 10)
    elif event.reply_to_msg_id:
        start = datetime.now()
        reply = await event.get_reply_message()
        mone = await edit_or_reply(event, "`Распаковка....`")
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                filename = attr.file_name
        filename = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, filename)
        c_time = time.time()
        try:
            dl = io.FileIO(filename, "a")
            await event.client.fast_download_file(
                location=reply.document,
                out=dl,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "Пытаюсь скачать")
                ),
            )
            dl.close()
        except Exception as e:
            return await edit_delete(mone, f"**Ошибка:**\n__{e}__")
        if not is_tarfile(filename):
            return await edit_delete(
                mone, "`Ответный файл не является файлом tar, чтобы распаковать его, проверьте его`"
            )
        await mone.edit("`Скачать готовый Распаковать сейчас`")
        destination = os.path.join(
            Config.TMP_DOWNLOAD_DIRECTORY, (os.path.basename(filename).split("."))[0]
        )

        if not os.path.exists(destination):
            os.mkdir(destination)
        file = tar_open(filename)
        # extracting file
        file.extractall(destination)
        file.close()
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
            f"**Затраченное время :** `{ms} секунд`\
                \nРаспаковал ответный файл и сохранил в `{destination}`"
        )
        os.remove(filename)
    else:
        await edit_delete(
            mone,
            "`Либо ответьте на tar-файл, либо укажите путь к tar-файлу вместе с командой`",
        )
