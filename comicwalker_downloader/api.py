import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

TIMEOUT = (5, 30)

VIEWER_URL = 'https://comic-walker.com/api/contents/viewer'

MOBILE_SIZE_TYPE = 'width:768'
DESKTOP_SIZE_TYPE = 'width:1284'

IMAGE_SIZE_TYPES = (MOBILE_SIZE_TYPE, DESKTOP_SIZE_TYPE)


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    return session

