import logging
# from main import num_of_game

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)