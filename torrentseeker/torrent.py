import typing as t
from datetime import datetime
from textwrap import dedent

from torrentseeker.jackett.categories import CategoryType
from torrentseeker.utils import file_size_format

CategoryList = t.List[CategoryType]


class TorrentItem:
    def __init__(
        self,
        Title: str,
        Tracker: str,
        ResourceLink: str,
        TorrentFileLink: str,
        MagnetLink: str,
        Peers: int,
        Seeders: int,
        Size: int,
        PublishDate: datetime,
    ):
        self.Title = Title
        self.Tracker = Tracker
        self.ResourceLink = ResourceLink
        self.TorrentFileLink = TorrentFileLink
        self.MagnetLink = MagnetLink
        self.Peers = Peers
        self.Seeders = Seeders
        self.Size = Size
        self.PublishDate = PublishDate

    def __str__(self):
        return dedent(
            f"""
            Tracker: {self.Tracker}
            Title: {self.Title}
            Published: {self.PublishDate}
            Size: {file_size_format(self.Size)}
            Seders/Peers: {self.Seeders}/{self.Peers}
            ResourceLink: {self.ResourceLink}
            TorrentFileLink: {self.TorrentFileLink}
            MagnetLink: {self.MagnetLink}
        """
        )
