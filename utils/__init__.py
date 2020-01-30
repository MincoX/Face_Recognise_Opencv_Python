import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] %(message)s',
)

logger = logging.getLogger()
