import re

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

def is_valid_url(url: str) -> bool:
    pattern = r'^(https?://)?comic-walker\.com/detail/KC_\d+_S(/episodes/KC_\d+_E)?(?:\?.*)?$'
    return bool(re.match(pattern, url))

def sanitize_dirname(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()
