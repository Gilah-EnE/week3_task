import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from urllib.parse import urlparse

count = 0
tasks = []


async def download():
    url = await ainput("> ")
    tasks.append(asyncio.create_task(download()))
    global count
    print(f"Started downloading a file from {urlparse(url).netloc}")
    count += 1
    print(f"Downloading {count} files")

    with ProcessPoolExecutor() as executor:
        file = await asyncio.get_event_loop().run_in_executor(executor, requests.get, url)

        with open(url.split("/")[-1], "wb") as savefile:
            savefile.write(file.content)

    count -= 1
    print(f"Finished downloading a file from {urlparse(url).netloc}")

    if count > 0:
        print(f"Downloading {count} files")
    elif count == 0:
        print("All files finished downloading")


async def ainput(prompt: str = "") -> str:
    with ThreadPoolExecutor(1, "AsyncInput") as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)


async def main():
    x = 0
    while True:
        tasks.append(asyncio.create_task(download()))
        await tasks[x]
        tasks.pop(0)
        await tasks[x + 1]
        x += 2


asyncio.run(main())
