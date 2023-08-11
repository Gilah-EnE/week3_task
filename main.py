from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from urllib.parse import urlparse
import asyncio
import re
import requests
import validators

count = 0  # кількість поточних завантажень
tasks = []  # список для збереження всіх створених корутин


async def download() -> None:
    """
    Основна функція даної програми.
    Виконує отримання та валідацію URL від користувача і завантаження.
    :return:
    """
    global count
    global tasks

    url = await async_input("> ")

    if not re.match("(?:http|ftp|https)://", url):  # якщо URL не починається з назви протоколу, додаємо http://
        url = f"http://{url}"

    tasks.append(asyncio.create_task(download()))   # створення корутини, яка буде виконуватися наступною

    if validators.url(url):  # перевірка URL на валідність
        print(f"Started downloading a file from {urlparse(url).netloc}")

        count += 1  # додали завантаження

        print(f"Downloading {count} files")

        try:
            with ProcessPoolExecutor() as executor:
                file = await asyncio.get_event_loop().run_in_executor(
                    executor, requests.get, url
                )

            try:
                with open(url.split("/")[-1], "wb") as savefile:
                    savefile.write(file.content)

            except Exception as save_exc:
                print(f"File save error: {save_exc}")

        except Exception as download_exc:
            print(f"Download error: {download_exc}")

        count -= 1  # завершили завантаження

        print(f"Finished downloading a file from {urlparse(url).netloc}")

        if count > 0:
            print(f"Downloading {count} files")
        elif count == 0:
            print("All files finished downloading")

    else:
        print("Invalid URL")


async def async_input(prompt: str = ""):
    """
    Функція-обгортка для асинхронного запуску синхронної функції
    builtins.input(prompt) за допомогою ThreadPoolExecutor.
    :param prompt: повторює параметр prompt функції builtins.input()
    :type prompt: str
    :return:
    """
    with ThreadPoolExecutor(1, "AsyncInput") as executor:
        return await asyncio.get_event_loop().run_in_executor(
            executor, input, prompt
        )


async def main() -> None:
    x = 0   # лічильник для списку корутин

    while True:
        tasks.append(asyncio.create_task(download()))
        await tasks[x]
        await tasks[x + 1]
        x += 2


asyncio.run(main())
