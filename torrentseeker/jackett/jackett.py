import typing as t
from operator import attrgetter

import aiohttp
from dateutil import parser
from torrentseeker.magneter import MagnetFinder
from torrentseeker.torrent import CategoryList, TorrentItem


class Jackett(object):
    def __init__(
        self,
        Endpoint: str,
        ApiKey: str,
        Trackers: t.Optional[t.List[str]] = None,
        Categories: t.Optional[CategoryList] = None,
    ):
        self.Endpoint = Endpoint
        self.ApiKey = ApiKey
        self.Trackers = Trackers or []
        self.Categories = Categories or []

        self.session = aiohttp.ClientSession(Endpoint)

    async def search(
        self,
        query: str,
        limit: int = 25,
        sort_by: str = "Seeders",
        magnet_finder: t.Optional[bool] = False,
        categories: t.Optional[CategoryList] = None,
        trackers: t.Optional[str] = None,
    ) -> t.List[TorrentItem]:
        params = [
            ("apikey", self.ApiKey),
            ("Query", query.strip()),
        ]
        if categories is not None:
            for category in categories:
                params.append(("Category[]", str(category.value)))
        else:
            for category in self.Categories:
                params.append(("Category[]", str(category.value)))

        if trackers is not None:
            for tracker in trackers:
                params.append(("Tracker[]", str(tracker)))
        else:
            for tracker in self.Trackers:
                params.append(("Tracker[]", str(tracker)))

        async with self.session.get(
            url="/api/v2.0/indexers/all/results",
            params=params,
        ) as response:
            response = await response.json()
            items = self._parse_items(response)
            if sort_by is not None:
                items.sort(key=attrgetter(sort_by), reverse=True)

            items = items[:limit]
            if magnet_finder:
                for item in items:
                    await MagnetFinder(item)

            return items

    def _parse_items(self, data: dict) -> t.List[TorrentItem]:
        results: t.List[t.Dict] = data["Results"]
        parsed_items = []
        for result in results:
            publish_date = parser.parse(result["PublishDate"])
            item = {
                "Title": result["Title"].strip(),
                "Tracker": result["Tracker"],
                "ResourceLink": result["Details"],
                "TorrentFileLink": result["Link"],
                "MagnetLink": result["MagnetUri"],
                "Size": result["Size"],
                "Peers": result["Peers"],
                "Seeders": result["Seeders"],
                "PublishDate": publish_date,
            }
            parsed_items.append(TorrentItem(**item))

        return parsed_items
