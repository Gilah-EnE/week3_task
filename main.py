import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor


async def download():
    url = await ainput("> ")
    tasks.append(asyncio.create_task(download()))

    print(f"Started {url}")
    await asyncio.sleep(4)  # емуляція процесу завантаження
    print(f"Done {url}")


async def ainput(prompt: str = "") -> str:
    with ThreadPoolExecutor(1, "AsyncInput") as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)


async def main():
    x = 0
    global tasks
    tasks = []
    while True:
        tasks.append(asyncio.create_task(download()))
        await tasks[x]
        tasks.pop(0)
        await tasks[x + 1]
        x += 2


asyncio.run(main())
