from decouple import config
from split_settings.tools import include

include(
    "base.py",
)

DEBUG = config("DEBUG", default=False, cast=bool)
