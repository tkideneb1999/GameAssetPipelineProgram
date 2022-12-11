
LOG_LEVEL_DEBUG = 10
LOG_LEVEL_INFO = 20
LOG_LEVEL_WARNING = 30
LOG_LEVEL_ERROR = 40

log_level = 10


def debug(msg):
    if log_level <= 10:
        print("[GAPA][DEBUG]: " + msg)


def info(msg):
    if log_level <= 20:
        print("[GAPA][INFO]: " + msg)


def warning(msg):
    if log_level <= 30:
        print("[GAPA][WARNING]: " + msg)


def error(msg):
    if log_level <= 40:
        print("[GAPA][ERROR]: " + msg)
