import asyncio
from email.policy import default
from functools import wraps

import click

from torrentseeker.jackett import Jackett


def coro_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        asyncio.run(func(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@click.command()
@click.option("-h", "--host", default="127.0.0.1", show_default=True, type=str)
@click.option("-p", "--port", default=9117, show_default=True, type=int)
@click.option("-k", "--apikey", required=True, type=str)
@click.option("-q", "--query", required=True, type=str)
@click.option("-l", "--limit", default=10, type=int)
@click.option("-m", "--magnet-find", is_flag=True, type=bool)
@coro_wrap
async def jackett(host, port, apikey, query, limit, magnet_find):
    endpoint = f"http://{host}:{port}"
    jackett = Jackett(Endpoint=endpoint, ApiKey=apikey)

    items = await jackett.search(
        query=query,
        magnet_finder=magnet_find,
        limit=limit,
    )

    for item in items:
        print(item)

    await jackett.session.close()


cli.add_command(jackett)

if __name__ == "__main__":
    cli()
