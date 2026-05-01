# websites domain
import os

REDDIT = os.environ.get("REDDIT", "")
SHOPPING = os.environ.get("SHOPPING", "")
SHOPPING_ADMIN = os.environ.get("SHOPPING_ADMIN", "")
GITLAB = os.environ.get("GITLAB", "")
WIKIPEDIA = os.environ.get("WIKIPEDIA", "")
MAP = os.environ.get("MAP", "")
HOMEPAGE = os.environ.get("HOMEPAGE", "")
# Microsoft Dining (dining.microsoft.com) — internal Microsoft site for
# browsing on-campus cafes, viewing menus, ordering for pickup. Defaults
# to the production URL since there is no self-hostable variant.
DINING = os.environ.get("DINING", "https://dining.microsoft.com")

assert (
    REDDIT
    and SHOPPING
    and SHOPPING_ADMIN
    and GITLAB
    and WIKIPEDIA
    and MAP
    and HOMEPAGE
), (
    f"Please setup the URLs to each site. Current: \n"
    + f"Reddit: {REDDIT}\n"
    + f"Shopping: {SHOPPING}\n"
    + f"Shopping Admin: {SHOPPING_ADMIN}\n"
    + f"Gitlab: {GITLAB}\n"
    + f"Wikipedia: {WIKIPEDIA}\n"
    + f"Map: {MAP}\n"
    + f"Homepage: {HOMEPAGE}\n"
)


ACCOUNTS = {
    "reddit": {"username": "MarvelsGrantMan136", "password": "test1234"},
    "gitlab": {"username": "byteblaze", "password": "hello1234"},
    "shopping": {
        "username": "emma.lopez@gmail.com",
        "password": "Password.123",
    },
    "shopping_admin": {"username": "admin", "password": "admin1234"},
    "shopping_site_admin": {"username": "admin", "password": "admin1234"},
    # Dining uses Microsoft SSO; the storage_state JSON exported from the
    # Edge user-data-dir at ~/.dining_context is the credential.
    "dining": {"username": "<msft sso>", "password": "<msft sso>"},
}

URL_MAPPINGS = {
    REDDIT: "http://reddit.com",
    SHOPPING: "http://onestopmarket.com",
    SHOPPING_ADMIN: "http://luma.com/admin",
    GITLAB: "http://gitlab.com",
    WIKIPEDIA: "http://wikipedia.org",
    MAP: "http://openstreetmap.org",
    HOMEPAGE: "http://homepage.com",
    DINING: "http://dining.microsoft.com",
}
