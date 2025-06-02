import logging
import sys

NUMBER_OF_PAGES_TO_CHECK = 5
SIMILARITY_THRESHOLD = 0.3
BLOCKED_DOMAINS = [
    "youtube.com",
    "youtu.be",
    "instagram.com",
    "pinterest.com",
    "tiktok.com",
    "facebook.com",
    "fbcdn.net",
    "twitter.com",
    "x.com",
    "twimg.com",
    "reddit.com",
    "redd.it",
    "snapchat.com",
    "tumblr.com",
    "flickr.com",
    "imgur.com",
    "deviantart.com",
    "canva.com",
    "unsplash.com",
    "pexels.com",
    "pixabay.com",
    "tenor.com",
    "giphy.com",
    "dribbble.com",
    "behance.net",
    "soundcloud.com",
    "spotify.com",
    "vimeo.com",
    "dailymotion.com",
    "linkedin.com",
    "github.com",
]


def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel("INFO")

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger
