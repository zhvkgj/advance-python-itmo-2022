#!/usr/bin/python3
import asyncio
import pathlib
from uuid import uuid4

import aiofiles
import aiohttp
import click


async def fetch_picture(session, out_dir, url="https://picsum.photos/200"):
    async with session.get(url) as response:
        if response.status == 200:
            image_name = f"{uuid4()}.jpg"
            path = f"{out_dir}/{image_name}"
            async with aiofiles.open(path, "wb") as file:
                await file.write(await response.read())


async def download_image(out_dir, n):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_picture(session, out_dir) for _ in range(n)]
        await asyncio.gather(*tasks)


proj_dir = pathlib.Path(__file__).parent.parent.resolve()


@click.command()
@click.option("--out_dir", default=f"{proj_dir}/artifacts/easy", help="Directory to save photos")
@click.option("--n", default=5, help="Count of photos to download")
def main(out_dir: str, n: int):
    asyncio.run(download_image(out_dir, n))


if __name__ == "__main__":
    main()
