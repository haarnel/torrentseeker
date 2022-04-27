# TorrentSeeker.

Help you to find torrents using different resources. At the moment, it only supports search using Jackett API.

## Usage

```python
from torrentseeker.jackett import Jackett
from torrentseeker.jackett.categories import CategoryType
from torrentseeker.magneter import MagnetFinder


async def main():
    jackett = Jackett(
        Endpoint="http://127.0.0.1:9117",
        ApiKey="<API-KEY>",
        Trackers=["1337x", "bitsearch"],
    )
    items = await jackett.search(
        query="Nirvana",
        limit=5,
        sort_by="Seeders",
        magnet_finder=False,
        categories=[CategoryType.AUDIO],
    )

    # For some torrents magnet links can be missing,
    # MagnetFinder will try to find them.
    tasks = [MagnetFinder(item) for item in items]
    await asyncio.gather(*tasks)

    for item in items:
        print(item)

    await jackett.session.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## Cli mode

```shell
torrentseeker-cli jackett -k "<API-KEY>" -q "Shrek 2" -l 2 -m
```

Search result output example:

```
Tracker: The Pirate Bay
Title: Shrek (2001) 1080p BrRip x264 - 1GB- YIFY
Published: 2012-03-11 05:08:05+04:00
Size: 1018.8MiB
Seders/Peers: 217/22
ResourceLink: https://thepirabay.org/description.php?id=73223112
TorrentFileLink: ...
MagnetLink: magnet:?xt=urn:btih:7B923E54B2198EAC53..

...
```


## TO-DO

- [x] Search using Jackett API.
- [ ] Extend cli mode support.
- [ ] Improve Magnet link searcher.
- [ ] Add more search methods.
- [ ] Add tests.
