from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


_FRESHNESS_MARGIN = timedelta(minutes=5)


@dataclass(frozen=True)
class Page:
    number: int
    width: int
    height: int
    drm_mode: str
    drm_hash: str
    image_url: str

    @classmethod
    def from_api(cls, data: dict) -> 'Page':
        return cls(
            number=data.get('page'),
            width=data.get('width', 0),
            height=data.get('height', 0),
            drm_mode=data.get('drmMode', ''),
            drm_hash=data.get('drmHash', ''),
            image_url=data.get('drmImageUrl', ''),
        )


@dataclass(frozen=True)
class Rendition:
    size_type: str
    pages: tuple[Page, ...] = ()
    expires_at: datetime | None = None

    @classmethod
    def from_api(cls, size_type: str, data: dict) -> 'Rendition':
        return cls(
            size_type=size_type,
            pages=tuple(Page.from_api(p) for p in data.get('manuscripts') or ()),
            expires_at=_parse_datetime(data.get('expiresAt')),
        )

    @property
    def width(self) -> int:
        return self.pages[0].width

    @property
    def height(self) -> int:
        return self.pages[0].height

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def pixels(self) -> int:
        return self.width * self.height

    @property
    def is_stale(self) -> bool:
        if self.expires_at is None:
            return False
        return self.expires_at - datetime.now(timezone.utc) < _FRESHNESS_MARGIN


@dataclass(frozen=True)
class Work:
    title: str
    code: str
    episodes: tuple['Episode', ...] = ()
    current_episode: 'Episode | None' = None

    @classmethod
    def from_api(cls, work_data: dict, episode_data: dict) -> 'Work':
        work = work_data.get('work') or {}
        listing = work_data.get('firstEpisodes') or {}
        current = episode_data.get('episode') or {}
        return cls(
            title=work.get('title', ''),
            code=work.get('code', ''),
            episodes=tuple(Episode.from_api(raw) for raw in listing.get('result') or ()),
            current_episode=Episode.from_api(current) if current else None,
        )

    @property
    def active_episodes(self) -> tuple['Episode', ...]:
        return tuple(ep for ep in self.episodes if ep.is_active)

    def find_episode(self, number: int) -> 'Episode | None':
        return next((ep for ep in self.active_episodes if ep.number == number), None)


@dataclass(frozen=True)
class Episode:
    id: str
    code: str
    number: int
    title: str
    page_count: int
    kind: str                                   # 'normal' | 'extra' | 'pr'
    is_active: bool
    delivery_period: datetime | None = None  # free access ends at this moment

    @classmethod
    def from_api(cls, data: dict) -> 'Episode':
        internal = data.get('internal') or {}
        return cls(
            id=data.get('id', ''),
            code=data.get('code', ''),
            number=internal.get('episodeNo'),
            title=data.get('title', ''),
            page_count=internal.get('pageCount', 0),
            kind=internal.get('episodetype') or data.get('type') or 'normal',
            is_active=bool(data.get('isActive')),
            delivery_period=_parse_datetime(data.get('deliveryPeriod')),
        )
