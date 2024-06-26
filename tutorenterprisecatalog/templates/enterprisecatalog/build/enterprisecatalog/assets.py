from .base import *

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# Get rid of the "local" handler
if "local" in LOGGING["handlers"]:
    LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    if "local" in logger["handlers"]:
        logger["handlers"].remove("local")
